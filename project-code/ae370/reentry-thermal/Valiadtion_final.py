# Archived notebook code; see README.md for authorship, dependencies, and saved-run limitations.

# %%
# ============================================================
# solver.py  (FV+CN core; the ONLY “correct” core version)
# ============================================================
import numpy as np
import math as m

"""
Scheme A: Fully consistent spherical Finite-Volume (FV)
  M dT/dt = K T + f
  - exact shell volumes and face areas
  - harmonic-mean k at faces
  - surface heat flux q'' enters as +q_in * A_surf power into last cell
  - CN (trapezoid) time integration with a tridiagonal Thomas solver

Includes:
  - RK4 reentry trajectory (simple atmosphere + variable gravity)
  - Sutton–Graves stagnation-point heat flux

Notes:
  - q_in > 0 means heat enters the solid.
"""

# Physical constants
# ------------------------
R_EARTH = 6371000.0
G0 = 9.81


# Atmosphere & gravity
# ------------------------
def atmosphere_rho(h):
    rho0 = 1.225
    H = 7200.0
    h = np.maximum(h, 0.0)
    return rho0 * np.exp(-h / H)

def gravity(h):
    return G0 * (R_EARTH / (R_EARTH + np.maximum(h, 0.0)))**2


# Sutton–Graves heat flux
# ------------------------
def sutton_graves_q(h, V, Rn, K=1.e-4):
    rho = atmosphere_rho(h)
    return K * np.sqrt(rho) * np.abs(V)**3 / np.sqrt(Rn)


# Material database
# ------------------------
MATERIAL_DB = {
    "Resin":        dict(rho=1040.0, cp=1506.0, k=0.09),
    "Composite":    dict(rho=1800.0, cp=1000.0, k=0.5),
    "Foam":         dict(rho=300.0,  cp=1400.0, k=0.08),
    "Structural":   dict(rho=1600.0, cp=900.0,  k=0.4),
}

def compute_single_material_layers(material, TPS_inner, TPS_outer):
    # NOTE: r_outer must be increasing so assignment works.
    tps = MATERIAL_DB[material]
    structure = dict(rho=2700.0, cp=900.0, k=200.0)  # placeholder metal (Al-like)
    return [
        (TPS_inner, structure["rho"], structure["cp"], structure["k"]),  # inner structure: 0..TPS_inner
        (TPS_outer, tps["rho"],      tps["cp"],      tps["k"]),          # outer TPS: TPS_inner..R
    ]


# Material assignment (piecewise constant from center outward)
# ------------------------
def assign_material_properties(r_centers, layers):
    rho = np.zeros_like(r_centers, dtype=float)
    cp  = np.zeros_like(r_centers, dtype=float)
    k   = np.zeros_like(r_centers, dtype=float)
    for i, ri in enumerate(r_centers):
        for r_outer, rh, c, kk in layers:
            if ri <= r_outer + 1e-15:
                rho[i], cp[i], k[i] = rh, c, kk
                break
        else:
            rho[i], cp[i], k[i] = layers[-1][1], layers[-1][2], layers[-1][3]
    return rho, cp, k


# Tridiagonal utilities
# ------------------------
def apply_tridiag(a, b, c, x):
    y = b * x
    y[1:]  += a * x[:-1]
    y[:-1] += c * x[1:]
    return y

def thomas_solve(a, b, c, d):
    n = len(b)
    ac = a.astype(float).copy()
    bc = b.astype(float).copy()
    cc = c.astype(float).copy()
    dc = d.astype(float).copy()

    for i in range(1, n):
        w = ac[i-1] / bc[i-1]
        bc[i] -= w * cc[i-1]
        dc[i] -= w * dc[i-1]

    x = np.zeros(n, dtype=float)
    x[-1] = dc[-1] / bc[-1]
    for i in range(n-2, -1, -1):
        x[i] = (dc[i] - cc[i] * x[i+1]) / bc[i]
    return x


# FV build: returns everything needed for CN updates
# ------------------------
def build_spherical_fv_system(N, R, layers):
    dr = R / N

    r_faces   = np.linspace(0.0, R, N+1)
    r_centers = 0.5 * (r_faces[:-1] + r_faces[1:])

    A_faces = 4.0 * np.pi * r_faces**2
    V_cells = (4.0/3.0) * np.pi * (r_faces[1:]**3 - r_faces[:-1]**3)

    rho, cp, k_cell = assign_material_properties(r_centers, layers)

    # harmonic mean k at interior faces
    k_faces = np.zeros(N+1, dtype=float)
    k_faces[0] = k_cell[0]   # unused since A_faces[0]=0
    for j in range(1, N):
        kL, kR = k_cell[j-1], k_cell[j]
        k_faces[j] = 2.0 * kL * kR / (kL + kR)
    k_faces[N] = k_cell[-1]

    Gw = k_faces[:-1] * A_faces[:-1] / dr
    Ge = k_faces[1:]  * A_faces[1:]  / dr

    # surface face handled by flux forcing, not K
    Ge[-1] = 0.0

    K_diag  = -(Gw + Ge)
    K_lower = Gw[1:]
    K_upper = Ge[:-1]

    M_diag = rho * cp * V_cells

    return (r_centers, r_faces, dr, rho, cp, k_cell, V_cells, A_faces,
            M_diag, K_lower, K_diag, K_upper)


# CN FV time step (supports optional qdot for MMS)
# ------------------------
def trapezoid_step_fv(Tn, dt, M_diag, K_lower, K_diag, K_upper,
                      V_cells, A_faces, q_n, q_np1, qdot_n=None, qdot_np1=None):
    q_mid = 0.5 * (q_n + q_np1)

    # power forcing per cell
    f_mid = np.zeros_like(Tn)
    f_mid[-1] += q_mid * A_faces[-1]  # q>0 injects heat into solid

    if (qdot_n is not None) and (qdot_np1 is not None):
        qdot_mid = 0.5 * (qdot_n + qdot_np1)
        f_mid += qdot_mid * V_cells

    Kx = apply_tridiag(K_lower, K_diag, K_upper, Tn)
    RHS = M_diag * Tn + 0.5 * dt * Kx + dt * f_mid

    a = -0.5 * dt * K_lower
    b = M_diag - 0.5 * dt * K_diag
    c = -0.5 * dt * K_upper

    return thomas_solve(a, b, c, RHS)


def integrate_conduction_fv(T0, dt, q_array, system):
    (r_centers, r_faces, dr, rho, cp, k_cell, V_cells, A_faces,
     M_diag, K_lower, K_diag, K_upper) = system

    T = T0.copy()
    sol = [T.copy()]
    for n in range(len(q_array) - 1):
        T = trapezoid_step_fv(T, dt, M_diag, K_lower, K_diag, K_upper,
                              V_cells, A_faces, q_array[n], q_array[n+1])
        sol.append(T.copy())
    return np.array(sol)


# Reentry dynamics
# ------------------------
def rk4(f, t, y, dt, *args):
    k1 = f(t, y, *args)
    k2 = f(t + dt/2, y + dt/2*k1, *args)
    k3 = f(t + dt/2, y + dt/2*k2, *args)
    k4 = f(t + dt,   y + dt*k3,   *args)
    return y + dt*(k1 + 2*k2 + 2*k3 + k4)/6

def reentry_rhs(t, y, m0, Cd, Aref):
    h, vx, vz = y
    h = max(h, 0.0)
    rho = atmosphere_rho(h)
    g = gravity(h)
    V = np.hypot(vx, vz)
    D = 0.0 if V < 1e-12 else 0.5*rho*V**2*Cd*Aref/m0
    ax = -D*vx/V if V > 0 else 0.0
    az = -g - D*vz/V if V > 0 else -g
    return np.array([vz, ax, az])

def integrate_reentry(y0, R_sphere, t_final, dt_traj, m0=200.0, Cd=1.2):
    t = 0.0
    y = y0.copy()
    Aref = np.pi * R_sphere**2
    T_hist = [t]
    Y_hist = [y.copy()]
    while y[0] > 0.0 and t < t_final:
        y = rk4(reentry_rhs, t, y, dt_traj, m0, Cd, Aref)
        y[0] = max(y[0], 0.0)
        t += dt_traj
        T_hist.append(t)
        Y_hist.append(y.copy())
    return np.array(T_hist), np.array(Y_hist)


# %%
# ============================================================
# verification_mms.py  (A1)
#   - run AFTER the solver.py cell above
# ============================================================
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# A1: MMS Convergence Test (Scheme A FV)
#   - Uses same FV operator and CN step as implementation
#   - Integrates to exact t_final (no rounding-time mismatch)
#   - SPACE test: oscillatory mode (n=8) to make spatial error visible
#   - TIME  test: smooth mode (n=2) + very fine N to isolate CN time order
# ============================================================

def fv_error_norms(T_num, T_ex, V_cells, Tref):
    e = T_num - T_ex
    l2_abs = np.sqrt(np.sum(V_cells * e**2) / np.sum(V_cells))
    linf   = np.max(np.abs(e))
    l2_rel = l2_abs / (Tref if Tref != 0 else 1.0)
    linf_rel = linf / (Tref if Tref != 0 else 1.0)
    return l2_abs, linf, l2_rel, linf_rel

# -----------------------------
# Smooth, r=0-regular manufactured field using j0 mode:
#   theta(r,t) = A exp(-t/tau) * j0(lam r)
# Choose lam so that d/dr theta(R,t)=0  => tan(lam R)=lam R
# (Neumann homogeneous at outer face), which keeps forcing clean.
# -----------------------------
def roots_tan_eq_x(n_roots):
    roots = []
    f = lambda x: np.tan(x) - x
    k = 1
    while len(roots) < n_roots and k < 20000:
        a = k*np.pi + 1e-8
        b = k*np.pi + np.pi/2 - 1e-8
        fa, fb = f(a), f(b)
        if np.sign(fa) != np.sign(fb):
            lo, hi = a, b
            for _ in range(80):
                mid = 0.5*(lo+hi)
                fm = f(mid)
                if np.sign(fa) != np.sign(fm):
                    hi = mid
                    fb = fm
                else:
                    lo = mid
                    fa = fm
            roots.append(0.5*(lo+hi))
        k += 1
    return np.array(roots)

def j0(x):
    out = np.ones_like(x)
    mask = np.abs(x) > 1e-14
    out[mask] = np.sin(x[mask]) / x[mask]
    return out

def j0_prime(x):
    # derivative of sin(x)/x: (x cos x - sin x)/x^2
    out = np.zeros_like(x)
    mask = np.abs(x) > 1e-14
    out[mask] = (x[mask]*np.cos(x[mask]) - np.sin(x[mask])) / (x[mask]**2)
    return out

# -----------------------------
# MMS definitions
# -----------------------------
def theta_exact(r, t, Aamp, tau, lam):
    return Aamp * np.exp(-t/tau) * j0(lam * r)

def theta_t_exact(r, t, Aamp, tau, lam):
    return (-Aamp/tau) * np.exp(-t/tau) * j0(lam * r)

def theta_rr_exact(r, t, Aamp, tau, lam):
    # For spherical: Laplacian(theta) = theta_rr + (2/r) theta_r
    # But we'll build qdot from exact PDE in conservative form:
    # rho cp theta_t = (1/r^2) d/dr (k r^2 theta_r) + qdot
    # so qdot = rho cp theta_t - k * Laplacian(theta)
    # We can compute Laplacian analytically via:
    # theta_r = A exp(-t/tau) * lam * j0'(lam r)
    # For j0, Laplacian(j0(lam r)) = -lam^2 j0(lam r)
    # so Laplacian(theta) = -lam^2 theta / (A exp(-t/tau)) * (A exp(-t/tau)) = -lam^2 theta
    return None

def qdot_exact(r, t, rho, cp, k, Aamp, tau, lam):
    # Using Laplacian(theta) = -lam^2 * theta for spherical j0 mode
    th = theta_exact(r, t, Aamp, tau, lam)
    th_t = theta_t_exact(r, t, Aamp, tau, lam)
    lap = - (lam**2) * th
    return rho*cp*th_t - k*lap

def cell_avg_exact(r_faces, t, Aamp, tau, lam):
    # Volume-average in each shell:
    # <theta> = ( ∫_{ra}^{rb} theta(r,t) * 4π r^2 dr ) / ( ∫ 4π r^2 dr )
    ra = r_faces[:-1]
    rb = r_faces[1:]
    # numerical quadrature per cell (fine subgrid) to stay consistent & simple
    out = np.zeros_like(ra)
    for i,(a,b) in enumerate(zip(ra,rb)):
        rq = np.linspace(a,b,80)
        wq = rq**2
        thq = theta_exact(rq, t, Aamp, tau, lam)
        out[i] = np.trapz(thq*wq, rq) / np.trapz(wq, rq)
    return out

# -----------------------------
# MMS runner
# -----------------------------
def run_mms(N, dt, t_final, R, rho, cp, k, Tref, Aamp, tau, nmode):
    # choose Neumann eigenvalue: tan(x)=x, lam=x/R
    x = roots_tan_eq_x(nmode)[-1]
    lam = x / R

    layers = [(R, rho, cp, k)]
    system = build_spherical_fv_system(N, R, layers)
    r_centers, r_faces, _, _, _, _, V_cells, A_faces, M_diag, K_lower, K_diag, K_upper = system

    # initial condition = exact cell-average theta at t=0
    theta0 = cell_avg_exact(r_faces, 0.0, Aamp, tau, lam)
    Tn = theta0.copy()

    # march exactly to t_final
    nsteps = int(np.round(t_final/dt))
    t = 0.0
    for n in range(nsteps):
        qn = 0.0
        qnp1 = 0.0
        qdot_n   = qdot_exact(r_centers, t,     rho, cp, k, Aamp, tau, lam)
        qdot_np1 = qdot_exact(r_centers, t+dt,  rho, cp, k, Aamp, tau, lam)

        Tn = trapezoid_step_fv(
            Tn, dt, M_diag, K_lower, K_diag, K_upper,
            V_cells, A_faces, qn, qnp1,
            qdot_n=qdot_n, qdot_np1=qdot_np1
        )
        t += dt

    Tex = cell_avg_exact(r_faces, t_final, Aamp, tau, lam)
    l2_abs, linf, l2_rel, linf_rel = fv_error_norms(Tn, Tex, V_cells, Tref)
    return l2_abs, linf

# -----------------------------
# Convergence tests
# -----------------------------
R = 0.2
rho = 1000.0
cp  = 1000.0
k   = 1.0
Tref = 1.0

t_final = 0.5

# SPACE: oscillatory mode to expose spatial error
Aamp = 10.0
tau  = 1.0
nmode_space = 8
dt_space = 1e-3

Ns = [30, 60, 120, 240, 480, 960]
errs = []
hs = []

print("Space convergence (vol-weighted abs L2):")
for N in Ns:
    h = R/N
    l2, linf = run_mms(N, dt_space, t_final, R, rho, cp, k, Tref, Aamp, tau, nmode_space)
    errs.append(l2)
    hs.append(h)
    print(f"  N={N:4d}, h={h:.3e}, err={l2:.3e}")

for i in range(1,len(Ns)):
    p = np.log(errs[i-1]/errs[i]) / np.log(hs[i-1]/hs[i])
    print(f"  order between N={Ns[i-1]} and {Ns[i]}: p≈{p:.3f}")

plt.figure()
plt.loglog(hs, errs, marker="o")
plt.gca().invert_xaxis()
plt.xlabel("h = R/N [m]")
plt.ylabel("vol-weighted abs L2 error")
plt.title("MMS space convergence")
plt.grid(True, which="both")

# TIME: smooth mode + very fine N to isolate time error
Aamp = 10.0
tau  = 1.0
nmode_time = 2
N_time = 2000

dts = [0.1, 0.05, 0.025, 0.0125]
errs_t = []

print("Time convergence (vol-weighted abs L2):")
for dt in dts:
    l2, linf = run_mms(N_time, dt, t_final, R, rho, cp, k, Tref, Aamp, tau, nmode_time)
    errs_t.append(l2)
    print(f"  dt={dt:.3e}, err={l2:.3e}")

for i in range(1,len(dts)):
    p = np.log(errs_t[i-1]/errs_t[i]) / np.log(dts[i-1]/dts[i])
    print(f"  order between dt={dts[i-1]} and {dts[i]}: p≈{p:.3f}")

plt.figure()
plt.loglog(dts, errs_t, marker="o")
plt.gca().invert_xaxis()
plt.xlabel("dt [s]")
plt.ylabel("vol-weighted abs L2 error")
plt.title("MMS time convergence")
plt.grid(True, which="both")

plt.show()


# %%
# ============================================================
# verification_analytic.py  (A2)
#   - run AFTER the solver.py cell above
# ============================================================
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# A2: Analytical check — constant inward flux on uniform sphere
#   - Compare FV to analytical series solution
#   - Uses cell-average analytical evaluation for FV consistency
# ============================================================

# -----------------------------
# Roots of tan(x)=x
# -----------------------------
def roots_tan_eq_x(n_roots):
    roots = []
    f = lambda x: np.tan(x) - x
    k = 1
    while len(roots) < n_roots and k < 20000:
        a = k*np.pi + 1e-8
        b = k*np.pi + np.pi/2 - 1e-8
        fa, fb = f(a), f(b)
        if np.sign(fa) != np.sign(fb):
            lo, hi = a, b
            for _ in range(80):
                mid = 0.5*(lo+hi)
                fm = f(mid)
                if np.sign(fa) != np.sign(fm):
                    hi = mid
                    fb = fm
                else:
                    lo = mid
                    fa = fm
            roots.append(0.5*(lo+hi))
        k += 1
    return np.array(roots)

def j0(x):
    out = np.ones_like(x)
    mask = np.abs(x) > 1e-14
    out[mask] = np.sin(x[mask]) / x[mask]
    return out

# -----------------------------
# Build analytical series for constant-flux sphere
# -----------------------------
def build_theta_series(R, B, n_terms, quad_N=40000):
    x = roots_tan_eq_x(n_terms)
    lam = x / R

    rq = np.linspace(0.0, R, quad_N)
    wq = rq**2

    theta0 = -B * rq**2

    c0 = (3.0/R**3) * np.trapz(theta0 * wq, rq)

    coeffs = np.zeros(n_terms, dtype=float)
    norms  = np.zeros(n_terms, dtype=float)
    for n in range(n_terms):
        phi = j0(lam[n]*rq)
        norms[n] = np.trapz(phi*phi*wq, rq)
        coeffs[n] = np.trapz(theta0*phi*wq, rq) / norms[n]

    return c0, coeffs, lam, norms

def theta_series_cellavg(r_faces, t, R, B, alpha, c0, coeffs, lam, norms, quad_per_cell=80):
    ra = r_faces[:-1]
    rb = r_faces[1:]
    out = np.zeros_like(ra)

    for i,(a,b) in enumerate(zip(ra,rb)):
        rq = np.linspace(a,b,quad_per_cell)
        wq = rq**2

        # series part (homogeneous Neumann)
        th = np.zeros_like(rq) + c0
        for n in range(len(coeffs)):
            th += coeffs[n] * j0(lam[n]*rq) * np.exp(-(lam[n]**2)*alpha*t)

        # particular r^2 term
        th += B * rq**2
        g = 2*R*B            # B = (q/k)/(2R) => q/k = 2RB
        beta = 3.0 * alpha * g / R   # = 6 alpha B
        th += beta * t

        out[i] = np.trapz(th*wq, rq) / np.trapz(wq, rq)
    return out

# -----------------------------
# Run A2
# -----------------------------
R = 0.2
rho = 1000.0
cp  = 1000.0
k   = 1.0
alpha = k/(rho*cp)

q_in = 5e4               # inward heat flux [W/m^2]
B = (q_in / k) / (2*R)   # so that d/dr(B r^2)|_{R} = q/k

terms = 200
c0, coeffs, lam, norms = build_theta_series(R, B, terms, quad_N=40000)

N = 960
dt = 0.01
t_final = 10
steps = int(np.round(t_final/dt))
t_grid = np.linspace(0.0, steps*dt, steps+1)

layers = [(R, rho, cp, k)]
system = build_spherical_fv_system(N, R, layers)
r_centers, r_faces, _, _, _, _, V_cells, A_faces, M_diag, K_lower, K_diag, K_upper = system

q_array = np.full_like(t_grid, q_in, dtype=float)

T0 = 300.0
T = np.ones(N)*T0
sol = [T.copy()]
for n in range(len(t_grid)-1):
    T = trapezoid_step_fv(T, dt, M_diag, K_lower, K_diag, K_upper,
                          V_cells, A_faces, q_array[n], q_array[n+1])
    sol.append(T.copy())
sol = np.array(sol)

T_num = sol[-1]
T_ex  = T0 + theta_series_cellavg(r_faces, t_grid[-1], R, B, alpha, c0, coeffs, lam, norms, quad_per_cell=80)

e = T_num - T_ex
l2 = np.sqrt(np.sum(V_cells * e**2) / np.sum(V_cells))
linf = np.max(np.abs(e))

print(f"Analytical check (cell-avg analytical): N={N}, dt={dt}, terms={terms}")
print(f"  vol-weighted L2 error = {l2:.3e} K")
print(f"  Linf error            = {linf:.3e} K")

plt.figure()
plt.plot(r_centers, T_num, label="FV")
plt.plot(r_centers, T_ex,  "--", label="Analytical (cell-avg)")
plt.xlabel("r [m]")
plt.ylabel("T [K]")
plt.title(f"Analytical check: constant-flux sphere at t={t_grid[-1]:.2f}s")
plt.grid(True)
plt.legend()
plt.show()


# %%
# ============================================================
# resolution_study.py  (dt/N/dt_traj sweep)
#   - run AFTER the solver.py cell above
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# -----------------------------
# Build q''(t) reference on fine trajectory grid, then interpolate
# -----------------------------
def make_q_reference(y0, R_sphere, t_final, dt_traj_ref):
    times, Y = integrate_reentry(y0, R_sphere, t_final, dt_traj_ref)
    altitudes = Y[:, 0]
    Vmag = np.linalg.norm(Y[:, 1:], axis=1)
    q_ref = sutton_graves_q(altitudes, Vmag, R_sphere)
    return times, q_ref

def sample_q(times_ref, q_ref, dt_cond):
    t = np.arange(0.0, times_ref[-1] + 1e-12, dt_cond)
    q = np.interp(t, times_ref, q_ref)
    return t, q

# -----------------------------
# Outputs + metrics
# -----------------------------
def extract_outputs(sol_T, r_centers, TPS_inner):
    T_surface = sol_T[:, -1]
    T_back_center = sol_T[:, 0]
    T_back_iface = np.array([np.interp(TPS_inner, r_centers, sol_T[n, :]) for n in range(sol_T.shape[0])])
    return T_surface, T_back_center, T_back_iface

def metrics_vs_ref(t, y, t_ref, y_ref):
    y_ref_i = np.interp(t, t_ref, y_ref)
    err = y - y_ref_i
    peak_rel = abs(np.max(y) - np.max(y_ref_i)) / np.max(y_ref_i)
    linf = np.max(np.abs(err))
    l2 = np.sqrt(np.mean(err**2))
    return peak_rel, linf, l2

# -----------------------------
# One coupled run
# -----------------------------
def run_one(material, N, dt_cond, times_qref, q_ref, R_sphere, TPS_inner, TPS_outer, Tinit=300.0):
    layers = compute_single_material_layers(material, TPS_inner, TPS_outer)
    system = build_spherical_fv_system(N, R_sphere, layers)
    r_centers = system[0]
    t, q = sample_q(times_qref, q_ref, dt_cond)
    sol_T = integrate_conduction_fv(np.ones(N)*Tinit, dt_cond, q, system)
    return t, q, sol_T, r_centers

# -----------------------------
# Resolution study + plots
# -----------------------------
def resolution_study_and_plots(
    material,
    R_sphere,
    TPS_inner,
    TPS_outer,
    Alt_0,
    V_0,
    gamma_deg,
    t_final,
    dt_traj_ref,
    dt_list,
    N_list,
    N_ref,
    dt_ref,
    Tinit=300.0
):
    y0 = np.array([Alt_0, V_0*np.cos(np.radians(gamma_deg)), V_0*np.sin(np.radians(gamma_deg))])
    times_qref, q_ref = make_q_reference(y0, R_sphere, t_final, dt_traj_ref)

    # reference run
    tR, qR, solR, rR = run_one(material, N_ref, dt_ref, times_qref, q_ref, R_sphere, TPS_inner, TPS_outer, Tinit=Tinit)
    Ts_R, TbC_R, TbI_R = extract_outputs(solR, rR, TPS_inner)

    # dt sweep (fix N_ref)
    rows_dt = []
    dt_curves = {}
    for dtc in dt_list:
        t, q, sol, r = run_one(material, N_ref, dtc, times_qref, q_ref, R_sphere, TPS_inner, TPS_outer, Tinit=Tinit)
        Ts, TbC, TbI = extract_outputs(sol, r, TPS_inner)

        epeakI, einfI, el2I = metrics_vs_ref(t, TbI, tR, TbI_R)
        epeakS, einfS, el2S = metrics_vs_ref(t, Ts,  tR, Ts_R)

        rows_dt.append([dtc, epeakI, einfI, el2I, epeakS, einfS, el2S])
        dt_curves[dtc] = (t, TbI)

    df_dt = pd.DataFrame(rows_dt, columns=[
        "dt_cond",
        "peak_rel_back_iface", "Linf_back_iface_K", "L2_back_iface_K",
        "peak_rel_surface",    "Linf_surface_K",    "L2_surface_K"
    ])

    # N sweep (fix dt_ref)
    rows_N = []
    N_curves = {}
    for N in N_list:
        t, q, sol, r = run_one(material, N, dt_ref, times_qref, q_ref, R_sphere, TPS_inner, TPS_outer, Tinit=Tinit)
        Ts, TbC, TbI = extract_outputs(sol, r, TPS_inner)

        epeakI, einfI, el2I = metrics_vs_ref(t, TbI, tR, TbI_R)
        epeakS, einfS, el2S = metrics_vs_ref(t, Ts,  tR, Ts_R)

        dx = R_sphere / N
        rows_N.append([N, dx, epeakI, einfI, el2I, epeakS, einfS, el2S])
        N_curves[N] = (t, TbI)

    df_N = pd.DataFrame(rows_N, columns=[
        "N", "dx",
        "peak_rel_back_iface", "Linf_back_iface_K", "L2_back_iface_K",
        "peak_rel_surface",    "Linf_surface_K",    "L2_surface_K"
    ])

    print("\n--- dt sweep (N fixed at N_ref) ---")
    display(df_dt)
    print("\n--- N sweep (dt fixed at dt_ref) ---")
    display(df_N)

    # plots
    plt.figure()
    for dtc in dt_list:
        t, TbI = dt_curves[dtc]
        plt.plot(t, TbI, label=f"dt={dtc}")
    plt.plot(tR, TbI_R, "k--", label="ref")
    plt.xlabel("Time [s]")
    plt.ylabel("T_back_iface [K]")
    plt.title(f"{material}: Back interface temperature — dt sweep (N={N_ref})")
    plt.legend()
    plt.grid(True)

    plt.figure()
    plt.loglog(df_dt["dt_cond"], df_dt["peak_rel_back_iface"], marker="o")
    plt.gca().invert_xaxis()
    plt.xlabel("dt_cond [s]")
    plt.ylabel("peak_rel (back iface)")
    plt.title("Back-iface peak relative error vs dt_cond")
    plt.grid(True, which="both")

    plt.figure()
    plt.loglog(df_N["dx"], df_N["peak_rel_back_iface"], marker="o")
    plt.gca().invert_xaxis()
    plt.xlabel("dx = R/N [m]")
    plt.ylabel("peak_rel (back iface)")
    plt.title("Back-iface peak relative error vs dx")
    plt.grid(True, which="both")

    plt.show()

    return df_dt, df_N


# -----------------------------
# Run the study (edit lists only)
# -----------------------------
R_sphere = 0.2
TPS_inner = 0.195
TPS_outer = R_sphere

Alt_0 = 120000.0
V_0 = 8000.0
gamma_deg = -2.0

t_final = 400.0
dt_traj_ref = 0.05

dt_list = [4, 2.0, 1.0]
N_list  = [3200,6400,12800]
N_ref   = 25600
dt_ref  = 0.5

df_dt, df_N = resolution_study_and_plots(
    material="Resin",
    R_sphere=R_sphere,
    TPS_inner=TPS_inner,
    TPS_outer=TPS_outer,
    Alt_0=Alt_0,
    V_0=V_0,
    gamma_deg=gamma_deg,
    t_final=t_final,
    dt_traj_ref=dt_traj_ref,
    dt_list=dt_list,
    N_list=N_list,
    N_ref=N_ref,
    dt_ref=dt_ref,
    Tinit=300.0
)


# %%
# ============================================================
# dt_traj sensitivity / convergence (forcing sampling only)
#   Fix: dt_cond small, N large
#   Sweep: dt_traj
#   Metric: back-interface peak temperature + L2 trace vs reference
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def run_coupled_given_dt_traj(
    material,
    R_sphere, TPS_inner, TPS_outer,
    Alt_0, V_0, gamma_deg,
    t_final,
    dt_traj,
    dt_cond,
    N,
    Tinit=300.0
):
    # 1) generate forcing with dt_traj
    y0 = np.array([Alt_0, V_0*np.cos(np.radians(gamma_deg)), V_0*np.sin(np.radians(gamma_deg))])
    times, Y = integrate_reentry(y0, R_sphere, t_final, dt_traj)
    altitudes = Y[:, 0]
    Vmag = np.linalg.norm(Y[:, 1:], axis=1)
    q_traj = sutton_graves_q(altitudes, Vmag, R_sphere)

    # 2) interpolate forcing to conduction grid (dt_cond)
    t = np.arange(0.0, times[-1] + 1e-12, dt_cond)
    q = np.interp(t, times, q_traj)

    # 3) conduction
    layers = compute_single_material_layers(material, TPS_inner, TPS_outer)
    system = build_spherical_fv_system(N, R_sphere, layers)
    r_centers = system[0]

    sol_T = integrate_conduction_fv(np.ones(N)*Tinit, dt_cond, q, system)

    # 4) back-interface temperature trace
    TbI = np.array([np.interp(TPS_inner, r_centers, sol_T[n, :]) for n in range(sol_T.shape[0])])

    return t, TbI, times, q_traj


def trace_metrics_vs_ref(t, y, t_ref, y_ref):
    y_ref_i = np.interp(t, t_ref, y_ref)
    err = y - y_ref_i
    peak_rel = abs(np.max(y) - np.max(y_ref_i)) / np.max(y_ref_i)
    linf = np.max(np.abs(err))
    l2 = np.sqrt(np.mean(err**2))
    return peak_rel, linf, l2


# -----------------------------
# Choose fixed "accurate conduction" settings
# -----------------------------
material = "Resin"

R_sphere = 0.2
TPS_inner = 0.195
TPS_outer = R_sphere

Alt_0 = 120000.0
V_0 = 8000.0
gamma_deg = -2.0
t_final = 400.0

# FIX these so conduction error is small:
dt_cond_fix = 0.25
N_fix = 6400

# dt_traj sweep list
dt_traj_list = [0.5, 0.25, 0.1, 0.05, 0.02]

# reference = smallest dt_traj in list
dt_traj_ref = min(dt_traj_list)
t_ref, Tb_ref, times_ref, q_ref = run_coupled_given_dt_traj(
    material, R_sphere, TPS_inner, TPS_outer,
    Alt_0, V_0, gamma_deg,
    t_final,
    dt_traj_ref, dt_cond_fix, N_fix
)

rows = []
curves = {}

for dtt in dt_traj_list:
    t, Tb, times, q_traj = run_coupled_given_dt_traj(
        material, R_sphere, TPS_inner, TPS_outer,
        Alt_0, V_0, gamma_deg,
        t_final,
        dtt, dt_cond_fix, N_fix
    )
    peak_rel, linf, l2 = trace_metrics_vs_ref(t, Tb, t_ref, Tb_ref)
    rows.append([dtt, np.max(Tb), peak_rel, linf, l2])
    curves[dtt] = (t, Tb)

df_dt_traj = pd.DataFrame(rows, columns=[
    "dt_traj", "TbI_peak_K", "peak_rel_vs_ref", "Linf_vs_ref_K", "L2_vs_ref_K"
]).sort_values("dt_traj", ascending=False)

display(df_dt_traj)

# plot traces
plt.figure()
for dtt in dt_traj_list:
    t, Tb = curves[dtt]
    plt.plot(t, Tb, label=f"dt_traj={dtt}")
plt.plot(t_ref, Tb_ref, "k--", label=f"ref dt_traj={dt_traj_ref}")
plt.xlabel("Time [s]")
plt.ylabel("T_back_iface [K]")
plt.title(f"{material}: dt_traj sweep (fix dt_cond={dt_cond_fix}, N={N_fix})")
plt.legend()
plt.grid(True)

# plot peak relative error vs dt_traj
plt.figure()
plt.loglog(df_dt_traj["dt_traj"], df_dt_traj["peak_rel_vs_ref"], marker="o")
plt.gca().invert_xaxis()
plt.xlabel("dt_traj [s]")
plt.ylabel("Peak relative error (back iface)")
plt.title("Forcing sampling sensitivity: peak error vs dt_traj")
plt.grid(True, which="both")

plt.show()


# %%
# ============================================================
# run_case.py  (final case plots)
#   - run AFTER the solver.py cell above
#   - Uses resolution-study-chosen parameters:
#       dt_traj = 0.05  (forcing sampling)
#       dt_cond = 1.0   (conduction time step)
#       N       = 12800 (spatial resolution)
# ============================================================
import numpy as np
import matplotlib.pyplot as plt

def run_simulation(material, first):
    layers = compute_single_material_layers(material, TPS_inner, TPS_outer)

    # --- (1) Reentry trajectory on dt_traj grid ---
    y0 = np.array([
        Alt_0,
        V_0*np.cos(np.radians(gamma_deg)),
        V_0*np.sin(np.radians(gamma_deg))
    ])
    times_traj, Y = integrate_reentry(y0, R_sphere, t_final, dt_traj)

    altitudes = Y[:, 0]
    Vmag = np.linalg.norm(Y[:, 1:], axis=1)
    q_traj = sutton_graves_q(altitudes, Vmag, R_sphere)

    # --- (2) Conduction grid on dt_cond, interpolate forcing ---
    times = np.arange(0.0, times_traj[-1] + 1e-12, dt_cond)
    q_array = np.interp(times, times_traj, q_traj)

    system = build_spherical_fv_system(N, R_sphere, layers)
    r_centers = system[0]

    sol_T = integrate_conduction_fv(np.ones(N)*300.0, dt_cond, q_array, system)
    T_surface = sol_T[:, -1]

    if first == 1:
        plt.figure()
        plt.plot(times_traj, altitudes/1000)
        plt.xlabel("Time [s]")
        plt.ylabel("Altitude [km]")
        plt.title("Altitude vs Time")
        plt.grid(True)

        plt.figure()
        plt.plot(times_traj, q_traj)
        plt.xlabel("Time [s]")
        plt.ylabel("q'' [W/m^2]")
        plt.title("Sutton–Graves heat flux forcing (trajectory grid)")
        plt.grid(True)

    plt.figure()
    plt.plot(times, T_surface, color="orange")
    plt.xlabel("Time [s]")
    plt.ylabel("Surface Temperature [K]")
    plt.title(f"{material}: Surface Temperature")
    plt.grid(True)

    plt.figure()
    r_mask = r_centers >= 0.180
    r_plot = r_centers[r_mask]
    for idx in np.linspace(0, len(times)-1, 4, dtype=int):
        plt.plot(
            np.hstack([r_plot, R_sphere])*1000,
            np.hstack([sol_T[idx, r_mask], T_surface[idx]]),
            label=f"t={times[idx]:.0f}s"
        )
    plt.xlabel("Radius [mm]")
    plt.ylabel("Temperature [K]")
    plt.title(f"{material}: Radial Temperature Profiles")
    plt.legend()
    plt.grid(True)

    plt.show()


# -----------------------------
# Simulation / numerical parameters
# -----------------------------
R_sphere = 0.2
TPS_inner = 0.195
TPS_outer = R_sphere

Alt_0 = 120000.0
V_0 = 8000.0
gamma_deg = -2.0
t_final = 400.0

# chosen from resolution studies
dt_traj = 0.05
dt_cond = 1.0
N = 12800


# -----------------------------
# Run
# -----------------------------
first = 1
for mat in MATERIAL_DB:
    run_simulation(mat, first)
    first = 0


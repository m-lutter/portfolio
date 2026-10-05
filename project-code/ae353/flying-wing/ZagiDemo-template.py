# Archived notebook code; see README.md for authorship, dependencies, and saved-run limitations.

# %%
# These modules are part of other existing libraries
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym
from scipy import linalg
from IPython.display import display, Markdown

# This is my own script (it is an interface to the pybullet simulator)
import ae353_zagi

# %%
# Time
t = sym.Symbol('t', real=True)

# Components of position (meters)
p_x, p_y, p_z = sym.symbols('p_x, p_y, p_z', real=True)

# Yaw, pitch, and roll angles (radians)
psi, theta, phi = sym.symbols('psi, theta, phi', real=True)

# Components of linear velocity in the body frame (meters / second)
v_x, v_y, v_z = sym.symbols('v_x, v_y, v_z', real=True)

# Components of angular velocity in the body frame (radians / second)
w_x, w_y, w_z = sym.symbols('w_x, w_y, w_z', real=True)

# Elevon angles
delta_r, delta_l = sym.symbols('delta_r, delta_l', real=True)

# Aerodynamic parameters
rho, S, c, b = sym.symbols('rho, S, c, b', real=True)
C_L_0, C_L_alpha, C_L_q, C_L_delta_e = sym.symbols('C_L_0, C_L_alpha, C_L_q, C_L_delta_e', real=True)
C_D_0, C_D_alpha, C_D_q, C_D_delta_e = sym.symbols('C_D_0, C_D_alpha, C_D_q, C_D_delta_e', real=True)
C_m_0, C_m_alpha, C_m_q, C_m_delta_e = sym.symbols('C_m_0, C_m_alpha, C_m_q, C_m_delta_e', real=True)
C_Y_0, C_Y_beta, C_Y_p, C_Y_r, C_Y_delta_a = sym.symbols('C_Y_0, C_Y_beta, C_Y_p, C_Y_r, C_Y_delta_a', real=True)
C_l_0, C_l_beta, C_l_p, C_l_r, C_l_delta_a = sym.symbols('C_l_0, C_l_beta, C_l_p, C_l_r, C_l_delta_a', real=True)
C_n_0, C_n_beta, C_n_p, C_n_r, C_n_delta_a = sym.symbols('C_n_0, C_n_beta, C_n_p, C_n_r, C_n_delta_a', real=True)
e, alpha_0, C_D_p, M = sym.symbols('e, alpha_0, C_D_p, M', real=True)
k, k_e = sym.symbols('k, k_e', real=True)

# Mass and inertia parameters
J_x, J_y, J_z, J_xz = sym.symbols('J_x, J_y, J_z, J_xz', real=True)
m, g = sym.symbols('m, g', real=True)

# %%
params = {
    g: 9.81,               # Gravity (m/s²)
    m: 1.56,               # Mass of the UAV (kg)
    J_x: 0.1147,           # Moment of inertia about x-axis (kg·m²) [UPDATED 02/28/2025]
    J_y: 0.0576,           # Moment of inertia about y-axis (kg·m²) [UPDATED 02/28/2025]
    J_z: 0.1712,           # Moment of inertia about z-axis (kg·m²) [UPDATED 02/28/2025]
    J_xz: 0.0000,          # Product of inertia (kg·m²)             [UPDATED 10/07/2025]

    S: 0.4696,             # Wing area (m²)
    b: 1.4224,             # Wingspan (m)
    c: 0.3302,             # Mean aerodynamic chord (m)

    rho: 1.2682,           # Air density (kg/m³)

    # Lift Coefficients
    C_L_0: 0.2,            # Lift coefficient at zero AoA
    C_L_alpha: 4.8,        # Lift curve slope (1/rad)
    C_L_q: 2.2,            # Pitch rate effect on lift (1/rad)

    # Drag Coefficients
    C_D_0: 0.02,           # Zero-lift drag coefficient
    C_D_alpha: 0.30,       # Drag change per AoA (1/rad)
    C_D_q: 0.0,            # Pitch rate effect on drag (1/rad)
    C_D_p: 0.03,           # Parasitic drag coefficient

    # Pitching Moment Coefficients
    C_m_0: -0.02,          # Pitching moment at zero AoA
    C_m_alpha: -0.6,       # Pitching moment change per AoA (1/rad)
    C_m_q: -1.8,           # Pitch rate effect on moment (1/rad)
    C_m_delta_e: -0.35,    # Effect of elevator deflection on pitching moment (1/rad)

    # Side Force Coefficients
    C_Y_0: 0.0,            # Side force at zero sideslip
    C_Y_beta: -0.08,       # Side force per sideslip angle (1/rad)
    C_Y_p: 0.0,            # Side force due to roll rate
    C_Y_r: 0.0,            # Side force due to yaw rate
    C_Y_delta_a: 0.0,      # Side force due to aileron deflection

    # Roll Moment Coefficients
    C_l_0: 0.0,            # Roll moment at zero sideslip
    C_l_beta: -0.10,       # Roll moment due to sideslip (1/rad)
    C_l_p: -0.45,          # Roll damping derivative (1/rad)
    C_l_r: 0.03,           # Roll moment due to yaw rate (1/rad)
    C_l_delta_a: 0.18,     # Aileron effect on roll (1/rad)

    # Yaw Moment Coefficients
    C_n_0: 0.0,            # Yaw moment at zero sideslip
    C_n_beta: 0.008,       # Yaw moment due to sideslip (1/rad)
    C_n_p: -0.022,         # Yaw moment due to roll rate (1/rad)
    C_n_r: -0.009,         # Yaw damping derivative (1/rad)
    C_n_delta_a: -0.004,   # Aileron effect on yaw (1/rad)

    # Control Derivatives
    C_L_delta_e: 0.30,     # Effect of elevator deflection on lift (1/rad)
    C_D_delta_e: 0.32,     # Effect of elevator deflection on drag (1/rad)

    # Efficiency Factors
    e: 0.85,               # Oswald efficiency factor
    alpha_0: 0.45,         # Zero-lift angle of attack (rad)

    # Additional Drag & Lift Coefficients
    M: 50.0,               # Sigmoid blending function parameter
    k_e: 0.01,             # Drag due to elevator deflection (empirical coefficient)
    k: 0.048               # Induced drag factor
}

# %%
# Get airspeed, angle of attack, and angle of sideslip
V_a = sym.sqrt(v_x**2 + v_y**2 + v_z**2)
alpha = sym.atan(v_z / v_x)
beta = sym.asin(v_y / V_a)

# Convert from right and left elevon deflections to equivalent elevator and aileron deflections
delta_e = (delta_r + delta_l) / 2
delta_a = (-delta_r + delta_l) / 2

# Longitudinal aerodynamics
C_L = C_L_0 + C_L_alpha * alpha
F_lift = rho * V_a**2 * S * (C_L + C_L_q * (c / (2 * V_a)) * w_y + C_L_delta_e * delta_e) / 2
F_drag = rho * V_a**2 * S * ((C_D_0 + k * C_L**2) + C_D_q * (c / (2 * V_a)) * w_y + k_e * (C_L_delta_e * delta_e)**2) / 2
f_x, f_z = sym.Matrix([[sym.cos(alpha), -sym.sin(alpha)], [sym.sin(alpha), sym.cos(alpha)]]) @ sym.Matrix([[-F_drag], [-F_lift]])
tau_y = rho * V_a**2 * S * c * (C_m_0 + C_m_alpha * alpha + C_m_q * (c / (2 * V_a)) * w_y + C_m_delta_e * delta_e) / 2

# Lateral aerodynamics
f_y =   rho * V_a**2 * S *     (C_Y_0 + C_Y_beta * beta + C_Y_p * (b / (2 * V_a)) * w_x + C_Y_r * (b / (2 * V_a)) * w_z + C_Y_delta_a * delta_a) / 2
tau_x = rho * V_a**2 * S * b * (C_l_0 + C_l_beta * beta + C_l_p * (b / (2 * V_a)) * w_x + C_l_r * (b / (2 * V_a)) * w_z + C_l_delta_a * delta_a) / 2
tau_z = rho * V_a**2 * S * b * (C_n_0 + C_n_beta * beta + C_n_p * (b / (2 * V_a)) * w_x + C_n_r * (b / (2 * V_a)) * w_z + C_n_delta_a * delta_a) / 2

# %%
v_inB_ofWB = sym.Matrix([v_x, v_y, v_z])
w_inB_ofWB = sym.Matrix([w_x, w_y, w_z])

# %%
J_inB = sym.Matrix([[  J_x,    0, -J_xz],
                    [    0,  J_y,     0],
                    [-J_xz,    0,   J_z]])

# %%
Rz = sym.Matrix([[sym.cos(psi), -sym.sin(psi), 0],
                 [sym.sin(psi), sym.cos(psi), 0],
                 [0, 0, 1]])

Ry = sym.Matrix([[sym.cos(theta), 0, sym.sin(theta)],
                 [0, 1, 0],
                 [-sym.sin(theta), 0, sym.cos(theta)]])

Rx = sym.Matrix([[1, 0, 0],
                 [0, sym.cos(phi), -sym.sin(phi)],
                 [0, sym.sin(phi), sym.cos(phi)]])

# %%
R_inW_ofB = Rz @ Ry @ Rx

# %%
# First, compute the inverse of N
Ninv = sym.Matrix.hstack((Ry @ Rx).T @ sym.Matrix([0, 0, 1]),
                              (Rx).T @ sym.Matrix([0, 1, 0]),
                                       sym.Matrix([1, 0, 0]))

# Then, take the inverse of this result to compute N
N = sym.simplify(Ninv.inv())
N

# %%
# Total force
f_inB = R_inW_ofB.T @ sym.Matrix([0, 0, m * g]) + sym.Matrix([f_x, f_y, f_z])

# Total torque
tau_inB = sym.Matrix([tau_x, tau_y, tau_z])

# %%
f_sym = sym.Matrix.vstack(
    R_inW_ofB @ v_inB_ofWB,
    N @ w_inB_ofWB,
    (1 / m) * (f_inB - w_inB_ofWB.cross(m * v_inB_ofWB)),
    J_inB.inv() @ (tau_inB - w_inB_ofWB.cross(J_inB @ w_inB_ofWB)),
)


# %%
f_sym = f_sym[[1, 3, 4, 5, 6, 7, 8, 9, 10, 11], 0]

# %%
f_sym = f_sym.subs(params)

# %%
# First, create a function that accepts 12 arguments and returns a
# 2-D array that has each element of f
f_tmp = sym.lambdify([p_y, psi, theta, phi, v_x, v_y, v_z, w_x, w_y, w_z, delta_r, delta_l], f_sym)

# Second, modify this function so that it accepts 1 argument (a 1-D array
# of total length 12) and returns a 1-D array that has each element of f
f_num = lambda x: f_tmp(*x).flatten().astype(float)

# %%
from scipy.optimize import least_squares
sol = least_squares(
    fun=f_num,
    x0=np.array([
        0.,     # p_y
        0.,     # psi
        .05, # theta cant be zero
        0.,     # phi should be zero
        10.,     # v_x cant be zero
        0.,     # v_y should be zero
        -0.4,    # v_z cant be zero
        0.,     # w_x must be zero
        0.,     # w_y must be zero
        0.,    # w_z must be zero
        -0.1,    # delta_r
        -0.1,    # delta_l
    ]),
)
assert sol.success
m_eq = sol.x[0:10]
n_eq = sol.x[10:12]

with np.printoptions(precision=4, suppress=True):
    print("Equilibrium state (m):")
    print(m_eq)
    print("Equilibrium inputs (n):")
    print(n_eq)

# %%
params.update({
    p_y: m_eq[0],
    psi: m_eq[1],
    theta: m_eq[2],
    phi: m_eq[3],
    v_x: m_eq[4],
    v_y: m_eq[5],
    v_z: m_eq[6],
    w_x: m_eq[7],
    w_y: m_eq[8],
    w_z: m_eq[9],
    delta_r: n_eq[0],
    delta_l: n_eq[1],
})
m = sym.Matrix([p_y, psi, theta, phi, v_x, v_y, v_z, w_x, w_y, w_z])
n = sym.Matrix([delta_r, delta_l])
A = sym.nsimplify(f_sym.jacobian(m).subs(params), tolerance=1e-7, rational=True)
B = sym.nsimplify(f_sym.jacobian(n).subs(params), tolerance=1e-7, rational=True)
A

# %%
B

# %%
A = np.array(A).astype(np.float64)
B = np.array(B).astype(np.float64)

# %%
def w(A, B):
        n = A.shape[0]
        W = B
        for i in range(1, n):
            c = np.linalg.matrix_power(A, i) @ B
            W = np.block([W, c])
        return W
W = w(A, B)
controllable = sym.Matrix(W).rank() == A.shape[0] # checks if W is full rank
controllable 

# %%
simulator = ae353_zagi.Simulator(
    display=False,      # the display must be off for the simulation to run in a timely manner
)

# %%
simulator.camera_catview()

# %%
Q = np.diag([1, 12.5, 350, 500, 300, 100, 20, 10, 60, 6])
R = 6900 * np.eye(2)

# %%
P = linalg.solve_continuous_are(A, B, Q, R)
K = np.linalg.inv(R) @ B.T @ P

# %%
print(np.linalg.eigvals(A - B @ K).real.round(3))

# %%
class Controller:
    def __init__(self):
        self.me = me
        self.ne = ne
        self.K = K
        pass
    
    def reset(self):
        pass
    
    def run(
            self,
            t,                      # current time
            p_x, p_y, p_z,          # components of position (+z is down!)
            psi, theta, phi,        # yaw, pitch, and roll angles
            v_x, v_y, v_z,          # components of linear velocity in the body frame
            w_x, w_y, w_z,          # components of angular velocity in the body frame
        ):
        # Compute the state error
        m = np.array([
            [p_y],
            [psi],
            [theta],
            [phi],
            [v_x],
            [v_y],
            [v_z],
            [w_x],
            [w_y],
            [w_z]
        ])
        me = self.me
        x = m - me
        K = self.K
        u = -K @ x
        # print(me.shape)

        ne = self.ne
        # print(u[0], ne[0])
        delta_r = u[0] + ne[0]
        delta_l = u[1] + ne[1]

        return delta_r[0], delta_l[0]

# %%
controller = Controller()

# %%
def simulate_trials(N):
    data = []
    results = []
    for i in range(N):
        simulator.reset()
        controller.reset()
        datum = simulator.run(controller, maximum_time=20.0)
        data.append(datum)
        results.append(simulator.has_landed())
    return data, results
data, results = simulate_trials(4000)

# %%
print(f'Successful landings: {sum(results)} out of {len(results)}')
successRate = 100 * sum(results) / len(results)
print(f'Success rate: {successRate:.1f}%')

# %%
plt.rcParams.update({'font.size': 14}) # font size for plots
counter = 0
counter2 = 0
maximum = 20
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
for i in range(len(data)):
    if not results[i] and counter < maximum // 2: # Identify failed landings
        if counter == 0:
            label = 'Failed Landings'
        else:
            label = None
        counter += 1
        datum = data[i]
        x = datum['p_x'][:len(datum['p_x'])//6 * 5]
        y = datum['p_y'][:len(datum['p_y'])//6 * 5]
        z = datum['p_z'][:len(datum['p_z'])//6 * 5]
        ax1.plot(x, -z, 'r', linewidth=0.4, label=label)
        ax2.plot(x, y, 'r', linewidth=0.4, label=label)
    if results[i] and counter2 < maximum: # Identify successful landings
        if counter2 == 0:
            label = 'Successful Landings'
        else:
            label = None
        counter2 += 1
        datum = data[i]
        x = datum['p_x']
        y = datum['p_y']
        z = datum['p_z']
        ax1.plot(x, -z, 'g', linewidth=0.3, label=label)
        ax2.plot(x, y, 'g', linewidth=0.3, label=label)
# plot platform
platx = np.linspace(147.5, 167.5, 10)
platy = np.linspace(-1.75, 1.75, 30)
ax1.plot(platx, np.ones_like(platx)*-15.0, 'k--', linewidth=1)
ax1.set_ylabel('p_z (m)')
ax1.set_ylim(-20, 2)
ax2.plot(platx, np.ones_like(platx)*1.75, 'k--', linewidth=1)
ax2.plot(platx, np.ones_like(platx)*-1.75, 'k--', linewidth=1)
ax2.plot(np.ones_like(platy)*147.5, platy, 'k--', linewidth=1)
ax2.plot(np.ones_like(platy)*167.5, platy, 'k--', linewidth=1)
ax2.set_ylabel('p_y (m)')
ax2.set_xlabel('p_x (m)')
ax2.set_ylim(-17, 17)
ax1.legend(loc='upper right', fontsize=16)
for ax in (ax1, ax2):
    ax.grid(True, alpha = 0.3)
fig.set_tight_layout(True)
fig.savefig('pzpy_px.pdf', facecolor='white', transparent=False)
plt.show()

# %%
counter = 0
counter2 = 0
maximum = 20
fig, (ax1) = plt.subplots(1, 1, figsize=(10, 6))
for i in range(len(data)):
    if not results[i] and counter < maximum // 2: # Identify failed landings
        if counter == 0:
            label = 'Failed Landings'
        else:
            label = None
        counter += 1
        datum = data[i]
        x = datum['p_x'][:len(datum['p_x'])//6 * 5]
        t = datum['t'][:len(datum['t'])//6 * 5]
        ax1.plot(t, x, 'r', linewidth=0.3, label=label)
    if results[i] and counter2 < maximum: # Identify successful landings
        if counter2 == 0:
            label = 'Successful Landings'
        else:
            label = None
        counter2 += 1
        datum = data[i]
        x = datum['p_x']
        t = datum['t']
        ax1.plot(t, x, 'g', linewidth=0.3, label=label)
# plot platform
platx = np.ones(100)*147.5
platy = np.linspace(0, 20, 100)
plt.plot(platy, platx, 'k--', linewidth=1)
plt.plot(platy, platx + 20, 'k--', linewidth=1)
ax1.set_xlabel('Time (s)', fontsize=20)
ax1.set_ylabel('p_z (m)', fontsize = 20)
ax1.legend(loc='lower right', fontsize=16)
ax1.grid(True, alpha = 0.3)
fig.set_tight_layout(True)
fig.savefig('px_time.pdf', facecolor='white', transparent=False)
plt.show()

# %%
counter = 0
counter2 = 0
maximum = 10
phi_0 = []
theta_0 = []
psi_0 = []
# orientation over time
fig, (ax_yaw, ax_pitch, ax_roll) = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
for i in range(len(data)):
    datum = data[i]
    t = datum['t']
    yaw = datum['psi']
    pitch = datum['theta']
    roll = datum['phi']
    if results[i] and counter < maximum:
        if counter == 0:
            label = 'Successful Landings'
        else:
            label = None
        ax_yaw.plot(t, yaw, 'g', label=None)
        ax_pitch.plot(t, pitch, 'g', label=label)
        ax_roll.plot(t, roll, 'g', label=None)
        counter += 1
    if not results[i]:
        slice = len(yaw)//40 * 31
        yaw = yaw[:slice]
        pitch = pitch[:slice]
        roll = roll[:slice]
        t = t[:slice]
        phi_0.append(roll[0])
        theta_0.append(pitch[0])
        psi_0.append(yaw[0])
        if counter2 < maximum // 2:
            if counter2 == 0:
                label = 'Failed Landings'
            else:
                label = None
            ax_yaw.plot(t, yaw, 'r', label=None)
            ax_pitch.plot(t, pitch, 'r', label=None)
            ax_roll.plot(t, roll, 'r', label=label)
            counter2 += 1

ax_yaw.set_ylabel('Yaw (rad)', fontsize=18)
ax_pitch.set_ylabel('Pitch (rad)', fontsize=18)
ax_roll.set_ylabel('Roll (rad)', fontsize=18)
ax_roll.set_xlabel('Time (s)', fontsize=18)
ax_yaw.set_ylim(-0.75, 0.85)
ax_pitch.set_ylim(-0.8, 0.6)
ax_roll.set_ylim(-0.5, 0.6)
for ax in (ax_yaw, ax_pitch, ax_roll):
    ax.grid(True, alpha = 0.3)
ax_pitch.legend(loc='lower right', fontsize=15)
ax_roll.legend(loc='lower right', fontsize=15)
fig.set_tight_layout(True)
fig.savefig('orientation_time.pdf', facecolor='white', transparent=False)
plt.show()

# %%
psi = np.asarray(psi_0)
theta = np.asarray(theta_0)
phi = np.asarray(phi_0)

xmin = np.min([psi.min(), theta.min(), phi.min()])
xmax = np.max([psi.max(), theta.max(), phi.max()])
bins = np.linspace(xmin, xmax, len(psi)//10)

fig, axes = plt.subplots(1, 3, figsize=(12, 3), sharex=True, sharey=True)

axes[0].hist(psi,   bins=bins, density=False)
axes[0].set_xlabel('Yaw (rad)', fontsize=16)
axes[1].hist(theta, bins=bins, density=False)
axes[1].set_xlabel('Pitch (rad)', fontsize=16)
axes[2].hist(phi,   bins=bins, density=False)
axes[2].set_xlabel('Roll (rad)', fontsize=16)

# Only one set of axis labels for the whole figure:
axes[0].set_ylabel('Frequency', x=0.03, fontsize=16)

for ax in axes:
    ax.grid(True, alpha = 0.3)

fig.tight_layout()
fig.savefig('failed_orientations.pdf', facecolor='white', transparent=False)

plt.show()


# Archived notebook code; see README.md for authorship, dependencies, and saved-run limitations.

# %%
# Standard modules
import time
import numpy as np
import matplotlib.pyplot as plt

# My own script (an interface to the simulator)
import ae353_spacecraft_simulate

# %%
import sympy as sym
import numpy as np
from IPython.display import display, Markdown
import ae353_spacecraft_design as design

# Suppress the use of scientific notation when printing small numbers
np.set_printoptions(suppress=True)

# %%
# Create the visualizer
vis = design.create_visualizer()

# Show the visualizer in this notebook
vis.jupyter_cell()

# %%
dstar = np.arcsin(1/3)
print(np.degrees(dstar))
wheels = [
    {'alpha': 0, 'delta': -np.pi / 2},
    {'alpha': np.pi, 'delta': dstar},
    {'alpha': 5*np.pi/3, 'delta': dstar},
    {'alpha': 7*np.pi/3, 'delta': dstar}    
]

# %%
design.show_wheels(vis, wheels)

# %%
m, J = design.create_spacecraft(wheels)

display(Markdown(
       r'$$'
    + fr'm = {sym.latex(np.round(m, decimals=2))}'
    +  r' \qquad\qquad '
    + fr'J = {sym.latex(sym.Matrix(J.round(decimals=2)))}'
    +  r'$$'
))

# %%
stars = [
    {'alpha':  0.00, 'delta':  0.00},
    {'alpha':  0.00, 'delta':  0.1},
    {'alpha':  0.10, 'delta':  0.10},
    {'alpha':  0.10, 'delta':  -0.10},
    {'alpha':  -0.10, 'delta':  -0.10},
    {'alpha':  -0.10, 'delta':  0.10},
    {'alpha': 0., 'delta': -0.1}# <-- To add a star, append a copy of this dict to the list. To change
                                      #     the location of a star, change the value of alpha and delta
]
# np.random.seed(1)
# angles1 = np.random.uniform(-0.3, 0.3, size=10)
# angles2 = np.random.uniform(-0.3, 0.3, size=10)
# angles = list(zip(angles1, angles2))
# stars = [
#     {'alpha': angle[0], 'delta': angle[1]} for angle in angles
# ]

# %%
design.show_stars(stars)

# %%
design.create_stars(stars)

# %%
# Define yaw, pitch, roll angles
psi, theta, phi = sym.symbols('psi, theta, phi')

# Define angular velocities
w_x, w_y, w_z = sym.symbols('w_x, w_y, w_z')

# Define torques
tau_1, tau_2, tau_3, tau_4 = sym.symbols('tau_1, tau_2, tau_3, tau_4')

# Compute resultant torques
T1 = - tau_1 * sym.Matrix(wheels[0]['xyz']) / np.linalg.norm(wheels[0]['xyz'])
T2 = - tau_2 * sym.Matrix(wheels[1]['xyz']) / np.linalg.norm(wheels[1]['xyz'])
T3 = - tau_3 * sym.Matrix(wheels[2]['xyz']) / np.linalg.norm(wheels[2]['xyz'])
T4 = - tau_4 * sym.Matrix(wheels[3]['xyz']) / np.linalg.norm(wheels[3]['xyz'])
T = sym.nsimplify(T1 + T2 + T3 + T4)

# Define rotation matrices
Rz = sym.Matrix([[sym.cos(psi), -sym.sin(psi), 0], [sym.sin(psi), sym.cos(psi), 0], [0, 0, 1]])
Ry = sym.Matrix([[sym.cos(theta), 0, sym.sin(theta)], [0, 1, 0], [-sym.sin(theta), 0, sym.cos(theta)]])
Rx = sym.Matrix([[1, 0, 0], [0, sym.cos(phi), -sym.sin(phi)], [0, sym.sin(phi), sym.cos(phi)]])

# Define the transformation from angular velocity to angular rates
ex = sym.Matrix([[1], [0], [0]])
ey = sym.Matrix([[0], [1], [0]])
ez = sym.Matrix([[0], [0], [1]])
M = sym.simplify(sym.Matrix.hstack((Ry @ Rx).T @ ez, Rx.T @ ey, ex).inv(), full=True)

# Define euler's equations
Jx, Jy, Jz = [sym.nsimplify(j) for j in np.diag(J)]
euler = sym.Matrix([[(1 / Jx) * (T[0] + (Jy - Jz) * w_y * w_z)],
                    [(1 / Jy) * (T[1] + (Jz - Jx) * w_z * w_x)],
                    [(1 / Jz) * (T[2] + (Jx - Jy) * w_x * w_y)]])

# Define equations of motion
f = sym.simplify(sym.Matrix.vstack(M @ sym.Matrix([[w_x], [w_y], [w_z]]), euler), full=True)

# %%
f

# %%
alpha_star_i, delta_star_i = sym.symbols('alpha_star_i, delta_star_i')

# %%
# Position of star in space frame
p_star_in_space = sym.Matrix([[sym.cos(delta_star_i) * sym.cos(alpha_star_i)],
                              [sym.sin(alpha_star_i) * sym.cos(delta_star_i)],
                              [sym.sin(delta_star_i)]])

# Orientation of body frame in space frame
R_body_in_space = Rz @ Ry @ Rx

# Position of star in body frame (assuming origin of body and space frames are the same)
p_star_in_body = R_body_in_space.T @ p_star_in_space

# Position of star in image frame
r = sym.nsimplify(design.scope_radius)
p_star_in_image = (1 / r) * sym.Matrix([[p_star_in_body[1] / p_star_in_body[0]],
                                        [p_star_in_body[2] / p_star_in_body[0]]])

# Sensor model for star $i$
g_star_i = sym.simplify(p_star_in_image, full=True)

# %%
g_star_i

# %%
m = sym.Matrix([psi, theta, phi, w_x, w_y, w_z])
n = sym.Matrix([tau_1, tau_2, tau_3, tau_4])
params = {
    psi: 0.,
    theta: 0.,
    phi: 0.,
    w_x: 0.,
    w_y: 0.,
    w_z: 0.,
    tau_1: 0.,
    tau_2: 0.,
    tau_3: 0.,
    tau_4: 0.
}
A = f.jacobian(m).subs(params)
A = np.array(A).astype(np.float64)
A

# %%
B = f.jacobian(n).evalf(15, chop=True)
B = np.array(B).astype(np.float64)
B

# %%
W = B
for i in range(1,len(B)):
    col = np.linalg.matrix_power(A,i) @ B
    W = np.hstack((W,col))
rank = np.linalg.matrix_rank(W)
print(f'Rank = {rank}')

# Fixed controller weights
Q = 1000 * np.diag([16, 12, 8, 96, 36, 36])
R = 40 * np.eye(4)

def lqr(A, B, Q, R):
    """Solve the continuous time LQR controller.

    dx/dt = A x + B u

    cost = integral x.T*Q*x + u.T*R*u dt
    """
    from scipy import linalg

    # Solve the Riccati equation
    P = linalg.solve_continuous_are(A, B, Q, R)

    # Compute the LQR gain
    K = np.linalg.inv(R) @ B.T @ P

    return K, P
# Continuous-time LQR to get K (fixed for all Qo, Ro)
K, P_K = lqr(A, B, Q, R)

from scipy import linalg
from sympy.physics import mechanics
# Find the optimal cost matrix and gain matrix (both should be 2D NumPy arrays)
P = linalg.solve_continuous_are(A,B,Q,R)
K = np.linalg.inv(R) @ B.T @ P

# Latex output
K_r = np.around(K, decimals=2)
K_sym = sym.Matrix(K_r)
# print(mechanics.mlatex(K_sym))
K_sym

# %%
eigvals, eigvecs = np.linalg.eig(A - B @ K)
print(np.all(eigvals.real < 0))

# %%
star_meas_eq = []
C = []
C_sym = g_star_i.jacobian(m)
for i in range(len(stars)):
    alpha = stars[i]['alpha']
    delta = stars[i]['delta']
    g_input = {psi:0,
               theta:0,
               phi:0,
               alpha_star_i:alpha,
               delta_star_i:delta}
    
    row = np.array(g_star_i.subs(g_input)).astype(np.float64).reshape((2,)).tolist()
    star_meas_eq.append(row)

    coord = {alpha_star_i:alpha,
             delta_star_i:delta}
    C_nominal = C_sym.subs(coord).subs(params)
    C_i = np.array(C_nominal).astype(np.float64)
    C.append(C_i.tolist())

C = np.vstack(C)
star_meas_eq = np.hstack(star_meas_eq)
sym.Matrix(C)

# %%
import sympy as sym
from scipy import linalg
def W_o(A, c):
    """Compute the observability matrix W_o for given A and C matrices."""
    n = A.shape[0]
    W = c
    for i in range(1, n):
        W = np.vstack((W, c @ np.linalg.matrix_power(A, i)))
    return W
    
rank = sym.Matrix(W_o(A, C).T).rank()
print(f"Column rank of W_o for (A, C):", rank)
print(f"Is (A, C) observable?", rank == A.shape[0])

# %%
def lqr(A, B, Q, R):
    P = linalg.solve_continuous_are(A, B, Q, R)
    K = linalg.inv(R) @ B.T @ P
    return K, P
print(C.shape)
Qo = 10 * np.diag([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])
Ro = 5 * np.diag([10., 10., 10., 1., 1., 1.])
L_transpose, P = lqr(A.T, C.T, linalg.inv(Ro), linalg.inv(Qo))
L = np.round(L_transpose.T, 10)
sym.Matrix(L)

# %%
eigvals2, eigvecs2 = np.linalg.eig(A - L @C)
print(np.all(eigvals2.real < 0))

# %%
simulator = ae353_spacecraft_simulate.Simulator(
    display=False,
    seed=None,
)

# %%
simulator.camera_scopeview()

# %%
class Controller:
    def __init__(self):
        self.variables_to_log = ['tau', 'xhat']
        self.dt = 0.04
        self.psi_e, self.theta_e, self.phi_e = 0., 0., 0.
        self.w_x_e, self.w_y_e, self.w_z_e = 0., 0., 0.
        self.q_e = star_meas_eq
        self.tau1_e, self.tau2_e, self.tau3_e, self.tau4_e = 0., 0., 0., 0.
        self.tau_e = np.array([self.tau1_e, self.tau2_e, self.tau3_e, self.tau4_e])
        # state space
        self.A = A
        self.B = B
        self.C = C
        # controller and observer gain
        self.K = K
        self.L = L
    
    def reset(self):
        self.tau = np.array([0., 0., 0., 0.])
        self.xhat = np.array([0., 0., 0., 0., 0., 0.])
    
    def run(self, t, star_meas):
        """
        The variable t is the current time.

        The variable star_meas is a 1d array of length twice the
        number N of stars:

            [y_1, z_1, y_2, z_2, ..., y_N, z_N]
        
        The image coordinates y_i and z_i of the i'th star (for i = 1, ..., N)
        are at index 2 * i - 2 and 2 * i - 1 of this array, respectively.
        """
        q = star_meas
        u = - self.K @ self.xhat
        tau = u + self.tau_e
        y = q - self.q_e # CAREFUL: use q, not xhat
        tau = np.clip(u + self.tau_e, -2., 2.)
        self.xhat += self.dt * (self.A @ self.xhat + self.B @ tau - self.L @ (self.C @ self.xhat - y))
        self.tau = tau
        return tau[0], tau[1], tau[2], tau[3]

# %%
import numpy as np
import ae353_spacecraft_simulate

def simulate_trials(
    n_trials,
    scope_noise=0.1,   # std dev of image noise (tune as you like)
    max_time=60.0,
    display=False,      # turn off display for speed
    seed=None           # set to an int for reproducibility
):
    """
    Run n_trials Monte Carlo simulations with:
      - random initial conditions (initial_conditions=None)
      - given scope_noise
      - space_debris=True

    Returns
    -------
    data_list : list of dict
        Logged data for each trial (the dicts returned by simulator.run).
    success_list : list of bool
        True if the space-cat docked in that trial, False otherwise.
    """

    # Create a single simulator instance
    simulator = ae353_spacecraft_simulate.Simulator(
        display=display,
        seed=seed,
    )

    data_list = []
    success_list = []

    for k in range(n_trials):
        # Random initial conditions, noise on, debris on
        simulator.reset(
            initial_conditions=None,   # random ICs
            scope_noise=scope_noise,   # nonzero noise
            space_debris=True,         # debris on
        )

        # Fresh controller for each trial
        controller = Controller()
        controller.reset()

        # Run the simulation
        data = simulator.run(
            controller,
            max_time=max_time,
            data_filename=None,
            video_filename=None,
            print_debug=False,
        )

        data_list.append(data)
        success_list.append(simulator.has_docked())

    return data_list, success_list
data_list, success_list = simulate_trials(25)
# output success rate
success_rate = sum(success_list) / len(success_list)
print(f"Success rate: {success_rate * 100:.1f}%")

# %%
import numpy as np

def check_observer_requirement(data_list,
                               angle_tol_deg=2.0,
                               t_window=(20.0, 60.0),
                               min_success_frac=0.85):
    """
    Requirement:
      q95 = 95th percentile of attitude error over t in [t_window]
      q95 <= angle_tol_deg in at least min_success_frac of trials
    """

    q95_values = []

    for data in data_list:
        t = np.asarray(data["t"])
        psi   = np.asarray(data["psi"])
        theta = np.asarray(data["theta"])
        phi   = np.asarray(data["phi"])

        # xhat assumed logged as [psi_hat, theta_hat, phi_hat, w_x_hat, w_y_hat, w_z_hat]
        xhat = np.asarray(data["xhat"])
        psi_hat   = xhat[:, 0]
        theta_hat = xhat[:, 1]
        phi_hat   = xhat[:, 2]

        # Restrict to t in [20, 60] (or whatever t_window is)
        mask = (t >= t_window[0]) & (t <= t_window[1])
        if not np.any(mask):
            continue  # no samples in window for this trial

        # Attitude error magnitude in radians
        err_rad = np.sqrt(
            (psi[mask]   - psi_hat[mask])**2 +
            (theta[mask] - theta_hat[mask])**2 +
            (phi[mask]   - phi_hat[mask])**2
        )

        # Convert to degrees and compute 95th percentile
        err_deg = np.degrees(err_rad)
        q95 = np.percentile(err_deg, 95)
        q95_values.append(q95)

    if len(q95_values) == 0:
        print("No valid trials with samples in the specified time window.")
        return

    q95_values = np.array(q95_values)
    num_ok = np.sum(q95_values <= angle_tol_deg)
    frac_ok = num_ok / len(q95_values)

    print(f"{num_ok}/{len(q95_values)} trials "
          f"({100*frac_ok:.1f}%) have q95 ≤ {angle_tol_deg:.1f}°.")

    if frac_ok >= min_success_frac:
        print("Observer requirement SATISFIED.")
    else:
        print("Observer requirement NOT satisfied.")
check_observer_requirement(data_list,
                           angle_tol_deg=5.0,
                           t_window=(20.0, 60.0),
                           min_success_frac=0.85)

# %%
def plot_observer_q95(q95_values,
                      angle_tol_deg=3.5,
                      min_success_frac=0.85):
    n = len(q95_values)
    trial_idx = np.arange(1, n + 1)

    passed = q95_values <= angle_tol_deg

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=False)

    # --- Plot 1: q95 per trial ---
    ax1.scatter(trial_idx[passed], q95_values[passed], label='Pass', marker='o')
    ax1.scatter(trial_idx[~passed], q95_values[~passed], label='Fail', marker='x')
    ax1.axhline(angle_tol_deg, linestyle='--',
                label=f'{angle_tol_deg:.1f}° requirement')
    ax1.set_ylabel('q95 (deg)')
    ax1.grid(True)
    ax1.legend()

    # --- Plot 2: histogram of q95 ---
    ax2.hist(q95_values, bins=10)
    ax2.axvline(angle_tol_deg, linestyle='--',
                label=f'{angle_tol_deg:.1f}° requirement')
    ax2.set_xlabel('q95 (deg)')
    ax2.set_ylabel('Count')
    ax2.grid(True)
    ax2.legend()


    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig('95th.pdf', facecolor='white', transparent=False)
    plt.show()
plot_observer_q95(q95_values)


# %%
import matplotlib.pyplot as plt
for i in range(len(data_list)):
    if i != 0:
        break # run for only the first trial for now
    data = data_list[i]
    # plot xhat[0] and psi over time,
    psi_hat = []
    for i in range(len(data['xhat'])):
        psi_hat.append(data['xhat'][i][0])
    time = data['t']
    plt.figure()
    plt.plot(time, psi_hat, label='xhat[0]')
    plt.plot(time, data['psi'], label='psi')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (rad)')
    plt.title('xhat[0] and psi over time')
    plt.grid()
    plt.show()
    # plot xhat[1] and theta over time,
    theta_hat = []
    for i in range(len(data['xhat'])):
        theta_hat.append(data['xhat'][i][1])
    time = data['t']
    plt.figure()
    plt.plot(time, theta_hat, label='xhat[1]')
    plt.plot(time, data['theta'], label='theta')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (rad)')
    plt.title('xhat[1] and theta over time')
    plt.grid()
    plt.show()
    # plot xhat[2] and phi over time,
    phi_hat = []
    for i in range(len(data['xhat'])):
        phi_hat.append(data['xhat'][i][2])
    time = data['t']
    plt.figure()
    plt.plot(time, phi_hat, label='xhat[2]')
    plt.plot(time, data['phi'], label='phi')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (rad)')
    plt.title('xhat[2] and phi over time')
    plt.grid()
    plt.show()
    # plot xhat[3] and w_x over time,
    w_x_hat = []
    for i in range(len(data['xhat'])):
        w_x_hat.append(data['xhat'][i][3])
    time = data['t']
    plt.figure()
    plt.plot(time, w_x_hat, label='xhat[3]')
    plt.plot(time, data['w_x'], label='w_x')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Rate (rad/s)')
    plt.title('xhat[3] and w_x over time')
    plt.grid()
    plt.show()
    # plot xhat[4] and w_y over time,
    w_y_hat = []
    for i in range(len(data['xhat'])):
        w_y_hat.append(data['xhat'][i][4])
    time = data['t']
    plt.figure()
    plt.plot(time, w_y_hat, label='xhat[4]')
    plt.plot(time, data['w_y'], label='w_y')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Rate (rad/s)')
    plt.title('xhat[4] and w_y over time')
    plt.grid()
    plt.show()
    # plot xhat[5] and w_z over time
    w_z_hat = []
    for i in range(len(data['xhat'])):
        w_z_hat.append(data['xhat'][i][5])
    time = data['t']
    plt.figure()
    plt.plot(time, w_z_hat, label='xhat[5]')
    plt.plot(time, data['w_z'], label='w_z')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Rate (rad/s)')
    plt.title('xhat[5] and w_z over time')
    plt.grid()
    plt.show()

# %%
# plot torques over time
for i in range(len(data_list)):
    if i != 0:
        break # run for only the first trial for now
    data = data_list[i]
    tau1 = []
    tau2 = []
    tau3 = []
    tau4 = []
    for i in range(len(data['tau'])):
        tau1.append(data['tau'][i][0])
        tau2.append(data['tau'][i][1])
        tau3.append(data['tau'][i][2])
        tau4.append(data['tau'][i][3])
    time = data['t']
    plt.figure()
    plt.plot(time, tau1, label='tau1')
    plt.plot(time, tau2, label='tau2')
    plt.plot(time, tau3, label='tau3')
    plt.plot(time, tau4, label='tau4')
    # plot torque limits from simulator
    plt.hlines(y=simulator.tau_max, xmin=time[0], xmax=time[-1], colors='r', linestyles='dashed', label='torque limits')
    plt.hlines(y=-simulator.tau_max, xmin=time[0], xmax=time[-1], colors='r', linestyles='dashed')

    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Torque (N·m)')
    plt.title('Control Torques over Time')
    plt.grid()
    plt.show()

# %%
print(len(data_list), len(success_list))

# %%
import numpy as np
import matplotlib.pyplot as plt

# Collect initial conditions for trials that fail in the first 10 seconds
psi0_failed = []
theta0_failed = []
phi0_failed = []

t_fail_threshold = 10.0  # seconds

for idx, data in enumerate(data_list):
    t = data['t']
    t_final = t[-1]

    # "Fail in the first 10 seconds" = did not dock AND sim ended before 10 s
    if (not success_list[idx]) and (t_final < t_fail_threshold):
        psi0_failed.append(data['psi'][0])    # yaw
        theta0_failed.append(data['theta'][0])  # pitch
        phi0_failed.append(data['phi'][0])    # roll

psi0_failed = np.array(psi0_failed)
theta0_failed = np.array(theta0_failed)
phi0_failed = np.array(phi0_failed)

print(f"Number of trials that failed within {t_fail_threshold} s: {len(psi0_failed)}")

if len(psi0_failed) == 0:
    print("No trials failed within the first 10 seconds; nothing to plot.")
else:
    # Separate figure with 3 histograms: yaw, pitch, roll
    plt.rcParams.update({'font.size': 14})
    fig, axes = plt.subplots(3, 1, figsize=(8, 10), sharex=False)

    # Histogram of initial yaw (psi)
    axes[0].hist(psi0_failed, bins=15, edgecolor='black')
    axes[0].set_title('Initial Yaw (ψ) for Trials that Fail < 10 s')
    axes[0].set_xlabel('ψ₀ (rad)')
    axes[0].set_ylabel('Count')
    axes[0].grid(alpha=0.1)

    # Histogram of initial pitch (theta)
    axes[1].hist(theta0_failed, bins=15, edgecolor='black')
    axes[1].set_title('Initial Pitch (θ) for Trials that Fail < 10 s')
    axes[1].set_xlabel('θ₀ (rad)')
    axes[1].set_ylabel('Count')
    axes[1].grid(alpha=0.1)

    # Histogram of initial roll (phi)
    axes[2].hist(phi0_failed, bins=15, edgecolor='black')
    axes[2].set_title('Initial Roll (φ) for Trials that Fail < 10 s')
    axes[2].set_xlabel('φ₀ (rad)')
    axes[2].set_ylabel('Count')
    axes[2].grid(alpha=0.1)
    

    fig.tight_layout()
    plt.show()

# %%
times = []
for i in range(len(data_list)):
    data = data_list[i]
    if not success_list[i]:
        # create a histogram of maximum time of failed trials
       times.append(data['t'][-1])
plt.figure()
plt.hist(times, bins=15, edgecolor='black')
plt.xlabel('Time (s)')
plt.ylabel('Frequency')
plt.title('Histogram of Maximum Time for Failed Trials')
plt.grid()
plt.show()


# %%
controller = Controller()

# %%
simulator.reset(
    initial_conditions={
        'psi': 0.,
        'theta': 0.,
        'phi': 0.,
        'w_x': 0.,
        'w_y': 0.,
        'w_z': 0.,
    },
    scope_noise=0.1,        # <-- standard deviation of each image coordinate of each star tracker measurement
    space_debris=True,      # <-- whether or not there is space debris
)

# %%
simulator.reset(
    initial_conditions=None,
    scope_noise=0.0,        # <-- standard deviation of each image coordinate of each star tracker measurement
    space_debris=True,      # <-- whether or not there is space debris
)

# %%
controller.reset()

# %%
data = simulator.run(
    controller,           # <-- required (an instance of your Controller class)
    max_time=60.0,         # <-- optional (how long you want to run the simulation in seconds)
    data_filename=None,   # <-- optional (name of file to which you want data saved, e.g., 'my_data.json')
    video_filename=None,  # <-- optional (name of file to which you want video saved, e.g., 'my_video.mov')
    print_debug=False,    # <-- optional (whether to print debug text - this is recommended when saving video)
)

# %%
has_docked = simulator.has_docked()
if has_docked:
    print('The space-cat docked.')
else:
    print('The space-cat did not dock.')

# %%
# Set the width and height of the snapshot (must be multiples of 16)
simulator.set_snapshot_size(
    640, # <-- width
    480, # <-- height
)

# Get snapshot as height x width x 4 numpy array of RGBA values
rgba = simulator.snapshot()

# Display snapshot
plt.figure(figsize=(8, 8))
plt.imshow(rgba)

# Save snapshot
plt.imsave('my_snapshot.png', rgba)

# %%
# Create a figure with three subplots, all of which share the same x-axis
fig, (ax_ori, ax_vel, ax_rwvel, ax_rwtau) = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

# Plot yaw, pitch, roll angles
ax_ori.plot(data['t'], data['psi'], label=r'$\psi$ (rad)', linewidth=4)
ax_ori.plot(data['t'], data['theta'], label=r'$\theta$ (rad)', linewidth=4)
ax_ori.plot(data['t'], data['phi'], label=r'$\phi$ (rad)', linewidth=4)
ax_ori.grid()
ax_ori.legend(fontsize=16, ncol=3, loc='upper right')
ax_ori.tick_params(labelsize=14)

# Plot x, y, z components of angular velocity
ax_vel.plot(data['t'], data['w_x'], label=r'$w_x$ (rad/s)', linewidth=4)
ax_vel.plot(data['t'], data['w_y'], label=r'$w_y$ (rad/s)', linewidth=4)
ax_vel.plot(data['t'], data['w_z'], label=r'$w_z$ (rad/s)', linewidth=4)
ax_vel.grid()
ax_vel.legend(fontsize=16, ncol=3, loc='upper right')
ax_vel.tick_params(labelsize=14)

# Plot angular velocity of each reaction wheel
ax_rwvel.plot(data['t'], data['wheel_1_velocity'], label=r'$v_1$ (rad/s)', linewidth=4)
ax_rwvel.plot(data['t'], data['wheel_2_velocity'], label=r'$v_2$ (rad/s)', linewidth=4)
ax_rwvel.plot(data['t'], data['wheel_3_velocity'], label=r'$v_3$ (rad/s)', linewidth=4)
ax_rwvel.plot(data['t'], data['wheel_4_velocity'], label=r'$v_4$ (rad/s)', linewidth=4)
ax_rwvel.plot(
    data['t'], np.ones_like(data['t']) * simulator.v_max,
    ':', linewidth=4, color='C4', zorder=0,
)
ax_rwvel.plot(
    data['t'], -np.ones_like(data['t']) * simulator.v_max,
    ':', linewidth=4, color='C4', zorder=0,
)
ax_rwvel.grid()
ax_rwvel.legend(fontsize=16, ncol=4, loc='upper right')
ax_rwvel.tick_params(labelsize=14)
ax_rwvel.set_ylim(-1.2 * simulator.v_max, 1.2 * simulator.v_max)

# Plot torque applied to each reaction wheel
ax_rwtau.plot(data['t'], data['torque_1'], label=r'$\tau_1$ (N-m)', linewidth=4)
ax_rwtau.plot(data['t'], data['torque_2'], label=r'$\tau_2$ (N-m)', linewidth=4)
ax_rwtau.plot(data['t'], data['torque_3'], label=r'$\tau_3$ (N-m)', linewidth=4)
ax_rwtau.plot(data['t'], data['torque_4'], label=r'$\tau_4$ (N-m)', linewidth=4)
ax_rwtau.plot(
    data['t'], np.ones_like(data['t']) * simulator.tau_max,
    ':', linewidth=4, color='C4', zorder=0,
)
ax_rwtau.plot(
    data['t'], -np.ones_like(data['t']) * simulator.tau_max,
    ':', linewidth=4, color='C4', zorder=0,
)
ax_rwtau.grid()
ax_rwtau.legend(fontsize=16, ncol=4, loc='upper right')
ax_rwtau.tick_params(labelsize=14)


# Set x-axis properties (only need to do this on the last
# subplot since all subplots share the same x-axis)
ax_rwtau.set_xlabel('time (s)', fontsize=20)
ax_rwtau.set_xlim([data['t'][0], data['t'][-1]])
ax_rwtau.set_ylim(-1.2 * simulator.tau_max, 1.2 * simulator.tau_max)

# Make the arrangement of subplots look nice
fig.tight_layout()

# %%
fig.savefig('my_figure.png', facecolor='white', transparent=False)

# %%
if len(simulator.stars) < 1:
    raise Exception('There must be at least one star in order to plot star locations.')

# Create a figure with one subplots
fig, ax = plt.subplots(1, 1, figsize=(9, 9))

# Scatter-plot the position of all stars at all time steps in the scope
for i in range(len(simulator.stars)):
    y = data['star_meas'][:, 2 * i]
    z = data['star_meas'][:, 2 * i + 1]
    ax.plot(y, z, label=f'star {i + 1}', linestyle='none', marker='.', markersize=6)

# Change appearance of axes
ax.grid()
ax.legend(fontsize=16)
ax.tick_params(labelsize=14)
ax.set_xlim(1., -1.) # <-- the "y_star" axis points left (not right)
ax.set_ylim(-1., 1.) # <-- the "z_star" axis points up

# Make the arrangement of subplots look nice
fig.tight_layout()

# %%


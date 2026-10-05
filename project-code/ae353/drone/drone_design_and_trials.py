# Archived notebook code; see README.md for authorship and saved-run scope.

# %%
import sympy as sym
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import secrets
import ae353_drone

# Suppress the use of scientific notation when printing small numbers
np.set_printoptions(suppress=True)

# %%
params = {
    'm': 0.5,
    'Jx': 0.0023,
    'Jy': 0.0023,
    'Jz': 0.0040,
    'l': 0.175,
    'g': 9.81,
}

# %%
# components of position (meters)
p_x, p_y, p_z = sym.symbols('p_x, p_y, p_z')

# yaw, pitch, roll angles (radians)
psi, theta, phi = sym.symbols('psi, theta, phi')

# components of linear velocity (meters / second)
v_x, v_y, v_z = sym.symbols('v_x, v_y, v_z')
v_in_body = sym.Matrix([v_x, v_y, v_z])

# components of angular velocity (radians / second)
w_x, w_y, w_z = sym.symbols('w_x, w_y, w_z')
w_in_body = sym.Matrix([w_x, w_y, w_z])

# components of net rotor torque
tau_x, tau_y, tau_z = sym.symbols('tau_x, tau_y, tau_z')

# net rotor force
f_z = sym.symbols('f_z')

# parameters
m = sym.nsimplify(params['m'])
Jx = sym.nsimplify(params['Jx'])
Jy = sym.nsimplify(params['Jy'])
Jz = sym.nsimplify(params['Jz'])
l = sym.nsimplify(params['l'])
g = sym.nsimplify(params['g'])
J = sym.diag(Jx, Jy, Jz)

# rotation matrices
Rz = sym.Matrix([[sym.cos(psi), -sym.sin(psi), 0], [sym.sin(psi), sym.cos(psi), 0], [0, 0, 1]])
Ry = sym.Matrix([[sym.cos(theta), 0, sym.sin(theta)], [0, 1, 0], [-sym.sin(theta), 0, sym.cos(theta)]])
Rx = sym.Matrix([[1, 0, 0], [0, sym.cos(phi), -sym.sin(phi)], [0, sym.sin(phi), sym.cos(phi)]])
R_body_in_world = Rz @ Ry @ Rx

# angular velocity to angular rates
ex = sym.Matrix([[1], [0], [0]])
ey = sym.Matrix([[0], [1], [0]])
ez = sym.Matrix([[0], [0], [1]])
M = sym.simplify(sym.Matrix.hstack((Ry @ Rx).T @ ez, Rx.T @ ey, ex).inv(), full=True)

# applied forces
f_in_body = R_body_in_world.T @ sym.Matrix([[0], [0], [-m * g]]) + sym.Matrix([[0], [0], [f_z]])

# applied torques
tau_in_body = sym.Matrix([[tau_x], [tau_y], [tau_z]])

# equations of motion
f = sym.Matrix.vstack(
    R_body_in_world @ v_in_body,
    M @ w_in_body,
    (1 / m) * (f_in_body - w_in_body.cross(m * v_in_body)),
    J.inv() @ (tau_in_body - w_in_body.cross(J @ w_in_body)),
)

f = sym.simplify(f, full=True)

# %%
f

# %%
# Position of drone in world frame
p_in_world = sym.Matrix([p_x, p_y, p_z])

# Position of markers in body frame
a_in_body = sym.Matrix([l, 0, 0])  # <-- marker on front rotor
b_in_body = sym.Matrix([-l, 0, 0]) # <-- marker on back rotor

# Position of markers in world frame
a_in_world = p_in_world + R_body_in_world @ a_in_body
b_in_world = p_in_world + R_body_in_world @ b_in_body

# Sensor model
g = sym.simplify(sym.Matrix.vstack(a_in_world, b_in_world))

# %%
g

# %%
# All elements of the state (of the nonlinear system) as symbolic variables
m = [p_x, p_y, p_z, psi, theta, phi,
     v_x, v_y, v_z, w_x, w_y, w_z]


# All elements of the input (of the nonlinear system) as symbolic variables
n = [tau_x, tau_y, tau_z, f_z]

# %%
# f as a lambda function that can be evaluated for different choices of m and n
f_num = sym.lambdify(m + n, f)

# Equilibrium value of all elements of the state (of the nonlinear system)
m_e = [0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0]
# Equilibrium value of all elements of the input (of the nonlinear system)
n_e = [0, 0, 0, .5 * 9.81 ]

# Check if m_e, n_e really is an equilibrium point.
assert(np.isclose(f_num(*(m_e + n_e)), 0).all())

# %%
# Create lambda functions to evaluate the Jacobian of f with respect to m and n at different values of m_e and n_e.
A_num = sym.lambdify(m + n, f.jacobian(m))
B_num = sym.lambdify(m + n, f.jacobian(n))

# Evaluate these lambda functions at the values of m_e and n_e

A = A_num(*(m_e + n_e))
B = B_num(*(m_e + n_e))

# %%
# Lambda functions to evaluate the Jacobian of g with
# respect to m and n at different values of m_e and n_e.
C_num = sym.lambdify(m + n, g.jacobian(m))
D_num = sym.lambdify(m + n, g.jacobian(n))

# Evaluate these lambda functions at these values of m_e and n_e.
C = C_num(*(m_e + n_e))
D = D_num(*(m_e + n_e))

# g as a lambda function that can be evaluated for different choices of m and n
g_num = sym.lambdify(m + n, g)

# Find the sensor measurements that you would expect to see at equilibrium
o_e = g_num(*(m_e + n_e)).reshape(-1)

# %%
m_e = np.array(m_e)
n_e = np.array(n_e)
o_e = np.array(o_e)

assert(m_e.ndim == 1)
assert(n_e.ndim == 1)
assert(o_e.ndim == 1)

# %%
# Verify that the controllability matrix is full rank.
def w(A, B):
    n = A.shape[0]
    W = B
    for i in range(1, n):
        W = np.hstack((W, np.linalg.matrix_power(A, i) @ B))
    return W
assert(np.linalg.matrix_rank(w(A, B)) == A.shape[0])

# %%
from scipy.linalg import solve_continuous_are
def lqr(A, B, Q, R):
    P = solve_continuous_are(A, B, Q, R)
    return np.linalg.inv(R) @ B.T @ P # = K

# %%
Q_c = 0.1 * np.diag([10, 10, 2e4, 5, 10, 10, 50, 50, 50, 100, 100, 100])
R_c = 1e4 * np.eye(4)
R_c[3,3] = 50 # this was changed to get better altitude response

# %%
K = lqr(A, B, Q_c, R_c)
sym.Matrix(np.round(K, decimals=10))

# %%
# Verify that the observability matrix is full rank.
def Wo(A, C):
    n = A.shape[0]
    O = C
    for i in range(1, n):
        O = np.vstack((O, C @ np.linalg.matrix_power(A, i)))
    return O
assert(np.linalg.matrix_rank(Wo(A, C)) == A.shape[0])

# %%
Q_o = 1 * np.diag([1,1,1,1,1,1])
R_o = np.diag([1,1,1,1,1,1,1,1,1,1,1,1])

# %%
L = lqr(A.T, C.T, R_o, Q_o).T
sym.Matrix(np.round(L, decimals=10))

# %%
def rnd(a, decimals=5):
    return np.round(a, decimals=decimals).tolist()

# %%
print(f'        self.A = np.array({rnd(A)})')
print(f'        self.B = np.array({rnd(B)})')
print(f'        self.C = np.array({rnd(C)})')
print(f'        self.K = np.array({rnd(K)})')
print(f'        self.L = np.array({rnd(L)})')
print(f'        self.m_e = np.array({rnd(m_e)})')
print(f'        self.n_e = np.array({rnd(n_e)})')
print(f'        self.o_e = np.array({rnd(o_e)})')

# %%
# code to generate random seeds. This is optional since using seed 'None' will give random initial conditions and obstacle/ring placements.
seeds = []
for i in range(100):
    seed = secrets.randbits(32)
    seeds.append(seed)
print(seeds)
# for reproducibility:
seeds = [2812816404, 3319318006, 4134580205, 512536746, 3273172, 1482039977, 2105047229, 734853473, 1447591964, 280058207, 2403158312, 1730952578, 2965541946, 1227161350, 1712631873, 3262058154, 1832764077, 3289404194, 2054551452, 3095679145, 815448959, 2484579243, 3380000840, 3561208952, 3607607621, 1056684227, 1906033592, 430846658, 2375084387, 2523463334, 3731812540, 580132413, 2816419673, 343654134, 1550748766, 1665080722, 3782336809, 1910171075, 2082180065, 2667812483, 537464174, 2096516479, 3135564586, 530478035, 3798215386, 3920953163, 264578494, 3465300166, 4078772635, 1825318116, 3612984420, 2711104723, 388136987, 1184547647, 536264869, 177462116, 1590664855, 2831844785, 2514272229, 379307730, 1910761814, 1394130460, 668871610, 1689662277, 2968722032, 3501356906, 1613659932, 1554197767, 1558299263, 4151255549, 113833022, 1933679150, 1254406836, 592777328, 1520712260, 1695080225, 2268309066, 1626161924, 2048803010, 2582911230, 3341063493, 2364145758, 1307744386, 2358205254, 1939055455, 1870801166, 2050707370, 3308510432, 622200493, 3309875839, 789211350, 640582918, 2195910550, 873730423, 2422743589, 1682204637, 2117565206, 594633587, 205111785, 2740526439]

# %%
simulator = ae353_drone.Simulator(seed=seeds[0]) # in this case, the first seed from the list

# %%
simulator.add_view(
    'back_view',  # name of view (must be unique)
    'back',       # type of view (start, top, right, left, or back)
)

# %%
import numpy as np

class Controller:
    def __init__(self):
        # System matrices and gains (assumed defined globally)
        self.A = A
        self.B = B
        self.C = C
        self.K = K
        self.L = L
        # Equilibrium (hover, level)
        self.m_e = np.zeros(12)
        self.n_e = np.array([0.0, 0.0, 0.0, 4.905])
        self.o_e = np.array([0.175, 0.0, 0.0, -0.175, 0.0, 0.0])
        self.f_ze = self.n_e[3]

        # Timing
        self.dt = 0.04  # 25 Hz

        # Obstacle repulsion (dogs / other drones)
        self.k_repel      = 0.5 # gain for real obstacles
        self.k_repel_ring = 0.2 # smaller gain for ring obstacle (tune this)
        self.r_drone = 0.3      # safe radius around drone
        self.R_far   = 4.0      # radius within which repulsion is active

        # Reference motion (low-pass waypoint tracking, base values)
        self.k_ref_pos = 2.85   # p_ref' = k_ref_pos (p_target - p_ref)
        self.v_max     = 1.0    # |v_ref| <= v_max

        # Ring targeting (near/far waypoints)
        self.vertical_offset     = 0.2
        self.horizontal_offset   = 0.85
        self.near_reached_radius = 0.75
        self.far_reached_radius  = 0.75

        # Ring geometry (for closest-point calculation)
        self.ring_radius = 1.0

        # Active ring visit state
        self.active_ring_center    = None
        self.active_ring_dir       = None
        self.active_side_sign      = 1.0
        self.ring_phase            = 'near'   # 'near' or 'far'
        self.active_ring_completed = True

        # All rings seen so far: list of dicts {'center': ..., 'dir': ...}
        self.rings = []

        # Internal reference position
        self.p_ref = None

        # Logging
        self.variables_to_log = ['xhat', 'xdes']

    def get_color(self):
        # Team Luke
        return [0.114, 0.788, 0.42]

    def reset(self, p_x, p_y, p_z, yaw):
        # State estimate
        self.xhat = np.array([
            p_x, p_y, p_z,
            yaw, 0.0, 0.0,
            0.0, 0.0, 0.0,
            0.0, 0.0, 0.0
        ])
        self.xdes = np.zeros(12)

        # Reference position
        self.p_ref = np.array([p_x, p_y, p_z], dtype=float)

        # Ring visit state
        self.active_ring_center    = None
        self.active_ring_dir       = None
        self.active_side_sign      = 1.0
        self.ring_phase            = 'near'
        self.active_ring_completed = True

        # Clear ring list
        self.rings = []

    def _register_ring(self, pos_ring, dir_ring):
        # Store each ring (center + unit normal) once.
        center = np.array(pos_ring, dtype=float)
        n = np.array(dir_ring, dtype=float)
        n_norm = np.linalg.norm(n)
        n = n / n_norm if n_norm > 1e-6 else np.array([1.0, 0.0, 0.0])

        for r in self.rings:
            if np.linalg.norm(r['center'] - center) < 1e-3:
                r['dir'] = n
                return

        self.rings.append({'center': center, 'dir': n})

    def _closest_ring_point(self, p_est):
        # Determine closest point on hoop of closest ring to p_est.
        if len(self.rings) == 0:
            return None

        best_point = None
        best_dist = np.inf

        for r in self.rings:
            c = r['center']
            n = r['dir']

            # Vector from center to drone
            q = p_est - c
            # Decompose into plane (perpendicular to n)
            d_n = np.dot(q, n)
            q_plane = q - d_n * n
            r_plane = np.linalg.norm(q_plane)

            if r_plane < 1e-6:
                # Drone is almost on the normal through the center:
                if abs(n[0]) < 0.9:
                    a = np.array([1.0, 0.0, 0.0])
                else:
                    a = np.array([0.0, 1.0, 0.0])
                q_plane_dir = np.cross(n, a)
                q_plane_dir /= np.linalg.norm(q_plane_dir)
            else:
                q_plane_dir = q_plane / r_plane

            # Closest point on ring hoop
            ring_point = c + self.ring_radius * q_plane_dir

            d = np.linalg.norm(p_est - ring_point)
            if d < best_dist:
                best_dist = d
                best_point = ring_point

        return best_point

    def _lock_new_ring_visit(self, p_est, pos_ring, dir_ring):
        # Lock in a new ring visit (center, dir, side) when no active ring is present.
        center = np.array(pos_ring, dtype=float)
        n = np.array(dir_ring, dtype=float)
        n_norm = np.linalg.norm(n)
        n = n / n_norm if n_norm > 1e-6 else np.array([1.0, 0.0, 0.0])

        v_to_ring = p_est - center
        side_sign = -1.0 if np.dot(v_to_ring, n) < 0.0 else 1.0

        self.active_ring_center    = center
        self.active_ring_dir       = n
        self.active_side_sign      = side_sign
        self.ring_phase            = 'near'
        self.active_ring_completed = False

    def _obstacle_repulsion(self, p_est, pos_list, gain):
        # Generic repulsion for a list of obstacle positions using a specified gain.
        if gain <= 0.0 or pos_list is None or len(pos_list) == 0:
            return np.zeros(3)

        h_repel = np.zeros(3)
        for obst_pos in np.atleast_2d(pos_list):
            diff = p_est - obst_pos
            dist = np.linalg.norm(diff)
            if dist < 1e-6 or dist > self.R_far:
                continue

            d_clear = dist - self.r_drone
            if d_clear <= 0.0:
                d_clear = 0.05

            denom_far = self.R_far - self.r_drone
            if denom_far <= 0.0:
                denom_far = 0.1

            mag = (1.0 / d_clear) - (1.0 / denom_far)
            if mag <= 0.0:
                continue

            h_repel += mag * (diff / dist)

        return gain * h_repel

    def _local_speed_limits(self, p_est, ring_center, pos_all_for_speed):
        # Slow speed near ring and obstacles,
        # speed up when far away
        d_ring = np.linalg.norm(p_est - ring_center)

        d_obst = np.inf
        if pos_all_for_speed is not None and len(pos_all_for_speed) > 0:
            for obst_pos in np.atleast_2d(pos_all_for_speed):
                d = np.linalg.norm(obst_pos - p_est)
                if d < d_obst:
                    d_obst = d

        v = self.v_max
        k = self.k_ref_pos
        
        if d_obst > 4.0:    # Far from everything
            v *= 2.5
            k *= 2.0
        elif d_obst > 2.5:  # Medium distance
            v *= 2.0
            k *= 1.5
        elif d_obst < 1.5:  # Very close to ring or obstacle
            v *= 0.7
            k *= 0.8
        return v, k
    def run(self, pos_markers, pos_ring, dir_ring, is_last_ring, pos_others):
        # Position estimate
        p_est = self.xhat[0:3]
        if self.p_ref is None:
            self.p_ref = p_est.copy()

        # Track rings and ring visit logic (near → far)
        self._register_ring(pos_ring, dir_ring)

        if self.active_ring_center is None or self.active_ring_completed:
            self._lock_new_ring_visit(p_est, pos_ring, dir_ring)

        center = self.active_ring_center
        n      = self.active_ring_dir
        side   = self.active_side_sign
        v_off  = self.vertical_offset
        h_off  = self.horizontal_offset

        p_near = center + side * n * h_off        + np.array([0.0, 0.0, v_off])
        p_far  = center - side * 1.25 * n * h_off + np.array([0.0, 0.0, v_off])

        if is_last_ring:
            p_target_nominal = center + np.array([0.0, 0.0, 0.1])
            self.active_ring_completed = True
        elif self.ring_phase == 'near':
            p_target_nominal = p_near
            if np.linalg.norm(p_est - p_near) <= self.near_reached_radius:
                self.ring_phase = 'far'
        else:
            p_target_nominal = p_far
            if np.linalg.norm(p_est - p_far) <= self.far_reached_radius:
                self.active_ring_completed = True

        # Define ring obstacle (only in 'near' phase)
        ring_obst = None
        if self.ring_phase == 'near':
            ring_obst = self._closest_ring_point(p_est)

        # Combined list for speed-limiting logic (dogs/drones + ring point if present)
        if ring_obst is not None:
            if pos_others is None or len(pos_others) == 0:
                pos_all_for_speed = np.array(ring_obst, ndmin=2)
            else:
                pos_all_for_speed = np.vstack([np.atleast_2d(pos_others), ring_obst])
        else:
            pos_all_for_speed = pos_others

        # Obstacle repulsion with separate gains for ring and other obstacles
        h_repel_other = self._obstacle_repulsion(p_est, pos_others, self.k_repel)
        if ring_obst is not None:
            h_repel_ring = self._obstacle_repulsion(p_est,
                                                    np.array(ring_obst, ndmin=2),
                                                    self.k_repel_ring)
        else:
            h_repel_ring = np.zeros(3)

        h_repel = h_repel_other + h_repel_ring

        # Reference position update with obstacle repulsion
        p_target = p_target_nominal + h_repel
        v_max_local, k_ref_local = self._local_speed_limits(p_est, center, pos_all_for_speed)

        e_ref = p_target - self.p_ref
        v_ref = k_ref_local * e_ref

        speed = np.linalg.norm(v_ref)
        if speed > v_max_local:
            v_ref *= v_max_local / speed

        self.p_ref = self.p_ref + self.dt * v_ref
        p_des, v_des = self.p_ref, v_ref

        # Desired state
        xdes = np.zeros(12)
        xdes[0:3] = p_des
        xdes[6:9] = v_des
        self.xdes = xdes

        # Control Law with torque and force limits
        u = -self.K @ (self.xhat - xdes)
        u[2] = np.clip(u[2], -0.16, 0.16)
        u[3] = np.clip(u[3], -22.68, 22.68)

        # Update observer
        y = self.C @ self.xhat
        self.xhat = self.xhat + self.dt * (
            self.A @ self.xhat + self.B @ u + self.L @ (pos_markers - y)
        )

        # Outputs
        tau_x, tau_y, tau_z = u[0], u[1], u[2]
        f_z = u[3] + self.f_ze

        return tau_x, tau_y, tau_z, f_z


# %%
# Run a single simulation with the view enabled
simulator.add_drone(Controller, 'mlutter2', 'mlutter2.png')
simulator.reset()
simulator.run(max_time=90.0, print_debug=False)
simulator.clear_drones()

def simulate_trials(n, seeds=None):
    data_list = []
    success_list = []
    finish_times = []
    rings_per_trial = []   # NEW: store rings for each trial

    for i in range(n):
        # initialize simulator with specific seed if provided
        if seeds is not None and i < len(seeds):
            simulator = ae353_drone.Simulator(seed=seeds[i])
        else:
            simulator = ae353_drone.Simulator(seed=None)

        simulator.disable_views()
        simulator.add_drone(Controller, 'mlutter2', 'mlutter2.png')
        simulator.reset()
        simulator.run(max_time=85.0, print_debug=False)

        # data for this trial
        rings_out = []
        for r in simulator.rings:
            rings_out.append({
                'p': np.array(r['p'], dtype=float).copy(),      # center (3,)
                'R': np.array(r['R'], dtype=float).copy(),      # rotation matrix (3x3)
                'radius': float(r['radius']),                   # scalar
            })
        rings_per_trial.append(rings_out)
        data_list.append(simulator.get_data('mlutter2'))
        did_it_finish, finish_time = simulator.get_result('mlutter2')[1:]
        success_list.append(did_it_finish)
        if did_it_finish:
            finish_times.append(finish_time)
        # clear drones in this simulator instance
        simulator.clear_drones()

    return data_list, success_list, finish_times, rings_per_trial


# %%
data_list, success_list, finish_times, rings_per_trial = simulate_trials(len(seeds), seeds)
success_rate = sum(success_list) / len(success_list)
print(f'Success rate: {success_rate * 100}%')

# %%
finish_times = np.asarray(finish_times)

if finish_times.size == 0:
    print("No successful runs — average completion time undefined.")
else:
    avg_time = np.mean(finish_times)
    std_time = np.std(finish_times)
    min_time = np.min(finish_times)
    max_time = np.max(finish_times)

    print(f"Average completion time: {avg_time:.2f} s")
    print(f"Std dev: {std_time:.2f} s")
    print(f"Min / Max: {min_time:.2f} / {max_time:.2f} s")


# %%
import numpy as np
import matplotlib.pyplot as plt

def plot_3d_with_rings(
    data_list,
    success_list,
    rings_per_trial,
    max_success=0,
    max_failure=0,
    plot_success=False,
    plot_failure=False,
):
    label_fs = 16
    tick_fs  = 14

    fig3d = plt.figure(figsize=(8, 6))
    ax3d = fig3d.add_subplot(111, projection='3d')
    fig2d, ax2d = plt.subplots(figsize=(7, 5))

    colors = plt.cm.tab10(np.linspace(0, 1, 10))

    # ----- choose which trials go in 3D -----
    indices_3d = []
    success_count_3d = 0
    failure_count_3d = 0

    for i, success in enumerate(success_list):
        if success:
            if not plot_success or success_count_3d >= max_success:
                continue
            success_count_3d += 1
        else:
            if not plot_failure or failure_count_3d >= max_failure:
                continue
            failure_count_3d += 1
        indices_3d.append(i)

    # ----- choose which trials go in 2D (up to double the 3D caps) -----
    indices_2d = []
    success_count_2d = 0
    failure_count_2d = 0

    for i, success in enumerate(success_list):
        if success:
            if not plot_success or success_count_2d >= 2 * max_success:
                continue
            success_count_2d += 1
        else:
            if not plot_failure or failure_count_2d >= 2 * max_failure:
                continue
            failure_count_2d += 1
        indices_2d.append(i)

    # ----- plot 3D + 2D for 3D trials -----
    color_idx = 0
    for i in indices_3d:
        data = data_list[i]

        color = colors[color_idx % len(colors)]
        color_idx += 1

        x = np.array([
            data['p_x'], data['p_y'], data['p_z'],
            data['yaw'], data['pitch'], data['roll'],
            data['v_x'], data['v_y'], data['v_z'],
            data['w_x'], data['w_y'], data['w_z']
        ]).T
        xhat = np.array(data['xhat'])

        pos_actual = x[:, 0:3]
        pos_est    = xhat[:, 0:3]

        # 3D trajectories
        ax3d.plot(pos_actual[:, 0], pos_actual[:, 1], pos_actual[:, 2], color=color)
        ax3d.plot(pos_est[:, 0], pos_est[:, 1], pos_est[:, 2],
                  linestyle='--', color=color, alpha=0.7)

        ax3d.scatter(pos_actual[0, 0],  pos_actual[0, 1],  pos_actual[0, 2],
                     marker='o', color=color)
        ax3d.scatter(pos_actual[-1, 0], pos_actual[-1, 1], pos_actual[-1, 2],
                     marker='x', color=color)

        # 2D trajectories (x-y)
        ax2d.plot(pos_actual[:, 0], pos_actual[:, 1], color='red', alpha=0.9)
        ax2d.plot(pos_est[:, 0], pos_est[:, 1],
                  linestyle='--', color='red', alpha=0.5)

        ax2d.scatter(pos_actual[0, 0],  pos_actual[0, 1],
                     marker='o', color='red')
        ax2d.scatter(pos_actual[-1, 0], pos_actual[-1, 1],
                     marker='x', color='red')

        # 3D rings for this trial (same color)
        rings = rings_per_trial[i]
        for ring in rings:
            p = ring['p']
            R = ring['R']
            r = ring['radius']

            theta = np.linspace(0, 2 * np.pi, 200)
            circle_local = np.vstack([
                np.zeros_like(theta),
                r * np.cos(theta),
                r * np.sin(theta)
            ])  # (3, N)

            circle_world = p.reshape(3, 1) + R @ circle_local

            ax3d.plot(circle_world[0, :],
                      circle_world[1, :],
                      circle_world[2, :],
                      color=color, linewidth=1)

    # ----- plot extra 2D-only trials -----
    for i in indices_2d:
        if i in indices_3d:
            continue  # already plotted above

        data = data_list[i]
        x = np.array([
            data['p_x'], data['p_y'], data['p_z'],
            data['yaw'], data['pitch'], data['roll'],
            data['v_x'], data['v_y'], data['v_z'],
            data['w_x'], data['w_y'], data['w_z']
        ]).T
        xhat = np.array(data['xhat'])

        pos_actual = x[:, 0:3]
        pos_est    = xhat[:, 0:3]

        ax2d.plot(pos_actual[:, 0], pos_actual[:, 1], color='red', alpha=0.6)
        ax2d.plot(pos_est[:, 0], pos_est[:, 1],
                  linestyle='--', color='red', alpha=0.4)

        ax2d.scatter(pos_actual[0, 0],  pos_actual[0, 1],
                     marker='o', color='red')
        ax2d.scatter(pos_actual[-1, 0], pos_actual[-1, 1],
                     marker='x', color='red')

    # ----- 2D rings: use the first 3D trial if it exists -----
    if indices_3d:
        first_idx = indices_3d[0]
        rings_2d = rings_per_trial[first_idx]

        for ring in rings_2d:
            p = ring['p']
            R = ring['R']
            r = ring['radius']

            theta = np.linspace(0, 2 * np.pi, 200)
            circle_local = np.vstack([
                np.zeros_like(theta),
                r * np.cos(theta),
                r * np.sin(theta)
            ])
            circle_world = p.reshape(3, 1) + R @ circle_local

            ax2d.plot(circle_world[0, :],
                      circle_world[1, :],
                      color='k', linewidth=2, alpha=0.7)

    # ----- Axes formatting -----
    ax3d.set_xlabel('x [m]', fontsize=label_fs)
    ax3d.set_ylabel('y [m]', fontsize=label_fs)
    ax3d.set_zlabel('z [m]', fontsize=label_fs, labelpad=8)  # key line
    ax3d.set_xlim(0.0, 17.5)
    ax3d.set_ylim(-5.0, 5.0)
    ax3d.set_zlim(0.0, 6.0)
    ax3d.tick_params(axis='both', labelsize=tick_fs)
    ax3d.tick_params(axis='z', labelsize=tick_fs)

    # keep default axes position; no tight_layout on 3D
    # (optional) tweak a bit if you want more right margin:
    # fig3d.subplots_adjust(right=0.88)

    ax2d.set_xlabel('x [m]', fontsize=label_fs)
    ax2d.set_ylabel('y [m]', fontsize=label_fs)
    ax2d.set_xlim(-4.0, 20.0)
    ax2d.set_ylim(-6.0, 6.0)
    ax2d.set_aspect('equal', adjustable='box')
    ax2d.tick_params(axis='both', labelsize=tick_fs)

    fig2d.tight_layout()
    fig2d.savefig('trajectories.pdf', bbox_inches='tight')
    plt.show()

plot_3d_with_rings(
    data_list,
    success_list,
    rings_per_trial,
    max_failure=3,
    plot_failure=True,
)

# %%
def collect_position_errors(data_list):
    """
    Returns:
      err_act_des : 1D array of |p - p_des| over all trials and timesteps
      err_act_est : 1D array of |p - p_hat| over all trials and timesteps
    """
    err_act_des_all = []
    err_act_est_all = []

    for data in data_list:
        # actual positions (N, 3)
        p = np.vstack([data['p_x'], data['p_y'], data['p_z']]).T  # (N, 3)

        # desired and estimated states (N, 12)
        xdes = np.asarray(data['xdes'])
        xhat = np.asarray(data['xhat'])

        p_des = xdes[:, 0:3]
        p_hat = xhat[:, 0:3]

        err_act_des = np.linalg.norm(p - p_des, axis=1)
        err_act_est = np.linalg.norm(p - p_hat, axis=1)

        err_act_des_all.append(err_act_des)
        err_act_est_all.append(err_act_est)

    if len(err_act_des_all) == 0:
        return np.array([]), np.array([])

    return np.concatenate(err_act_des_all), np.concatenate(err_act_est_all)


def extract_completion_times(success_list, data_list):
    """
    Supported patterns (per element of success_list):
      1) tuple: (failed, finished, finish_time)
      2) dict:  {'failed': bool, 'finished': bool, 'finish_time': float}
      3) bool:  True => treat last time in data['t'] as completion

    Returns:
      completion_times : 1D array of finish times for successful runs
    """
    completion_times = []

    for i, s in enumerate(success_list):
        # case 1: tuple
        if isinstance(s, tuple) and len(s) == 3:
            failed, finished, finish_time = s
            if finished and not failed and (finish_time is not None):
                completion_times.append(finish_time)

        # case 2: dict
        elif isinstance(s, dict):
            failed = s.get('failed', False)
            finished = s.get('finished', False)
            finish_time = s.get('finish_time', None)
            if finished and not failed and (finish_time is not None):
                completion_times.append(finish_time)

        # case 3: plain bool
        elif isinstance(s, bool):
            if s:
                t = np.asarray(data_list[i]['t'])
                if t.size > 0:
                    completion_times.append(t[-1])

        # otherwise: ignore

    return np.asarray(completion_times)


def collect_run_times(data_list):
    """
    Assumes each data dict has key 'run_time' with per-step controller runtime.
    Returns:
      run_times : 1D array of all controller runtimes across all trials.
    """
    all_rt = []
    for data in data_list:
        if 'run_time' in data:
            all_rt.append(np.asarray(data['run_time']))
    if len(all_rt) == 0:
        return np.array([])
    return np.concatenate(all_rt)


def plot_error_histograms(
    data_list,
    bins=50,
    label_fs=16,
    tick_fs=14,
    filename='hist_errors.pdf'
):
    """
    Figure 1: histograms of |p - p_des| and |p - p_hat|.
    """
    err_act_des, err_act_est = collect_position_errors(data_list)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    ax1, ax2 = axes

    # 1) |actual - desired|
    if err_act_des.size > 0:
        ax1.hist(err_act_des, bins=bins * 50)
        ax1.set_xlim(left=0, right=np.percentile(err_act_des, 97.5))
    ax1.set_xlabel(r'$||p - p_{des}||$ [m]', fontsize=label_fs)
    ax1.set_ylabel('Count', fontsize=label_fs)
    ax1.tick_params(axis='both', labelsize=tick_fs)

    # 2) |actual - estimated|
    if err_act_est.size > 0:
        ax2.hist(err_act_est, bins=bins * 20)
        ax2.set_xlim(left=0, right=np.percentile(err_act_est, 97.5))
    ax2.set_xlabel(r'$||p - \hat{p}||$ [m]', fontsize=label_fs)
    # ax2.set_ylabel('Count', fontsize=label_fs)
    ax2.tick_params(axis='both', labelsize=tick_fs)
    

    fig.tight_layout()
    fig.savefig(filename)
    return fig, axes


def plot_completion_histogram(
    data_list,
    success_list,
    label_fs=16,
    tick_fs=14,
    filename='hist_completion_times.pdf'
):
    """
    Figure 2: histogram of completion times (successful runs).
    """
    completion_times = extract_completion_times(success_list, data_list)

    fig, ax = plt.subplots(1, 1, figsize=(5, 4))

    if completion_times.size > 0:
        ax.hist(completion_times, bins=20)

    ax.set_xlabel('Time to Finish [s]', fontsize=label_fs)
    ax.set_ylabel('Count', fontsize=label_fs)
    ax.tick_params(axis='both', labelsize=tick_fs)

    fig.tight_layout()
    fig.savefig(filename)
    return fig, ax


def plot_runtime_histogram(
    data_list,
    bins=50,
    label_fs=16,
    tick_fs=14,
    filename='hist_run_times.pdf'
):
    """
    Figure 3: histogram of controller computation times.
    """
    run_times = collect_run_times(data_list)

    fig, ax = plt.subplots(1, 1, figsize=(5, 4))

    if run_times.size > 0:
        ax.hist(run_times, bins=bins * 20)
        ax.set_xlim(left=0, right=np.percentile(run_times, 97.5))

    ax.set_xlabel('Run Time per Step [s]', fontsize=label_fs)
    ax.set_ylabel('Count', fontsize=label_fs)
    ax.tick_params(axis='both', labelsize=tick_fs)

    # --- Scientific notation on x-axis ---
    fmt = ScalarFormatter(useMathText=True)
    fmt.set_powerlimits((-3, 3))   # use 10^k when values are small/large
    ax.xaxis.set_major_formatter(fmt)

    fig.tight_layout()
    fig.savefig(filename)
    return fig, ax


# Example usage:
fig_err, axes_err = plot_error_histograms(
    data_list,
    bins=50,
    label_fs=16,
    tick_fs=14,
    filename='hist_errors.pdf'
)

fig_comp, ax_comp = plot_completion_histogram(
    data_list,
    success_list,
    label_fs=16,
    tick_fs=14,
    filename='hist_completion_times.pdf'
)

fig_rt, ax_rt = plot_runtime_histogram(
    data_list,
    bins=50,
    label_fs=16,
    tick_fs=14,
    filename='hist_run_times.pdf'
)

plt.show()


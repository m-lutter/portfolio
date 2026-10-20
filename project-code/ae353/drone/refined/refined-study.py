# Refined AE353 DP4 study: frozen 1,000-course presentation version.
# Extracted without changing code-cell contents from the saved HTML export.
# Original project: Maxwell Lutter and Landon Lopez; later extension by Maxwell Lutter.
# Course staff supplied the simulator, assets, measurements, actuator rules, and scoring.
# Read README.md and source-provenance.json before interpreting or running this file.
# This is a code-cell export: executing it runs the evaluation and creates plots.

# %% Frozen code cell 1
from pathlib import Path
from collections import Counter
from contextlib import contextmanager, redirect_stdout
import io
import math
import os
import secrets
import sys
import time

import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
from scipy.linalg import solve_continuous_are
from scipy.stats import qmc

# Look in the working folder and its parents for the simulator and its assets.
# *Path.cwd().parents unpacks the parent folders into the search list.
# next(..., None) returns the first matching folder, or None if none match.
SIMULATOR_DIR = next(
    (folder for root in (Path.cwd(), *Path.cwd().parents)
     for folder in (root, root / "course", root / "AE353 Drone Lab" / "course")
     if (folder / "ae353_drone.py").is_file() and (folder / "urdf").is_dir()),
    None,
)
if SIMULATOR_DIR is None:
    raise FileNotFoundError("Place ae353_drone.py and its urdf/ assets beside the notebook or in course/.")
# Add the simulator's folder to Python's import search path.
if str(SIMULATOR_DIR) not in sys.path:
    sys.path.insert(0, str(SIMULATOR_DIR))
import ae353_drone

np.set_printoptions(suppress=True)


# %% Frozen code cell 2
N_TRIALS = 1000
MAX_TIME_S = 80.0       # Stop each flight after this many simulated seconds.
RUN_LIVE_VIEW = False
RUN_SEARCH = False

PLOT_DIR = Path.cwd() / "plots"  # Save plots here; rerunning a plot replaces its PNG.


# %% Frozen code cell 3
params = {
    'm': 0.5, # Drone mass [kg]
    'Jx': 0.0023, # Moment of inertia about body x [kg m^2]
    'Jy': 0.0023, # Moment of inertia about body y [kg m^2]
    'Jz': 0.0040, # Moment of inertia about body z [kg m^2]
    'l': 0.175, # Distance from the body center to a rotor [m]
    'g': 9.81, # Gravitational acceleration [m/s^2]
}


# %% Frozen code cell 4
# Position is measured along the fixed world axes [m].
p_x, p_y, p_z = sym.symbols('p_x, p_y, p_z')

# Orientation uses yaw, pitch, and roll, in that order [rad].
psi, theta, phi = sym.symbols('psi, theta, phi')

# Linear velocity is expressed along the rotating body axes [m/s].
v_x, v_y, v_z = sym.symbols('v_x, v_y, v_z')
v_in_body = sym.Matrix([v_x, v_y, v_z])

# Angular velocity also uses body axes [rad/s]. These are not Euler angle rates.
w_x, w_y, w_z = sym.symbols('w_x, w_y, w_z')
w_in_body = sym.Matrix([w_x, w_y, w_z])

# Combined rotor torque about each body axis [N m].
tau_x, tau_y, tau_z = sym.symbols('tau_x, tau_y, tau_z')

# Combined rotor thrust along positive body z [N].
f_z = sym.symbols('f_z')

# Use exact SymPy numbers so the symbolic algebra can cancel terms cleanly.
m = sym.nsimplify(params['m'])
Jx = sym.nsimplify(params['Jx'])
Jy = sym.nsimplify(params['Jy'])
Jz = sym.nsimplify(params['Jz'])
l = sym.nsimplify(params['l'])
g = sym.nsimplify(params['g'])
J = sym.diag(Jx, Jy, Jz)

# Map body vectors into world axes.
Rz = sym.Matrix([[sym.cos(psi), -sym.sin(psi), 0], [sym.sin(psi), sym.cos(psi), 0], [0, 0, 1]])
Ry = sym.Matrix([[sym.cos(theta), 0, sym.sin(theta)], [0, 1, 0], [-sym.sin(theta), 0, sym.cos(theta)]])
Rx = sym.Matrix([[1, 0, 0], [0, sym.cos(phi), -sym.sin(phi)], [0, sym.sin(phi), sym.cos(phi)]])
R_body_in_world = Rz @ Ry @ Rx

# Euler rotation axes expressed in body coordinates.
ex = sym.Matrix([[1], [0], [0]])
ey = sym.Matrix([[0], [1], [0]])
ez = sym.Matrix([[0], [0], [1]])
M = sym.simplify(sym.Matrix.hstack((Ry @ Rx).T @ ez, Rx.T @ ey, ex).inv(), full=True)

# Rotate world gravity into body axes, then add thrust along body z.
f_in_body = R_body_in_world.T @ sym.Matrix([[0], [0], [-m * g]]) + sym.Matrix([[0], [0], [f_z]])

# The control input supplies net rotor torque in body axes.
tau_in_body = sym.Matrix([[tau_x], [tau_y], [tau_z]])

# Stack four three-component equations to form the 12-state derivative.
# The cross products account for using a rotating body frame and for gyroscopic coupling.
f = sym.Matrix.vstack(
    R_body_in_world @ v_in_body,  # World position rate
    M @ w_in_body,  # Yaw, pitch, and roll rates
    (1 / m) * (f_in_body - w_in_body.cross(m * v_in_body)),  # Body velocity rate
    J.inv() @ (tau_in_body - w_in_body.cross(J @ w_in_body)),  # Body angular acceleration
)

f = sym.simplify(f, full=True)


# %% Frozen code cell 5
# Position of the body center in world coordinates.
p_in_world = sym.Matrix([p_x, p_y, p_z])

# Marker locations are fixed relative to the body center.
a_in_body = sym.Matrix([l, 0, 0])  # Front marker
b_in_body = sym.Matrix([-l, 0, 0]) # Back marker

# Rotate each marker's body offset into world axes and add the body position.
a_in_world = p_in_world + R_body_in_world @ a_in_body
b_in_world = p_in_world + R_body_in_world @ b_in_body

# Stack the two marker positions into the six measured coordinates.
g = sym.simplify(sym.Matrix.vstack(a_in_world, b_in_world))


# %% Frozen code cell 6
# Nonlinear state vector
m = [p_x, p_y, p_z, psi, theta, phi,
     v_x, v_y, v_z, w_x, w_y, w_z]


# Rotor torques and total thrust.
n = [tau_x, tau_y, tau_z, f_z]

# lambdify turns the symbolic expression into a numerical Python function.
# m + n joins the state and input lists to define its argument order.
f_num = sym.lambdify(m + n, f)

# Hover at the origin with zero angles and velocities.
m_e = [0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0]
# At hover, rotor torques are zero and thrust balances weight.
n_e = [0, 0, 0, .5 * 9.81 ]

# verify that the chosen hover condition is an equilibrium point.
# * unpacks the combined list into separate function arguments.
assert(np.isclose(f_num(*(m_e + n_e)), 0).all())

A_num = sym.lambdify(m + n, f.jacobian(m))
B_num = sym.lambdify(m + n, f.jacobian(n))

# Evaluate the Jacobians at hover to obtain constant linear-model matrices.

A = A_num(*(m_e + n_e))
B = B_num(*(m_e + n_e))

# Differentiate the sensor model in the same way. C maps state changes to
# measurement changes; D describes any direct dependence on control input.
C_num = sym.lambdify(m + n, g.jacobian(m))
D_num = sym.lambdify(m + n, g.jacobian(n))

# Use the same hover condition for the sensor and dynamics linearizations.
C = C_num(*(m_e + n_e))
D = D_num(*(m_e + n_e))

# Evaluate the sensor model to find the constant marker offsets at hover.
g_num = sym.lambdify(m + n, g)

# reshape(-1) makes this a flat six-element vector instead of a column matrix.
o_e = g_num(*(m_e + n_e)).reshape(-1)

# Use one-dimensional NumPy arrays for the numerical calculations below.
m_e = np.array(m_e)
n_e = np.array(n_e)
o_e = np.array(o_e)

assert(m_e.ndim == 1)
assert(n_e.ndim == 1)
assert(o_e.ndim == 1)


# %% Frozen code cell 7
def controllability_matrix(A, B):
    """Build [B, AB, A^2B, ...] to check which states the inputs can affect."""
    return np.hstack([np.linalg.matrix_power(A, i) @ B for i in range(A.shape[0])])


def observability_matrix(A, C):
    """Stack C, CA, CA^2, ... to check which states the outputs can reveal."""
    return np.vstack([C @ np.linalg.matrix_power(A, i) for i in range(A.shape[0])])


# Full rank means all 12 linearized states are controllable and observable.
controllability_rank = np.linalg.matrix_rank(controllability_matrix(A, B))
observability_rank = np.linalg.matrix_rank(observability_matrix(A, C))
assert controllability_rank == observability_rank == 12
assert np.allclose(D, 0)
print(f"Controllability: {controllability_rank}/12; observability: {observability_rank}/12")
print(f"Matrix shapes: A{A.shape}, B{B.shape}, C{C.shape}, D{D.shape}")


# %% Frozen code cell 8
def lqr(A, B, Q, R):
    """Compute the continuous-time LQR gain for the feedback law u = -Kx."""
    P = solve_continuous_are(A, B, Q, R)
    # P solves the Riccati equation; the feedback gain is K = R^-1 B.T P.
    return np.linalg.inv(R) @ B.T @ P


# Q_c weights state error in the state order defined above. R_c weights control effort.
Q_c = 0.1 * np.diag([10, 10, 2e4, 16, 10, 10, 50, 50, 50, 100, 100, 100])
R_c = 5e3 * np.eye(4)
R_c[3, 3] = 50  # Lower the effort penalty on the thrust increment.
K = lqr(A, B, Q_c, R_c)


# %% Frozen code cell 9
Q_o = np.diag([1, 1, 1, 1, 1, 1])
R_o = 5 * np.diag([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
# Observer design uses the dual LQR problem: transpose A and C, then transpose the gain.
# R_o supplies the 12-state weight and Q_o the six-output weight in this call.
# These are tuning weights; no measured noise covariance is assumed here.
L = lqr(A.T, C.T, R_o, Q_o).T

# The observer uses raw marker coordinates. This check confirms that L cancels
# their constant hover offset, so it has no effect on the observer correction.
assert np.allclose(L @ o_e, 0, atol=1e-12)
feedback_poles = np.linalg.eigvals(A - B @ K)
observer_poles = np.linalg.eigvals(A - L @ C)
# Continuous-time poles need negative real parts. After a forward Euler step,
# the discrete observer poles must lie inside the unit circle instead.
euler_observer_poles = np.linalg.eigvals(np.eye(12) + 0.04 * (A - L @ C))
assert np.max(feedback_poles.real) < 0
assert np.max(observer_poles.real) < 0
assert np.max(np.abs(euler_observer_poles)) < 1
print(f"Largest feedback-pole real part: {feedback_poles.real.max():.3f} 1/s")
print(f"Largest observer-pole real part: {observer_poles.real.max():.3f} 1/s")
print(f"Euler observer spectral radius: {np.abs(euler_observer_poles).max():.4f}")


# %% Frozen code cell 10
class Controller:
    """Waypoint guidance, reference tracking, and a linear state observer.

    State order: position, yaw/pitch/roll, linear velocity, angular velocity.
    Position uses world coordinates; both velocity vectors use body coordinates.
    A, B, C, K, and L must already exist in the notebook.
    """

    def __init__(self):
        # Model and gains from the preceding cells.
        self.A = A
        self.B = B
        self.C = C
        self.K = K
        self.L = L

        # Hover thrust [N]; feedback supplies the thrust increment.
        self.f_ze = 4.905
        self.dt = 0.04  # Simulation update interval, seconds.

        # Repulsion gains and geometry.
        self.k_repel = 0.5738086292675473
        self.k_repel_ring = 0.1538708995208036
        self.r_drone = 0.3
        self.R_far = 3.065142516730786
        self.ring_radius = 1.0

        # Reference speed and acceleration settings.
        self.k_ref_pos = 2.35068440264575
        self.v_max = 1.0822375538836575
        self.speed_near = 1.1799076547742369
        self.speed_far = 3.877616775315845
        self.a_ref_max = 5.526681078277944

        # Waypoint offsets and arrival tolerances [m].
        self.vertical_offset = 0.024085183610920987
        self.horizontal_offset = 1.0917208492102501
        self.near_reached_radius = 1.1280457117471288
        self.far_reached_radius = 0.6470852712756208


    def get_color(self):
        return [0.114, 0.788, 0.42]

    def reset(self, p_x, p_y, p_z, yaw):
        # Initialize from measured position and yaw; other states start at zero.
        self.xhat = np.array([
            p_x, p_y, p_z,
            yaw, 0.0, 0.0,
            0.0, 0.0, 0.0,
            0.0, 0.0, 0.0,
        ])
        self.xdes = np.zeros(12)
        self.p_ref = np.array([p_x, p_y, p_z], dtype=float)

        # Clear navigation state for the new flight.
        self.active_ring_center = None
        self.active_ring_dir = None
        self.active_side_sign = 1.0
        self.ring_phase = 'near'
        self.active_ring_completed = True
        self.rings = []

    def run(self, pos_markers, pos_ring, dir_ring, is_last_ring, pos_others):
        # 1. Choose the ring waypoint.
        p_est = self.xhat[0:3]
        p_nominal = self._nominal_target(
            p_est, pos_ring, dir_ring, is_last_ring
        )

        # 2. Include hoop avoidance during approach.
        ring_obst = None
        if self.ring_phase == 'near':
            ring_obst = self._closest_ring_point(p_est)

        # Include other objects and the hoop point in speed scheduling.
        if ring_obst is None:
            pos_all_for_speed = pos_others
        elif pos_others is None or len(pos_others) == 0:
            pos_all_for_speed = np.array(ring_obst, ndmin=2)
        else:
            pos_all_for_speed = np.vstack([
                np.atleast_2d(pos_others), ring_obst
            ])

        # Shift the target away from nearby objects.
        h_other = self._obstacle_repulsion(p_est, pos_others, self.k_repel)
        if ring_obst is None:
            h_ring = np.zeros(3)
        else:
            h_ring = self._obstacle_repulsion(
                p_est, np.array(ring_obst, ndmin=2), self.k_repel_ring
            )
        h_repel = h_other + h_ring
        p_target = p_nominal + h_repel

        # 3. Update the moving reference with speed and acceleration limits.
        self._update_reference(p_est, p_target, pos_all_for_speed)

        # 4. Apply feedback, then advance the observer.
        u = -self.K @ (self.xhat - self.xdes)
        # Limit yaw torque [N m] and thrust increment [N].
        u[2] = np.clip(u[2], -0.16, 0.16)
        u[3] = np.clip(u[3], -22.68, 22.68)

        # Forward Euler observer; the constant marker offset cancels through L.
        y = self.C @ self.xhat
        self.xhat = self.xhat + self.dt * (
            self.A @ self.xhat + self.B @ u + self.L @ (pos_markers - y)
        )

        # The observer uses clipped u; motor-speed limiting happens later in the simulator.
        tau_x, tau_y, tau_z = u[0], u[1], u[2]
        f_z = u[3] + self.f_ze
        return tau_x, tau_y, tau_z, f_z

    def _nominal_target(self, p_est, pos_ring, dir_ring, is_last_ring):
        """Choose the waypoint for the current ring and crossing phase."""
        self._register_ring(pos_ring, dir_ring)
        if self.active_ring_center is None or self.active_ring_completed:
            self._lock_new_ring_visit(p_est, pos_ring, dir_ring)

        center = self.active_ring_center
        n = self.active_ring_dir
        side = self.active_side_sign
        h_off = self.horizontal_offset
        v_off = self.vertical_offset

        # Place the departure waypoint 25% farther from the ring center.
        p_near = center + side * n * h_off + np.array([0.0, 0.0, v_off])
        p_far = center - side * 1.25 * n * h_off + np.array([0.0, 0.0, v_off])

        if is_last_ring:
            # Aim just above the final ring center.
            target = center + np.array([0.0, 0.0, 0.1])
            self.active_ring_completed = True
        elif self.ring_phase == 'near':
            target = p_near
            if np.linalg.norm(p_est - p_near) <= self.near_reached_radius:
                # Hoop avoidance ends now; this call still uses the near target.
                self.ring_phase = 'far'
        else:
            target = p_far
            if np.linalg.norm(p_est - p_far) <= self.far_reached_radius:
                self.active_ring_completed = True
        return target

    def _update_reference(self, p_est, p_target, pos_all_for_speed):
        """Move the reference toward the target and put it into the desired state."""
        v_max_local, k_ref_local = self._local_speed_limits(
            p_est, pos_all_for_speed
        )

        # Limit goal speed without changing direction.
        v_goal = k_ref_local * (p_target - self.p_ref)
        speed = np.linalg.norm(v_goal)
        if speed > v_max_local:
            v_goal *= v_max_local / speed

        # Limit the change from the previous reference velocity to a_max * dt.
        v_previous = self.xdes[6:9].copy()
        delta_v = v_goal - v_previous
        delta_speed = np.linalg.norm(delta_v)
        max_delta_speed = self.a_ref_max * self.dt
        if delta_speed > max_delta_speed:
            delta_v *= max_delta_speed / delta_speed
        v_ref = v_previous + delta_v

        # Integrate the limited velocity; braking can briefly exceed a reduced speed cap.
        self.p_ref = self.p_ref + self.dt * v_ref
        xdes = np.zeros(12)
        xdes[0:3] = self.p_ref
        # Near-hover approximation: use world reference velocity as body velocity.
        xdes[6:9] = v_ref
        self.xdes = xdes

    def _local_speed_limits(self, p_est, pos_all_for_speed):
        """Set speed and position gain smoothly from the nearest-object distance."""
        d_obst = np.inf
        if pos_all_for_speed is not None and len(pos_all_for_speed) > 0:
            offsets = np.atleast_2d(pos_all_for_speed) - p_est
            d_obst = np.min(np.linalg.norm(offsets, axis=1))

        # Blend near/far settings; no obstacles gives the fastest setting.
        t = np.clip(
            (d_obst - self.speed_near) / (self.speed_far - self.speed_near),
            0.0, 1.0,
        )
        # Smoothstep has zero slope at both distance thresholds.
        blend = t * t * (3.0 - 2.0 * t)
        v = self.v_max * (0.7 + 1.8 * blend)
        k = self.k_ref_pos * (0.8 + 1.2 * blend)
        return v, k

    def _obstacle_repulsion(self, p_est, pos_list, gain):
        """Add target offsets that point away from nearby objects."""
        if gain <= 0.0 or pos_list is None or len(pos_list) == 0:
            return np.zeros(3)

        h_repel = np.zeros(3)
        for obst_pos in np.atleast_2d(pos_list):
            diff = p_est - obst_pos
            dist = np.linalg.norm(diff)
            # Skip zero distance and objects beyond the influence radius.
            if dist < 1e-6 or dist > self.R_far:
                continue
            
            # Use surface clearance, with a 0.05 m fallback when nonpositive.
            d_clear = dist - self.r_drone
            if d_clear <= 0.0:
                d_clear = 0.05
            # Subtract the far-radius term so repulsion vanishes at R_far.
            denom_far = self.R_far - self.r_drone
            if denom_far <= 0.0:
                denom_far = 0.1

            mag = (1.0 / d_clear) - (1.0 / denom_far)
            if mag <= 0.0:
                continue
            h_repel += mag * (diff / dist)
        return gain * h_repel

    def _register_ring(self, pos_ring, dir_ring):
        """Remember ring centers and normals for the hoop-avoidance calculation."""
        center = np.array(pos_ring, dtype=float)
        n = np.array(dir_ring, dtype=float)
        n_norm = np.linalg.norm(n)
        n = n / n_norm if n_norm > 1e-6 else np.array([1.0, 0.0, 0.0])

        # Match remembered rings within 1 mm.
        for ring in self.rings:
            if np.linalg.norm(ring['center'] - center) < 1e-3:
                ring['dir'] = n
                return
        self.rings.append({'center': center, 'dir': n})

    def _lock_new_ring_visit(self, p_est, pos_ring, dir_ring):
        """Keep the ring and approach side fixed until the departure waypoint is reached."""
        center = np.array(pos_ring, dtype=float)
        n = np.array(dir_ring, dtype=float)
        n_norm = np.linalg.norm(n)
        n = n / n_norm if n_norm > 1e-6 else np.array([1.0, 0.0, 0.0])

        # Choose the approach side from the current position.
        v_to_ring = p_est - center
        side_sign = -1.0 if np.dot(v_to_ring, n) < 0.0 else 1.0
        self.active_ring_center = center
        self.active_ring_dir = n
        self.active_side_sign = side_sign
        self.ring_phase = 'near'
        self.active_ring_completed = False

    def _closest_ring_point(self, p_est):
        """Find the closest point on any ring hoop seen so far."""
        if len(self.rings) == 0:
            return None

        best_point = None
        best_dist = np.inf
        for ring in self.rings:
            center = ring['center']
            n = ring['dir']

            # Project the center-to-drone vector into the ring's plane.
            q = p_est - center
            d_n = np.dot(q, n)
            q_plane = q - d_n * n
            r_plane = np.linalg.norm(q_plane)

            if r_plane < 1e-6:
                # On the ring axis, choose any perpendicular direction in the ring plane.
                if abs(n[0]) < 0.9:
                    axis = np.array([1.0, 0.0, 0.0])
                else:
                    axis = np.array([0.0, 1.0, 0.0])
                q_plane_dir = np.cross(n, axis)
                q_plane_dir /= np.linalg.norm(q_plane_dir)
            else:
                q_plane_dir = q_plane / r_plane

            ring_point = center + self.ring_radius * q_plane_dir
            dist = np.linalg.norm(p_est - ring_point)
            if dist < best_dist:
                best_dist = dist
                best_point = ring_point
        return best_point


# %% Frozen code cell 11
# These navigation settings can be overridden for a trial or a search candidate.
PARAMETER_NAMES = (
    "v_max", "a_ref_max", "speed_near", "speed_far", "k_ref_pos",
    "k_repel", "k_repel_ring", "R_far", "vertical_offset",
    "horizontal_offset", "near_reached_radius", "far_reached_radius",
)


def random_seeds(n, exclude=()):
    """Choose fresh 32-bit seeds, skipping any already listed in exclude."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    used, values = set(exclude), []
    while len(values) < n:
        seed = secrets.randbits(32)
        if seed not in used:
            used.add(seed)
            values.append(seed)
    return values


def validate_parameters(controller_class, parameters=None):
    """Check trial settings and combine them with the controller defaults."""
    instance = controller_class()
    values = {name: float(getattr(instance, name)) for name in PARAMETER_NAMES}
    overrides = {} if parameters is None else dict(parameters)
    unknown = set(overrides) - set(values)
    if unknown:
        raise ValueError(f"Unknown parameters: {sorted(unknown)}")
    for name, value in overrides.items():
        if isinstance(value, (bool, np.bool_)) or not np.isscalar(value):
            raise ValueError(f"{name} must be a finite number")
        values[name] = float(value)
    if not all(np.isfinite(value) for value in values.values()):
        raise ValueError("All parameters must be finite")
    for name in ("v_max", "a_ref_max", "k_ref_pos", "horizontal_offset",
                 "near_reached_radius", "far_reached_radius"):
        if values[name] <= 0:
            raise ValueError(f"{name} must be positive")
    if min(values["k_repel"], values["k_repel_ring"]) < 0:
        raise ValueError("Repulsion gains must be nonnegative")
    if not 0 <= values["speed_near"] < values["speed_far"]:
        raise ValueError("Require 0 <= speed_near < speed_far")
    if values["R_far"] <= instance.r_drone:
        raise ValueError("R_far must exceed r_drone")
    return values


@contextmanager
def simulator_directory():
    """Temporarily use the simulator folder so its relative asset paths work."""
    previous = Path.cwd()
    try:
        os.chdir(SIMULATOR_DIR)
        yield
    finally:
        os.chdir(previous)


def trial_controller(controller_class, parameters, keep_data):
    """Make a trial-specific controller that also logs the estimate used for feedback."""
    values = validate_parameters(controller_class, parameters)
    original = controller_class()
    # Keep the trial's model and gains fixed.
    matrices = {name: np.asarray(getattr(original, name)).copy()
                for name in ("A", "B", "C", "K", "L")}

    # Wrap the controller to apply trial settings and log the estimate.
    class LoggedController(controller_class):
        def __init__(self):
            super().__init__()
            for name, value in values.items():
                setattr(self, name, value)
            for name, value in matrices.items():
                setattr(self, name, value.copy())
            self.variables_to_log = ["diag_xhat_before"] if keep_data else []

        def run(self, *args):
            # Log the pre-update estimate to match the simulator's current truth.
            if keep_data:
                self.diag_xhat_before = self.xhat.copy()
            return super().run(*args)

    return LoggedController


def terminal_reason(outcome, error):
    """Use the simulator outcome or error text to label how a flight ended."""
    if outcome == "finished":
        return "success"
    if outcome == "time_limit":
        return "time_limit"
    text = str(error or "").lower()
    if "out of bounds" in text:
        return "out_of_bounds"
    if "inactive" in text:
        return "inactive"
    if "timeout" in text or "maximum run time" in text:
        return "timing"
    return "controller_error" if text else "unspecified_failure"


def run_trial(controller_class, seed, *, max_time=85.0, parameters=None,
              keep_data=True, live=False):
    """Run one seeded course and return its outcome, geometry, and requested traces."""
    if isinstance(seed, (bool, np.bool_)) or not isinstance(seed, (int, np.integer)) or not 0 <= int(seed) < 2**32:
        raise ValueError("seed must be an unsigned 32-bit integer")
    if not np.isfinite(max_time) or not 0 < max_time <= 180:
        raise ValueError("max_time must be in (0, 180] seconds")
    configured = trial_controller(controller_class, parameters, keep_data)
    # Keep startup messages for initialization errors.
    sim, messages = None, io.StringIO()
    started = time.perf_counter()
    with simulator_directory():
        try:
            with redirect_stdout(messages):
                sim = ae353_drone.Simulator(seed=int(seed), display_pybullet=live)
                sim.disable_views()
                sim.add_drone(configured, "candidate", image=None)
            drone = sim.get_drone_by_name("candidate")
            if drone is None:
                raise RuntimeError(f"Controller initialization failed:\n{messages.getvalue()}")
            with redirect_stdout(messages):
                sim.reset()
            if not drone["running"]:
                raise RuntimeError(f"Controller reset failed:\n{drone.get('error')}")

            # Keep ring geometry for trajectory plots.
            rings = [{name: np.array(ring[name]).copy() if name in ("p", "R") else ring[name]
                      for name in ("p", "R", "radius", "width")} for ring in sim.rings]
            # Pace live viewing by wall time; stop trials using simulated time.
            sim.start_time = time.time() - sim.t
            while sim.time_step * sim.dt < max_time and drone["running"]:
                sim.step(print_debug=False)

            failed, finished, finish_time = sim.get_result("candidate")
            outcome = "finished" if finished else "failed" if failed else "time_limit"
            error = drone.get("error")
            return dict(
                seed=int(seed), outcome=outcome, finish_time=finish_time,
                terminal_reason=terminal_reason(outcome, error), error=error,
                ring=int(drone["cur_ring"]), rings=rings,
                callback_limit_s=float(sim.max_controller_run_time),
                rotor_mix=sim.M.copy(),  # Applied wrench -> squared rotor speeds.
                rotor_speed_limits_rad_s=[sim.min_spin_rate, sim.max_spin_rate],
                controller_timeout_violations=int(drone["num_run_time_violations"]),
                simulation_time_s=sim.time_step * sim.dt,
                wall_seconds=time.perf_counter() - started,
                data=sim.get_data("candidate") if keep_data else {},
            )
        # Disconnect even if the trial raises an error.
        finally:
            if sim is not None:
                with redirect_stdout(messages):
                    sim.disconnect()


def simulate_trials(controller_class, seeds, *, max_time=85.0, parameters=None,
                    keep_data=True, progress=True):
    """Run the same controller settings on each seed and collect the results."""
    results = []
    for i, seed in enumerate(seeds, start=1):
        result = run_trial(controller_class, seed, max_time=max_time,
                           parameters=parameters, keep_data=keep_data)
        results.append(result)
        if progress and (i == 1 or i % 10 == 0 or i == len(seeds)):
            completed = sum(trial["outcome"] == "finished" for trial in results)
            print(f"Evaluated {i}/{len(seeds)} courses; {completed} completed.")
    return results


# %% Frozen code cell 12
seeds = random_seeds(N_TRIALS)
print(f"Prepared {len(seeds)} distinct random courses.")


# %% Frozen code cell 13
# Keep the tested parameter values with this evaluation.
evaluation_parameters = validate_parameters(Controller)
results = simulate_trials(Controller, seeds, max_time=MAX_TIME_S,
                          parameters=evaluation_parameters)


# %% Frozen code cell 14
# Shared plot data and formatting.
plt.rcParams.update({"font.size": 14, "axes.titlesize": "medium"})
PLOT_DIR.mkdir(parents=True, exist_ok=True)
if not results:
    raise ValueError("Run the evaluation before preparing plots.")

finished = np.array([trial["outcome"] == "finished" for trial in results])
trial_number = np.arange(1, len(results) + 1)
finish_times = np.array([trial["finish_time"] for trial in results if trial["outcome"] == "finished"])
mean_time = finish_times.mean() if finish_times.size else np.nan
violations = np.array([trial["controller_timeout_violations"] for trial in results])
labels, group_masks = ["Successful", "Failed"], [finished, ~finished]

STATE_KEYS = ("p_x", "p_y", "p_z", "yaw", "pitch", "roll",
              "v_x", "v_y", "v_z", "w_x", "w_y", "w_z")
# Per-component scales: position [m], angle [rad], velocity [m/s], angular rate [rad/s].
# Comparison weights only, not acceptance limits.
ERROR_SCALES = np.repeat([0.1, 0.1, 0.5, 0.5], 3)
positions, estimates, state_errors, callback_times = [], [], [], []
rotor_min, rotor_max = [], []
omitted_errors = omitted_times = 0

for trial in results:
    data = trial["data"]
    truth = np.column_stack([data[key] for key in STATE_KEYS])
    estimate = np.asarray(data["diag_xhat_before"]).reshape(-1, 12)
    assert truth.shape == estimate.shape, "Estimate and truth must be aligned."
    positions.append(truth[:, :3])
    estimates.append(estimate[:, :3])
    error = estimate - truth
    # Wrap Euler-angle errors to [-pi, pi).
    error[:, 3:6] = (error[:, 3:6] + np.pi) % (2 * np.pi) - np.pi
    # Drop samples with any nonfinite state error or time.
    valid = np.isfinite(error).all(axis=1) & np.isfinite(data["t"])
    # One normalized whole-state error per time sample.
    state_errors.append(np.sqrt(np.mean((error[valid] / ERROR_SCALES)**2, axis=1)))
    omitted_errors += np.count_nonzero(~valid)

    milliseconds = 1000 * np.asarray(data["run_time"])
    valid = np.isfinite(milliseconds) & (milliseconds >= 0)
    # Keep reported zeros from limited clock resolution.
    callback_times.append(milliseconds[valid])
    omitted_times += np.count_nonzero(~valid)

    # Reconstruct rotor speeds from applied torque/thrust after motor limiting.
    applied = np.column_stack([data[key] for key in ("tau_x", "tau_y", "tau_z", "f_z")])
    squared_speeds = applied @ np.asarray(trial["rotor_mix"]).T
    if np.any(squared_speeds < 0):
        raise ValueError("Applied wrench gives a negative squared rotor speed.")
    speeds = np.sqrt(squared_speeds)
    # Bounds cover all rotors and samples; empty traces remain unverified.
    rotor_min.append(speeds.min() if speeds.size else np.nan)
    rotor_max.append(speeds.max() if speeds.size else np.nan)

rotor_min, rotor_max = np.array(rotor_min), np.array(rotor_max)
# Allow a small tolerance for floating-point roundoff.
rotor_ok = np.isfinite(rotor_min) & np.isfinite(rotor_max) & (rotor_min >= 100 - 1e-6) & (rotor_max <= 900 + 1e-6)
# Pool samples by outcome; longer flights contribute more samples.
error_groups = []
for mask in group_masks:
    selected = [error for error, keep in zip(state_errors, mask) if keep]
    error_groups.append(np.concatenate(selected) if selected else np.array([]))
print(f"Timing requirement: {np.count_nonzero(violations <= 9)}/{len(results)} trials meet the <=9-call rule")
print(f"Applied rotor limits verified: {rotor_ok.sum()}/{len(results)} trials")
print(f"Nonfinite error samples omitted: {omitted_errors}; invalid callback times omitted: {omitted_times}")
print("Unsuccessful reasons:", dict(Counter(t["terminal_reason"] for t in results if t["outcome"] != "finished")))
print("PNG folder:", PLOT_DIR)


# %% Frozen code cell 15
print(f"Completed: {finished.sum()}/{len(results)} ({finished.mean():.1%})")
print(f"Mean successful completion time: {mean_time:.2f} s")


# %% Frozen code cell 16
fig, ax = plt.subplots(figsize=(8, 5))
if finish_times.size:
    ax.hist(finish_times, bins="auto", label=f"Completed trials (n={finish_times.size})")
    ax.axvline(finish_times.mean(), color="C1", label=f"Mean: {finish_times.mean():.2f} s")
else:
    ax.text(0.5, 0.5, "No completed trials; mean is undefined", ha="center", transform=ax.transAxes)
ax.axvline(80, color="C3", linestyle="--", label="Mean requirement: <80 s")
ax.set(xlabel="Completion time [s]", ylabel="Completed trials [count]",
       title="Completion times of successful flights")
ax.legend()
fig.savefig(PLOT_DIR / "completion_time_histogram.png", dpi=600, bbox_inches="tight")
plt.show()


# %% Frozen code cell 17
fig, ax = plt.subplots(figsize=(8, 5))
for mask, label in zip(group_masks, labels):
    ax.scatter(trial_number[mask], violations[mask], label=f"{label} (n={mask.sum()})")
# The tenth call over 10 ms ends the trial.
ax.axhline(10, color="C3", linestyle="--", label="Program termination")
ax.set(xlabel="Trial number", ylabel="Calls exceeding 10 ms [count]",
       title="Controller execution-time violations per trial")
ax.legend()
fig.savefig(PLOT_DIR / "execution_time_violations_per_trial.png", dpi=600, bbox_inches="tight")
plt.show()


# %% Frozen code cell 18
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(trial_number, rotor_min, ".", label="Minimum over all rotors and steps")
ax.plot(trial_number, rotor_max, ".", label="Maximum over all rotors and steps")
ax.axhline(100, color="C3", linestyle="--", label="Lower limit: 100 rad/s")
ax.axhline(900, color="C3", linestyle=":", label="Upper limit: 900 rad/s")
ax.set(xlabel="Trial number", ylabel="Applied rotor speed [rad/s]",
       title="Applied rotor-speed bounds across trials")
ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
fig.savefig(PLOT_DIR / "applied_rotor_speed_bounds.png", dpi=600, bbox_inches="tight")
plt.show()


# %% Frozen code cell 19
from matplotlib.ticker import MaxNLocator

# Select a failed trial with retained positions.
TRIAL_INDEX = next((i for i, ok in enumerate(finished) if not ok and positions[i].size), None)
if TRIAL_INDEX is not None:
    trial = results[TRIAL_INDEX]
    actual, estimate = positions[TRIAL_INDEX], estimates[TRIAL_INDEX]
    angle = np.linspace(0, 2 * np.pi, 100)
    ring_curves = []
    for ring in trial["rings"]:
        # Rotate and translate the local hoop circle into world coordinates.
        local = ring["radius"] * np.array([np.zeros(100), np.cos(angle), np.sin(angle)])
        ring_curves.append((np.asarray(ring["p"])[:, None] + np.asarray(ring["R"]) @ local).T)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(projection="3d")
    ax.plot(*actual.T, label="Actual position")
    ax.plot(*estimate.T, "--", label="Estimated position")
    ax.scatter(*actual[0], marker="o", label="Start")
    ax.scatter(*actual[-1], marker="x", label="Last logged position")
    for j, curve in enumerate(ring_curves):
        ax.plot(*curve.T, color="0.7", label="Ring hoops" if j == 0 else None)
    points = np.vstack([actual, estimate, *ring_curves])
    points = points[np.isfinite(points).all(axis=1)]
    ax.set_box_aspect(np.maximum(np.ptp(points, axis=0), 1))
    ax.set(xlabel="World x [m]", ylabel="World y [m]", zlabel="World z [m]",
           title=f"Trial {TRIAL_INDEX + 1}, seed {trial['seed']}: {trial['terminal_reason']}")
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.labelpad = 18
        axis.set_major_locator(MaxNLocator(4))
    ax.legend(loc="upper left", bbox_to_anchor=(1.25, 1))
    fig.savefig(PLOT_DIR / f"failed_trajectory_3d_s{trial['seed']}.png", dpi=600, bbox_inches="tight")
    plt.show()
else:
    print("No unsuccessful flight with retained positions.")


# %% Frozen code cell 20
# Overhead view of the same trial selected above.
if TRIAL_INDEX is not None:
    fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    ax.plot(actual[:, 0], actual[:, 1], label="Actual position")
    ax.plot(estimate[:, 0], estimate[:, 1], "--", label="Estimated position")
    ax.scatter(*actual[0, :2], marker="o", label="Start")
    ax.scatter(*actual[-1, :2], marker="x", label="Last logged position")
    for j, curve in enumerate(ring_curves):
        ax.plot(curve[:, 0], curve[:, 1], color="0.7", label="Ring hoops" if j == 0 else None)
    ax.set(xlabel="World x [m]", ylabel="World y [m]",
           title=f"Overhead: trial {TRIAL_INDEX + 1}, seed {trial['seed']}")
    ax.set_aspect("equal", adjustable="box")
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    fig.savefig(PLOT_DIR / f"failed_trajectory_overhead_s{trial['seed']}.png", dpi=600, bbox_inches="tight")
    plt.show()
else:
    print("No unsuccessful flight with retained positions.")


# %% Frozen code cell 21
all_errors = np.concatenate(state_errors)
if all_errors.size:
    # Display exact zeros in the first log bin; retain them unchanged in the statistics.
    positive = all_errors[all_errors > 0]
    floor = 0.98 * positive.min() if positive.size else 1e-12
    # Use common logarithmic bins for both outcomes.
    bins = np.geomspace(floor, max(1.02 * all_errors.max(), 10 * floor), 61)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True, layout="constrained")
    for ax, errors, mask, label, color in zip(axes, error_groups, group_masks, labels, ("C0", "C1")):
        if errors.size:
            rmse = np.sqrt(np.mean(errors**2))
            p95 = np.percentile(errors, 95)
            # Weight samples so bar heights show percentages.
            ax.hist(np.maximum(errors, floor), bins=bins, weights=np.full(errors.size, 100 / errors.size), color=color)
            ax.axvline(rmse, color="black", label=f"RMSE = {rmse:.3g}")
            ax.axvline(p95, color="C3", linestyle="--", label=f"p95 = {p95:.3g}")
            ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncols=2, frameon=False)
        else:
            ax.text(0.5, 0.5, "No retained errors", ha="center", transform=ax.transAxes)
        ax.set(xscale="log", xlim=(bins[0], bins[-1]), xlabel="Normalized whole-state error (log scale)")
        ax.set_title(f"{label} ({mask.sum()} trials)", pad=42)
    axes[0].set_ylabel("Samples per bin [%]")
    fig.savefig(PLOT_DIR / "whole_state_error_histograms.png", dpi=600, bbox_inches="tight")
    plt.show()
else:
    print("No finite aligned state-estimation errors to plot.")


# %% Frozen code cell 22
times = np.concatenate(callback_times)
fig, ax = plt.subplots(figsize=(8, 5))
if times.size:
    bins = np.linspace(0, max(times.max(), 10) * 1.05, 51)
    ax.hist(times, bins=bins, label=f"All retained calls (n={times.size:,})")
    # Show rare slow calls with a log count axis.
    ax.set_yscale("log")
else:
    ax.text(0.5, 0.5, "No logged durations", ha="center", transform=ax.transAxes)
ax.axvline(10, color="C3", linestyle="--", label="Execution-time cutoff: 10 ms")
ax.set(xlabel="Execution time [ms]", ylabel="Controller calls [count, log scale]",
       title="Controller callback execution times, including reported zeros")
ax.legend()
fig.savefig(PLOT_DIR / "execution_time_histogram.png", dpi=600, bbox_inches="tight")
plt.show()
print(f"Reported zero-duration calls included: {np.count_nonzero(times == 0):,}/{times.size:,}")


# %% Frozen code cell 23
above_cutoff = []
for outcome in (True, False):
    calls = [t for t, ok in zip(callback_times, finished) if ok == outcome]
    times = np.concatenate(calls) if calls else np.array([])
    above_cutoff.append(times[times > 10])
fig, ax = plt.subplots(figsize=(8, 5))
# The scatter shows every call, including boxplot outliers.
ax.boxplot(above_cutoff, tick_labels=labels, showfliers=False)
for position, group, label in zip((1, 2), above_cutoff, labels):
    ax.scatter(np.full(group.size, position), group, label=f"{label} (n={group.size} calls)")
    if not group.size:
        ax.text(position, 0.5, "No logged exceedances", ha="center", transform=ax.get_xaxis_transform())
ax.axhline(10, color="C3", linestyle="--", label="Execution-time cutoff: 10 ms")
ax.set(xlabel="Trial outcome", ylabel="Above-cutoff execution time [ms]",
       title="Logged calls above 10 ms by outcome")
ax.legend()
fig.savefig(PLOT_DIR / "above_cutoff_execution_times.png", dpi=600, bbox_inches="tight")
plt.show()


# %% Frozen code cell 24
print("Evaluated input parameters:")
for name, value in evaluation_parameters.items():
    print(f"{name}: {value}")


# %% Frozen code cell 25
if RUN_LIVE_VIEW:
    run_trial(Controller, seeds[0], max_time=MAX_TIME_S, live=True)


# %% Frozen code cell 26
def search_controller(
    controller_class, input_parameters, parameter_ranges, base_parameters=None,
    *, n_candidates=2000, n_trials=30, min_completion=0.95, max_time=70.0,
    sampling_seed=None, course_seeds=None, reject_impossible=True,
):
    """Find fast settings that meet the required completion fraction.

    Test the current settings first, then Latin hypercube samples. Every candidate
    sees the same courses. Return scores and rankings in memory.
    """
    # Validate the search settings before running simulations.
    for name, value in (("n_candidates", n_candidates), ("n_trials", n_trials)):
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < 1:
            raise ValueError(f"{name} must be a positive integer.")
    n_candidates, n_trials = int(n_candidates), int(n_trials)
    if not np.isfinite(min_completion) or not 0 < min_completion <= 1:
        raise ValueError("min_completion must be in (0, 1].")
    if not np.isfinite(max_time) or not 0 < max_time <= 180:
        raise ValueError("max_time must be in (0, 180] seconds.")
    if not isinstance(reject_impossible, (bool, np.bool_)):
        raise ValueError("reject_impossible must be a boolean.")

    base = validate_parameters(controller_class, base_parameters)
    names = list(input_parameters)
    if not names or any(not isinstance(name, str) for name in names) or len(set(names)) != len(names):
        raise ValueError("Specify distinct parameter names.")
    bounds = []
    for name in names:
        if name not in base or name not in parameter_ranges:
            raise ValueError(f"Missing supported parameter or range: {name}")
        lo, hi, scale = parameter_ranges[name]
        lo, hi = float(lo), float(hi)
        if (not np.isfinite([lo, hi]).all() or lo >= hi
                or scale not in ("linear", "log") or (scale == "log" and lo <= 0)):
            raise ValueError(f"Invalid bounds or sampling scale for {name}.")
        bounds.append((lo, hi, scale))

    def uint32(value):
        return (not isinstance(value, (bool, np.bool_))
                and isinstance(value, (int, np.integer)) and 0 <= value < 2**32)

    sampling_seed = secrets.randbits(32) if sampling_seed is None else sampling_seed
    if not uint32(sampling_seed):
        raise ValueError("sampling_seed must be an unsigned 32-bit integer or None.")
    sampling_seed = int(sampling_seed)
    # Use the same courses for fair candidate comparisons.
    cohort = random_seeds(n_trials) if course_seeds is None else list(course_seeds)
    if len(cohort) != n_trials or not all(uint32(seed) for seed in cohort) or len(set(cohort)) != n_trials:
        raise ValueError("course_seeds must contain n_trials distinct unsigned 32-bit integers.")
    cohort = list(map(int, cohort))

    # Test current settings first, then Latin hypercube candidates.
    candidates = [base.copy()]
    if n_candidates > 1:
        samples = qmc.LatinHypercube(d=len(names), seed=sampling_seed).random(n_candidates - 1)
        for sample in samples:
            parameters = base.copy()
            # Map samples linearly or by equal ratios for log-scaled parameters.
            for name, u, (lo, hi, scale) in zip(names, sample, bounds):
                parameters[name] = float(
                    np.exp(np.log(lo) + u * np.log(hi / lo))
                    if scale == "log" else lo + u * (hi - lo)
                )
            candidates.append(parameters)

    candidates = [validate_parameters(controller_class, p) for p in candidates]
    # Round up required successes (95% of 30 needs 29), allowing for roundoff.
    required = math.ceil(float(min_completion) * n_trials - 1e-12)
    settings = dict(
        n_candidates=n_candidates, n_trials=n_trials,
        min_completion=float(min_completion), required_successes=required,
        max_time=float(max_time), reject_impossible=bool(reject_impossible),
    )
    all_results = []
    best = None
    status = "complete"

    def record_candidate(index, parameters, flights, candidate_status):
        """Store this candidate and update the fastest qualifying result."""
        nonlocal best
        completed = len(flights) == n_trials
        successes = sum(flight["outcome"] == "finished" for flight in flights)
        times = [flight["finish_time"] for flight in flights if flight["outcome"] == "finished"]
        qualifies = completed and successes >= required and bool(times)
        # Partial batches cannot qualify; unrun flights remain unknown.
        row = dict(
            candidate=index, status=candidate_status, parameters=parameters.copy(),
            trials_evaluated=len(flights), trials_planned=n_trials,
            successes=successes, failures_observed=len(flights) - successes,
            skipped_trials=n_trials - len(flights), complete=completed,
            completion_fraction=successes / n_trials if completed else None,
            completion_upper_bound=(successes + n_trials - len(flights)) / n_trials,
            mean_time_s=float(np.mean(times)) if completed and times else None,
            qualifies=qualifies, wall_seconds=sum(f["wall_seconds"] for f in flights),
            trials=flights.copy(),
        )
        all_results.append(row)
        if qualifies and (best is None or row["mean_time_s"] < best["mean_time_s"]):
            best = row
        if completed:
            speed = "no finishes" if not times else f'{row["mean_time_s"]:.2f} s'
            label = "qualifies" if qualifies else "below cutoff"
            print(f"{index + 1}/{n_candidates}: {successes}/{n_trials}, {speed}, {label}")
        else:
            print(f"{index + 1}/{n_candidates}: {candidate_status} after {len(flights)}/{n_trials} flights; "
                  f"{len(flights) - successes} failures observed")

    for index, parameters in enumerate(candidates):
        flights = []
        candidate_status = "complete"
        try:
            for seed in cohort:
                # Keep scores only during search.
                result = run_trial(
                    controller_class, seed, max_time=max_time,
                    parameters=parameters, keep_data=False,
                )
                outcome, finish_time = result["outcome"], result["finish_time"]
                if outcome not in ("finished", "failed", "time_limit"):
                    raise RuntimeError(f"Unexpected simulation outcome: {outcome}")
                if outcome == "finished" and (finish_time is None or not np.isfinite(finish_time)):
                    raise RuntimeError("A finished flight must have a finite finish time.")
                flights.append(dict(
                    seed=int(seed), outcome=outcome, finish_time=finish_time,
                    terminal_reason=result.get("terminal_reason"),
                    controller_timeout_violations=result.get("controller_timeout_violations", 0),
                    wall_seconds=float(result["wall_seconds"]),
                ))
                successes = sum(flight["outcome"] == "finished" for flight in flights)
                remaining = n_trials - len(flights)
                # Stop if even all remaining successes cannot meet the cutoff.
                if reject_impossible and remaining and successes + remaining < required:
                    candidate_status = "pruned"
                    break
        # Keep completed work if the search is interrupted.
        except KeyboardInterrupt:
            record_candidate(index, parameters, flights, "interrupted")
            status = "interrupted"
            print("Interrupted; recorded candidates remain available. Unrun flights are unknown.")
            break
        except Exception:
            # Record partial results, then propagate the error.
            record_candidate(index, parameters, flights, "error")
            raise
        record_candidate(index, parameters, flights, candidate_status)

    ranking = sorted(
        (row for row in all_results if row["qualifies"]),
        key=lambda row: row["mean_time_s"],
    )
    return dict(
        status=status, best=best, all_results=all_results, ranking=ranking,
        course_seeds=cohort, sampling_seed=sampling_seed, settings=settings,
    )


# %% Frozen code cell 27
# Ranges: (lower bound, upper bound, 'linear' or 'log').
PARAMETER_RANGES = {'v_max': (1.05, 1.3, 'linear'),
 'a_ref_max': (4.0, 8.0, 'log'),
 'speed_near': (1.05, 1.3, 'linear'),
 'speed_far': (3.5, 4.25, 'linear'),
 'k_ref_pos': (1.9, 2.8, 'log'),
 'k_repel': (0.47, 0.67, 'log'),
 'k_repel_ring': (0.12, 0.19, 'log'),
 'R_far': (2.52, 3.5, 'linear'),
 'vertical_offset': (0.0, 0.09, 'linear'),
 'horizontal_offset': (0.9, 1.15, 'linear'),
 'near_reached_radius': (1.0, 1.3, 'linear'),
 'far_reached_radius': (0.5, 0.9, 'linear')}
INPUT_PARAMETERS = list(PARAMETER_RANGES)
BASE_PARAMETERS = validate_parameters(Controller)
SEARCH_SETTINGS = dict(
    n_candidates=2000,
    n_trials=30,
    min_completion=0.95,
    max_time=70.0,
    sampling_seed=None,
    reject_impossible=True,
)

search = None
if RUN_SEARCH:
    search = search_controller(
        Controller, INPUT_PARAMETERS, PARAMETER_RANGES, BASE_PARAMETERS,
        # Keep search and evaluation courses separate.
        course_seeds=random_seeds(SEARCH_SETTINGS["n_trials"], exclude=seeds),
        **SEARCH_SETTINGS,
    )


# %% Frozen code cell 28
winner = search["best"] if search is not None else None
if winner is None:
    print("No qualifying result from this session. Enable RUN_SEARCH to run a search.")
else:
    settings = search["settings"]
    print(f"Completion cutoff: {settings['min_completion']:.0%}; flight horizon: {settings['max_time']:g} s")
    print(f"Search winner: {winner['successes']}/{winner['trials_planned']} complete; mean {winner['mean_time_s']:.2f} s")
    for name, value in winner["parameters"].items():
        print(f"{name}: {value}")

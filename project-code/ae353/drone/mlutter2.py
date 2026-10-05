import numpy as np

class Controller:
    def __init__(self):
        # System matrices and gains (assumed defined globally)
        self.A = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0, 0.0, 1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 9.81, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, -9.81, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0, -0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
        self.B = np.array([[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 2.0], [434.78261, 0.0, 0.0, 0.0], [0.0, 434.78261, 0.0, 0.0], [0.0, 0.0, 250.0, 0.0]])
        self.C = np.array([[1.0, 0.0, 0.0, -0.0, -0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.175, -0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0, -0.175, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, -0.175, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0, 0.175, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
        self.K = np.array([[0.0, -0.00913, 0.0, -0.0, 0.0, 0.06, 0.0, -0.01095, 0.0, 0.01851, 0.0, -0.0], [0.00913, -0.0, 0.0, 0.0, 0.06, 0.0, 0.01095, -0.0, 0.0, 0.0, 0.01851, -0.0], [-0.0, 0.0, -0.0, 0.00289, 0.0, -0.0, -0.0, 0.0, -0.0, -0.0, -0.0, 0.00947], [0.0, -0.0, 0.40825, -0.0, 0.0, 0.0, 0.0, -0.0, 0.63895, 0.0, 0.0, -0.0]])
        self.L = np.array([[2.92711, -0.0, -0.21977, 2.92711, -0.0, 0.21977], [-0.0, 2.97538, 0.0, -0.0, 2.97538, 0.0], [0.0, 0.0, 1.09868, 0.0, 0.0, 1.09868], [0.0, 2.13087, 0.0, 0.0, -2.13087, 0.0], [1.25582, -0.0, -0.3043, 1.25582, -0.0, 0.3043], [0.0, -1.30543, -0.0, 0.0, -1.30543, -0.0], [8.11629, -0.0, -1.19153, 8.11629, -0.0, 1.19153], [-0.0, 8.35286, 0.0, -0.0, 8.35286, 0.0], [0.0, 0.0, 0.70711, 0.0, 0.0, 0.70711], [0.0, -0.70711, -0.0, 0.0, -0.70711, -0.0], [0.67683, -0.0, -0.20469, 0.67683, -0.0, 0.20469], [0.0, 0.70711, -0.0, 0.0, -0.70711, 0.0]])
        
        # Equilibrium (hover, level)
        self.m_e = np.zeros(12)
        self.n_e = np.array([0.0, 0.0, 0.0, 4.905])
        self.o_e = np.array([0.175, 0.0, 0.0, -0.175, 0.0, 0.0])
        self.f_ze = self.n_e[3]

        # Timing
        self.dt = 0.04  # 25 Hz

        # Obstacle repulsion (dogs / other drones)
        self.k_repel      = 0.3   # gain for real obstacles
        self.k_repel_ring = 0.075  # smaller gain for ring obstacle (tune this)
        self.r_drone = 0.7
        self.R_far   = 7.0

        # Reference motion (low-pass waypoint tracking, base values)
        self.k_ref_pos = 0.95   # p_ref' = k_ref_pos (p_target - p_ref)
        self.v_max     = 1.0    # |v_ref| <= v_max

        # Ring targeting (near/far waypoints)
        self.vertical_offset     = 0.2
        self.horizontal_offset   = 0.75
        self.near_reached_radius = 0.65
        self.far_reached_radius  = 0.6

        # Ring geometry (for closest-point calculation)
        self.ring_radius = 1.0  # approximate hoop radius (m)

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

    # ---------- Ring bookkeeping and closest-point helper ----------

    def _register_ring(self, pos_ring, dir_ring):
        """
        Store each ring (center + unit normal) once.
        """
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
        """
        Return the closest point on the hoop of the closest ring to p_est.
        If no rings are known, return None.
        """
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

    # ---------- Existing helpers ----------

    def _lock_new_ring_visit(self, p_est, pos_ring, dir_ring):
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
        """
        Generic repulsion for a list of obstacle positions using a specified gain.
        """
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
        """
        Choose (v_max_local, k_ref_local) based on distance to ring and obstacles.
        Uses combined obstacle list (including ring point) for conservatism.
        """
        d_ring = np.linalg.norm(p_est - ring_center)

        d_obst = np.inf
        if pos_all_for_speed is not None and len(pos_all_for_speed) > 0:
            for obst_pos in np.atleast_2d(pos_all_for_speed):
                d = np.linalg.norm(obst_pos - p_est)
                if d < d_obst:
                    d_obst = d

        v = self.v_max
        k = self.k_ref_pos
        
        if d_obst > 4.0:  # far from everything
            v *= 2.5
            k *= 2.0
        elif d_obst > 2.5:  # medium distance
            v *= 2.0
            k *= 1.5
        elif d_ring < 1.0 or d_obst < 1.5:  # very close to ring or obstacle
            v *= 0.7
            k *= 0.7
       
        return v, k

    # ---------- Main loop ----------

    def run(self, pos_markers, pos_ring, dir_ring, is_last_ring, pos_others):
        # --- 1. Estimated position ---
        p_est = self.xhat[0:3]
        if self.p_ref is None:
            self.p_ref = p_est.copy()

        # --- 2. Track rings and ring visit logic (near → far) ---
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

        if self.ring_phase == 'near':
            p_target_nominal = p_near
            if np.linalg.norm(p_est - p_near) <= self.near_reached_radius:
                self.ring_phase = 'far'
        else:
            p_target_nominal = p_far
            if np.linalg.norm(p_est - p_far) <= self.far_reached_radius:
                self.active_ring_completed = True

        # --- 3. Build obstacle sets ---
        # Ring obstacle: only active in 'near' phase
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

        # --- 4. Obstacle repulsion (separate gains) ---
        h_repel_other = self._obstacle_repulsion(p_est, pos_others, self.k_repel)
        if ring_obst is not None:
            h_repel_ring = self._obstacle_repulsion(p_est,
                                                    np.array(ring_obst, ndmin=2),
                                                    self.k_repel_ring)
        else:
            h_repel_ring = np.zeros(3)

        h_repel = h_repel_other + h_repel_ring

        # --- 5. Reference target and dynamics (with local speed limits) ---
        p_target = p_target_nominal + h_repel
        v_max_local, k_ref_local = self._local_speed_limits(p_est, center, pos_all_for_speed)

        e_ref = p_target - self.p_ref
        v_ref = k_ref_local * e_ref

        speed = np.linalg.norm(v_ref)
        if speed > v_max_local:
            v_ref *= v_max_local / speed

        self.p_ref = self.p_ref + self.dt * v_ref
        p_des, v_des = self.p_ref, v_ref

        # --- 6. Desired state ---
        xdes = np.zeros(12)
        xdes[0:3] = p_des
        xdes[6:9] = v_des
        self.xdes = xdes

        # --- 7. LQR control ---
        u = -self.K @ (self.xhat - xdes)
        u[2] = np.clip(u[2], -0.16, 0.16)
        u[3] = np.clip(u[3], -22.68, 22.68)

        # --- 8. Observer update ---
        y = self.C @ self.xhat
        self.xhat = self.xhat + self.dt * (
            self.A @ self.xhat + self.B @ u + self.L @ (pos_markers - y)
        )

        # --- 9. Map to simulator commands ---
        tau_x, tau_y, tau_z = u[0], u[1], u[2]
        f_z = u[3] + self.f_ze

        return tau_x, tau_y, tau_z, f_z

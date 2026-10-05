# Archived notebook code; see README.md for authorship, dependencies, and saved-run limitations.

# %%
# These modules are part of other existing libraries
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import linalg
from scipy.sparse.linalg import expm_multiply  # most stable for time sweep

# This is professor Bretl's script (it is an interface to the pybullet simulator)
import ae353_catbot

# %%
import sympy as sym
import numpy as np
from IPython.display import display, Markdown
from sympy.physics import mechanics
mechanics.init_vprinting()

# %%
# Time
t = sym.Symbol('t')

# Horizontal position of wheel axle
zeta = mechanics.dynamicsymbols('zeta', real=True)

# Angle of body from vertical (positive means leaning forward)
theta = mechanics.dynamicsymbols('theta', real=True)

# Torque applied by the body on the wheel
tau = sym.symbols('tau', real=True)

# Wheel parameters
#   m_w  mass
#   J_w  moment of inertia
#   r_w  radius
m_w, J_w, r_w = sym.symbols('m_w, J_w, r_w', real=True, positive=True)

# Body parameters
#   m_b  mass
#   J_b  moment of inertia (about center-of-mass)
#   r_b  distance between wheel axle and body center-of-mass
m_b, J_b, r_b = sym.symbols('m_b, J_b, r_b', real=True, positive=True)

# Acceleration of gravity
g = sym.symbols('g', real=True, positive=True)

# %%
# Position of wheel and body
p_w = sym.Matrix([zeta, r_w])
p_b = sym.Matrix([zeta + r_b * sym.sin(theta), r_w + r_b * sym.cos(theta)])

# Linear velocity of wheel and body
v_w = p_w.diff(t)
v_b = p_b.diff(t)

# Angular velocity of wheel (assume rolling without slipping on flat ground) and body
omega_w = zeta.diff(t) / r_w
omega_b = theta.diff(t)

# Kinetic and potential energy
T = (m_w * v_w.dot(v_w) + m_b * v_b.dot(v_b) + J_w * omega_w**2 + J_b * omega_b**2) / 2
V = (m_w * p_w[1] * g) + (m_b * p_b[1] * g)

# Lagrangian
L = sym.Matrix([sym.simplify(T - V)])

# %%
# Generalized coordinates
q = sym.Matrix([zeta, theta])

# Generalized velocities
v = q.diff(t)

# Coefficients in the equations of motion
M = sym.simplify(L.jacobian(v).jacobian(v))
N = sym.simplify(L.jacobian(v).jacobian(q) @ v - L.jacobian(q).T)
F = sym.simplify(sym.Matrix([(zeta / r_w) - theta]).jacobian(q).T)

# Show results
display(Markdown(f'$$ M(q) = {mechanics.mlatex(M)} $$'))
display(Markdown(f'$$ N(q, \\dot{{q}}) = {mechanics.mlatex(N)} $$'))
display(Markdown(f'$$ F(q) = {mechanics.mlatex(F)} $$'))

# %%
##########################################
# Temporary variables that can be ignored

# Dimensions of chassis
dx = 0.5
dy = 0.5
dz = 1.0

# Distance between axle and COM of chassis
h = 0.15

# Half-distance between wheels
a = 0.375

# Mass of chassis
mb = 12.

# MOI of chassis
Jbx = (mb / 12) * (dy**2 + dz**2)
Jby = (mb / 12) * (dx**2 + dz**2)
Jbz = (mb / 12) * (dx**2 + dy**2)

# Radius of each wheel
r = 0.5

# Width of each wheel
hw = 0.2

# Mass of each wheel
mw = 2.

# MOI of each wheel
Jw = (mw / 2) * r**2
Jwt = (mw / 12) * (3 * r**2 + hw**2)

# Total mass
m = mb + 2 * mw

# Total MOI
Jx = Jbx + 2 * Jwt
Jy = Jby
Jz = Jbz + 2 * Jwt

##########################################
# Parameters

# Define them
params = {
    r_w: r,
    m_w: 2 * mw,
    J_w: 2 * Jw,
    r_b: h,
    m_b: mb,
    J_b: Jby,
    g: 9.81,
}

# Show them
s = ''
for key, val in params.items():
    s += fr'{key} &= {mechanics.mlatex(val)} \\ '
s = s[:-3]
display(Markdown(fr'$$ \begin{{align*}}{s}\end{{align*}} $$'))

# %%
eq = sym.Eq(M @ q.diff(t, 2) + N , F * tau)
eq1 = sym.Eq(eq.lhs[0], eq.rhs[0])
eq2 = sym.Eq(eq.lhs[1], eq.rhs[1])

# %%
# alpha_dot
theta_ddot = sym.simplify(sym.solve(eq1, theta.diff(t, 2))[0])
theta_ddot

# %%
# z_dot
zeta_ddot = sym.simplify(sym.solve(eq2, zeta.diff(t, 2))[0])
zeta_ddot

# %%
alpha = mechanics.dynamicsymbols('alpha', real=True)
z = mechanics.dynamicsymbols('z', real=True)

alpha = theta.diff(t)
z = zeta.diff(t)

f = sym.Matrix((0, 0, 0, 0))

f[0] = alpha        # m_dot[0]
f[1] = z            # m_dot[1]
f[2] = theta_ddot   # m_dot[2]
f[3] = zeta_ddot    # m_dot[3]

f

# %%
# Create lambda function
f_jacob = f.jacobian([theta, zeta, alpha, z]) # jacobian for A

f_jacob2 = f.jacobian([tau]) # jacobian for B

display(Markdown(f'$${mechanics.mlatex(f_jacob)} $$'))
display(Markdown(f'$${mechanics.mlatex(f_jacob2)} $$'))


# %%
g = 9.81
mb = 12.0
rb = 0.15
rw = 0.5

A = np.array([
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [g, 0, 0, 0]
])
sym.Matrix(A) # display A

# %%

B = np.array([
    [0],
    [0],
    [1/(mb*rb*rw)],
    [-1/(mb*rb)]
])
sym.Matrix(B) # display B

# %%
def find_K_uniform():
    K = np.zeros((1, 4))
    while True:
        # Generate random values in some range small enough to not consistently reach max. torque
        arr = np.array([random.uniform(0, 30) for _ in range(4)])
        # Assign random values to elements of K
        K[0, 0] = arr[0]
        K[0, 1] = arr[1]
        K[0, 2] = arr[2]
        K[0, 3] = arr[3]
        # Compute eigenvalues
        F = A - B @ K
        vals = linalg.eigvals(F)
        # Test eigenvalues: if all negative, then the system is stable
        if vals.real.max() < 0:
            return K
# Example:
K = find_K_uniform()
print('Feedback Gain Matrix K: ', K)
print('Real components of eigenvalues: ', linalg.eigvals(A - B @ K).real)

# %%
n = 500 # how many test points
# create 1D arrays for each element of K
K1 = np.zeros((n))
K2 = np.zeros((n))
K3 = np.zeros((n))
K4 = np.zeros((n))
# Populate arrays with valid K values
for i in range(n):
    K = find_K_uniform()
    K1[i] = K[0, 0]
    K2[i] = K[0, 1]
    K3[i] = K[0, 2]
    K4[i] = K[0, 3]

# create box plots
fig, ax = plt.subplots(ncols=1, figsize=(6, 5), sharey=True)

bp1 = ax.boxplot([K1, K2, K3, K4], tick_labels=['K$_1$', 'K$_2$', 'K$_3$', 'K$_4$'], patch_artist=True, widths=0.6)
for box in bp1['boxes']:
    box.set_facecolor('#dddddd')
ax.set_xlabel('Dataset')
ax.set_ylabel('Value')
ax.grid(True, axis='y', linestyle=':', linewidth=0.8)

plt.tight_layout()
plt.show()

# %%
class Controller:
    def __init__(self):
        self.K = K
    
    def reset(self):
        pass      
    
    def run(
            self,
            t,
            wheel_position,
            wheel_velocity,
            pitch_angle,
            pitch_rate,
        ):
        
        x = np.array([
            pitch_angle,
            wheel_position,
            pitch_rate,
            wheel_velocity,
        ])
        u = (self.K @ x)[0]  # state feedback controller

        wheel_torque = np.clip(u, -5, 5)  # torque limits of the simulator
        return wheel_torque

# %%
# do not run without simulator fix
import IPython # Used just for aesthetic purposes
def simulateK():
    simulator = ae353_catbot.Simulator(
        display=True,
        sound=False, # if enabled, may cause a crash
        launch_cat=True,
    )
    catSaved = False
    turns = 2 # number of passes to be considered passable
    turn = 0
    while turn != turns:
        if turn == 0:               # first pass through or just failed so must generate a new K
            K = find_K_uniform()
        controller = Controller()   # create a controller instance for this K
        simulator.reset()           # reset the simulator for some initial conditions
        controller.reset()
        data = simulator.run(
            controller,             # an instance of the Controller class
            maximum_time=20.0,      # how long you want to run the simulation in seconds
        )
        catSaved = simulator.did_save_cat()
        if catSaved:
            turn += 1
        else:
            IPython.display.clear_output()
            turn = 0
        print('Progress: |' + turn * '-' + (turns - turn) * ' ' + '|', K)
    return K
# K = simulateK()
# print('Feedback Gain Matrix K: ', K)
# print('Real components of eigenvalues: ', linalg.eigvals(A - B @ K).real)

# %%
K = np.array([[28.33116424,  1.62511889, 9.04966716,  4.34551019]])
vals = linalg.eigvals(A - B @ K)

# %%
# plot the stability of the system
F = np.asarray(A - B @ K, dtype=np.float64)
x0 = np.array([0.1, 0.1, 0.0, 0.0], dtype=np.float64)

# Time grid
T = 15.0  
N = 1000
t_eval = np.linspace(0.0, T, N)

X = expm_multiply(F, x0, start=0.0, stop=T, num=N, endpoint=True)  # shape (N, 4)

# Plot
labels = [r'$\theta$ (rad)', r'$\zeta$ (m)', r'$\omega$ (rad/s)', r'$v$ (m/s)']
plt.figure(figsize=(10, 4.5))
for i in range(X.shape[1]):
    plt.plot(t_eval, X[:, i], label=labels[i], linewidth = 4)
plt.xlabel('Elapsed Time (s)', fontsize = 20)
plt.ylabel('State', fontsize = 20)
plt.grid(True)
plt.legend(fontsize = 17, loc = 'upper right')
plt.tick_params(labelsize=18)
plt.tight_layout()
plt.savefig('catbot_state_response.pdf', facecolor='white', transparent=False)
plt.show()

# %%
# Open the meshcat simulator. Only run this once.
simulator = ae353_catbot.Simulator(
    display=True,
    sound=False, # if enabled, may cause a crash
    launch_cat=True,
)


# %%
# Pick a camera angle
simulator.camera_sideview() 
# simulator.camera_wideview()
# simulator.camera_topview()
# simulator.camera_catview()

# %%
controller = Controller() # create an instance of the controller
simulator.reset() # reset the simulation with random initial conditions
controller.reset() # reset the controller
data = simulator.run( # run the simulator
    controller,           # an instance of the controller class
    maximum_time=20.0,     # how long you want to run the simulation in seconds
    data_filename=None,   # <-- optional (save data to this file, e.g., 'my_data.json')
    video_filename=None,  # <-- optional (save video to this file, e.g., 'my_video.mov')
)

# %%
did_save_cat = simulator.did_save_cat()
if did_save_cat:
    print(f'A cat was saved!')
else:
    print(f'No cat was saved.')

# %%
# Get snapshot as height x width x 4 numpy array of RGBA values
rgba = simulator.snapshot()

# Display snapshot
plt.figure(figsize=(8, 8))
plt.imshow(rgba)

# Save snapshot
plt.imsave('my_snapshot.png', rgba)

# %%
# --- Figure 1: kinematics (4 subplots sharing time axis) ---
fsize = 22
fig1, (ax_wheel_position, ax_wheel_velocity, ax_pitch_angle, ax_pitch_rate) = plt.subplots(
    4, 1, figsize=(12, 8), sharex=True
)

# Wheel position
ax_wheel_position.plot(
    data['t'], data['wheel_position'], label='Wheel Position (m)', linewidth=4, color = 'blue'
)
ax_wheel_position.grid()
ax_wheel_position.legend(fontsize=fsize, loc = 'center right')
ax_wheel_position.tick_params(labelsize=fsize)

# Wheel velocity
ax_wheel_velocity.plot(
    data['t'], data['wheel_velocity'], label='Wheel Velocity (m/s)', linewidth=4, color = 'blue'
)
ax_wheel_velocity.grid()
ax_wheel_velocity.legend(fontsize=fsize, loc = 'upper right')
ax_wheel_velocity.tick_params(labelsize=fsize)

# Pitch angle
ax_pitch_angle.plot(
    data['t'], data['pitch_angle'], label='Pitch Angle (rad)', linewidth=4, color = 'blue'
)
ax_pitch_angle.grid()
ax_pitch_angle.legend(fontsize=fsize)
ax_pitch_angle.tick_params(labelsize=fsize)

# Pitch rate
ax_pitch_rate.plot(
    data['t'], data['pitch_rate'], label='Pitch Rate (rad/s)', linewidth=4, color = 'blue'
)
ax_pitch_rate.grid()
ax_pitch_rate.legend(fontsize=fsize)
ax_pitch_rate.tick_params(labelsize=fsize)

# Shared x-axis formatting on the last subplot
ax_pitch_rate.set_xlabel('Elapsed Time (s)', fontsize= fsize)
ax_pitch_rate.set_xlim([data['t'][0], data['t'][-1]])

fig1.tight_layout()


# --- Figure 2: torques (single subplot) ---
fig2, ax_wheel_torque = plt.subplots(1, 1, figsize=(12, 4))

ax_wheel_torque.plot(
    data['t'], data['wheel_torque_command'], label='Wheel Torque Command (N·m)', linewidth=4,
)
ax_wheel_torque.plot(
    data['t'], data['wheel_torque'], '--', label='Wheel Torque (N·m)', linewidth=4,
)



# ± max torque lines
ax_wheel_torque.plot(
    data['t'], np.ones_like(data['t']) * simulator.maximum_wheel_torque,
    ':', linewidth=2, color='C4', zorder=0
)
ax_wheel_torque.plot(
    data['t'], -np.ones_like(data['t']) * simulator.maximum_wheel_torque,
    ':', linewidth=2, color='C4', zorder=0
)

ax_wheel_torque.grid()
ax_wheel_torque.legend(fontsize=fsize)
ax_wheel_torque.tick_params(labelsize=fsize)
ax_wheel_torque.set_ylim(
    -1.2 * simulator.maximum_wheel_torque,
     1.2 * simulator.maximum_wheel_torque,
)
ax_wheel_torque.set_xlabel('Elapsed Time (s)', fontsize=fsize)
ax_wheel_torque.set_xlim([data['t'][0], data['t'][-1]])

fig2.tight_layout()


# %%
fig1.savefig('state_plots.pdf', facecolor='white', transparent=False)
fig2.savefig('torque_plot.pdf', facecolor='white', transparent=False)

# %%


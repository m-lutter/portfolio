# Archived notebook code; see README.md for authorship, dependencies, and saved-run limitations.

# %%
import numpy as np
import matplotlib.pyplot as plt

# %%
# reference values
g0 = 9.80665 # m/s
# geopotential altitude
h1 = 11000 # m
h2 = 25000 # m
h3 = 47000 # m
rE = 6.3781e6 # radius of the earth, m
# Ambient Temperature
T0 = 288.16 # K at sea level
T1 = 216.66 # K at 11 km
T2 = T1
T3 = 282.66 # K
# Atmospheric Pressure
p0 = 101325 # Pa at sea level
p1 = 2.2700e4 # at 11km
p2 = 2.4495e3 # at 25km
p3 = 1.1973e2 # at 47km
# Air Density
rho0 = 1.2250   # kg / m^3
rho1 = 0.36480  # kg / m^3 at 11 km
rho2 = 0.039333 # kg / m^3 at 25 km
rho3 = 1.4757e-3 # kg / m^3 at 47 km
R = 287 # J / kg*K

# %%
def T(h):
    if h <= 11000: # gradient layer
        return T0 + (T1-T0) / h1 * h
    elif h <= 25e3: # isothermal layer
        return T1
    else: # gradient layer
        return  T2 + (T3 - T2) / (h3 - h2) * (h - h2)
def p(h):
    if h <= 11000: # gradient layer
        c = (T1 - T0) / h1
        return p0 * (T(h) / T0)**(-g0/(c*R))
    elif h <= 25e3: # isothermal layer
        return p1 * np.exp(-g0/(R*T(h))*(h-h1))
    c = (T3 - T2) / (h - h2) # gradient layer
    return p2 * (T(h) / T2)**(-g0/(c*R))

def rho(h):
    if h <= 11000: # gradient layer
        c = (T1 - T0) / h1
        return rho0 * (T(h) / T0)**(-g0/(c*R)-1)
    elif h <= 25e3: # isothermal layer
        return rho1 * np.exp(-g0/(R*T(h))*(h-h1))
    c = (T3 - T2) / (h - h2) # gradient layer
    return rho2 * (T(h) / T2)**(-g0/(c*R) - 1)

def hg(h): # returns the geometric altitude at the geopotential altitude
    return h*rE / (rE - h)
def g(hg): # returns the force of gravity at the geopotential altitude
    return g0 * rE / (rE + hg)

# %%
# Will use Euler Method -> First Define acceleration
t0 = 0.0002 # m
massPayload = 3.0 # kg
massGas = 0.5 # kilograms

molarMassGas = 2.016 # H2
r0 = (3*(massGas*1000/molarMassGas)*8.314*T0/(4*np.pi*p0))**(1/3) # initial radius, m
densityLatex = 920 # kg/m^3
latexVolume = ((r0 + t0)**3 - r0**3)*np.pi * (4/3) # kg / m^3
massBalloon =  densityLatex * latexVolume # kg
massTotal = massGas + massBalloon + massPayload

Cd = 0.47
G = 0.000500e9 # Pa Shear Modulus
criticalStress0 = 3.4e6 # Pa critical stress at STP (needs more research)
criticalStress = criticalStress0

# %%
def balloonRadius(a, b, c, d, e, f):
    # determines the radius of the balloon from a 5th degree polynomial
    poly = np.polynomial.polynomial.Polynomial([a, b, c, d, e, f])
    roots = poly.roots()
    # Filter to only real roots (using a tolerance for the imaginary part) and non-negative values.
    positive_real_roots = [r.real for r in roots if np.isclose(r.imag, 0, atol=1e-8) and r.real >= 0]
    # Return the smallest positive real root if available; otherwise, return NaN.
    if not positive_real_roots:
        return np.nan
    return min(positive_real_roots)

def proximityToFailure(r, t): # evaluates the proximity to critical stress
    return criticalStress - G*t0/t*(r0/r - r0**4/r**4)

a = np.linspace(0,47000,47001)
diameterValues = np.ones(np.size(a))
temperatureValues = np.zeros(np.size(a))
pressureValues = np.zeros(np.size(a))
densityValues = np.zeros(np.size(a))


for i in range(np.size(a)):
    temperatureValues[i] = T(a[i])
    pressureValues[i] = p(a[i])/1000
    densityValues[i] = rho(a[i])
    diameterValues[i] = 2*balloonRadius(-2*G*t0*r0**4, 0, -3*(massGas/2.016)*8.314e3*T(a[i]), 2*G*t0*r0, 0, 4*np.pi*p(a[i]))
a /= 1000 # convert to km for clear plotting

# %%
plt.plot(diameterValues, a, 'k')
plt.xlabel("Diameter (m)")
plt.ylabel("Altitude (km)")
plt.figtext(0,-0.01,"Figure #. The diameter of a balloon in meters versus the altitude in kilometers in the atmosphere, assuming no failure.", weight = 'bold', va = 'center_baseline')
plt.show()

# %%
plt.plot(temperatureValues, a, 'k')
plt.xlabel("Temperature (K)")
plt.ylabel("Altitude (km)")
plt.figtext(0,-0.01,"Figure #. The temperature of the air in Kelvin versus the altitude in kilometers in the atmosphere.", weight = 'bold', va = 'center_baseline')
plt.show()

# %%
plt.plot(pressureValues, a, 'k')
plt.xlabel("Atmospheric Pressure (kPa)")
plt.ylabel("Altitude (km)")
plt.figtext(0,-0.01,"Figure #. The atmospheric pressure in kPa versus the altitude in kilometers in the atmosphere.", weight = 'bold', va = 'center_baseline')
plt.show()

# %%
plt.plot(densityValues, a,'k')
plt.xlabel("Air Density (kg / m^3)")
plt.ylabel("Altitude (km)")
plt.figtext(0,-0.01,"Figure #. The density of the air in kilograms per cubic meter versus the altitude in kilometers in the atmosphere.", weight = 'bold', va = 'center_baseline')
plt.show()

# %%
def eulerMethod(t0, massGas, tf, dt):
    time = np.arange(0, tf + dt, dt) # time array
    y = np.zeros(np.size(time)) # altitude array
    vy = np.zeros(np.size(time)) # velocity array
    forces = np.zeros(np.size(time)) # force array
    diameter = np.zeros(np.size(time)) # radius array
    pToF = np.zeros(np.size(time)) # proximity to failure array
    # initial conditions:
    y[0] = 0 # launch altitude
    vy[0] = 0 # launch velocity

    success = False

    for n in range(len(time) - 1):
        # radius function call for the current altitude
        radius = balloonRadius(-2*G*t0*r0**4, 0, -3*(massGas*1000/2.016)*8.314*T(y[n]), 2*G*t0*r0, 0, 4*np.pi*p(y[n]))
        diameter[n] = radius * 2 # log diameter for output

        t = t0 * (r0/radius)**2 # new thickness due to balloon expansion

        criticalStress = criticalStress0 * (1 - .01*(T(y[n])-T0))
        pToF[n] = proximityToFailure(radius, t)
        if pToF[n] < 0:
            print("The Balloon Popped! The altitude is", y[n])
            success = False
            break

        # now calculate forces to find net force on the balloon
        drag = .5*rho(y[n])*Cd*vy[n]*(radius**2*np.pi)    # force due to drag on the balloon
        Fb = rho(y[n])*(radius + t)**3*np.pi*(4/3)*g(y[n])# force of buoyancy due to pressure gradient
        Fg = - massTotal*g(y[n]) # force of gravity on the balloon
        force = Fb + Fg - drag # net force on the balloon
        forces[n] = force

        ayn = force / massTotal # newton's second law

        vy[n + 1] = vy[n] + ayn * dt # velocity at next timestep

        y[n + 1] = y[n] + vy[n] * dt # position at next timestep

        if (vy[n] < 0 or y[n] < 0): # check if balloon is moving downward
            if y[n] < 350000:
                break
            print("The maximum altitude is ", y[n])
    return vy, y, time, forces, diameter, pToF

# %%
# simulation
massGas = 0.2
t0 = 0.0002
while True:
    vy, y, time, forces, diameter, proxToFail = eulerMethod(t0, massGas, 20000, 0.5)
    if (np.max(y) >= 35000): # condition for success
        print("The balloon has reached the target altitude!", massGas, "kg of gas was used with initial thickness", t0, "m")
        break
    else:
        print("failure with", massGas, "kg H2 with initial thickness", t0, "m, at height", np.max(y))
        massGas += 0.01 # increment the amount of gas used if success is not achieved
    # recalculate the radius, volume, and mass for this additional gas
    r0 = (3*(massGas/molarMassGas)*8.314e3*T0/(4*np.pi*p0))**(1/3) # (3*initialVolume/(4*np.pi))**(1/3) from volume
    latexVolume = ((r0 + t0)**3 - r0**3)*np.pi * (4/3)
    massBalloon =  densityLatex * latexVolume # kg
    massTotal = massGas + massBalloon + massPayload

for i in range(2, np.size(time)):
    # remove zero values at the end of the arrays output
    if y[i] == 0:
        vy[i] = np.nan
        y[i] = np.nan
        forces[i] = np.nan
        diameter[i] = np.nan
        time[i] = np.nan
        proxToFail[i] = np.nan

# %%
y /= 1000  # convert to km
time /= 60 # convert to minutes
plt.plot(time, y, 'k')
plt.xlabel("Time Elapsed (min)")
plt.ylabel("Altitude (km)")
plt.figtext(0,-0.01,"Figure #. The altitude in kilometers versus the time elapsed in minutes for the balloon.", weight = 'bold', va = 'center_baseline')
plt.show()

# %%
plt.plot(time, vy, 'k')
plt.xlabel("Time Elapsed (min)")
plt.ylabel("Velocity (m/s)")
plt.figtext(0,-0.01,"Figure #. The velocity in meters per second versus the time elapsed in minutes for the balloon.", weight = 'bold', va = 'center_baseline')
plt.show()

# %%
plt.plot(time, forces, 'k')
plt.xlabel("Time Elapsed (min)")
plt.ylabel("Net Force (N)")
plt.figtext(0,-0.01,"Figure #. The net force in Newtons versus the time elapsed in minutes for the balloon.", weight = 'bold', va = 'center_baseline')
plt.show()

# %%
plt.plot(time, diameter, 'k')
plt.xlabel("Time Elapsed (min)")
plt.ylabel("Balloon Diameter (m)")
plt.figtext(0,-0.01,"Figure #. The diameter of the balloon in meters versus the time elapsed in minutes.", weight = 'bold', va = 'center_baseline')
plt.show()

# %%
proxToFail /= 1000000
plt.plot(y, proxToFail, 'k')
plt.xlabel("Altitude (km)")
plt.ylabel("Proximity to Failure (MPa)")
plt.figtext(0,-0.04,"Figure #. The proximity to failure in MPa versus the altitude of the balloon.", weight = 'bold', va = 'center_baseline')
plt.show()

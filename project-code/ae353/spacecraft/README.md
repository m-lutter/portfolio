# Spacecraft feedback and attitude observer — AE353 DP3

Controller and observer work reported jointly by Maxwell Lutter and Adrian Huang. The report does not divide individual functions between the teammates. Tim Bretl, Wayne Chang, and the course staff supplied the dynamics, spacecraft-design utilities, and simulation infrastructure.

[SpacecraftDemo.ipynb](SpacecraftDemo.ipynb) / [Python code](SpacecraftDemo.py) contain wheel placement, nonlinear and sensor models, linearization and rank checks, LQR feedback, an attitude observer, trial helpers, and observer-error calculations.

The archived notebook retains text output from a 25-trial run with 64% mission success; the submitted report describes 200 trials. The notebook's observer-check call uses a 5° threshold, whereas the report and plotted criterion use 3.5°. These saved results and current parameters are preserved, and no fresh experiment is claimed. Graphical/HTML display outputs were removed for source browsing.

The [portfolio case study and report](https://m-lutter.github.io/portfolio/projects/spacecraft-attitude.html) preserve both conclusions: the reported estimation criterion was met, while integrated mission success remained below the 80% requirement.

Dependencies include NumPy, SciPy, SymPy, Matplotlib, IPython, and the supplied `ae353_spacecraft_design` / `ae353_spacecraft_simulate` modules. Follow the [course repository's environment instructions](https://github.com/tbretl/ae353-fa25) and use its `projects/03_spacecraft` directory and assets. Notebook setup can regenerate spacecraft/star assets and initialize the simulator; use a separate working copy when exploring it.

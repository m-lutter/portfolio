# Balancing cat-catching robot — AE353 DP1

[CMGDemo-Team17.ipynb](CMGDemo-Team17.ipynb) identifies Max Lutter and Luke Phan as its authors. It explicitly credits Tim Bretl, Wayne Chang, and the AE353 course staff for the equations of motion, and Bretl for the simulation interface. The notebook does not allocate individual functions between its student coauthors.

The [Python code export](CMGDemo-Team17.py) and notebook include symbolic modeling/linearization, stabilizing feedback-gain searches, eigenvalue checks, linear state responses, a bounded wheel-torque controller, and simulation setup. A saved catch demonstration informs the [portfolio case study](https://m-lutter.github.io/portfolio/projects/cat-catching-robot.html), rather than a measured catch-success percentage. The notebook also discusses display-dependent behavior that hindered automated gain screening.

Source cells and available text outputs are preserved; graphical/HTML outputs were removed. The files were not rerun for publication.

Dependencies include NumPy, SciPy, SymPy, Matplotlib, IPython, and the supplied `ae353_catbot` module. Follow the [Fall 2025 course repository's setup instructions](https://github.com/tbretl/ae353-fa25) and use its `projects/01_catbot` directory, simulator, and assets. Running the notebook initializes the simulator and writes plot files.

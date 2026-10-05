# Flying-wing landing controller — AE353 DP2

Controller-design and evaluation work reported jointly by Maxwell Lutter and Navid Navidzadeh. The available report does not divide individual functions between the teammates. Tim Bretl, Wayne Chang, and the AE353 course staff supplied the aircraft dynamics and simulation infrastructure.

- [DP2_Team33.ipynb](DP2_Team33.ipynb) / [Python code](DP2_Team33.py): trim search, symbolic linearization, controllability checks, LQR feedback, simulation trials, and failure plots. Its saved output reports 1,757 successful landings out of 2,000 (87.8%); its current trial call requests one run.
- [ZagiDemo-template.ipynb](ZagiDemo-template.ipynb) / [Python code](ZagiDemo-template.py): despite its retained template filename, this is a modified project notebook with controller/evaluation code. Its saved output reports 3,491 of 4,000 successful landings (87.3%), corresponding to the submitted report's result.

These are archived development states, with graphical/HTML outputs removed and source cells preserved. They were not rerun for publication. Use the [portfolio report and case study](https://m-lutter.github.io/portfolio/projects/flying-wing-control.html) for the submitted conclusions.

The notebooks import NumPy, SciPy, SymPy, Matplotlib, IPython, and `ae353_zagi`. To investigate execution, follow the environment instructions in the [Fall 2025 course repository](https://github.com/tbretl/ae353-fa25) and place a notebook in its `projects/02_zagi` directory, alongside the supplied simulation module and assets. Simulation functions can write plot files and initialize PyBullet; review the trial count before running. The course framework remains credited to its authors.

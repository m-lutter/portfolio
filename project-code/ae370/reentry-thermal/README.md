# Reentry thermal-protection study — AE370 Project 2

Team report by Jeremy Zang, Landon Lopez, Danfeng Ye, Max Lutter, and Kenny Carter. The report credits Danfeng Ye with the conduction solver, verification suite, parameter sweeps, and run scripts. Maxwell Lutter contributed implementation/verification writing, consistency checks, interpretation, plotting, and report editing. The archived code is presented as team source.

- [GP-2-Implementation.ipynb](GP-2-Implementation.ipynb) / [Python code](GP-2-Implementation.py): an implementation notebook coupling an RK4 reentry trajectory and prescribed surface heating to a spherical conduction model.
- [Valiadtion_final.ipynb](Valiadtion_final.ipynb) / [Python code](Valiadtion_final.py): a later notebook containing conservative finite-volume/Crank–Nicolson routines, tridiagonal solution, verification calculations, and material comparisons. The original filename spelling is retained.

Code cells and available text outputs are preserved; graphical/HTML outputs were removed. These are distinct historical notebook versions, not a consolidated release, and their current parameters need not reproduce the submitted figures. No full numerical study was rerun for publication. See the [portfolio case study and report](https://m-lutter.github.io/portfolio/projects/reentry-thermal-model.html) for the reported convergence and material-study conclusions.

Dependencies include NumPy, Matplotlib, and pandas, plus Jupyter for notebook viewing. Review simulation settings before execution: the verification notebook currently contains a 12,800-cell material run, so executing all cells can be expensive. Python exports preserve code-cell order and execute those cells when run as scripts.

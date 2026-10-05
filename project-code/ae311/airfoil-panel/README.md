# Airfoil panel-method study — AE311 Project 2

[panel_method_export.py](panel_method_export.py) was recovered from `6412/Untitled6.html`, an HTML notebook export in the team's Overleaf report archive. The recovered code is preserved with an added provenance header. It includes source/vortex influence calculations, streamline calculations, a Kutta condition, circulation, lift, and pressure plotting.

The submitted report credits teammate Jackson Rees with implementing the solver, adapted from JoshTheEngineer. Maxwell Lutter's documented contribution was glider-design research and interpretation, rather than sole authorship of the solver. The [portfolio case study and report](https://m-lutter.github.io/portfolio/projects/airfoil-panel-study.html) retain those roles.

JoshTheEngineer's [Panel_Methods repository](https://github.com/jte0419/Panel_Methods) carries an MIT license. Its copyright and license notice are included in [LICENSE-JoshTheEngineer.txt](LICENSE-JoshTheEngineer.txt) for the adapted components. Team adaptations retain their original authorship; this notice does not relicense the entire portfolio.

This is recovered source for inspection, with Python syntax checked and no numerical rerun. NumPy and Matplotlib are imported, along with `XFOIL`, panel-integral, streamline, and circulation helper modules. Several helpers are defined again in the export, but the referenced XFOIL wrapper/executable and original execution environment were not present in the recovered archive. Consult the upstream project for that environment; the preserved file is not packaged as a standalone runnable application.

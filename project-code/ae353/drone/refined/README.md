# AE353 DP4: refined controller and simulation study

This archive documents the later, individual extension of the original quadrotor-race project. It matches the saved study behind the presentation's **971/1,000 completed courses (97.1%)** and **64.26 s mean successful completion time**.

## Contents

- `refined-study.ipynb`: source-only notebook, with all 28 frozen code cells and no outputs.
- `refined-study.py`: the same code cells in a readable Python export. Executing it runs the study and writes plots.
- `evaluation-config.json`: tested navigation settings, model/gain matrices, 1,000 course seeds, and 80 s trial horizon.
- `evaluation-summary.json`: verified aggregate results and per-trial scalar outcomes.
- `source-provenance.json`: source hashes, extraction details, and version limitations.
- `requirements.txt`: known local working dependency versions, rather than a claimed lockfile from the original evaluation.

## Ownership and contribution

The original course study was a collaboration between **Maxwell Lutter and Landon Lopez**. Maxwell led system modeling and control design, navigation strategy and final controller development, and simulation automation and visualization. Landon contributed controller implementation and obstacle avoidance, experimental methods and results analysis, and report structure and technical writing. The final report and technical decisions were shared.

The later parameter refinement, smooth reference-motion changes, additional simulation, diagnostics, and presentation were Maxwell's individual extensions. These files do not imply that Maxwell authored the complete course simulator. Course staff supplied `ae353_drone.py`, its `urdf/` assets, physics, sensor measurements, actuator rules, and scoring.

The original notebook and report remain separate historical evidence. The [original report](https://m-lutter.github.io/portfolio/reports/drone-obstacle-course.pdf) reports 95 completions in 100 trials and 73.35 s mean among successful flights. The refined study used a different cohort. The 12.4% reduction in reported mean time is a descriptive comparison; the completion-rate difference has not been established as statistically significant.

## Version and result limits

The source comes from the saved `DP4 Drone(Lutter) - Submission.html` export associated with the 1,000-course result. The mutable working notebook later changed to 100 trials and changed the departure-waypoint multiplier from 1.25 to 1.5. Those later edits and outputs are not part of this snapshot.

The extraction preserves each code cell's text. The Python export adds comments between cells; the notebook adds this archive's context and removes all outputs. Source paths and contact details are not included.

The saved result JSON provides configuration, matrices, seeds, stopping reasons, and timing-violation counters, but no frozen controller source hash or raw telemetry. The saved HTML supplies matching controller/evaluator source and the figures presented with the cohort. This archive therefore documents that association, without claiming a complete execution-time provenance chain. The observer-error and applied-rotor-speed figures cannot be reconstructed from the compact scalar JSON alone.

Of the 29 unsuccessful trials, 16 ended under the inactivity rule and 13 ended out of bounds. A plotted trajectory can suggest a collision, but does not prove one. All 1,000 trials met the no-more-than-nine calls above 10 ms rule; the maximum was two. These timing observations are specific to the evaluation environment.

This is simulation work. Known geometry, fixed model parameters, idealized sensor behavior, and immediate actuator response limit transfer to a physical drone.

## Run or inspect

Use Python 3.12 with the listed dependencies and obtain the [course simulator and assets](https://github.com/tbretl/ae353-fa25/tree/main/projects/04_drone). Place `ae353_drone.py` and `urdf/` together beside the notebook or in `course/`. Open the notebook to inspect the derivation, controller, trial runner, plots, and optional Latin hypercube search. Running every cell performs a new study; its fresh random seeds and results will differ from the preserved cohort.

For the preserved course cohort, replace the seed-generation cell with a load of `evaluation-config.json` and use its `seeds` and `simulation_horizon_s`. The archived configuration includes the matrices and navigation settings for checking the setup. Machine timing can change on rerun. Search and live viewing are disabled by default.

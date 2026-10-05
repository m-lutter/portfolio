# Drone obstacle-course control and observer — AE353 DP4

Team study by Maxwell Lutter and Landon Lopez. The seven-page report's contribution appendix identifies Maxwell as the primary developer of the final drone code and credits his work on linearization, gain selection, navigation strategy, repeated-trial data collection, figures, and report revisions. Landon contributed controller implementation, obstacle avoidance, experimental-method writing, and analysis/conclusions. The dynamics, sensor model, simulator, and course assets are supplied AE353 material.

- [DP4 Drone(Lutter).ipynb](DP4%20Drone%28Lutter%29.ipynb): the retained notebook with controller/observer design, navigation logic, trial helpers, plots, and matching saved results.
- [drone_design_and_trials.py](drone_design_and_trials.py): notebook code cells exported in their original order for inspection.
- [mlutter2.py](mlutter2.py): the related standalone controller file from the course's `students` directory, copied without changes. Its controller source differs from the notebook version; use the notebook/report for the reported performance.

The report and saved notebook text give **95 successful course completions in 100 trials**, with a **73.35 s mean among successful runs**. The saved range is 68.36–79.12 s. These exceeded the course's 80% completion and below-80-second mean requirements. Five failures were retained and analyzed near the obstacle region. See the [portfolio case study and complete report](https://m-lutter.github.io/portfolio/projects/drone-obstacle-course.html).

Original code cells, markdown, execution counts, and available text outputs are preserved. Graphical/HTML outputs were removed for easier source browsing; selected original figures appear on the case-study page. No new simulation was run for publication. The current seed list differs from the seed list printed with the saved run, so a new execution is not an exact reproduction of the historical study.

Dependencies include NumPy, SciPy, SymPy, Matplotlib, IPython/Jupyter, and the supplied `ae353_drone` simulator and assets. Follow the [Fall 2025 course repository's environment instructions](https://github.com/tbretl/ae353-fa25) and use its `projects/04_drone` directory. Review the 100-trial loop before execution; the notebook initializes simulator/visualizer instances and writes plot files. A filename ending in `.py` does not remove those runtime requirements.

Original authors retain their rights. The root portfolio MIT license does not apply to this course-source archive.

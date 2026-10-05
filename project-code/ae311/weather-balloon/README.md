# Weather-balloon ascent — AE311 Project 1

Maxwell Lutter was the technical lead for the three-person study, responsible for the mathematical model, Python simulation, plots, and solution documentation, as described in the submitted report.

[311CodeProject1.ipynb](311CodeProject1.ipynb) / [Python code](311CodeProject1.py) are an available development copy with atmosphere and gravity functions, an expanding balloon model, a failure calculation, Euler integration, gas-mass iteration, and plots. The retained notebook is a hydrogen-model working state. It has no saved cell outputs and should not be treated as a complete reproduction of the report's hydrogen-versus-helium comparison or selected masses.

The [portfolio case study and report](https://m-lutter.github.io/portfolio/projects/weather-balloon.html) remain the basis for the reported 0.43 kg hydrogen recommendation and gas comparison. No simulation was rerun when preparing these files.

Dependencies are NumPy and Matplotlib, plus Jupyter to open the notebook. The `.py` export preserves the code cells in order for inspection. The notebook performs a mass-sweep simulation and produces plots when executed; its existing parameter choices and historical model limitations are retained.

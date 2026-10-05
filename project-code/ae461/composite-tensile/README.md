# Composite tensile-test analysis — AE461 Lab 6

[stress_strain_analysis.py](stress_strain_analysis.py) was recovered from the Python `verbatim` appendix in the team's Overleaf report archive. The code is preserved with an added provenance header. It reads Instron and digital-image-correlation CSV records, derives engineering stress from force and specimen dimensions, and plots stress–strain comparisons for the three fiber orientations.

The report is by Alp Alptekin, Eli Bennett, Maxwell Lutter, and Srijesh Konakanchi. Its contribution table credits Maxwell with the stress–strain curves, specific modulus/strength, apparatus, uncertainty, and manufacturing-history sections. The appendix does not separately assign authorship of each Python function, so the recovered implementation is credited to the team. See the [portfolio case study](https://m-lutter.github.io/portfolio/projects/composite-tensile-testing.html).

Required libraries are pandas, NumPy, and Matplotlib. Input files are expected in the current directory: `A06CCF00_1.csv`, `A06CCF45_1.csv`, `A06CCF90_1.csv`, `Strain_0.csv`, `Strain_45.csv`, and `Strain_90.csv`. The report archive contains figures and summary tables but not these complete time-history CSV files. Python syntax was checked; no new processing run is claimed.

Original authors retain their rights. The root portfolio MIT license does not apply to this team-source archive.

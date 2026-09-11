# Portfolio source review — September 2026

The portfolio owner requested a review of all descriptions against the original reports and added laboratory archives and controls notebooks. This review checked the 13 existing case studies, all eight digital-circuit summaries, and five newly included projects. It did not rerun the scientific experiments or control simulations.

## Results clarified

| Project | Source and interpretation retained in the portfolio |
| --- | --- |
| Flying-wing landing | AE353 DP2, results/conclusion: 87.3% across 4,000 trials, exceeding 85%. A saved notebook output records 3,491/4,000. Another notebook retains 1,757/2,000 while its edited call requests one trial. Use the submitted report’s metric; do not combine development runs. |
| Spacecraft control | AE353 DP3, p. 6–7: observer errors satisfy the stated criterion in the plotted trials; combined mission success is 64% in a reported 200-trial study, below 80%. The saved notebook has 25 trials and a 5° checker call, while the plot/report use 3.5°. Present the positive observer conclusion and mission shortfall separately. |
| Reentry thermal model | AE370, numerical verification and Results/Discussion: near-second-order convergence and a 0.0161 K analytical benchmark discrepancy. Restore the report’s conductivity/thermal-mass conclusions rather than reducing the project to verification alone. Avoid quoting absolute reentry temperatures as validated physical performance. Maxwell’s role is documented on p. 14; Danfeng Ye is credited for the solver. |
| Weather balloon | AE311 Project 1, tables 1–2 and interpretation on p. 19: report recommendation is 0.43 kg hydrogen versus 0.95 kg helium, with simulated maxima 43.12/39.14 km and report-assumed gas costs $2.07/$90.36. Restore this conclusion and label it as the original model result, not current pricing or a new flight test. |
| Airfoil panel study | AE311 Project 2, results table/discussion: NACA 6412 has the highest lift coefficient among the four tested airfoils at the tested angles. This is a lift comparison, not an overall glider optimum. Preserve Maxwell’s research role and the solver attribution to Jackson Rees/JoshTheEngineer. |
| Finite-wing study | AE311 Project 3, p. 24–25: retain 11 m span, 1 m root, 0.4 m tip, no twist. Explain the manufacturing rationale and that the no-twist recommendation extrapolates the rectangular-wing twist comparison to the proposed taper. |

## New projects and contribution basis

| Project | Source | Attribution and result scope |
| --- | --- | --- |
| Cat-catching robot | `CMGDemo-Team17.ipynb`, author cell, gain selection, controller, saved catch output and plots | Max Lutter and Luke Phan are named coauthors. Course staff supply dynamics and simulator. A saved successful catch is shown; no catch percentage is claimed. |
| Photoelastic stress | AE461 Lab 2, “Comparison” and “Conclusion” | Four-person report; no individual task split. Notch concentrations observed; U-notch approximation agrees more closely with FEA; V-notch approximation is outside its geometry range. |
| Rod buckling | AE461 Lab 4, support/material/eccentricity comparisons and conclusion | Four-person report; no individual task split. Support trend has a fixed–fixed exception (710 N measured versus 2194.26 N predicted); material trend follows stiffness; eccentric loading gives gradual bending. |
| Beam modal testing | AE461 Lab 5, FRF analysis, EDM comparison and conclusion | Four-person report; no individual task split. Five impact-test modes over 17 locations agree with EDM frequencies within 0.4%. The separate shaker sequence is not conflated with this result. |
| Composite tensile testing | AE461 Lab 6, stress–strain/specific-property sections, conclusion and individual-contribution table | Maxwell: stress–strain comparison, specific modulus/strength, apparatus, uncertainty, manufacturing-quality/environment/cure-history discussion. Primary modulus/strength extraction and theoretical predictions are attributed to the named teammates. Preserve the report’s qualitative agreement and quantitative disagreement. |

## Other descriptions reviewed

- The Other Side: checked against all 18 presentation slides. Physical core behavior is complete; an independently timed second obstacle row and difficulty adjustment remain proposed additions. The deck does not divide subsystem ownership between Maxwell Lutter and Carlos Selvi.
- BCD decoder, EPROM decoder, Frogger Lite, and all eight circuit archive summaries: checked against their original repository notes. Keep the 40 **AND/OR** gate qualifier, simulation/build distinctions, and documented incomplete overflow/collision extensions.
- Orbital Training: checked against the public repository README. Its architecture, test types, and public-beta status match the description; native health integration remains experimental.
- FieldPlan and FieldMark2: descriptions remain grounded in the supplied current code and the previous processing/export checks. Preserve Talman ownership, the existing FieldPlan live link, and synthetic-test scope.

## Publication scope

This update publishes revised site copy, five new case studies, and nine selected source figures. Eight figures are byte-identical copies of report assets; the robot plot is a PNG rendering of the supplied PDF plot. It does not publish the mixed-authorship controls archive or change the source reports. The six previously authorized public report PDFs remain available. Local extraction, review scripts, and source documents remain outside the published tree.

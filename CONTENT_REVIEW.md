# Portfolio source review — September and October 2026

## October 5: report-grounded engineering stories

All 19 case pages were reviewed for a clear goal, consequential design or implementation decisions, outcome, and the technical evidence those choices provide. More involved controls, thermal, composites, and deployed software projects now have deeper narratives. Shorter circuit studies remain proportionate to their documented scope. The four selected projects and the category filters below them remain in place; supporting cards now show a short description as well as the outcome. Case pages include navigation to their story sections.

The academic copy was checked against the supplied report PDFs, complete report TeX in the Overleaf archive, and preserved notebook outputs. Newly used evidence includes the complete AE353 DP1 cat-catching report in the Overleaf archive, which discusses residual offsets after impact. No academic experiment or numerical simulation was rerun, and no synthetic academic results were introduced. Detailed source-version differences remain in linked code READMEs.

Image choices prioritize original simulation scenes, experimental photographs, apparatus diagrams, and decisive plots. New source visuals include balloon forces, airfoil streamlines, spacecraft and catbot simulation views, the photoelastic loading photograph, and the buckling apparatus. The composite apparatus is a labeled SVG adaptation of the report's TikZ schematic; FieldMark2 has a workflow diagram drawn from its maintained source. Existing result plots remain with the relevant interpretations. Original source reports, notebooks, and their attribution are unchanged.

The professional applications remain grounded in their maintained code and documentation. Orbital's public README was checked again on October 5; its deterministic engine, concurrency controls, immutable history, and test layers support the product-engineering narrative. The publicly reachable product currently opens to a sign-in page, so an architecture summary remains its primary visual rather than an unauthenticated screen presented as a working session. FieldPlan retains its live-app screenshots with explicitly synthetic data and no field-savings claim. Talman ownership remains explicit for both field tools.

Publication includes only curated content, generated pages/styles, and selected image assets. Private source ZIPs, review files, resumes, and contact details from the source documents remain outside the public tree. The existing seven public report PDFs are unchanged. The excluded Frogger C++ prototype remains excluded.

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

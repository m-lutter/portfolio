# Editing the portfolio website

The public site is built from the `docs/` folder and hosted on GitHub Pages.

- `content/projects.mjs`: selected-project ordering, original digital project copy, and the eight-circuit archive.
- `content/other-side.mjs`: the completed physical game, based on the final presentation.
- `content/controls.mjs`: the AE353 control studies and AE370 thermal-model verification study.
- `content/catbot.mjs`: the co-authored AE353 DP1 controller notebook and saved simulation evidence.
- `content/structures.mjs`: four AE461 laboratory studies with report-based contribution credit.
- `content/aerodynamics.mjs`: the three AE311 studies and documented individual contributions.
- `scripts/build.mjs`: homepage copy and shared page templates. Uses Node.js built-ins; no packages to install.
- `docs/styles.css`: colors, layout, typography, responsive styles, and print styles.
- `docs/site.js`: accessible featured-project filtering.
- `docs/assets/`: original portfolio images, presentation photos/diagrams, and figures extracted from the supplied project reports.
- `content/field-tools.mjs`: FieldPlan and FieldMark2 professional software entries, with Talman ownership attribution.
- `content/publication.mjs`: controls report-download visibility. The owner explicitly authorized publishing all six prepared copies.
- `docs/reports/`: six downloadable reports, with author addresses and a teammate email removed from the four affected documents.

Run `node scripts/build.mjs` after editing content or templates. Commit both the source and the generated `docs/` files. Run `node scripts/serve.mjs` for a local preview at `http://127.0.0.1:4173/portfolio/`.

GitHub Pages configuration: deploy from branch `main`, folder `/docs`. A `.nojekyll` file makes this a plain static site. There are no runtime dependencies, analytics scripts, API keys, or sign-in requirements.

Counts, project numbers, and filter badges derive from the selected project list. A project with `listed: false` still gets a case page and sitemap entry; this preserves the earlier Frogger Lite URL while featuring its physical final project. Optional `context`, `roleLabel`, `evidenceNote`, `gallery`, and section `figure` fields support team attribution and multiple original figures. Use `cardFit: 'contain'` for plots to preserve axes and legends.

## Content basis

The initial page uses the public `m-lutter/portfolio` digital-systems collection and the public `m-lutter/orbital-training` README. Orbital is identified as a deployed beta, not a finished stable release. The pump repository contained only a planning skeleton when reviewed and is not featured. The owner authorized including FieldPlan and FieldMark2 based on the supplied current Python files. The site presents descriptions and links; application source and field inputs stay in the separate project repositories. Talman Consultants, LLC owns the application copyright.

Digital projects retain distinctions between simulated designs, physical builds, and incomplete extensions. The 75-to-40 gate comparison comes from the original 5421 BCD write-up and is not a power or timing measurement. Original project folders are preserved.

The EPROM and Frogger images were copied from working image attachments in their original README files. The BCD image is the original Tinkercad export. Several original local JPEG/MOV files contain only two bytes; they are not linked as usable media.

The biography reflects the owner's September 2026 Job Research context: UIUC aerospace engineering, expected December 2026 graduation, launch-vehicle systems/integration, and GNC/avionics integration. Update the graduation wording when appropriate. Contact uses the owner's connected GitHub profile email.

## Aerospace extension sources

- The Other Side: the 18-slide final presentation by Maxwell Lutter and Carlos Selvi, linked in the case study. Its core physical build is complete; the independently timed second obstacle row and difficulty adjustment remain proposed hardware extensions.
- AE311 Project 1: weather-balloon report, 28 pages; Maxwell is technical lead. The 35 km altitude and 3 kg payload are requirements. The 0.43 kg hydrogen recommendation, simulated altitudes, and gas costs are explicitly the report’s results and historical assumptions, not new simulations or flight validation.
- AE311 Project 2: airfoil/panel-method report, 31 pages; Maxwell is real-world problem lead. Preserve the solver attribution to JoshTheEngineer and teammate Jackson Rees’s technical role.
- AE311 Project 3: finite-wing report, 30 pages; Maxwell is team lead. The recommended geometry is a preliminary result for a hypothetical design scenario, not a built aircraft wing.
- AE353 Project 2: flying-wing landing report, 6 pages; joint work with Navid Navidzadeh. Reported 87.3% success across 4,000 randomized simulations exceeds the 85% course requirement.
- AE353 Project 3: spacecraft report, 7 pages; joint work with Adrian Huang. Present both report conclusions: successful observer accuracy and 64% combined mission success across 200 reported trials against an 80% requirement. The supplied notebook instead retains a 25-trial run and a 5° checker call; the report’s observer plot shows 25 results below 3.5°. Keep saved-run details distinct from the submitted report’s evaluation.
- AE370 Project 2: reentry thermal study, 15 pages; five authors with individual roles on page 14. Maxwell contributed verification/implementation writing, consistency checks, interpretation, plotting, and report editing. The solver is credited to Danfeng Ye. Describe both numerical verification and the report’s conductivity/thermal-mass tradeoffs. Numerical benchmark error is not a physical-temperature accuracy guarantee.

Source figures are reproduced from the reports without redrawing their data. The owner explicitly authorized publication of all six prepared reports. Author addresses were removed from the three AE311 PDFs and a teammate email from the spacecraft PDF using actual text redaction. Later pages were checked for unchanged text; the other two PDFs are byte-identical copies. Local research files and original contact-bearing documents are excluded from publication and are not needed to build the site.

## Laboratory and controls-code extension

The four AE461 archives contain LaTeX reports and reused figures from earlier labs. Only figures actually referenced by the relevant report are used. Lab 2 compares photoelastic stresses, analytical approximations, and included Abaqus results. Lab 4 documents a fixed–fixed exception to the expected support trend. Lab 5 keeps shaker frequencies separate from impact-test frequencies and reports FRF/EDM agreement within 0.4%. Lab 6 credits Maxwell’s stress–strain, specific-property, uncertainty, apparatus, and manufacturing-history sections directly from its contribution table.

The AE353 archive contains both completed notebooks and course examples/tutorials. The DP1 notebook credits Maxwell and Luke Phan. Flying-wing and spacecraft notebooks inform implementation descriptions; they are saved development states, not clean rerun records. The site credits course equations and simulation interfaces to the instructors and credits controller studies jointly when individual authorship is not specified. The uploaded archive, framework source, templates, and private research extraction are not part of the static-site deployment.

## Field software sources

FieldPlan uses the supplied `fieldplan_v21.py` with Thermo readiness filtering,
plus the repository fix for an explicitly empty photo-color selection. Its live
link is https://fieldplan.streamlit.app/; the private source repository is not
presented as a public resource. FieldMark2 uses the supplied
`FieldMark2_compression_slider.py`, maintained as `FieldMark2.py` in
https://github.com/m-lutter/FieldMark2. Both carry Talman copyright attribution.
Synthetic checks support functionality descriptions; no measured field savings
or deployment-scale performance results are claimed. The user requested simple
inclusion without a separate demo. Plain text card artwork uses `artLabel`.

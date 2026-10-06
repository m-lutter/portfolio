# Editing the portfolio website

The public site is built from the `docs/` folder and hosted on GitHub Pages.

- `content/projects.mjs`: selected-project ordering, the four-project `highlights` map, original digital project copy, and the eight-circuit archive.
- `content/other-side.mjs`: the completed physical game, based on the final presentation.
- `content/controls.mjs`: the AE353 control studies and AE370 thermal-model verification study.
- `content/catbot.mjs`: the co-authored AE353 DP1 controller notebook and saved simulation evidence.
- `CONTENT_REVIEW.md`: report interpretations, attribution constraints, and the October engineering-story review.
- `content/drone.mjs`: the AE353 DP4 drone controller, observer, navigation, saved trial results, and explicit individual contributions.
- `content/structures.mjs`: four AE461 laboratory studies with report-based contribution credit.
- `content/aerodynamics.mjs`: the three AE311 studies and documented individual contributions.
- `scripts/build.mjs`: homepage copy and shared page templates. Uses Node.js built-ins; no packages to install.
- `docs/styles.css`: colors, layout, typography, responsive styles, and print styles.
- `docs/site.js`: accessible filtering of the supporting project collection.
- `docs/assets/`: original portfolio images, presentation photos/diagrams, and figures extracted from the supplied project reports.
- `content/field-tools.mjs`: FieldPlan and FieldMark2 professional software entries, with Talman ownership attribution.
- `content/publication.mjs`: controls report-download visibility. The owner explicitly authorized publishing all six prepared copies.
- `docs/reports/`: seven downloadable reports, with contact details removed where applicable.

Run `node scripts/build.mjs` after editing content or templates. Commit both the source and the generated `docs/` files. Run `node scripts/serve.mjs` for a local preview at `http://127.0.0.1:4173/portfolio/`.

GitHub Pages configuration: deploy from branch `main`, folder `/docs`. A `.nojekyll` file makes this a plain static site. There are no runtime dependencies, analytics scripts, API keys, or sign-in requirements.

Project numbers derive from the selected project list; category badges count only the supporting collection they filter. A project with `listed: false` still gets a case page and sitemap entry; this preserves the earlier Frogger Lite URL while featuring its physical final project. Optional `context`, `roleLabel`, `evidenceNote`, `gallery`, and section `figure` fields support team attribution and multiple original figures. Use `cardFit: 'contain'` for plots to preserve axes and legends.

The `highlights` map supplies the prominent cards' summary, result, evidence qualifier, contribution label, and optional direct report/application link. Their order follows the selected project list. These four cards always remain visible above the category controls, led by the drone obstacle-course controller. The fourteen supporting projects use images above their descriptions under “More engineering work,” including in the default “All other work” view. Their order groups controls, analysis, structures/testing, hardware, then software without separate category sections; the filters remain above the one collection. The flying-wing study leads this supporting collection. Filters apply only to this supporting collection. Image panels reuse the project's source image or existing graphic; report plots retain their axes. The leading selection balances aerospace relevance, physical integration, and developed software; keep simulated results, team work, and beta status explicit. Update `assetVersion` in `scripts/build.mjs` whenever changing shared CSS or JavaScript so returning visitors receive the matching assets.

## Larger images and drone selection

The drone obstacle-course controller leads the four selected projects; the flying-wing study leads the supporting collection. The selected cards retain larger image panels, and supporting projects use images above their descriptions rather than small side thumbnails. Case-study figures retain their earlier 570 px height ceiling and narrower body column, as requested after the homepage enlargement. Plots remain contained so axes and labels are preserved.

`drone-race-simulation.png` is a 1920 × 1080 capture from the actual AE353 PyBullet simulator using the final notebook controller, seed 2812816404, at 12 seconds. It is an illustrative partial run, separate from the archived 100-trial evaluation. The optional avatar billboard is disabled through the simulator setting; physics and course geometry are unchanged. The course simulator, scene, and mesh credits appear on the case page and in the linked code README. Private capture helpers, source hashes, and camera provenance remain under `research/drone-visual-2026-10/` and are excluded from publication. The completion-time histogram remains in the evaluation section alongside the position-error figure. Sections can use `figure` for one image or `figures` for several.

`flying-wing-simulator-model.png` is a 1920 × 1080 render of the original AE353 flying-wing model at its launch pose. The supplied visual elevons and pilot use the course Meshcat transforms in the PyBullet render; the nearby launcher is hidden visually to avoid occlusion. It is a model illustration, not a newly executed controller trial. Original report trajectory and failure plots remain in the evaluation section. Simulator and CC Attribution mesh credits appear in the case page and code README. Private helpers and provenance stay under `research/wing-visual-2026-10/`.

The six `orbital-*.jpg` images are actual browser screenshots of the public beta, captured October 5, 2026, after the owner signed in. They show the goals and schedule questionnaire, program overview and exercise prescriptions, workout logging, and a saved weekly review. Questionnaire captures use default setup choices. No program was generated or rebuilt, no sets were completed, and no review was submitted to produce the images. Account information and connected health traces are outside the captured views. `caseTheme: 'orbital'` applies the app’s navy, cyan, and sans-serif design cues only to its case page. The homepage uses the real overview image in the selected card; other portfolio pages retain their normal theme.

## Current projects

`content/current.mjs` contains three work-in-progress pages, separate from the four selected and fourteen supporting completed projects. The homepage places them after the completed collection and digital-systems archive, with three smaller cards. Status is explicitly a snapshot of October 5, 2026; change the date and stage only when new evidence supports it. The senior-design page leads with the assignment and lifecycle, then brief initial work. Do not describe the preliminary architecture as a built vehicle or a closed design.

Senior design uses the Fall 2026 AE443 Kairos launch-service RFP, Team A SRR/SDR presentation, the October 1 individual status report, and the October 2 local Submission Ready workbook. The ConOps image is the exact image from slide 5 of the `(1)` presentation copy, credited to Maxwell. The lifecycle is RFP → SRR/SDR (current) → PDR → CDR → launch vehicle provider guide. Materials are submitted; the reviewed status report does not establish review completion. The preliminary two-stage methalox/hydrolox concept, four Raptor 3 / one BE-3U, Kennedy launch site, and dimensions are team selections. The RFP targets the 2034 opportunity; workbook notes record instructor approval for an earlier 2033 reference. Do not turn ideal Δv margin or mass reserve into a payload-capability claim.

The vehicle is named **Hyperion**, and the page title is **Hyperion: Senior Design Project**. Its existing `kairos-launch-vehicle.html` URL remains in use. The primary Systems Engineer / Vehicle Integration and secondary GNC / Avionics Integration responsibilities follow the team role assignment and course maturity guide. Completed work is grounded in the September 18 and October 1 status reports; PDR/CDR responsibilities are prospective. Preserve the separate discipline ownership for trajectory/GNC and avionics. The page links to the original Kairos team's public repository, credited as mission context, and the unchanged ten-page course RFP at `docs/references/ae443-launch-service-rfp.pdf`. Optional `contextLinks` place those links below the introduction as well as in the evidence list.

The senior-design page displays the single cohesive `Requirements-Flowdown-2.png` from Downloads, preserved byte-for-byte as `kairos-requirements-flowdown.png`. It includes the complete structure from mission objectives through subsystem performance to individual component areas. The owner requested this image instead of two separate SRR/SDR slide excerpts and instead of the actual requirement statements. Do not add the requirement workbook, searchable baseline, or CSV to the public portfolio. `scripts/current-sections.mjs` renders the lifecycle and checkpoint visualizations. Source inspection and the unpublished detailed-baseline draft remain in private research.

The AE483 page uses the user-supplied motor-impairment proposal and October 23 / November 6 / November 20 planned checkpoints. The actual Ubuntu lab notebooks contain earlier flights, spatial/time alignment, three-axis pendulum inertia estimates, and newer force/moment calibration. Aggregate Kf ≈ 2.38e-6 N per command unit / 35 ms is a lab fit; Km is explicitly provisional (R² ≈ 0.18, cross-axis motion). Lab 5 preparation still has null adopted motor parameters and no saved demonstration. It does not establish completed impaired-motor flight or per-motor identification. The Crazyflie product photograph is extracted from Bitcraze's Rev. 3 Brushless datasheet, with manufacturer attribution. The rig photograph and force comparison come from retained lab evidence. The future no-deck project is distinct from motion-capture reference equipment used in the labs.

The AE460 page briefly covers wind-tunnel pressure calibration, an airfoil-pressure report draft, and turbojet analysis. The hero is the actual supplied MiniLab LabVIEW interface screen saved September 29, not an interface authored by Maxwell. Wind-tunnel probe anomalies, provisional photo angles, pressure-only drag, thermal transients, and estimated ambient conditions remain explicit. Original source plots are reproduced without changing data. The two large apparatus photographs are resized for web delivery with orientation applied and EXIF metadata removed; no scene content is retouched. Private extraction/capture helpers and unrelated school files are excluded from publication.

## Content basis

Descriptions summarize the task and approach; supporting cards also show `outcome` separately. Case-story `sections` receive stable numbered anchors and a generated table of contents. Write deeper stories for projects with meaningful integration, decision-making, or evaluation evidence. Use the source reports to connect goals, consequential decisions, obstacles, outcomes, and concrete demonstrated skills. Keep source-version bookkeeping in the linked code notes and preserve team credit and any unmet targets.

Prefer original simulation scenes, test photographs, apparatus diagrams, or the most informative plot. Caption any diagram adapted from a report explicitly; do not present it as a photograph or an independently built apparatus. Retain plot axes and source conclusions. The October image review adds original report/notebook visuals and two labeled vector diagrams without changing any academic data or report PDF.

The initial page uses the public `m-lutter/portfolio` digital-systems collection and the public `m-lutter/orbital-training` README. Orbital is identified as a deployed beta, not a finished stable release. The pump repository contained only a planning skeleton when reviewed and is not featured. The owner authorized including FieldPlan and FieldMark2 based on the supplied current Python files. The site presents descriptions and links; application source and field inputs stay in the separate project repositories. Talman Consultants, LLC owns the application copyright.

Digital projects retain distinctions between simulated designs, physical builds, and incomplete extensions. The 75-to-40 gate comparison comes from the original 5421 BCD write-up and is not a power or timing measurement. Original project folders are preserved.

The EPROM and Frogger images were copied from working image attachments in their original README files. The BCD image is the original Tinkercad export. Several original local JPEG/MOV files contain only two bytes; they are not linked as usable media.

The biography reflects the owner's September 2026 Job Research context: UIUC aerospace engineering, expected December 2026 graduation, launch-vehicle systems/integration, and GNC/avionics integration. Update the graduation wording when appropriate. Contact uses the owner's requested professional email, `luttermaxwell@gmail.com`, set in `scripts/build.mjs` as `contactEmail`.

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

The AE353 archive contains both completed notebooks and course examples/tutorials. The DP1 notebook credits Maxwell and Luke Phan. Flying-wing and spacecraft notebooks inform implementation descriptions; they are saved development states, not clean rerun records. The site credits course equations and simulation interfaces to the instructors and credits controller studies jointly when individual authorship is not specified. The uploaded archive, standalone course framework, unmodified templates, and private research extraction are excluded from publication. Selected modified project notebooks are published separately as documented below.

## Public project code

`project-code/` contains explicitly selected local source prepared October 5, 2026: the AE353 catbot, flying-wing, and spacecraft notebooks; the AE311 balloon notebook and recovered airfoil export; AE370 implementation/verification notebooks; and the editable EPROM KiCad schematic. Each project folder has a README identifying authorship, source status, dependencies, and the limits of saved evidence. The private provenance manifest stays under `research/course-code-2026-10/` and is excluded from publication. The local Frogger C++ prototype is excluded at the owner's request.

Notebook source cells, markdown, execution counts, and available text outputs are retained; graphical/HTML output formats and widget state are removed. Companion `.py` files contain code cells in order. These files were checked for syntax and source preservation, not rerun as new numerical studies. Preserve the existing distinctions between report results and saved development states. The balloon copy is a hydrogen-model development notebook and the airfoil export has missing execution dependencies. The EPROM addition is design source rather than a programming script. The recovered airfoil folder includes JoshTheEngineer's MIT notice; no blanket license is applied to team and course material.

Optional `codeLink: [label, url]` adds a visible link under the case-study introduction and on a highlighted project card. Resource lists also point to source folders and specific notebooks. Links use public GitHub paths under `project-code/`; the static `/docs` site does not need to duplicate the source files. Existing BCD and Frogger Logisim links stay in their original repository folders. The previously linked external AE370 team repository returned 404 when checked, so the case study now points to the locally retained team notebooks with the original contribution credits.

The October 5 Overleaf archive review identified the complete drone report in `Preparation of Papers for AIAA Technical Journals (2).zip` and a 106-line Python appendix inside the composites report. The drone page uses the seven-page `DP4 Control Design for a Drone Race.pdf`, the notebook with matching saved 95%/73.35 s results, and original notebook figures. The related `mlutter2.py` is a different retained controller version and carries no independent performance claim. The public report removes both author email addresses from page one; all later-page text was checked for preservation. Its appendix credits Maxwell as primary developer of the final drone code while documenting Landon's shared work. The composites Python appendix is credited to the team and documents its missing CSV input time histories. No new numerical experiments were run.

The larger archive is a private source collection; it is not uploaded wholesale. Candidate assessment and extracted TeX remain under `research/overleaf-80-2026-10/`. Resume files, cover letters, templates, study notes, and duplicate drafts are excluded from deployment. Other newly found reports are assessed for future additions rather than converted into new case studies automatically.

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

FieldPlan now uses three actual screenshots from its public Streamlit application, captured September 11, 2026. The map is the homepage and case-study lead image; project setup and route results appear beside the corresponding explanations. The example uses forty randomly placed synthetic HMA/PCC locations within Chicago, with thirty red and ten yellow sites and no green sites. Coordinates were checked against the City of Chicago community-area polygons (dataset `igwz-8jzy`). Three depot-balanced sectors use the app's Talman HQ preset in Westmont as the start and finish, and all three routes are displayed. Work records are fictional; the HQ location is the public app preset. Captions distinguish the displayed route estimates from measured field performance. Preserve the complete map and OpenStreetMap attribution when placing the screenshots. The synthetic workbook remains a local presentation source rather than a website download.

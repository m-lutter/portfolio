// Curated from the three supplied AE353 / AE370 reports. See SITE_EDITING.md.
export const controls = [
  {
    slug: 'flying-wing-control', title: 'LQR landing controller for an unpowered flying wing', name: 'LQR landing controller for an unpowered flying wing',
    category: 'controls', type: 'Flight dynamics & control', status: 'Evaluated in simulation', art: 'plot', cardFit: 'contain',
    context: 'AE353 · Two-person team project', roleLabel: 'Team contribution',
    role: 'Controller design and evaluation reported jointly with Navid Navidzadeh',
    description: 'Designed and evaluated an LQR landing controller with a teammate using supplied aircraft dynamics. Across 4,000 randomized simulations, the controller achieved 87.3% successful landings; failure analysis examined the effect of initial attitude.',
    tags: ['LQR', 'State-space modeling', 'Python', 'SymPy'],
    lead: 'Our two-person team found a trim condition, linearized the supplied flying-wing dynamics, and tuned an LQR controller for elevon-driven landing control. We evaluated 4,000 randomized approaches and analyzed initial-attitude distributions to investigate undershoot, lateral drift, and the limits of the local controller.',
    outcome: '87.3% landing success across 4,000 simulated trials',
    image: 'flying-wing-trajectories.png', imageWidth: 1045, imageHeight: 843,
    caption: 'Simulated trajectories for 20 successful landings in green and 10 failed landings in red. The dotted outline marks the runway. Report Figure 1, pages 4–5.',
    evidenceNote: 'AE353 DP2 report by Maxwell Lutter and Navid Navidzadeh. Results describe the supplied course simulation framework, not physical flight tests.',
    sections: [
      {title: 'Trim before feedback', paragraphs: ['Our team used a numerical least-squares search to establish an equilibrium for a ten-state model with two elevon inputs. Two position coordinates were excluded from the trim-state model so the aircraft could be in equilibrium while moving.', 'Jacobian linearization, a controllability check, and closed-loop eigenvalues established the basis for an LQR state-feedback controller. We iteratively tuned state and control weights to balance aircraft response against elevon motion.']},
      {title: 'Evaluate the landing, then investigate the misses', callout: '87.3% success over 4,000 randomized trials exceeded the project’s 85% landing requirement.', paragraphs: ['Evaluation began 150 m before and 15 m above the runway, with randomized initial airspeeds and small air disturbances. Successful and failed paths provided more useful evidence than a single nominal demonstration.', 'Failures included undershoot and lateral drift. Examining their initial yaw, pitch, and roll showed the limits of a controller designed around a local linear model: larger initial attitude offsets were harder to recover from.'], figure: {image: 'flying-wing-failure-attitudes.png', caption: 'Initial yaw, pitch, and roll distributions among failed landings, used to examine the controller’s operating limits. Report Figure 4, page 6.'}},
      {title: 'Scope & engineering takeaway', paragraphs: ['The reported result applies to the tested simulation conditions. No physical aircraft test is documented. The project demonstrates a complete control-design loop: operating point, linearization, feedback design, randomized evaluation, and failure analysis.']}
    ],
    resources: [['Full project report · 6 pages', '../reports/flying-wing-control.pdf', 'PDF']]
  },
  {
    slug: 'spacecraft-attitude', title: 'Spacecraft reaction-wheel control with star-based attitude estimation', name: 'Spacecraft reaction-wheel control with star-based attitude estimation',
    category: 'controls', type: 'Spacecraft control', status: 'Simulation · target unmet', art: 'plot', cardFit: 'contain',
    context: 'AE353 · Two-person team project', roleLabel: 'Team contribution',
    role: 'Controller and observer work reported jointly with Adrian Huang',
    description: 'A two-person study of LQR reaction-wheel control and star-measurement state estimation using supplied spacecraft dynamics. The integrated system achieved 64% mission success across 200 simulations with noise and debris disturbances, below the 80% target.',
    tags: ['LQR', 'State estimation', 'Reaction wheels', 'PyBullet'],
    lead: 'Our two-person team designed an LQR reaction-wheel controller and a dual-LQR observer to keep a spacecraft hatch oriented for an astronaut’s return. Using supplied course dynamics, we evaluated the combined system in Python/PyBullet with noisy star measurements and debris disturbances, documenting its missed mission-success requirement.',
    outcome: '64% mission success over 200 trials; 80% target unmet',
    image: 'spacecraft-yaw-estimation.png', imageWidth: 786, imageHeight: 595,
    caption: 'True and estimated yaw during one 60-second simulation with noisy measurements and disturbances. Report Figure 1, page 6.',
    evidenceNote: 'AE353 DP3 report by Maxwell Lutter and Adrian Huang. The combined controller/observer missed the mission requirement; proposed improvements are future work.',
    sections: [
      {title: 'Control from noisy measurements', paragraphs: ['The task was to keep a spacecraft hatch oriented for an astronaut’s return. Using the supplied course dynamics, our team worked with six attitude and angular-rate states, four reaction wheels in a tetrahedral arrangement, and seven observed stars producing fourteen image-plane measurements.', 'Rank-six controllability and observability checks supported LQR feedback and a dual-LQR observer. We tuned their weights and evaluated the resulting system in a Python/PyBullet simulation with noisy measurements and debris disturbances.']},
      {title: 'Evaluate the complete system', callout: 'The combined controller and observer achieved 64% successful entries in 200 sixty-second trials, below the 80% requirement.', paragraphs: ['The final mission result matters more than the controller’s earlier performance before noisy state estimation was introduced. Observer accuracy and reliable disturbance recovery are related, but they are not interchangeable acceptance criteria.', 'The report illustrates 25 observer trials below a 3.5-degree threshold for 95th-percentile attitude-estimation error. Their relationship to the full 200-trial mission set is not specified, so this figure does not establish that all mission trials passed the observer criterion.'], figure: {image: 'spacecraft-observer-error.png', caption: 'The 25 observer trials illustrated in the report lie below the 3.5-degree error threshold. The report does not specify their relationship to the full 200-trial mission set. Figure 2, page 6.'}},
      {title: 'What the missed target taught us', paragraphs: ['The study exposed an integration problem: gains that worked well in a simpler setting did not preserve mission success when estimation error, disturbances, and limited reaction-wheel torque interacted.', 'More systematic weight selection and tuning that explicitly accounts for actuator limits are possible next steps. The completed work here is the implemented controller/observer and its evaluation, including the unmet target.']}
    ],
    resources: [['Full project report · 7 pages', '../reports/spacecraft-attitude.pdf', 'PDF']]
  },
  {
    slug: 'reentry-thermal-model', title: 'Verifying a reentry heat-conduction model with numerical benchmarks', name: 'Verifying a reentry heat-conduction model with numerical benchmarks',
    category: 'analysis', type: 'Computational heat transfer', status: 'Completed team study', art: 'plot', cardFit: 'contain',
    context: 'AE370 · Five-person team project', roleLabel: 'My contribution',
    role: 'Verification and implementation writing, consistency checks, result interpretation, plotting, and report editing',
    description: 'Contributed verification writing, consistency checks, and result interpretation for a spherical reentry heat-conduction model. The team’s manufactured-solution and analytical benchmarks supported near-second-order convergence in space and time.',
    tags: ['Finite volumes', 'Crank–Nicolson', 'Manufactured solutions', 'Verification'],
    lead: 'I checked and documented the numerical evidence for a team-developed model coupling reentry heating to conduction through a layered spherical heat shield. My work connected the finite-volume and Crank–Nicolson implementation to manufactured-solution convergence, a homogeneous-sphere analytical benchmark, plots, and report explanations.',
    outcome: 'Near-second-order convergence in space and time',
    image: 'tps-spatial-convergence.png', imageWidth: 578, imageHeight: 459,
    caption: 'Manufactured-solution spatial convergence: the reported error decreases by about a factor of four when radial grid spacing is halved. Report Figure 3, page 7.',
    evidenceNote: 'AE370 report by Jeremy Zang, Landon Lopez, Danfeng Ye, Max Lutter, and Kenny Carter. Individual contributions are documented on page 14.',
    sections: [
      {title: 'Connect trajectory, heating, and conduction', paragraphs: ['The team coupled a reduced-order reentry trajectory and Sutton–Graves surface heating to radially symmetric conduction through a layered spherical thermal-protection system.', 'Conservative finite volumes on spherical shells, harmonic interface conductivity, Crank–Nicolson time integration, and a tridiagonal solver formed the conduction model. The trajectory used a point-mass model and RK4 integration.']},
      {title: 'Check the numerical method', callout: 'Observed spatial orders: 1.987–1.999. Observed temporal orders: 1.932–1.995.', paragraphs: ['Manufactured solutions measured convergence against a known temperature field. A separate constant-flux homogeneous-sphere benchmark compared finite-volume cell averages with cell-averaged analytical values.', 'For the reported analytical test at 960 radial cells and a 0.01 s time step, the maximum discrepancy was 0.0161 K. This measures agreement in a specific numerical benchmark; it does not establish that reentry temperature predictions are physically accurate to that tolerance.'], figure: {image: 'tps-analytical-check.png', caption: 'Numerical and cell-averaged analytical temperatures for a homogeneous sphere at 10 s. The reported maximum error in this benchmark is 0.0161 K. Figure 5, page 9.'}},
      {title: 'My contribution', paragraphs: ['I wrote portions of the implementation and numerical-reliability sections, checked methods and derivations against the code and course material, helped interpret verification results and resolve inconsistencies, and contributed to plotting, report structure, and editing.', 'The report credits Danfeng Ye with implementing the conduction solver, verification suite, parameter sweeps, and run scripts. My contribution focused on checking and communicating the technical evidence.']},
      {title: 'Scope of the evidence', paragraphs: ['The convergence and analytical tests support the discretization and numerical implementation. The report also contains unreconciled temperature and run-setting differences between its reentry result sections. Those physical temperature predictions require further review before they can support a material-selection or flight-design claim.']}
    ],
    resources: [['Full project report · 15 pages', '../reports/reentry-thermal-model.pdf', 'PDF'], ['Team source repository', 'https://github.com/Landon-Lopez57/AE370-Project-2', 'GitHub']]
  }
];

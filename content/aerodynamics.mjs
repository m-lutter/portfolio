// Source: the three completed AE311 team reports supplied by the portfolio owner.
export const aerodynamics = [
  {
    slug: 'weather-balloon', title: 'Modeling weather-balloon ascent and comparing hydrogen versus helium', name: 'Modeling weather-balloon ascent and comparing hydrogen versus helium',
    category: 'analysis', type: 'Atmospheric flight modeling', status: 'Completed modeling study', art: 'plot', cardFit: 'contain',
    context: 'AE311 · Technical lead · Three-person team', roleLabel: 'My contribution',
    role: 'Technical lead: mathematical model, Python simulation, plots, and solution documentation',
    description: 'Led a Python balloon-ascent study comparing hydrogen and helium for a 3 kg payload and 35 km altitude target. The report selected hydrogen as the lower gas-cost option, using modeled ascent and burst limits.',
    tags: ['Python', 'Numerical integration', 'Buoyancy', 'Trade studies'],
    lead: 'As technical lead, I developed and documented a Python ascent model that coupled atmospheric conditions, gas expansion, envelope stress, and balloon motion. Our team swept gas mass to compare hydrogen and helium for a 3 kg payload and 35 km altitude requirement, concluding that hydrogen met the modeled objective at a lower gas cost.',
    outcome: 'Report recommendation: 0.43 kg hydrogen as the lower gas-cost option',
    image: 'weather-balloon-trajectory.png', imageWidth: 976, imageHeight: 728,
    caption: 'Reported trajectory from the team’s simplified numerical balloon model. This is a model output, not a measured flight or independently validated prediction. Figure 11, page 15.',
    evidenceNote: 'AE311 Project 1 by Jackson M. Rees, Benjamin R. McDonald, and Maxwell G. Lutter. The report identifies Maxwell as technical lead on pages 1 and 19–20.',
    sections: [
      {title: 'Turn a mission into model requirements', paragraphs: ['The study compared hydrogen and helium for a balloon carrying a 3 kg payload to at least 35 km before burst. The gas species and initial quantity were decision variables; the envelope was modeled as a spherical natural-latex shell.', 'As technical lead, I helped simplify the physical problem, developed and documented the solution, simulated it in Python, and produced plots. The three-person team connected the technical analysis to a gas-cost comparison.']},
      {title: 'Couple the physics, then sweep the design variable', paragraphs: ['The model combined a layered atmosphere, ideal-gas behavior, envelope stress and expansion, buoyancy, gravity, drag, and a material-failure criterion. Euler integration advanced the balloon’s state through the ascent.', 'A gas-mass sweep in 0.01 kg increments generated trial results for the two gases. NumPy, Matplotlib, pandas, and CSV output supported calculation, plotting, and comparison.']},
      {title: 'Reported result & recommendation', callout: 'The report selected 0.43 kg of hydrogen rather than 0.95 kg of helium to meet the modeled altitude objective at lower gas cost.', paragraphs: ['The first successful mass-sweep cases reported 43.12 km for hydrogen and 39.14 km for helium, both above the 35 km requirement. Using the report’s gas-price assumptions, the corresponding gas costs were $2.07 and $90.36. These are the submitted study’s simulation results and historical cost estimates.', 'The recommendation addressed gas cost under the academic model. It did not compare complete launch costs or establish a flight-tested operating configuration. The model assumed a spherical envelope and constant drag coefficient, omitted wind and payload drag, and simplified material failure; the original calculations have not been rerun for this portfolio.']}
    ],
    resources: [['Full project report · 28 pages', '../reports/weather-balloon.pdf', 'PDF']]
  },
  {
    slug: 'airfoil-panel-study', title: 'Comparing NACA airfoils with panel methods and XFOIL', name: 'Comparing NACA airfoils with panel methods and XFOIL',
    category: 'analysis', type: 'Aerodynamics & design research', status: 'Completed team study', art: 'plot', cardFit: 'contain',
    context: 'AE311 · Real-world problem lead · Three-person team', roleLabel: 'My contribution',
    role: 'Glider design research, tradeoff framing, airfoil-selection context, and report coauthorship',
    description: 'Led glider design research for a team study comparing four NACA airfoils at four angles of attack. Connected airfoil-selection tradeoffs to panel-method lift and pressure results and XFOIL pressure comparisons.',
    tags: ['Design research', 'Panel methods', 'NACA airfoils', 'XFOIL'],
    lead: 'I led the glider design research and tradeoff framing for a three-person airfoil study. The team compared camber, thickness, and angle of attack across sixteen cases using a source/vortex panel method and XFOIL pressure distributions; my contribution connected the analysis to airfoil and wing-configuration choices.',
    outcome: '4 airfoil sections × 4 angles of attack, with XFOIL comparisons',
    image: 'airfoil-panel-xfoil-comparison.png', imageWidth: 1447, imageHeight: 1091,
    caption: 'Panel-method and XFOIL pressure distributions for NACA 6406, reproduced from the team’s comparison. Figure 20, page 22.',
    evidenceNote: 'AE311 Project 2 by Benjamin R. McDonald, Jackson M. Rees, and Maxwell G. Lutter. Maxwell’s research role is documented on pages 1, 25, and 28.',
    sections: [
      {title: 'Start with the design context', paragraphs: ['I led the real-world research for the three-person study, surveying glider history, modern designs, and tradeoffs in airfoil shape, aspect ratio, and wing configuration. That work helped connect practical design questions to the team’s numerical investigation.', 'The technical study compared NACA 0006, 0012, 6406, and 6412 at −3°, 0°, 3°, and 6° incidence: sixteen tabulated cases spanning changes in camber and thickness.']},
      {title: 'Compare pressure and lift', paragraphs: ['The team used a combined source/vortex panel method with impermeability and Kutta boundary conditions. Surface pressure and circulation provided two routes to lift, while XFOIL pressure distributions supplied a comparison reference.', 'The Python solver was adapted from JoshTheEngineer, as credited in the report. Jackson Rees held the technical-lead role and implemented the solver; my contribution was the design research and its connection to the analysis.'], figure: {image: 'airfoil-pressure-vectors.png', caption: 'Pressure-coefficient vectors for NACA 6406 from the team’s panel-method study. Figure 19, page 22.'}},
      {title: 'Results & design interpretation', callout: 'NACA 6412 produced the highest lift coefficient among the four airfoils at the tested angles.', paragraphs: ['The report found that camber and thickness affected lift and the pressure distribution. Cambered sections produced positive lift at zero incidence, while symmetric sections were approximately zero. For NACA 6412, the reported lift coefficient at zero degrees was about 0.729.', 'The result supports the report’s comparison of the tested geometries. The steady, inviscid, attached two-dimensional model does not predict stall, viscous drag, or complete-aircraft glide performance, so highest modeled lift is a narrower result than best overall glider performance.']}
    ],
    resources: [['Full project report · 31 pages', '../reports/airfoil-panel-study.pdf', 'PDF']]
  },
  {
    slug: 'finite-wing-study', title: 'Comparing finite-wing planforms, aspect ratio, and geometric twist', name: 'Comparing finite-wing planforms, aspect ratio, and geometric twist',
    category: 'analysis', type: 'Aerodynamic design trades', status: 'Preliminary design study', art: 'plot', cardFit: 'contain',
    context: 'AE311 · Team lead · Three-person team', roleLabel: 'My contribution',
    role: 'Team coordination, investigation scope, plot digitization, and technical documentation',
    description: 'Led a three-person lifting-line study under a 12 m span limit. Coordinated the investigation and supported documentation of the preliminary recommendation: an 11 m span, 0.4 taper ratio, and no geometric twist.',
    tags: ['Team leadership', 'Lifting-line theory', 'Python / Jupyter', 'Design trades'],
    lead: 'As team lead, I coordinated a lifting-line investigation of lift, induced drag, and span efficiency for a hypothetical recreational aircraft. I supported plot digitization and technical documentation as the team compared four planforms, aspect-ratio sweeps, and ±2° twist cases to recommend preliminary geometry within a 12 m span limit.',
    outcome: 'Recommended 11 m span, 0.4 taper ratio, and no geometric twist',
    image: 'wing-planform-drag-polars.png', imageWidth: 1458, imageHeight: 1161,
    caption: 'Modeled lift and induced drag for four planforms at 11 m span. These configurations also differ in aspect ratio, so this comparison does not isolate planform alone. Figure 13, page 23.',
    evidenceNote: 'AE311 Project 3 by Maxwell G. Lutter, Benjamin R. McDonald, and Jackson M. Rees. Maxwell’s team-lead and support contributions are documented on pages 1, 27, and 29.',
    sections: [
      {title: 'Frame a constrained decision', paragraphs: ['The scenario was a hypothetical small recreational aircraft with a maximum 12 m wingspan and manufacturing constraints that excluded an elliptical wing. The team compared simpler configurations using preliminary aerodynamic analysis.', 'As team lead and communicator, I coordinated scope, scheduling, and division of work. I also supported plot digitization, LaTeX equations, references, and report preparation, and contributed to discussions connecting the research to the design decision.']},
      {title: 'Explore planform, aspect ratio, and twist', paragraphs: ['The team’s Python/Jupyter model used Prandtl lifting-line theory, a horseshoe-vortex/downwash representation, and Fourier-series circulation to calculate lift, induced drag, and span efficiency.', 'The comparisons covered elliptical, rectangular, and two tapered planforms, along with aspect-ratio sweeps and ±2° geometric-twist cases. Benjamin McDonald was the technical lead responsible for the computational model; the report credits my contribution in coordination, analysis support, and documentation.'], figure: {image: 'wing-twist-drag-polars.png', caption: 'Comparison of ±2° geometric twist on a rectangular wing using the report’s lifting-line model. Figure 14, page 25.'}},
      {title: 'Recommendation & scope', callout: 'An 11 m span, 1 m root chord, 0.4 m tip chord, and no geometric twist.', paragraphs: ['The report favored high aspect ratio and low taper ratio to approach the elliptical reference’s induced-drag performance while simplifying manufacture. An 11 m span left clearance within the 12 m limit. The small benefit of washout on the tested rectangular wing was judged insufficient to justify added manufacturing complexity.', 'The no-twist recommendation for a tapered wing extends that rectangular-wing observation as an explicit assumption in the report. The study used small-angle, attached, inviscid flow; structural sizing, viscous effects, stall, and whole-aircraft behavior remained outside its scope.']}
    ],
    resources: [['Full project report · 30 pages', '../reports/finite-wing-study.pdf', 'PDF']]
  }
];

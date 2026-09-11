// Sources: the supplied AE461 laboratory reports, read from their LaTeX archives.
// Preserve team attribution; only Lab 6 supplies a division of individual work.
const team = 'AE461 · Four-person laboratory team';
const authors = 'Reports by A. Alptekin, E. Bennett, M. Lutter, and S. Konakanchi, as credited in the supplied documents.';

export const structures = [
  {
    slug: 'photoelastic-stress', title: 'Measuring notch stresses with photoelasticity and FEA', name: 'Measuring notch stresses with photoelasticity and FEA',
    category: 'structures', type: 'Experimental stress analysis', status: 'Completed laboratory study', art: 'plot', cardFit: 'contain',
    context: team, roleLabel: 'Team contribution', role: 'Co-authored the team’s experimental stress-analysis report',
    description: 'Compared stress patterns in unnotched, U-notched, and V-notched beams under four-point bending. The team used photoelastic fringes, analytical stress-concentration estimates, and Abaqus results to examine notch effects.',
    tags: ['Photoelasticity', 'Four-point bending', 'Stress concentration', 'Abaqus'],
    lead: 'Our four-person team used a polariscope to visualize bending stresses, calibrated a fringe constant from an unnotched specimen, and compared notched-beam results with analytical approximations and finite-element output. The study connected visible fringe patterns to localized stress at notch tips.',
    outcome: 'Observed notch stress concentrations; U-notch approximation agreed more closely with FEA',
    image: 'photoelastic-u-notch.png', imageWidth: 887, imageHeight: 322,
    caption: 'U-notched specimen under 100 N applied load, with fringe orders and measured locations annotated in the team’s Lab 2 report.',
    evidenceNote: `${authors} Lab 2: Measurement of Stress using Photoelasticity. The report does not divide individual tasks; results are credited to the team.`,
    sections: [
      {title: 'From fringes to stress', paragraphs: ['The experiment placed transparent beams in four-point bending inside a monochromatic dark-field polariscope. Camera images recorded the fringe patterns at several applied loads.', 'Using the unnotched beam as the calibration specimen, the team related fringe order, thickness, and the material fringe constant to stress. Comparing fringe locations through each section revealed how a notch changes the stress distribution.']},
      {title: 'Compare experiment, approximation, and FEA', paragraphs: ['The report gives Abaqus notch-tip compressive stresses of approximately 14.67 MPa for the U-notch and 19.95 MPa for the V-notch. It found closer agreement between the U-notch result and its analytical approximation.', 'The larger V-notch discrepancy was attributed to using an approximate stress-concentration relation outside its stated geometry range. The report therefore treats the approximation’s applicability as part of the comparison, rather than claiming uniform agreement across both notches.'], figure: {image: 'photoelastic-u-notch-fea.png', caption: 'U-notch bending stress contour reproduced from the Abaqus figure included in the team report.'}},
      {title: 'Conclusion & contribution', paragraphs: ['The team concluded that notches concentrate stress near the newly exposed edges, visible through denser fringes and higher inferred stresses. Additional polariscope observations, including a horseshoe specimen, identified peak-stress locations qualitatively.', 'I am a coauthor of the laboratory report. Because it does not assign individual calculations, measurements, or Abaqus work, those activities are presented as team work.']}
    ],
    resources: [['Original U-notch fringe image', '../assets/photoelastic-u-notch.png', 'Report figure'], ['Original U-notch FEA figure', '../assets/photoelastic-u-notch-fea.png', 'Report figure']]
  },
  {
    slug: 'rod-buckling', title: 'Testing how supports, material, and eccentricity affect rod buckling', name: 'Testing how supports, material, and eccentricity affect rod buckling',
    category: 'structures', type: 'Structural stability testing', status: 'Completed laboratory study', art: 'plot', cardFit: 'contain',
    context: team, roleLabel: 'Team contribution', role: 'Co-authored the team’s buckling-test and Euler-theory comparison',
    description: 'Compared measured buckling loads and force–deflection curves with Euler theory. The team examined support conditions, material stiffness, and eccentric loading, including a large fixed–fixed discrepancy attributed to imperfect restraints.',
    tags: ['Euler buckling', 'Force–deflection', 'Boundary conditions', 'Experimental mechanics'],
    lead: 'Our team tested slender rods in compression to investigate how mounting conditions, material stiffness, and load eccentricity affect structural stability. Force–deflection measurements provided a practical comparison with ideal Euler buckling predictions.',
    outcome: 'Material trends followed Euler theory; imperfect restraints affected measured critical loads',
    image: 'rod-buckling-force-deflection.png', imageWidth: 850, imageHeight: 547,
    caption: 'S2 specimen force–deflection curve from the Lab 4 report, showing a load plateau near 850 N.',
    evidenceNote: `${authors} Lab 4: Buckling of Slender Rods. The report provides joint results without an individual task breakdown.`,
    sections: [
      {title: 'Test the boundary conditions', paragraphs: ['The support comparison used similar steel specimens in pinned–pinned, fixed–pinned, and fixed–fixed arrangements. Theoretical critical loads were calculated using the corresponding effective buckling lengths.', 'Measured loads were 500 N, 950 N, and 710 N, compared with predictions of 548.56 N, 1116.75 N, and 2194.26 N. The first two followed the expected increase with restraint, but the fixed–fixed specimen did not. The report attributes this departure to imperfect clamping, alignment, and initial geometry.']},
      {title: 'Separate material and loading effects', paragraphs: ['For equal-geometry, pinned–pinned specimens, the measured buckling load increased from aluminum to brass to copper as Young’s modulus increased. This supported the expected stiffness dependence of Euler buckling.', 'In the eccentric-loading comparison, specimens began bending progressively rather than showing a sharp ideal buckling transition. Greater eccentricity was associated with lower maximum measured load and more gradual loss of stiffness.']},
      {title: 'Conclusion & contribution', paragraphs: ['The experiment demonstrated the usefulness of Euler theory while showing how real restraints and loading imperfections affect measured behavior. The fixed–fixed result is a documented exception to the ideal support trend, not evidence that every mounting case matched theory.', 'I coauthored the report with the laboratory team; the source does not assign individual ownership of the tests or calculations.']}
    ],
    resources: [['Original S2 force–deflection curve', '../assets/rod-buckling-force-deflection.png', 'Report figure']]
  },
  {
    slug: 'beam-modal-testing', title: 'Identifying cantilever vibration modes from impact-hammer tests', name: 'Identifying cantilever vibration modes from impact-hammer tests',
    category: 'structures', type: 'Experimental modal analysis', status: 'Completed laboratory study', art: 'plot', cardFit: 'contain',
    context: team, roleLabel: 'Team contribution', role: 'Co-authored the team’s vibration-testing and modal-analysis report',
    description: 'Identified five cantilever modes from frequency-response measurements at 17 impact locations. The team’s manually identified resonance frequencies agreed with EDM Modal results within 0.4% for every mode.',
    tags: ['Modal analysis', 'Impact hammer', 'Frequency response', 'EDM Modal'],
    lead: 'Our team used shaker excitation and roving impact-hammer measurements to identify cantilever-beam vibration behavior. The impact test connected frequency-response peaks to five natural frequencies and normalized mode shapes, with a comparison against analytical shapes and EDM Modal output.',
    outcome: 'Five impact-test frequencies agreed with EDM Modal within 0.4%',
    image: 'beam-shaker-mode.png', imageWidth: 537, imageHeight: 382,
    caption: 'Second mode observed during the shaker/stroboscope portion of Lab 5. The node annotations are from the original team report; impact-test mode comparisons appear below.',
    evidenceNote: `${authors} Lab 5: Structural Dynamics Experiment. The report does not assign individual measurement or analysis tasks.`,
    sections: [
      {title: 'Identify resonances from frequency response', paragraphs: ['The impact-hammer study used a fixed accelerometer and 17 excitation locations. Resonances were identified from magnitude peaks, imaginary-component extrema, and supporting real-component and phase behavior in the frequency response functions.', 'The reported frequencies were 24.0, 154.5, 428.2, 840.4, and 1383.4 Hz. Extracting and normalizing imaginary amplitudes across the impact locations gave an experimental estimate of each mode shape.']},
      {title: 'Compare identification methods', callout: 'FRF versus EDM Modal frequency differences: 0.29%, 0.39%, 0.20%, 0.25%, and 0.22%.', paragraphs: ['This agreement supported the manual selection of the five resonances. The mode-shape comparisons followed the same general trends, with stronger agreement at lower modes and more visible differences at higher modes.', 'The report also documents a separate shaker/stroboscope sequence at 3.75–213.1 Hz, with a 2.41% average difference from its prelab estimates. Those values belong to the shaker portion and are kept separate from the impact-test frequencies and the EDM comparison.'], figure: {image: 'beam-modal-shapes.png', caption: 'Five normalized mode-shape comparisons from Lab 5: FRF imaginary amplitudes, analytical shapes, and EDM Modal results across 17 impact locations.'}},
      {title: 'Conclusion & contribution', paragraphs: ['The report concludes that the experiment met its objective of identifying natural frequencies and mode shapes. It attributes the small FRF/EDM differences to measurement noise, damping, and finite frequency resolution, and notes that the tip accelerometer affects the measured beam dynamics.', 'I am a coauthor of this team report. The source does not identify which member processed individual FRFs or performed particular measurements.']}
    ],
    resources: [['Original five-mode comparison', '../assets/beam-modal-shapes.png', 'Report figure']]
  },
  {
    slug: 'composite-tensile-testing', title: 'Comparing composite tensile behavior with extensometer and DIC strain', name: 'Comparing composite tensile behavior with extensometer and DIC strain',
    category: 'structures', type: 'Composite materials testing', status: 'Completed laboratory study', art: 'plot', cardFit: 'contain',
    context: team, roleLabel: 'My contribution', role: 'Stress–strain comparisons, specific modulus and strength, apparatus and uncertainty documentation, and manufacturing-quality discussion',
    description: 'Analyzed stress–strain curves and weight-normalized properties for graphite/epoxy tensile specimens. Compared extensometer and DIC strain, documented experimental uncertainty, and connected the response to fiber orientation and manufacturing quality.',
    tags: ['Composite materials', 'Tensile testing', 'Digital image correlation', 'Experimental uncertainty'],
    lead: 'I contributed the stress–strain comparison, specific modulus and specific strength analysis, experimental apparatus description, and uncertainty discussion for a team study of graphite/epoxy coupons. The report connects manufacturing history to tensile behavior at 0°, ±45°, and 90° fiber orientations.',
    outcome: 'Strong orientation dependence, with measured strength and stiffness differing from ideal predictions',
    image: 'composite-stress-strain-0.png', imageWidth: 540, imageHeight: 393,
    caption: 'Original 0° stress–strain comparison from Lab 6, using extensometer and digital image correlation strain measurements.',
    evidenceNote: `${authors} Lab 6: Mechanical Property Testing of Composite Materials. Maxwell’s responsibilities are listed in “Contribution of Individual Group Members.”`,
    sections: [
      {title: 'Connect manufacturing to tensile response', paragraphs: ['The team tested graphite/epoxy coupons with fibers aligned with, transverse to, and at ±45° to the loading direction. Instron load measurements and specimen dimensions gave engineering stress; an extensometer and digital image correlation supplied strain measurements.', 'The report also incorporates the earlier composite-manufacturing work. My contributions there covered manufacturing quality, room temperature and humidity, and cure-cycle history.']},
      {title: 'My analysis and documentation', paragraphs: ['I completed the stress–strain curve section and the specific modulus/specific strength section, comparing properties on a mass-normalized basis. I also documented the apparatus and sources of uncertainty, including specimen thickness, alignment, and DIC image quality and region selection.', 'The report assigns the primary modulus and strength extraction to E. Bennett, the off-axis property and failure-load predictions to A. Alptekin, and laminate engineering constants and modulus comparisons to S. Konakanchi. Those results are credited to the team rather than presented as my sole analysis.'], figure: {image: 'composite-stress-strain-45.png', caption: 'Original ±45° stress–strain comparison included in the team’s report source.'}},
      {title: 'What the tests established', callout: 'The report gives 68.64 GPa modulus and 807.7 MPa ultimate tensile strength for the 0° specimen.', paragraphs: ['The 0° specimen was the stiffest and strongest; the 90° specimen was weakest in tension; the ±45° specimen sustained the largest strain before failure. The report’s specific-property comparison preserves the same directional trends.', 'Quantitative agreement with ideal micromechanics and laminate predictions was limited. The 0° and 90° coupons failed below predicted loads, while the ±45° coupon exceeded its prediction. The report calls the failure model conservative for that tested shear-dominated specimen and discusses manufacturing and measurement uncertainty as possible causes of disagreement.'], figure: {image: 'composite-stress-strain-90.png', caption: 'Original 90° stress–strain comparison from the team report, showing the weaker transverse tensile response.'}}
    ],
    resources: [['0° stress–strain comparison', '../assets/composite-stress-strain-0.png', 'Report figure'], ['±45° stress–strain comparison', '../assets/composite-stress-strain-45.png', 'Report figure'], ['90° stress–strain comparison', '../assets/composite-stress-strain-90.png', 'Report figure']]
  }
];

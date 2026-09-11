// Source: CMGDemo-Team17.ipynb and its saved plots in the supplied controls archive.
export const catbot = {
  slug: 'cat-catching-robot', title: 'Designing state feedback for a balancing cat-catching robot', name: 'Designing state feedback for a balancing cat-catching robot',
  category: 'controls', type: 'Robot feedback control', status: 'Simulated controller', art: 'plot', cardFit: 'contain',
  context: 'AE353 DP1 · Maxwell Lutter & Luke Phan', roleLabel: 'Team contribution', role: 'Co-authored the controller-design and simulation notebook with Luke Phan',
  description: 'Developed a state-feedback controller with Luke Phan for a wheeled robot that balances while catching a falling cat. Explored stabilizing gains, applied torque limits, and examined saved state and torque responses in the course simulator.',
  tags: ['State feedback', 'Eigenvalue analysis', 'Python / SciPy', 'PyBullet'],
  lead: 'With Luke Phan, I developed a controller-design notebook for a wheeled balancing robot in the AE353 simulation environment. The work connects a four-state linear model, feedback-gain selection, bounded wheel-torque commands, and a saved successful cat-catching demonstration.',
  outcome: 'Saved simulation records a successful catch and the robot’s state response',
  image: 'catbot-state-response.png', imageWidth: 1400, imageHeight: 934,
  caption: 'Saved simulation state histories from the team’s state_plots.pdf: wheel position, wheel velocity, body pitch, and pitch rate over 20 seconds.',
  evidenceNote: 'CMGDemo-Team17.ipynb identifies Max Lutter and Luke Phan as authors. It explicitly credits Tim Bretl, Wayne Chang, and the course staff for the equations of motion, and Bretl for the simulation interface.',
  sections: [
    {title: 'Select and implement feedback', paragraphs: ['The notebook explores candidate feedback gains by checking the real parts of the closed-loop eigenvalues. It also evaluates the linear state response with a matrix exponential and compares candidate gain distributions.', 'A Controller class uses measured wheel position and velocity, pitch, and pitch rate to command wheel torque, clipped to ±5 N·m. A selected gain is then exercised in the supplied nonlinear simulation.']},
    {title: 'Read the simulation evidence', paragraphs: ['The saved notebook output reports a successful catch and includes state-history and commanded-versus-applied torque plots. These document a worked demonstration, not a measured catch-success percentage.', 'The notebook describes a display-dependent simulator behavior that hindered automatic gain screening and motivated a manually selected demonstration gain. The saved run is therefore presented at its documented scope rather than as a statistically validated robustness result.']},
    {title: 'Contribution & course framework', paragraphs: ['The controller-design notebook is co-authored by Maxwell Lutter and Luke Phan; it does not assign individual functions to either author. The supplied equations, ae353_catbot interface, and simulation assets are course infrastructure.']}
  ],
  resources: [['Saved robot state histories', '../assets/catbot-state-response.png', 'Notebook figure']]
};

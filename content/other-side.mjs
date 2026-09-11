// Source: The Other Side final presentation, slides 1–18, reviewed September 2026.
export const otherSide = {
  slug: 'the-other-side', title: 'The Other Side: discrete-logic LED game', name: 'The Other Side: discrete-logic LED game',
  category: 'hardware', type: 'Digital systems integration', status: 'Built & demonstrated', art: 'photo',
  context: 'Team project · Maxwell Lutter & Carlos Selvi', roleLabel: 'Team & contribution',
  role: 'Co-authored with Carlos Selvi; digital-logic game design and implementation',
  description: 'Built a physical 4 × 4 RGB LED obstacle-avoidance game with Carlos Selvi. Integrated player-position state machines, obstacle counters, 555 timers, and collision/win logic, with push-button controls and reset.',
  tags: ['Finite state machines', '555 timers', 'Logisim', 'C++ prototyping'],
  lead: 'With Carlos Selvi, developed a C++ gameplay prototype, simulated the digital logic, and built a playable breadboard game. Two position state machines, obstacle counters, and 555 clocks drive a 4 × 4 RGB LED display with collision detection, win indication, and reset.',
  outcome: 'Physical game with bounded movement, win/loss freeze, and reset',
  image: 'other-side-hardware.jpg', imageWidth: 1536, imageHeight: 2048, cardFit: 'cover',
  caption: 'The team’s completed breadboard game and 4 × 4 RGB LED display, from slide 2 of the final presentation.',
  evidenceNote: 'Based on the 18-slide final presentation by Maxwell Lutter and Carlos Selvi. Team results are described collectively; the deck does not assign individual subsystem ownership.',
  sections: [
    {title: 'The system', paragraphs: ['The player moves a blue LED across a 4 × 4 display while red obstacle LEDs move through the middle rows. Reaching the top row produces a win; sharing a position with an obstacle produces a loss. Either condition freezes the game until an asynchronous reset restores its initial state.', 'Two two-bit finite state machines track horizontal and vertical position independently. A decoder maps those four bits to the player’s LED. Ring-counter outputs drive the obstacles, and combinational logic compares the decoded positions.'], figure: {image: 'other-side-block-diagram.png', caption: 'Original system block diagram, slide 4: input, state, timing, display, and termination logic.'}},
    {title: 'Decisions that mattered', paragraphs: ['We replaced a shift-register approach with bounded state machines so the player could not leave the screen. Independent horizontal and vertical state updates also made diagonal movement possible.', 'Sampling directional buttons on the rising edge of a 555 clock limited the player’s speed. The tradeoff was a less intuitive input response: a short press could fall between clock edges and be missed. Separate player and obstacle timers allowed different movement rates.', 'The display and decoder exposed an interface mismatch: the decoder’s active-low outputs had to be inverted to drive the RGB LED board. Collision and win logic then controlled the timers’ supply path through a tri-state buffer, freezing the displayed state.']},
    {title: 'From prototype to implementation', paragraphs: ['A rudimentary C++ demo in Visual Studio helped establish the gameplay and useful clock speeds. Logisim provided a complete logic simulation, with simplified clocks and display behavior. CircuitVerse and Tinkercad supported individual circuit experiments.', 'The final presentation documents the physical circuit, schematic, state assignments, transition logic, and game behavior. This is the built final project; the earlier Frogger Lite study remains available as a separate simulation case.']},
    {title: 'Result & next iteration', callout: 'A physical game with directional and diagonal movement, boundary handling, win/loss indication, freeze, and reset.', paragraphs: ['The team reported completing the planned core behavior. An independently timed second obstacle row and an adjustable difficulty control remained proposed extensions to the physical build. The richer obstacle behavior in simulation should not be confused with those unimplemented hardware additions.']}
  ],
  gallery: [{image: 'other-side-schematic.png', caption: 'Original full-circuit schematic, slide 5. Open the image to inspect the components and connections.'}],
  resources: [
    ['Final presentation · 18 slides', 'https://docs.google.com/presentation/d/1G4IhLfdZ-8-l1hMifEOL0JBLiHnG6s6grLI5HEp1oHA/edit', 'Google Slides'],
    ['Frogger Lite · earlier simulation', 'frogger-fsm.html', 'Case study'],
    ['Original simulation & design notes', 'https://github.com/m-lutter/portfolio/tree/main/Circuit6%3A%20Frogger%20Lite', 'GitHub']
  ]
};

// Portfolio copy. Edit this file, then run: node scripts/build.mjs
// Project claims are grounded in the linked repositories, presentation, and reports.
import { otherSide } from './other-side.mjs';
import { controls } from './controls.mjs';
import { aerodynamics } from './aerodynamics.mjs';
const portfolio = 'https://github.com/m-lutter/portfolio';
export const source = path => `${portfolio}/blob/main/${path.split('/').map(encodeURIComponent).join('/')}`;
export const directory = path => `${portfolio}/tree/main/${encodeURIComponent(path)}`;

const originalFeatured = [
  {
    slug: 'bcd-decoder', number: '01', title: 'Less logic. Same output.', name: '5421 BCD decoder',
    category: 'hardware', type: 'Digital logic', status: 'Designed & simulated', art: 'bcd',
    description: 'A seven-segment decoder optimized through shared Boolean terms, with a C++ check against the original truth table.',
    tags: ['Boolean optimization', 'C++', 'KiCad', 'Tinkercad'],
    lead: 'Turning a four-bit input into a readable digit—with fewer gates and an explicit check that the logic still matches the intended behavior.',
    role: 'Logic design, optimization & simulation', outcome: '40 AND/OR gates in the final design',
    image: 'bcd-circuit.png', caption: 'Original Tinkercad circuit from the digital-systems portfolio.',
    sections: [
      {title:'The problem', paragraphs:['Design a 5421 BCD decoder using only AND, OR, and NOT gates. A four-switch input drives a common-cathode seven-segment display. The design accepts alternate encodings of the same digit and blanks the display for input values of 10 or greater.']},
      {title:'The engineering work', paragraphs:['I started with a truth table and minimum sum-of-products and product-of-sums expressions. Those produced baseline counts of 75 and 87 gates. I then built a prime-implicant table using the Quine–McCluskey method and selected terms that could serve multiple segment outputs.','A C++ program checked the resulting expressions against the original truth table. Shared subexpressions guided the schematic, which I translated into KiCad and then a Tinkercad simulation.']},
      {title:'The result', callout:'75-gate SOP baseline → 40 AND/OR gates in the final circuit.', paragraphs:['The reduction came from looking across all seven outputs for reusable terms. The repository documents the truth table, prime-implicant work, verification code, schematic, and simulated circuit.']},
      {title:'What this demonstrates', bullets:['Converting an input/output requirement into a complete truth table.','Comparing design alternatives using a concrete resource measure.','Checking a simplified implementation against its original specification.']}
    ],
    resources:[['Original design notes',source('Circuit 1: 5421 BCD/readme.md'),'GitHub'],['Verification code',source('Circuit 1: 5421 BCD/5421BCD.cpp'),'C++'],['Circuit schematic',source('Circuit 1: 5421 BCD/schematic.pdf'),'PDF'],['Truth table & optimization',source('Circuit 1: 5421 BCD/TruthTable&QuineMcCluskey.png'),'Figure'],['KiCad source',source('Circuit 1: 5421 BCD/5421BCDml.kicad_sch'),'KiCad']]
  },
  {
    slug: 'orbital-training', number: '02', title: 'Orbital Training', name: 'Orbital Training',
    category:'software',type:'Product engineering',status:'Deployed · public beta',art:'orbital',
    description:'A strength and conditioning planner with deterministic program generation, persistent workout logging, and versioned weekly adaptation.',
    tags:['TypeScript','SvelteKit','PostgreSQL','Cloudflare'],
    lead:'An end-to-end software project that carries real-world constraints from program generation through workout execution and future adaptation.',
    role:'Domain modeling, full-stack development & deployment',outcome:'Production-deployed public beta',
    sections:[
      {title:'The problem',paragraphs:['A useful training plan must account for goals, available days, equipment, baseline ability, and recovery constraints. It also needs to survive ordinary use: incomplete sessions, substitutions, concurrent saves, and changing schedules.']},
      {title:'A deliberate separation of responsibilities',paragraphs:['I built a deterministic, versioned TypeScript programming engine. It produces explicit ready, needs-input, or infeasible outcomes, with policy metadata that makes decisions traceable. SvelteKit handles the interface and HTTP layer, while Supabase Auth and PostgreSQL manage identity and persistent data.','The architecture keeps domain rules separate from routes and persistence. That makes scheduling and adaptation logic easier to reason about and test independently.']},
      {title:'Designing for continuity',bullets:['Completed workout history stays immutable; weekly adaptation changes only future sessions.','Optimistic revisions and a single-flight save path address overlapping workout saves.','Backward-compatible parsing supports earlier saved program versions.','Database policies, bounded payloads, account export, and deletion define operational boundaries.']},
      {title:'Verification & current status',paragraphs:['The public repository includes Vitest checks, Playwright browser and end-to-end tests, and pgTAP database tests. It also documents release checks, migrations, and the separation between application and database validation.','Orbital is a deployed public beta, with continuing product and programming-policy development. The optional native health companion remains experimental and requires physical-device validation before store distribution.'],callout:'A shipped beta demonstrating constraint modeling, persistence, and release engineering.'}
    ],
    resources:[['Open Orbital Training','https://orbital-training.com','Live beta'],['Project overview & architecture','https://github.com/m-lutter/orbital-training','GitHub'],['Domain model','https://github.com/m-lutter/orbital-training/tree/main/src/lib/domain','Source'],['Database verification','https://github.com/m-lutter/orbital-training/tree/main/supabase/tests/database','Tests'],['Application checks','https://github.com/m-lutter/orbital-training/actions','CI']]
  },
  {
    slug:'eprom-display',number:'03',title:'From memory to display.',name:'EPROM display decoder',
    category:'hardware',type:'Digital hardware',status:'Built on a breadboard',art:'eprom',
    description:'An EPROM-based decoder connecting a seven-bit switch input to a two-digit display through programmed, active-low segment outputs.',
    tags:['EPROM','Digital interfaces','Breadboarding'],
    lead:'A physical circuit that turns a programmed lookup table into the signals needed to drive a two-digit seven-segment display.',
    role:'Decoder design, truth table & circuit assembly',outcome:'A documented breadboard implementation',
    image:'eprom-breadboard.jpg',caption:'The original EPROM decoder breadboard, photographed for the portfolio.',
    sections:[
      {title:'The problem',paragraphs:['Connect a seven-bit DIP-switch input to a common-anode, two-digit seven-segment display. The circuit uses an AM27C1024 EPROM to map the input to fourteen segment-control outputs.']},
      {title:'Interface decisions',paragraphs:['The common-anode display requires active-low output logic. I represented each digit as a segment pattern in hexadecimal and used a programmed truth table to define the output for each input.','The switch inputs connect to the seven least-significant address pins. Remaining address pins are grounded, and the two unused data outputs are left unconnected. The published circuit documents the schematic, truth table, component list, and breadboard.']},
      {title:'What this demonstrates',bullets:['Translating a desired display into a stored input/output mapping.','Accounting for active-low logic and component pin assignments.','Connecting a logical design to a physical implementation.']}
    ],
    resources:[['Original circuit notes',source('Circuit 8: EPROM Decoder/readme.md'),'GitHub'],['Schematic','https://github.com/user-attachments/assets/dee7567a-e77d-4661-99bc-7ac90fa3dc31','Figure'],['Programmed truth table','https://github.com/user-attachments/assets/e524ad68-d014-4a1c-b603-0beb05452ab0','Figure'],['Segment encoding','https://github.com/user-attachments/assets/e161b9f5-8774-4f64-8d71-b0cc880c67e4','Figure']]
  },
  {
    slug:'frogger-fsm',number:'04',title:'A game built from logic.',name:'Frogger Lite state machine',
    category:'hardware',type:'Sequential logic',status:'Simulated in Logisim',art:'frogger',
    description:'Player movement, moving obstacles, collision detection, and win logic integrated into a small digital game using finite state machines.',
    tags:['Finite state machines','Logisim','System integration'],
    lead:'A complete game simulation assembled from state machines, counters, decoders, and discrete logic—with each subsystem doing a defined job.',
    role:'State-machine design & subsystem integration',outcome:'Working collision and win logic in simulation',
    image:'frogger-circuit.png',caption:'Original Logisim circuit, including player and obstacle displays, collision logic, and reset.',
    sections:[
      {title:'The problem',paragraphs:['Move a player across a 4 × 4 display while obstacles cross the same logical space. A collision must freeze the game; reaching the top row must register a win. Separate player and obstacle displays represent the two layers in the simulation.']},
      {title:'Breaking the system into parts',paragraphs:['Two identical finite state machines track horizontal and vertical position. Each accepts a pair of directional inputs, holds its value when neither or both are asserted, and prevents movement beyond the display boundary. Binary state assignments feed the display decoder directly.','Ring counters generate moving obstacles. One includes an extra state so the obstacle spends a clock cycle off-screen before returning. The player and obstacle signals then feed collision and win logic, which interrupts the clocks to freeze the game.']},
      {title:'Integration details',bullets:['Asynchronous reset establishes a known initial state across the flip-flops.','Independent obstacle clocks create different movement rates.','Subcircuits separate player state, obstacle generation, display decoding, and game termination.','State diagrams, transition tables, and Karnaugh maps document the movement logic.']},
      {title:'Result & scope',paragraphs:['The published Logisim model includes working player movement, collision detection, and win logic. It demonstrates how individually understandable subsystems combine into a coherent behavior. This case study describes the simulation; the original final-project presentation is linked separately.']}
    ],
    resources:[['Original design notes',source('Circuit6: Frogger Lite/readme.md'),'GitHub'],['Logisim simulation',source('Circuit6: Frogger Lite/2DPlayerMovement.circ'),'Logisim'],['Player state diagram','https://github.com/user-attachments/assets/c1d59f7b-22d4-4de3-bd68-7fe14fceb976','Figure'],['Final-project presentation','https://docs.google.com/presentation/d/1G4IhLfdZ-8-l1hMifEOL0JBLiHnG6s6grLI5HEp1oHA/edit','Slides']]
  }
];

// Keep the earlier Frogger simulation URL available as supporting evidence.
// The built final project takes its place on the homepage.
originalFeatured.find(p => p.slug === 'frogger-fsm').listed = false;
originalFeatured.find(p => p.slug === 'frogger-fsm').resources.unshift(['The Other Side · physical final project', 'the-other-side.html', 'Case study']);
export const featured = [
  controls[0], otherSide, aerodynamics[2], controls[2],
  aerodynamics[1], aerodynamics[0], controls[1], ...originalFeatured
];

export const circuits=[
  ['01','5421 BCD decoder','Combinational','A shared-term Boolean design for a seven-segment display, with C++ verification and a Tinkercad implementation.','Circuit 1: 5421 BCD'],
  ['02','Four-bit adder & display','Hardware','A four-bit adder, BCD decoder, and common-anode display integrated on a breadboard. Building and checking the sections separately helped isolate wiring and component faults. Overflow handling was not completed.','4-Bit adder to 7 segment Common Anode display'],
  ['03','Clock & shift register','Sequential','A 555 timer and four-bit register combine user-controlled movement, initial-state loading, and a partially developed collision/reset mechanism.','Circuit3: Clock-Register'],
  ['04','Four-bit multiplier','Arithmetic','Two unsigned four-bit inputs produce an eight-bit result through addition and multiplexing. Includes a Logisim model and KiCad schematic.','Circuit4: Multiplier'],
  ['05','Counter & matrix decoder','Sequential','A JK-flip-flop counter selects patterns for a 4 × 4 display. The CircuitVerse model handles the display’s alternating draw and clear behavior.','Circuit5: Counter Decoder'],
  ['06','Frogger Lite','State machines','Player position state machines, obstacle ring counters, and collision/win logic combined in a playable Logisim simulation.','Circuit6: Frogger Lite'],
  ['07','Bouncing ball','State machines','Separate horizontal and vertical state machines move a point around an 8 × 8 screen. A decoder and demultiplexer map position to the display.','Circuit 7: Bouncing Ball'],
  ['08','EPROM display decoder','Hardware','A programmed AM27C1024 EPROM maps a seven-bit input to active-low outputs for a two-digit seven-segment display.','Circuit 8: EPROM Decoder']
];

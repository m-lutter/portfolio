// Portfolio copy. Edit this file, then run: node scripts/build.mjs
// Project claims are grounded in the linked repositories, presentation, and reports.
import { otherSide } from './other-side.mjs';
import { controls } from './controls.mjs';
import { aerodynamics } from './aerodynamics.mjs';
import { fieldTools } from './field-tools.mjs';
import { structures } from './structures.mjs';
import { catbot } from './catbot.mjs';
import { drone } from './drone.mjs';
const portfolio = 'https://github.com/m-lutter/portfolio';
export const source = path => `${portfolio}/blob/main/${path.split('/').map(encodeURIComponent).join('/')}`;
export const directory = path => `${portfolio}/tree/main/${encodeURIComponent(path)}`;

const originalFeatured = [
  {
    slug: 'bcd-decoder', number: '01', title: 'Optimizing a 5421 BCD display decoder', name: 'Optimizing a 5421 BCD display decoder',
    category: 'hardware', type: 'Digital logic', status: 'Designed & simulated', art: 'circuit', cardFit: 'contain',
    description: 'Reduced a seven-segment decoder from a 75-gate sum-of-products baseline to 40 AND/OR gates by sharing Boolean terms. Checked the simplified logic against its truth table in C++ and simulated the circuit in Tinkercad.',
    tags: ['Boolean optimization', 'C++', 'KiCad', 'Tinkercad'],
    lead: 'Designed and optimized the logic that converts a four-bit 5421 BCD input into a seven-segment digit. Shared Boolean terms reduced the final AND/OR gate count to 40, with C++ truth-table checks and a Tinkercad circuit simulation.',
    role: 'Logic design, optimization & simulation', outcome: '40 AND/OR gates in the final design',
    codeLink: ['View verification code', source('Circuit 1: 5421 BCD/5421BCD.cpp')],
    image: 'bcd-circuit.png', caption: 'Original Tinkercad circuit from the digital-systems portfolio.',
    sections: [
      {title:'The problem', paragraphs:['Design a 5421 BCD decoder using only AND, OR, and NOT gates. A four-switch input drives a common-cathode seven-segment display. The design accepts alternate encodings of the same digit and blanks the display for input values of 10 or greater.']},
      {title:'Design decision: optimize across outputs', paragraphs:['Minimizing each segment separately leaves opportunities for sharing unused. I first established complete truth-table behavior, including alternate digit encodings and the blanking requirement. Minimum sum-of-products and product-of-sums expressions gave baselines of 75 and 87 gates.','I then built a prime-implicant table using the Quine–McCluskey method and selected terms that could serve several segment outputs. This made gate count a system-level design decision rather than seven independent simplifications.']},
      {title:'Check the simpler circuit against the specification', paragraphs:['A C++ program checked the resulting expressions against the original truth table. That comparison protects the required display behavior while changing the implementation. I translated the shared terms into a KiCad schematic and a Tinkercad circuit simulation, connecting the Boolean design to a component-level model.']},
      {title:'The result', callout:'75-gate SOP baseline → 40 AND/OR gates in the final circuit.', paragraphs:['The reduction came from looking across all seven outputs for reusable terms. The repository documents the truth table, prime-implicant work, verification code, schematic, and simulated circuit.']},
      {title:'What this demonstrates', bullets:['Converting an input/output requirement into a complete truth table.','Comparing design alternatives using a concrete resource measure.','Checking a simplified implementation against its original specification.']}
    ],
    resources:[['Original design notes',source('Circuit 1: 5421 BCD/readme.md'),'GitHub'],['Verification code',source('Circuit 1: 5421 BCD/5421BCD.cpp'),'C++'],['Circuit schematic',source('Circuit 1: 5421 BCD/schematic.pdf'),'PDF'],['Truth table & optimization',source('Circuit 1: 5421 BCD/TruthTable&QuineMcCluskey.png'),'Figure'],['KiCad source',source('Circuit 1: 5421 BCD/5421BCDml.kicad_sch'),'KiCad']]
  },
  {
    slug: 'orbital-training', number: '02', title: 'Orbital Training: adaptive workout planning app', name: 'Orbital Training: adaptive workout planning app',
    category:'software',type:'Product engineering',status:'Deployed · public beta',art:'orbital',cardFit:'contain',caseTheme:'orbital',
    description:'Built and deployed a training-planning app from a deterministic rule engine through workout logging and weekly adaptation. Versioned policies, immutable completed history, and concurrency-aware saves keep the plan traceable and the record durable.',
    tags:['TypeScript','SvelteKit','PostgreSQL','Cloudflare'],
    lead:'I built Orbital to carry a training plan through the full cycle of scheduling, workout execution, and weekly adjustment. Its main engineering challenge is continuity: constraints must produce an actionable plan, incomplete or changed sessions must save reliably, and later adaptation must preserve what the user actually completed.',
    role:'Domain modeling, full-stack development & deployment',outcome:'Production-deployed public beta',
    image:'orbital-program-overview.jpg',imageWidth:1239,imageHeight:873,
    caption:'Orbital’s live beta presents the training block, weekly schedule, session target, and progression approach before the user opens an individual workout. Captured October 5, 2026.',
    evidenceNote:'Based on the public Orbital Training repository and the authenticated beta interface. App screenshots were captured October 5, 2026. Questionnaire views show default setup choices; the plan, logging, and review views show the user workflow. The case-page colors and typography borrow the app’s design tokens.',
    sections:[
      {title:'Goal: deliver a plan that survives ordinary use',paragraphs:['Goals, equipment, available days, baseline ability, and recovery limits all constrain a plan. A useful application must turn them into dated sessions with specific prescriptions, then handle substitutions, shortened workouts, missed work, and changing schedules.','For the user, this starts with a staged questionnaire: define the training goals, choose available days and session length, and supply the experience and equipment that matter to those goals. Optional expert settings stay behind controls so the initial setup remains manageable.','I developed the domain model, web interface, database, and deployment as one product. The scope reaches beyond generation: onboarding, calendar delivery, workout logging, and weekly review all need to agree about the same program.'],figures:[{image:'orbital-questionnaire-goals.jpg',imageWidth:1239,imageHeight:873,caption:'The questionnaire starts with goals and basic setup. Its section navigation makes the remaining decisions visible; this capture uses the form’s default choices.'},{image:'orbital-questionnaire-schedule.jpg',imageWidth:1239,imageHeight:873,caption:'Scheduling translates days and available time into planning constraints. The user can request assigned days or a flexible workout order; this view shows default setup choices.'}]},
      {title:'Make the programming decisions inspectable',paragraphs:['I separated a pure, deterministic TypeScript programming engine from SvelteKit routes and persistence. Versioned policy metadata makes generation and adaptation decisions traceable, while typed ready, needs-input, and infeasible results prevent impossible constraints from silently producing a plan.','The engine gives one actionable prescription. It emits an implement-rounded load when a suitable baseline supports it and otherwise uses a specific effort target. Cross-program invariants check dates, exercise identity, dose, and progression before persistence. These boundaries make domain decisions easier to test independently of the interface.','The resulting plan lets the user inspect a week’s purpose and open individual workouts before training. Each exercise has sets, repetitions, effort, and a load where supported; exercises without an established load are calibrated within the workout.'],figure:{image:'orbital-program-prescriptions.jpg',imageWidth:1239,imageHeight:873,caption:'The generated-plan view connects the week’s objective to concrete exercise prescriptions and a direct link to the workout. It shows sets, reps, effort, and either a prescribed load or a load to establish in the workout.'}},
      {title:'Connect workout logging to a weekly review',paragraphs:['The workout screen places the prescription beside the fields used to record each set: load, repetitions, effort, and completion. Workout and rest timers support execution, while substitutions and equipment choices handle changes during the session. The weekly review then explains completed work, the overall takeaway, and what happens next.','Completed workout history is immutable. Weekly reviews adjust only future work, with capped changes and a stored policy audit trail. Backward-compatible parsing keeps earlier saved programs usable as the engine evolves.','Workout execution introduced a different problem: rapid autosaves, exits, and completion requests can overlap. Optimistic revisions and a single-flight save path address those races, while server-side finish validation checks the transition from an editable workout to a completed record.','Substitutions also need semantic rules. Switching cardio modality preserves intended duration, effort, and interval structure while removing pace, distance, or heart-rate targets that do not transfer appropriately. This treats a change as a domain operation rather than merely replacing a label.'],figures:[{image:'orbital-workout-logging.jpg',imageWidth:1239,imageHeight:873,caption:'Set-by-set workout logging keeps the planned dose, plate display, rest target, and actual-entry fields together. The screenshot shows the prescribed values before any sets are marked complete.'},{image:'orbital-weekly-review.jpg',imageWidth:1239,imageHeight:873,caption:'A saved weekly review translates the training record into a readable takeaway and next-step guidance. The view shown summarizes completed work; later adaptation preserves that history.'}]},
      {title:'Verify the application and the durable boundary',paragraphs:['SvelteKit runs on Cloudflare Workers; Supabase Auth and PostgreSQL provide identity and persistence. Database functions and row-level-security policies enforce the multi-user boundary, while bounded payloads, versioned migrations, account export, and deletion support operation of the deployed product.','The repository includes Vitest application checks, Playwright browser and end-to-end tests, and pgTAP database tests for security, isolation, lifecycle, and persistence contracts. Release guidance separates application checks from database validation so a passing interface test is not treated as evidence for every layer.']},
      {title:'Outcome and technical competence',paragraphs:['Orbital is a deployed public beta with continued product and programming-policy development. The optional native health companion remains experimental and requires physical-device validation before store distribution.','The project demonstrates turning a constraint-heavy domain into explicit rules, designing state transitions that preserve history, building reliable persistence, and shipping a maintained application. The engineering controls make the implementation inspectable; they do not establish clinical validation or optimal programming for every athlete.'],callout:'A shipped beta spanning domain modeling, full-stack implementation, persistence, and release engineering.'}
    ],
    resources:[['Open Orbital Training','https://orbital-training.com','Live beta'],['Project overview & architecture','https://github.com/m-lutter/orbital-training','GitHub'],['Domain model','https://github.com/m-lutter/orbital-training/tree/main/src/lib/domain','Source'],['Database verification','https://github.com/m-lutter/orbital-training/tree/main/supabase/tests/database','Tests'],['Application checks','https://github.com/m-lutter/orbital-training/actions','CI']]
  },
  {
    slug:'eprom-display',number:'03',title:'EPROM decoder for a two-digit display',name:'EPROM decoder for a two-digit display',
    category:'hardware',type:'Digital hardware',status:'Built on a breadboard',art:'eprom',
    description:'Programmed an AM27C1024 EPROM and assembled a breadboard circuit that converts a seven-bit switch input into a two-digit seven-segment display, using a lookup table of active-low segment outputs.',
    tags:['EPROM','Digital interfaces','Breadboarding'],
    lead:'Designed the segment-encoding lookup table and assembled an EPROM decoder on a breadboard. Seven switch inputs select fourteen active-low outputs to drive a common-anode, two-digit seven-segment display.',
    role:'Decoder design, truth table & circuit assembly',outcome:'A documented breadboard implementation',
    codeLink:['View editable circuit source','https://github.com/m-lutter/portfolio/tree/main/project-code/digital/eprom'],
    image:'eprom-breadboard.jpg',caption:'The original EPROM decoder breadboard, photographed for the portfolio.',
    sections:[
      {title:'Goal: store the display behavior in memory',paragraphs:['The circuit maps a seven-bit DIP-switch input to a two-digit seven-segment display using an AM27C1024 EPROM. A stored lookup table replaces a separate Boolean implementation for each of the fourteen segment outputs.']},
      {title:'Design around polarity and pin assignments',paragraphs:['A common-anode display turns segments on with low outputs. I encoded each digit’s segment pattern in hexadecimal and constructed a truth table with that active-low behavior, so the memory contents agree with the electrical interface.','The seven switch bits connect to the least-significant address pins; unused address pins are grounded to keep the lookup in a defined address range. Two unused data outputs remain unconnected. The schematic and component list make those interface choices inspectable.']},
      {title:'Outcome and technical evidence',paragraphs:['The published notes document the programmed truth table, schematic, and assembled breadboard. Together, they connect the desired display, memory encoding, and physical pinout rather than stopping at a logical mapping.','This is evidence of translating behavior into a lookup table and integrating digital components with different signal conventions. The portfolio shows the documented build; it does not claim an exhaustive hardware test campaign.']}
    ],
    resources:[['Editable KiCad schematic & source notes','https://github.com/m-lutter/portfolio/tree/main/project-code/digital/eprom','Circuit source'],['Original circuit notes',source('Circuit 8: EPROM Decoder/readme.md'),'GitHub'],['Schematic','https://github.com/user-attachments/assets/dee7567a-e77d-4661-99bc-7ac90fa3dc31','Figure'],['Programmed truth table','https://github.com/user-attachments/assets/e524ad68-d014-4a1c-b603-0beb05452ab0','Figure'],['Segment encoding','https://github.com/user-attachments/assets/e161b9f5-8774-4f64-8d71-b0cc880c67e4','Figure']]
  },
  {
    slug:'frogger-fsm',number:'04',title:'Frogger Lite: state-machine game simulation',name:'Frogger Lite: state-machine game simulation',
    category:'hardware',type:'Sequential logic',status:'Simulated in Logisim',art:'frogger',
    description:'Built a playable Logisim simulation of a 4 × 4 obstacle-avoidance game. Combined player-position state machines, obstacle ring counters, display decoders, and collision/win logic that freezes the game until reset.',
    tags:['Finite state machines','Logisim','System integration'],
    lead:'Implemented and integrated the digital logic for a 4 × 4 obstacle-avoidance game in Logisim. The simulation includes bounded player movement, independently clocked obstacles, display decoding, collision detection, a win state, and asynchronous reset.',
    role:'State-machine design & subsystem integration',outcome:'Working collision and win logic in simulation',
    codeLink:['View Logisim source',source('Circuit6: Frogger Lite/2DPlayerMovement.circ')],
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
  drone, otherSide, fieldTools[0], originalFeatured[1],
  controls[0], controls[1], catbot,
  controls[2], aerodynamics[0], aerodynamics[2], aerodynamics[1],
  structures[3], structures[2], structures[0], structures[1],
  originalFeatured[0], originalFeatured[2], fieldTools[1], originalFeatured[3]
];

// Four entry points balance aerospace relevance, physical integration, and
// developed applications. Short homepage copy preserves the source-based cases.
export const highlights = {
  'drone-obstacle-course': {
    summary: 'Integrated a state observer, LQR feedback, and collision-avoidance guidance to navigate a drone through checkpoint rings, then automated trials and investigated failures.',
    result: '95% course completion',
    evidence: '100 simulated trials · 73.35 s mean among successful runs',
    contribution: 'Primary developer of final code · team controller study',
    link: ['Read the report', 'reports/drone-obstacle-course.pdf']
  },
  'the-other-side': {
    summary: 'Co-built a playable LED game, resolving movement boundaries, clocked inputs, and display polarity as the logic model became breadboard hardware.',
    result: 'Built & demonstrated',
    evidence: 'Physical hardware · movement, win/loss logic, and reset',
    contribution: 'Team hardware design & integration'
  },
  'fieldplan': {
    summary: 'Turned mixed work lists into a field workflow that reconciles locations and readiness before assigning areas and ordering driving routes.',
    result: 'Public field-planning app',
    evidence: 'Maps, assignments, and route exports · synthetic example shown',
    contribution: 'Developer · Talman Consultants, LLC',
    link: ['Open FieldPlan', 'https://fieldplan.streamlit.app/']
  },
  'orbital-training': {
    summary: 'Built and deployed a constraint-aware training app with traceable programming rules, reliable workout saves, and adaptation that preserves completed history.',
    result: 'Deployed public beta',
    evidence: 'Planning engine → workout logging → weekly adaptation',
    contribution: 'Full-stack development & deployment',
    link: ['Open Orbital', 'https://orbital-training.com']
  }
};

export const circuits=[
  ['01','5421 BCD decoder','Combinational','A shared-term Boolean design for a seven-segment display, with C++ verification and a Tinkercad implementation.','Circuit 1: 5421 BCD'],
  ['02','Four-bit adder & display','Hardware','A four-bit adder, BCD decoder, and common-anode display integrated on a breadboard. Building and checking the sections separately helped isolate wiring and component faults. Overflow handling was not completed.','4-Bit adder to 7 segment Common Anode display'],
  ['03','555 timer and four-bit shift register','Sequential','A 555 timer and four-bit register combine user-controlled movement, initial-state loading, and a partially developed collision/reset mechanism.','Circuit3: Clock-Register'],
  ['04','Four-bit multiplier','Arithmetic','Two unsigned four-bit inputs produce an eight-bit result through addition and multiplexing. Includes a Logisim model and KiCad schematic.','Circuit4: Multiplier'],
  ['05','Counter and decoder for a 4 × 4 LED display','Sequential','A JK-flip-flop counter selects patterns for a 4 × 4 display. The CircuitVerse model handles the display’s alternating draw and clear behavior.','Circuit5: Counter Decoder'],
  ['06','Frogger Lite game simulation','State machines','Player position state machines, obstacle ring counters, and collision/win logic combined in a playable Logisim simulation.','Circuit6: Frogger Lite'],
  ['07','Bouncing-ball controller for an 8 × 8 display','State machines','Separate horizontal and vertical state machines move a point around an 8 × 8 screen. A decoder and demultiplexer map position to the display.','Circuit 7: Bouncing Ball'],
  ['08','EPROM display decoder','Hardware','A programmed AM27C1024 EPROM maps a seven-bit input to active-low outputs for a two-digit seven-segment display.','Circuit 8: EPROM Decoder']
];

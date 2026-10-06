export const currentProjects = [
  {
    slug:'kairos-launch-vehicle',current:true,title:'Designing a two-stage launch vehicle for a Mars-transfer mission',name:'Kairos launch vehicle: requirements and system integration',
    type:'AE443 / Senior design',status:'At the SRR / SDR checkpoint',category:'systems',art:'image',cardFit:'contain',
    description:'Translate a Mars-launch-service RFP into an integrated vehicle concept, mission ConOps, and requirements flowing from customer needs to subsystem design.',
    lead:'Our senior-design team is developing a launch service to send two Kairos spacecraft toward Mars. My work connects the customer mission to vehicle and subsystem requirements, a shared configuration, and the operations sequence that the design must support.',
    context:'University of Illinois Urbana-Champaign · AE443 · Fall 2026 · Team A',
    role:'Systems engineering and vehicle integration, with GNC / avionics integration responsibilities. I developed the requirements architecture and ConOps diagram, reviewed the requirement baseline, investigated reusability and rideshare, and coordinated configuration across disciplines.',
    tags:['Systems engineering','Requirements traceability','Vehicle integration','Architecture trades'],
    outcome:'SRR / SDR materials submitted; preliminary architecture defined. Design closure and verification remain in progress.',
    image:'kairos-launch-conops.png',imageWidth:1774,imageHeight:887,
    caption:'My mission ConOps diagram from the Team A SRR / SDR presentation. It connects ascent, staging, alternative departure strategies, and independent release of Martian and Helios. The departure alternatives remain trades; the illustration is schematic.',
    evidenceNote:'Status as of October 5, 2026. Based on the RFP, submitted SRR / SDR materials, October 1 individual status report, and October 2 requirements-workbook copy. Preliminary values and planned verification are not completed compliance evidence.',
    sections:[
      {title:'Deliver a fixed customer payload to a Mars-bound trajectory',paragraphs:[
        'The RFP treats this as a launch-service acquisition: Martian and Helios must fly together, with a combined customer spacecraft mass of approximately 4,313 kg. The vehicle must achieve a physically feasible Trans-Mars Injection (TMI), then separate both spacecraft independently. Interplanetary cruise, Mars capture, and final mission insertion belong to the spacecraft.',
        'The customer leaves the launch site, staging, propellants, engine cycle, vehicle dimensions, and recovery strategy to the team. We must justify those choices while closing performance, payload interfaces, loads, cost, risk, and the development schedule. The RFP specifies the 2034 opportunity and an 8–11 km²/s² preliminary C₃ sizing range. The working baseline records instructor approval to study an earlier, April 2033 departure; the final window and capability still require confirmation.'
      ]},
      {title:'Mature the design through formal reviews',paragraphs:[
        'We are at the combined System Requirements Review / System Definition Review (SRR / SDR) checkpoint. The submitted package establishes the mission, requirements, operations concept, and preliminary architecture. The October 1 status report records the presentation and review feedback as pending.',
        'PDR must show that the integrated preliminary vehicle closes. CDR must bring the design, interfaces, loads, and verification approach to a more mature definition. The final course deliverable is a customer-facing launch vehicle provider guide, an engineering model, and a technical defense.'
      ],lifecycle:[
        {label:'RFP',detail:'Customer mission and payload interfaces',state:'complete'},
        {label:'SRR / SDR',detail:'Requirements and system architecture',state:'current'},
        {label:'PDR',detail:'Integrated preliminary design closure',state:'future'},
        {label:'CDR',detail:'Mature design and verification planning',state:'future'},
        {label:'Provider guide',detail:'Customer package, model, and defense',state:'future'}
      ]},
      {title:'Initial work: define the vehicle and its operations',paragraphs:[
        'My initial work focused on the requirements architecture, the ConOps diagram, and coordination between vehicle disciplines. I also investigated reusability and rideshare and helped prepare the SRR / SDR material. The ConOps turns the assignment into an operating sequence: liftoff, ascent, staging, TMI, and independent spacecraft separation.',
        'The preliminary concept uses two stages: methane / liquid oxygen with four Raptor 3 engines for the first stage, and hydrogen / liquid oxygen with one BE-3U for the upper stage. The SRR / SDR presentation identifies Kennedy Space Center, a 5.4 m vehicle diameter, a 77.3 m overall height, and a 14 m fairing with vertically stacked spacecraft. These are team design selections that remain subject to maturation.',
        'The reusability and rideshare work examines whether added development cost and complexity would benefit this customer mission. Direct injection, circular parking orbit, and elliptical parking orbit remain in the departure-strategy comparison.',
        'After SRR / SDR, my next work is to incorporate review feedback and coordinate shared design values with mission, propulsion, structures, and simulation contributors. The team still needs a consistent mass budget and demonstrated mission-performance closure before PDR. These initial selections establish a design direction; they are not a completed launch vehicle.'
      ]},
      {title:'Initial work: map the requirements from mission to components',paragraphs:[
        'I defined a trace-down structure that connects the customer mission to launch-vehicle functions, performance, and subsystem responsibilities. The complete diagram shows how that structure reaches the component level across structures and payload, propulsion, avionics, manufacturing, and operations. It provides a shared framework for developing the design and planning verification as the project progresses.'
      ],figure:{image:'kairos-requirements-flowdown.png',imageWidth:1919,imageHeight:1341,caption:'The complete requirement trace-down diagram: mission objectives → mission requirements → vehicle functions and performance → subsystem functions and performance → individual component areas. This is the initial allocation framework for the developing design.'}}
    ],
    resources:[['View the complete ConOps diagram','../assets/kairos-launch-conops.png','Diagram'],['View the complete requirement trace-down diagram','../assets/kairos-requirements-flowdown.png','Diagram']]
  },
  {
    slug:'crazyflie-motor-impairment',current:true,title:'Developing attitude control for a drone with a weakened motor',name:'Robust attitude control under partial motor impairment',
    type:'AE483 / Autonomous systems',status:'Proposal and early development',category:'controls',art:'image',cardFit:'contain',
    description:'Develop an inertial attitude observer, quaternion controller, and revised motor allocation for a Crazyflie with one partially weakened motor; compare attitude error, settling, and saturation.',
    lead:'Aging teaching drones can produce unequal motor output. Our proposed project asks how much partial motor impairment a Crazyflie can tolerate while maintaining stable attitude, and whether revising the motor allocation improves control under the same impairment.',
    context:'University of Illinois Urbana-Champaign · AE483 Autonomous Systems Lab · Fall 2026',
    role:'Team project development and laboratory modeling, calibration, and controller preparation. The final-project observer and quaternion controller are planned team implementations; individual final-project responsibilities are still being established.',
    tags:['Inertial estimation','Quaternion control','Motor allocation','Python / embedded C'],
    outcome:'Project proposed; recorded labs support the model. Impaired-motor control and the final flight evaluation are upcoming.',
    image:'crazyflie-brushless-platform.jpg',imageWidth:1024,imageHeight:1024,
    caption:'Crazyflie 2.1 Brushless, shown in Bitcraze’s Rev. 3 datasheet. Manufacturer platform photograph; it is not a photograph of our project demonstration. The proposed experiment uses onboard inertial sensing without an expansion deck.',
    evidenceNote:'Status as of October 5, 2026. Proposal and checkpoints supplied by the team; laboratory status checked against saved Ubuntu WSL notebooks and recordings. Course starter notebooks and client / firmware interfaces are credited to the AE483 staff.',
    sections:[
      {title:'Test partial impairment with a controlled comparison',paragraphs:[
        'We will apply a small, reversible reduction to one motor command to emulate reduced output. Our team plans to implement its own attitude observer from onboard inertial measurements and a quaternion-based attitude controller. The baseline is the power-distribution matrix from Lecture 6, which maps motor commands to total thrust and body torques.',
        'We will adjust that allocation for the weakened motor while respecting motor-command limits, then compare normal and impaired conditions using peak attitude error, settling time, steady error, and command saturation. The hypothesis is that the revised allocation reduces attitude error under the same impairment. More severe impairment may exceed the available control authority; the project will determine a compensable range rather than assume recovery from complete motor failure.',
        'Time permitting, a secondary study will investigate whether flight data can identify each motor’s thrust and torque coefficients, Kf and Km. This is an optional extension, not a completed capability.'
      ]},
      {title:'Use the course labs to establish the physical model',paragraphs:[
        'Labs 1–2 retain flight recordings, coordinate-frame transformations, and motion-capture alignment work. These checks establish how recorded poses and onboard estimates can be compared during validation. The proposed final controller will use onboard inertial sensing; external motion capture in the labs is a measurement reference.',
        'Lab 3 estimates the assembled drone’s 40 ± 1 g mass and three moments of inertia with a pendulum rig. The approximate propagated inertia uncertainties are substantial—about 54% for x and 51% for y—and the z recording has appreciable cross-axis motion. These limits matter when deciding how much confidence to place in a model-based controller.',
        'Lab 4 contains real force and moment flights, motor geometry, alignment checks, and regression fits. The saved force model estimates Kf ≈ 2.38 × 10⁻⁶ N per command unit with a 35 ms fitted delay and R² ≈ 0.79. The yaw-torque fit has R² ≈ 0.18 and large cross-axis motion, so Km remains provisional. These are aggregate lab coefficients; they do not establish separate coefficients for all four motors.',
        'Lab 5 prepares three controller models: feedback without actuator delay, with delay, and with delay plus integral action. The retained parameters file still lacks adopted motor coefficients, and no final demonstration log is saved there. The prepared models and firmware therefore support the next test step without establishing validated project flight performance.'
      ],figures:[
        {image:'ae483-inertia-rig.jpg',imageWidth:1350,imageHeight:1800,caption:'Our saved Lab 3 x-axis pendulum-rig photograph. Oscillation periods and the pivot-to-center-of-mass distance are used to estimate body inertia.'},
        {image:'ae483-force-calibration.png',imageWidth:986,imageHeight:390,caption:'Saved Lab 4 force-fit comparison from the calibration notebook. Measured thrust is compared with the summed-motor-command model after delay alignment; this is calibration evidence, not an impaired-motor project result.'}
      ]},
      {title:'Advance through three project checkpoints',paragraphs:[
        'The project is in early development. These dates describe planned demonstrations and analyses, not completed results.'
      ],checkpoints:[
        {label:'October 23',detail:'Demonstrate a simulation with an attitude observer and quaternion controller, plus stable physical flight with normal motors.',state:'future'},
        {label:'November 6',detail:'Implement allocation for a weakened motor and simulate several impairment levels.',state:'future'},
        {label:'November 20',detail:'Determine the impairment range the controller can compensate for and compare the agreed performance metrics.',state:'future'}
      ]},
      {title:'Implement on an open flight-control platform',paragraphs:[
        'The local firmware target is Crazyflie 2.1 Brushless. Bitcraze specifies an STM32F405 flight processor, onboard accelerometer and gyroscope, and four brushless motors. This gives us an accessible embedded platform for estimation, feedback control, motor allocation, and synchronized logging.',
        'AE483’s public crazyflie-client repository supplies Python flight and analysis interfaces and starter lab notebooks. The companion course firmware provides the onboard controller integration. The project builds on those course interfaces; its contribution will be the custom observer, quaternion controller, impairment-aware allocation, and measured comparison.'
      ]}
    ],
    resources:[['Course client and starter labs','https://github.com/tbretl/crazyflie-client','GitHub'],['Course firmware','https://github.com/tbretl/crazyflie-firmware','GitHub'],['Crazyflie 2.1 Brushless datasheet','https://www.bitcraze.io/documentation/hardware/crazyflie_2_1_brushless/crazyflie_2_1_brushless-datasheet.pdf','Hardware'],['AE483 course information','https://courses.illinois.edu/schedule/2026/fall/AE/483','Course']]
  },
  {
    slug:'aerodynamics-propulsion-lab',current:true,title:'Measuring wind-tunnel aerodynamics and turbojet performance',name:'Aerodynamics and propulsion laboratory',
    type:'AE460 / Experimental methods',status:'Labs completed; course in progress',category:'analysis',art:'image',cardFit:'contain',
    description:'Use pressure measurements, tuft observations, and a LabVIEW turbojet acquisition system to connect aerodynamic and thermodynamic models with laboratory data.',
    lead:'AE460 combines instrumented experiments with data reduction and checks on the underlying assumptions. The work completed so far covers wind-tunnel calibration, airfoil pressure and stall, and a turbojet operating sequence.',
    context:'University of Illinois Urbana-Champaign · AE460 · Fall 2026',
    role:'Laboratory measurements and analysis of pressure, aerodynamic-force, and turbojet time-history data. Reports, notebooks, and Python processing connect the recorded channels to the physical models.',
    tags:['LabVIEW data acquisition','Pressure instrumentation','Wind-tunnel testing','Python analysis'],
    outcome:'Three laboratory studies documented. The course is ongoing, and some interpretations remain conditional on calibration and experimental assumptions.',
    image:'ae460-turbojet-labview.png',imageWidth:1362,imageHeight:701,
    caption:'The actual MiniLab LabVIEW acquisition screen saved during the September 29 turbojet lab. It displays engine-station temperatures and pressures, speed, thrust, and fuel flow. This pre-start view documents the instrument interface, not an operating-performance result; the interface was supplied with the apparatus.',
    evidenceNote:'Status as of October 5, 2026. Based on the local AE460 datasets, laboratory photographs, wind-tunnel analysis, airfoil report draft, and turbojet report. Laboratory apparatus and acquisition interfaces are course / supplier equipment.',
    sections:[
      {title:'Calibrate the wind tunnel before interpreting airfoil data',paragraphs:[
        'The first lab compares a pressure rake, an Omega differential-pressure transducer, and a Dwyer manometer over twelve motor-speed settings. I reduced the total- and static-pressure channels to dynamic pressure and examined the calibration and instrument differences.',
        'A provisional linear fit has R² ≈ 0.9994, but one static probe shows a persistent anomaly and the manometer has a possible zero offset. The analysis retains all recorded points and separates diagnostic sensitivity checks from the primary fit. A strong fitted trend does not by itself establish instrument accuracy.'
      ],figure:{image:'ae460-wind-tunnel-calibration.png',caption:'Wind-tunnel calibration from the recorded pressure data, including the fit and residual behavior. The anomalous static probe remains in the primary dataset.'}},
      {title:'Connect airfoil pressures with stall observations',paragraphs:[
        'The second lab uses pressure taps across 17 angles of attack and tuft photographs to examine lift, pressure drag, and flow separation. The analysis converts each run to pressure coefficients and integrates a closed, piecewise-linear airfoil contour.',
        'The report draft places the main stall transition between 16° and 18°, with maximum sampled lift coefficient about 1.54 at 16°. Photograph-angle assignments remain provisional, and pressure integration does not include skin-friction drag. Those qualifications keep the plots and observed tufts from being interpreted as a fully validated total-drag measurement.'
      ],figures:[{image:'ae460-airfoil-tufts.jpg',imageWidth:1800,imageHeight:1350,caption:'Original tuft-test photograph from the airfoil lab. The tufts make surface-flow direction visible; the photograph’s precise angle assignment remains provisional.'},{image:'ae460-airfoil-lift.png',caption:'Pressure-integrated sectional lift coefficient from the lab dataset. The sampled lift peak and decrease bracket the reported stall transition.'}]},
      {title:'Read the turbojet through its acquisition channels',paragraphs:[
        'The turbojet lab uses the supplied LabVIEW interface to record station temperatures and pressures, RPM, fuel flow, and thrust. The retained run captures air start, light-off, acceleration, several throttle dwells, return to idle, and shutdown at approximately five samples per second.',
        'The analysis selects operating windows and compares compressor and air-standard cycle efficiencies. Nearly constant RPM does not imply thermal equilibrium: temperatures continue to drift during some windows. An initial compressor-efficiency estimate above 100% is retained as a model / measurement discrepancy rather than treated as valid performance. Ambient pressure is estimated and room temperature assumed because the barometer readings were unavailable.'
      ],figure:{image:'ae460-turbojet-rpm.png',caption:'Recorded turbojet RPM history with the selected averaging intervals. These are stable-RPM windows; the temperature channels show that some thermal transients remain.'}}
    ],
    resources:[['View the LabVIEW acquisition screen','../assets/ae460-turbojet-labview.png','Interface'],['View wind-tunnel calibration','../assets/ae460-wind-tunnel-calibration.png','Plot'],['View airfoil lift measurements','../assets/ae460-airfoil-lift.png','Plot'],['View the turbojet operating sequence','../assets/ae460-turbojet-rpm.png','Plot']]
  }
];

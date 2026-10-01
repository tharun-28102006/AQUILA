# AQUILA — Adaptive Software-Defined Sonar Transmitter Payload
## Revision A | Student / MoES demonstrator | Units: millimetres

This is a transmitter enclosure, not a receiver or hydrophone system. The STEP files are real boundary-representation solids. They can be imported into FreeCAD, Fusion 360, SolidWorks and other STEP-compatible CAD tools. STEP preserves named parts and solids, not the original feature tree. The included CadQuery Python source is the editable parametric master.

## Package structure
- AQUILA_assembly.step: assembled, named multi-part STEP assembly.
- AQUILA_exploded.step: displaced presentation assembly; do not use these positions for manufacture.
- parts/: individual STEP and binary STL exports. STL coordinates are millimetres, in assembly position. Center and orient each independently in your slicer.
- AQUILA_printable_parts.zip: the 11 custom printable parts only.
- AQUILA_engineering.pdf / AQUILA_drawing.svg: basic dimensioned GA drawing and engineering handover, not a released fabrication drawing.
- parameters.csv / parameters.json: current parameter list. The source parameter table P is authoritative; changing the JSON alone does not rebuild geometry.
- source/aquila.py: parametric generator. Requires Python 3.9+ and cadquery==2.5.2, including the OpenCascade runtime and system graphics/font libraries. Edit P and the named zone/port layouts, then regenerate. Derived dimensions update automatically; major envelope changes require a fresh fit review.
- source/create_handover.py: documentation/ZIP generator; requires reportlab.
- validation.json: B-rep validity, selected nominal interference checks, and STEP round-trip checks. This is not a certification or comprehensive tolerance analysis.

## Principal dimensions
Overall connector-tip length 330; cap-face length 316; cylindrical shell length 300. Shell diameter 110; internal bore 102; wall 4. Collar/end-cap diameter 120. Mounting clamp ears extend to 138 overall width. Rail bottom is Z=-69 and collar top is Z=60: total assembly height 129. The 110 mm figure refers to the shell, not the full mounting envelope.

End caps: 8 face thickness, 8 inward sealing lip, nominal lip diameter 101.4. Six 4.5 clearance holes per cap on 110 PCD. Matching 4.6 diameter x 9 deep blind insert pilots in collars; determine final pilot diameter, insertion depth and fastener length from the chosen insert. Do not install generic inserts without a test coupon. 3 mm alignment pins have 3.4 mm sockets and do not share fastener holes.

Radial seal concept: groove 3.2 wide x 1.5 deep, 2.0 nominal O-ring section. Radial lip/bore gap 0.3 gives a nominal 1.8 gland height and approximately 10 percent radial squeeze for the illustrative installed ring. Select actual catalog O-ring ID, stretch, hardness, gland fill and squeeze against supplier guidance; this provisional gland is NOT approved for immersion. No external pressure analysis has been performed.

Tray: 268 x 84 x 3, bottom Z=-20. Integral OD6.4 x 8 standoffs, 3.4 M3 clearance bores, cable channels and tie slots. Two integral body runners support it. Four retention holes at X +/-124, Y +/-40 accept M3 hardware with accessible nuts below the runners; install before boards if necessary. Runner and tray retention fasteners are not modeled. Fit-test runner sliding clearance before installing electronics.

AUV interface: two 220 x 16 x 5 rails at 76 centers. Saddles at X +/-91 (182 spacing); hull mounting slots at X +/-52 (104 spacing). All slots are 18 x 5.5 for M5. Lower saddles bolt to rails through the X +/-91 slots. Two split upper clamps retain the pod using M4 holes at Y +/-61. Use a thin compliant liner; nominal 0.3 radial allowance is illustrative. Final M4 clamp and M5 hull fasteners, nuts, washers and inserts are selected hardware and are not modeled. Check tool access and actual AUV hull geometry.

## Internal assembly and signal orientation
Coordinates: X is the longitudinal axis. Front service end is negative X. Rear output end is positive X. Z points upward. Tray order is sensor interface, FPGA, power regulation, analog TX board. Power is a separate supply branch, not a signal-processing stage.

Signal: Temperature / salinity / turbidity / depth-range sensors -> protected SENSOR INPUT bulkhead -> sensor interface -> MAX 10 FPGA -> DAC -> low-pass filter -> output amplifier -> rear ANALOG OUT. The last three component envelopes are co-located on the rear analog PCB. The rear TRANSDUCER position is a capped future-output reserve, not a receive channel. No actual electrical design, wiring harness or transducer is included.

Unverified PCB placeholders (length along X x width): sensor 28 x 50, FPGA 130 x 80, power 34 x 52, analog 60 x 68; all thickness 1.6. FPGA provision has an assumed 118 x 70 mounting rectangle. These values are design-space reservations, NOT asserted manufacturer dimensions. Standoff patterns are illustrative for all four boards. Component/connector height envelopes, underside solder joints and cable bends are not manufacturer-accurate.

Connector bores: SENSOR INPUT 16.2; DEBUG 12.2; STATUS 8.2; POWER 12.2; ANALOG OUT 12.2; TRANSDUCER 16.2. Front has sensor/debug/status, rear has power/analog/transducer. Use purchased pressure-appropriate bulkheads with manufacturer seals and locking hardware, or approved cable glands. Generic models have protected insert faces, hex mounting shoulders, recesses and reserved internal clearance; they are not functional connector CAD. An exposed USB socket is intentionally not included. Debug programming is through a sealed bulkhead adapter; oscilloscope measurement uses the rear analog feedthrough with a compatible test cable on a dry bench. Keep unused outputs capped.

## Printing and fabrication
The printable ZIP includes body, two caps, tray, two lower saddles, two upper clamps, two rails and the identification plate. PCB placeholders, connectors, O-rings, pins, fasteners and heat spreader are reference parts, not intended for printing. Prefer aluminum for heat spreader and rails. Obtain elastomer seals separately.

Material candidates: PETG, ABS, ASA or nylon after environmental and temperature review. Typical starting point: 0.2 mm layers, 5-6 perimeters and locally solid fastener/seal regions; calibrate extrusion and dimensional tolerances using coupons. Printed material properties are anisotropic. Do not infer strength or watertightness from infill settings.

Print the main tube vertically on a machine supporting a 300 mm tall part; use a brim and sufficient build volume. Internal horizontal runner undersides require removable support and may be awkward to clean. Do not casually split the shell into unsealed halves to fit a smaller printer. Print caps with the outside face on the bed and lip upward; radial grooves may require support/cleanup. Print the tray flat, standoffs upward. Orient split clamps on their axial faces; saddles may need support around the curved seat. Place rails flat. The conformal ID plate may need light support. Exterior collar/cap edges have small fillets, tray/rail/plate plan corners have radii; other edges should be deburred.

Post-machine or lap sealing lands and connector seats. Ream holes as needed. Use inserts according to manufacturer specifications, not printed threads. Printed walls may leak through porosity; coatings and seal treatments do not establish pressure rating. The ID plate is adhesively bonded, with AQUILA / ADAPTIVE SONAR TX / MoES PROTOTYPE / TX PAYLOAD engraved into geometry. Full project title belongs in the drawing and build documentation.

Thermal concept: an aluminum plate beneath the FPGA region and a provisional insulating thermal pad. Confirm where heat-producing components actually sit; never press a pad onto vulnerable solder joints. The present model reserves contact regions; it does not establish a continuous characterized heat path to the shell. A polymer shell is a poor heat conductor. Measure worst-case dissipation and internal temperature and redesign the spreader/shell interface if required. No fan or open ventilation path is included.

## Assembly sequence
1. Print/fabricate and inspect the parts; prove all nominal fits without electronics.
2. Finish seal surfaces, install qualified collar inserts and alignment pins, and clean all swarf.
3. Install purchased bulkheads with their specified seals/torques. Blank the future transducer port.
4. Fit heat spreader and electrically isolating thermal interface after confirming actual board underside clearance.
5. Populate the tray using measured mounting patterns, route/strain-relieve wiring, and keep the analog output lead short.
6. Slide tray onto runners and fit the four retention fasteners. Confirm service access before fixing boards.
7. Lubricate compatible O-rings, insert caps without twisting seals, and tighten six M4 cap fasteners evenly to a validated torque.
8. Attach lower saddles to rails, fit compliant liners and upper clamps, then bolt rails to the hull using M5 hardware.
9. Perform dry electrical and thermal checks. Only pursue controlled leak/pressure testing with appropriate safety precautions and no live electronics inside.

## Replace after measurement
- Real DE10-Lite outline, exact hole centers/diameters, board thickness, bottom components, maximum connector/display/header heights, and programming cable bend radius.
- Custom analog PCB outline/hole pattern; DAC, LPF and amplifier positions; amplifier heatsink requirements; output impedance/connector specification.
- Power board/fuses and sensor board dimensions, creepage/clearance and connector locations.
- Every purchased bulkhead cutout, keying flat, thread length, washer/nut, sealing land and pressure rating; rerun cap ligament and interference checks.
- Cable outside diameters, minimum bend radii and strain-relief space, which are not routed in the current assembly.
- Selected seal and insert dimensions, shrinkage/tolerances of the actual print process, hull slot geometry, mounting fasteners and environmental loads.

## Release limitations
NOT pressure-rated, certified waterproof, electrically validated or field-qualified. No depth rating is assigned. The model is suitable for mechanical layout review and a student demonstration, subject to real-hardware fit confirmation. Finite-element, buckling, fatigue, seal, thermal, buoyancy, corrosion and full tolerance analyses have not been performed. Do not describe this as tested field-deployable hardware or guaranteed compliance with any certification.

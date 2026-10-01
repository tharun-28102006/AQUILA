* AQUILA main run: change the following controls, then Run.
* MODE: 1=sine, 2=LFM, 3=geometric, 4=phase code, 5=forced ZOH of WAVE.
* WAVE selects 1..4 when MODE=5. ZOH=1 samples ALL other modes too.
* WIN: 0=rectangular pulse, 1=FPGA-equivalent Blackman envelope.
.param MODE=2 WAVE=2 ZOH=1 WIN=1
.param FCAR=300k FSTART=200k FEND=400k TPULSE=2m
.param SCALE=1
.include aquila_hardware_parameters.inc

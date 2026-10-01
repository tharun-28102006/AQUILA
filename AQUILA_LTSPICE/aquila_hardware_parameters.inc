* Common hardware values; each test bench supplies its own mode controls.
.param PI_AQ=3.141592653589793 FS=5Meg TS={1/FS}
.param TSTART=20u TSTOP={TSTART+TPULSE+80u} TMAX=10n
.param NSAMP={floor(TPULSE*FS+0.5)}
.param DAC_MID=1.25 DAC_SPAN=2.5 DAC_BITS=16 DAC_PEAK=350m
.param DAC_TAU={100n/ln(1000)}
.param RFILT=1.02k CFILT=220p
.param RG1=10k RF1=1.50k RG2=10k RF2=12.4k
.param RDRVF=806 RDRVG=806 RISO=10 RLOAD=50
.param CCOUPLE=100n RBIAS=100k
.param CODE0=1 CODE1=1 CODE2=-1 CODE3=1 CODE4=-1 CODE5=-1 CODE6=1
.param NCHIPS=7
* Supply choices: DAC unipolar 0..2.5 V span; amplifiers use split rails.
.param VS_OP=2.5 VS_DRV=5 DAC_AVDD=5 DAC_DVDD=1.8 DAC_VLOGIC=1.8
.param DAC_PVDD=5 DAC_PVSS=-2.5
* Baseline settings do NOT model temperature, PCB parasitics or converter losses.

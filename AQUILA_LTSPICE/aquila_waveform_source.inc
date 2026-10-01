* Mathematical FPGA/DAC command, NOT RTL and NOT an analog window circuit.
* Pin order: 1 CMD (absolute requested volts), 2 REF (analog reference).
* The idle command is midscale. External heartbeat forces sample breakpoints.
.func aq_u(t) {t-TSTART}
.func aq_n(t) {floor(max(aq_u(t),0)*FS+1e-9)}
.func aq_s(t) {if((ZOH>0.5)+(MODE==5),aq_n(t)/FS,max(aq_u(t),0))}
.func aq_mode(t) {if(MODE==5,WAVE,MODE)}
.func aq_idx(t) {min(NCHIPS-1,floor(aq_s(t)*NCHIPS/TPULSE))}
.func aq_code(k) {if(k<1,CODE0,if(k<2,CODE1,if(k<3,CODE2,if(k<4,CODE3,if(k<5,CODE4,if(k<6,CODE5,CODE6))))))}
.func aq_x(t) {if((ZOH>0.5)+(MODE==5),min(aq_n(t),NSAMP-1)/max(NSAMP-1,1),min(aq_s(t)/TPULSE,1))}
.func aq_window(t) {if(WIN>0.5,0.42-0.5*cos(2*PI_AQ*aq_x(t))+0.08*cos(4*PI_AQ*aq_x(t)),1)}
.func aq_lfm(s) {2*PI_AQ*(FSTART*s+(FEND-FSTART)*s*s/(2*TPULSE))}
* A tiny denominator floor keeps equal-frequency geometric runs well-defined.
.func aq_geo(s) {if(abs(ln(FEND/FSTART))<1e-9,2*PI_AQ*FSTART*s,2*PI_AQ*FSTART*TPULSE*(exp(ln(FEND/FSTART)*s/TPULSE)-1)/max(abs(ln(FEND/FSTART)),1e-12)*if(FEND>=FSTART,1,-1))}
.func aq_carrier(t) {if(aq_mode(t)==1,sin(2*PI_AQ*FCAR*aq_s(t)),if(aq_mode(t)==2,sin(aq_lfm(aq_s(t))),if(aq_mode(t)==3,sin(aq_geo(aq_s(t))),aq_code(aq_idx(t))*sin(2*PI_AQ*FCAR*aq_s(t)))))}
.func aq_gate(t) {if(aq_u(t)<0,0,if(aq_u(t)>=TPULSE,0,1))}
.subckt AQUILA_WAVEFORM_SOURCE CMD REF
Bcommand CMD REF V={DAC_MID+DAC_PEAK*SCALE*aq_gate(time)*aq_window(time)*aq_carrier(time)}
.ends AQUILA_WAVEFORM_SOURCE

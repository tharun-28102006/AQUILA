* Include once. All paths are relative to the project root.
.include vendor/OPA2835/OPA835.lib
.include models/OPA2835_model.lib
.include models/OPA2684_model.lib
.include models/AD3541R_model.lib
.include aquila_waveform_source.inc
.include aquila_analog_blocks.inc
* AGND is the SPICE reference. DGND is joined through an ideal net-tie sensor.
VAGND AGND 0 0
VGROUND_TIE DGND AGND 0
VOP_P OP_P AGND {VS_OP}
VOP_N OP_N AGND {-VS_OP}
VDRV_P DRV_P AGND {VS_DRV}
VDRV_N DRV_N AGND {-VS_DRV}
VAVDD AVDD AGND {DAC_AVDD}
VDVDD DVDD DGND {DAC_DVDD}
VVLOGIC VLOGIC DGND {DAC_VLOGIC}
VPVDD PVDD AGND {DAC_PVDD}
VPVSS PVSS AGND {DAC_PVSS}
* Local 100 nF at EVERY package/rail, plus one bulk capacitor per rail.
* Separate 20 mohm ESR resistors avoid pretending capacitors are lossless.
RDU1P OP_P du1p 20m
CDU1P du1p AGND 100n
RDU1N OP_N du1n 20m
CDU1N du1n AGND 100n
RDU2P OP_P du2p 20m
CDU2P du2p AGND 100n
RDU2N OP_N du2n 20m
CDU2N du2n AGND 100n
RDU3P DRV_P du3p 20m
CDU3P du3p AGND 100n
RDU3N DRV_N du3n 20m
CDU3N du3n AGND 100n
RDAV AVDD dav 20m
CDAV dav AGND 100n
RDDV DVDD ddv 20m
CDDV ddv DGND 100n
RDLG VLOGIC dlg 20m
CDLG dlg DGND 100n
RDPV PVDD dpv 20m
CDPV dpv AGND 100n
RDPN PVSS dpn 20m
CDPN dpn AGND 100n
RBOPP OP_P bopp 80m
CBOPP bopp AGND 4.7u
RBOPN OP_N bopn 80m
CBOPN bopn AGND 4.7u
RBDRP DRV_P bdrp 80m
CBDRP bdrp AGND 10u
RBDRN DRV_N bdrn 80m
CBDRN bdrn AGND 10u
RBAV AVDD bav 80m
CBAV bav AGND 4.7u
RBDV DVDD bdv 80m
CBDV bdv DGND 4.7u
RBLG VLOGIC blg 80m
CBLG blg DGND 1u
RBPV PVDD bpv 80m
CBPV bpv AGND 4.7u
RBPN PVSS bpn 80m
CBPN bpn AGND 4.7u
* Two OPA2835 packages, one OPA2684 package: include unused channels in Iq.
XU2B AGND spare835 OP_P OP_N spare835 AGND OPA2835_CH
XU3B AGND spare684 DRV_P DRV_N AGND AQUILA_DRIVER
* Behavioral monitors, volts numerically represent indicated SI quantity.
BLOADPOWER P_LOAD_W AGND V={V(V_LOAD,AGND)*V(V_LOAD,AGND)/RLOAD}
BPOWER835 P_OP_W AGND V={-V(OP_P,AGND)*I(VOP_P)-V(OP_N,AGND)*I(VOP_N)}
BPOWER684 P_DRV_PROXY_W AGND V={-V(DRV_P,AGND)*I(VDRV_P)-V(DRV_N,AGND)*I(VDRV_N)}
BSLEW SLEW_V_PER_US AGND V={ddt(V(V_AMP,AGND))*1u}
BHEADROOM HEADROOM_V AGND V={min(V(DRV_P,V_AMP),V(V_AMP,DRV_N))}
.options plotwinsize=0 numdgt=7 reltol=1e-4 abstol=1p vntol=1u

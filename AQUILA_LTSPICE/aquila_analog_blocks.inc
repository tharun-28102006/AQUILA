* Physical Sallen-Key sections; no ideal Laplace filter in the LTspice circuit.
* n1->OUT capacitor is the POSITIVE-feedback capacitor; n2->REF shunt capacitor.
* Model-order pins: IN OUT VP VN REF.
.subckt AQUILA_SK IN OUT VP VN REF params: RF=1.50k RG=10k
R1 IN n1 {RFILT}
R2 n1 n2 {RFILT}
Cfb n1 OUT {CFILT}
Cg n2 REF {CFILT}
Rf OUT neg {RF}
Rg neg REF {RG}
Xop n2 neg VP VN OUT REF OPA2835_CH
.ends AQUILA_SK
* Current-feedback amplifier: retain Rf even for spare/unity configurations.
.subckt AQUILA_DRIVER IN OUT VP VN REF
Rf OUT neg {RDRVF}
Rg neg REF {RDRVG}
Xop IN neg VP VN OUT REF OPA2684_EQ
.ends AQUILA_DRIVER

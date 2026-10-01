* AC drive is injected after the DAC: no sampled-data interpretation of AC.
* Normalize the filter to its own low-frequency resistor-set gain.
.param FILTER_DC={(1+RF1/RG1)*(1+RF2/RG2)}
.meas AC FILTER_DC_GAIN FIND mag(V(V_FILTER)/V(V_I_V)) AT=1k
.meas AC FILTER_F3DB WHEN mag(V(V_FILTER)/V(V_I_V))={FILTER_DC/sqrt(2)} FALL=1
.meas AC F100_DB FIND db(V(V_FILTER)/V(V_I_V)/FILTER_DC) AT=100k
.meas AC F200_DB FIND db(V(V_FILTER)/V(V_I_V)/FILTER_DC) AT=200k
.meas AC F300_DB FIND db(V(V_FILTER)/V(V_I_V)/FILTER_DC) AT=300k
.meas AC F400_DB FIND db(V(V_FILTER)/V(V_I_V)/FILTER_DC) AT=400k
.meas AC F500_DB FIND db(V(V_FILTER)/V(V_I_V)/FILTER_DC) AT=500k
.meas AC F700_DB FIND db(V(V_FILTER)/V(V_I_V)/FILTER_DC) AT=700k
.meas AC IMAGE_4P5M_DB FIND db(V(V_FILTER)/V(V_I_V)/FILTER_DC) AT=4.5Meg
.meas AC IMAGE_4P7M_DB FIND db(V(V_FILTER)/V(V_I_V)/FILTER_DC) AT=4.7Meg
.meas AC IMAGE_5P3M_DB FIND db(V(V_FILTER)/V(V_I_V)/FILTER_DC) AT=5.3Meg
.meas AC CHAIN_100K FIND mag(V(V_LOAD)/V(VIN_DAC)) AT=100k

# Focal-Mechanism
CAP operating package for Focal Mechanism\n
Need: Velocity Model File\n

1.Generate_Weight.sh\n
Generate the weight.dat for waveform\n
Usage: sh Generate_Weight.sh\n

2.Synthetic Waveforms Generation\n
  (1)make_syn_loc.pl(new01)\n
  Generate the synthetic waveforms(lcoal seismogram) in corresponding with the distance in the weight.\n
  Usage: perl make_syn_loc.pl <directory of weight.dat> <velocity model file name> <depth>\n
    (velocity model file is needed to be put in the current directory)\n
  (2)Green_Function_Cycle.sh\n
  Generate the synthetic waveforms for various distances in various depths\n
  Usage: sh Green_Function_Cycle.sh\n

3.CAP_Calculation.sh\n
Preprocessing of the real waveform\n
Usage: sh CAP_Calculation.sh(SAC file is needed to be put in the current directory)\n

4.Transfer.py\n
Components Rotation\n
Usage: \n
cd <current directory of SAC file>\n
pwd\n
python Transfer.py <directory of pwd>\n

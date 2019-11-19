# Focal-Mechanism

CAP operating package for Focal Mechanism  
Need: Velocity Model File

1.Generate_Weight.sh  
Generate the weight.dat for waveform  
Usage: sh Generate_Weight.sh

2.Synthetic Waveforms Generation  
  (1)make_syn_loc.pl(new01)  
  Generate the synthetic waveforms(lcoal seismogram) in corresponding with the distance in the weight.  
  Usage: perl make_syn_loc.pl <directory of weight.dat> <velocity model file name> <depth>  
    (velocity model file is needed to be put in the current directory)  
  (2)Green_Function_Cycle.sh  
  Generate the synthetic waveforms for various distances in various depths  
  Usage: sh Green_Function_Cycle.sh  

3.CAP_Calculation.sh  
Preprocessing of the real waveform  
Usage: sh CAP_Calculation.sh(SAC file is needed to be put in the current directory)  

4.Transfer.py  
Components Rotation  
Usage:   
cd <current directory of SAC file>  
pwd  
python Transfer.py <directory of pwd>  

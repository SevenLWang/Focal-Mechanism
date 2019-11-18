#Remove Mean&Trend 
SAC_DISPLAY_COPYRIGHT=0

for file in *.SAC; do
  sac <<EOF  
  r ${file}  
  rmean  
  rtrend  
  lp c o 1.0 p 2 n 4   
  quit
EOF
done

#Remove Equipment Response
sac> r *.SAC
sac> trans from pol s SAC.PZs to none freq 0.004 0.005 10 12
sac> mul 100
sac> w over

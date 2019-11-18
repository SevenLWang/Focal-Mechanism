# FK canculating for GreenFunction Cycle
for dist in {10..500..1}
do
  for var in {1..50..2}
  do
    fk.pl -MTest_Model/$var/k -N4096/0.1 $dist
  done
done 

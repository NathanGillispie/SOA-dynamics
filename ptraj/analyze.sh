cpptraj < closestwater.ptrajin
python retention_closest.py closestwater.dat retentiontimes_closest.txt
cpptraj < closestwaters.ptrajin
python retention.py closestwaters.dat retentiontimes.txt

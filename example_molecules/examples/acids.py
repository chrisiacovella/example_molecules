import mbuild as mb
from example_molecules import Acid

for i in range(1,15):
  
        acid = Acid(n=i, cap_start=True)
        acid_name = 'acid_n'+ str(i) + '.mol2'
        acid.save(str(acid_name), overwrite=True)
        
        acid2 = Acid(n=i, cap_start=False)
        acid_name2 = 'acid_nc_n'+ str(i) + '.mol2'
        acid2.save(acid_name2, overwrite=True)

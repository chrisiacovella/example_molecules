import mbuild as mb

for i in range(1,15):
    
        alcohol = Alcohol(n=i, cap_start=True)
        alcohol_name = 'alcohol_n'+ str(i) + '.mol2'
        alcohol.save(alcohol_name, overwrite=True)

        alcohol2 = Alcohol(n=i, cap_start=False)
        alcohol_name2 = 'alcohol_nc_n'+ str(i) + '.mol2'
        alcohol2.save(alcohol_name2, overwrite=True)


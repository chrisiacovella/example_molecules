import mbuild as mb

for i in range(1,15):
        alkane = Alkane(n=i, cap_start=True)
        alkane_name = 'alkane_n'+ str(i) + '.mol2'
        alkane.save(alkane_name, overwrite=True)

        alkane2 = Alkane(n=i, cap_start=False)
        alkane_name2 = 'alkane_nc_n'+ str(i) + '.mol2'
        alkane2.save(alkane_name2, overwrite=True)


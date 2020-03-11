"""
Primary function of recipe here
"""

import mbuild as mb
from mbuild.lib.moieties import CH2
from mbuild.lib.moieties import CH3

class OH(mb.Compound):
    def __init__(self):
        super(OH, self).__init__()
        self.add(mb.Particle(name='O', pos=[0.0, 0.0, 0.0]), label='O')
        self.add(mb.Particle(name='H', pos=[0.0, 0.1, 0.0]), label='H')
        self.add_bond((self['O'], self['H']))
        # add the port to the oxygen atom along the [0,-1, 0] direction
        self.add(mb.Port(anchor=self['O'], orientation=[0, -1, 0], separation=0.075), label='down')

class CH4(mb.Compound):
    """A methane. """
    def __init__(self):
        super(CH4, self).__init__()
        mb.load('utils/ch4.pdb', compound=self, relative_to_module=self.__module__,
                    infer_hierarchy=False)
        self.translate(-self[0].pos)  # Move carbon to origin.

class CH3_down(mb.Compound):
    """A CH3 moiety where the available port is labeled 'down'.
        This is done to enable consistent labeling of ports/connections."""
    def __init__(self):
        super(CH3, self).__init__()
        mb.load('utils/ch3.pdb', compound=self, relative_to_module=self.__module__,
                infer_hierarchy=False)
        self.translate(-self[0].pos)  # Move carbon to origin.
        self.add(mb.Port(anchor=self[0], orientation=[-1, 0, 0], separation=0.075), label='down')


class COOH(mb.Compound):
    """A COOH moiety. """
    def __init__(self):
        super(COOH, self).__init__()
        mb.load('utils/cooh.pdb', compound=self, relative_to_module=self.__module__,
                infer_hierarchy=False)
        self.translate(-self[0].pos)  # Move carbon to origin.
        self.add(mb.Port(anchor=self[0], orientation=[-1, 0, 0], separation=0.075), label='down')

class Methanol(mb.Compound):
    """A Methanol Molecule. """
    def __init__(self):
        super(Methanol, self).__init__()
        mb.load('utils/methanol.pdb', compound=self, relative_to_module=self.__module__,
                infer_hierarchy=False)
        self.translate(-self[0].pos)  # Move carbon to origin.



class Backbone(mb.Compound):
    """
    create a linear molecule class of varied length with a cap.

    Parameters
    ----------
    your_argument: int
    n: int, backbone length, default=1
    cap_start: bool, should the start of the molecule be capped with a hydroge
    cap_start_name: str, label of the capping group at the start of the molecule
    cap_start_mol: compound for capping the start of the molecule
    cap_start_port: name of the port
    
    cap_end: bool, should the end of the molecule be capped
    cap_end_name: str, label of the end capping group
    cap_end_mol: compound for capping the end of the molecule
    cap_end_port: name of the port
    """
    def __init__(self, n=1, cap_start_mol=CH3(),
                 cap_start_name= 'methyl_start', cap_start_port = 'up',
                 cap_end_mol = OH(), cap_end_name='OH',
                 cap_end_port= 'down'):
        super(Backbone, self).__init__()
        if n < 1:
            raise ValueError('n must be 1 or more')
        if n == 1:
            cap1 = cap_start_mol
            self.add(cap1, cap_start_name)
            cap2 = cap_end_mol
            self.add(cap2, cap_end_name)
            mb.force_overlap(cap1, cap1[cap_start_port], cap2[cap_end_port])
        if n == 2:
            cap1 = cap_start_mol
            self.add(cap1, cap_start_name)
            chain = CH2()
            self.add(chain, 'chain')
            mb.force_overlap(move_this=chain,
                             from_positions=chain['down'],
                             to_positions=cap1[cap_start_port], )

            cap2 = cap_end_mol
            self.add(cap2, cap_end_name)
            mb.force_overlap(move_this=cap2,
                             from_positions=cap2[cap_end_port],
                             to_positions=chain['up'])
        if n > 2:
            cap1 = cap_start_mol
            self.add(cap1, cap_start_name)
            chain = mb.recipes.Polymer(CH2(), n=n-1, port_labels=('up', 'down'))
            self.add(chain, 'chain')
            mb.force_overlap(move_this=chain,
                             from_positions=chain['down'],
                             to_positions=cap1[cap_start_port])
            cap2 = cap_end_mol
            self.add(cap2, cap_end_name)
            mb.force_overlap(move_this=cap2,
                             from_positions=cap2[cap_end_port],
                             to_positions=chain['up'])



class Alkane(mb.Compound):
    """
        create a linear alkane molecule .
        
        Parameters
        ----------
        your_argument: int
        n: int, total number of carbon atoms, default=1
        cap_start: bool, should the start of the molecule be capped
        """
    def __init__(self, n=1, cap_start=True):
        super(Alkane, self).__init__()
        if n < 1:
            raise ValueError('n must be 1 or more')
        if cap_start:
            #if n == 1, will simply return a a methane molecule
            if n == 1:
                self.add(CH4(), 'methyl_start')
            if n > 1:
                self.add(Backbone(n=n-1, cap_start_mol=CH3(),
                                  cap_start_name= 'methyl_start', cap_start_port = 'up',
                                  cap_end_mol = CH3_down(), cap_end_name='methyl_end',
                                  cap_end_port= 'dow'))
        else:
            #if n == 1, will simply return a a methane molecule,
            #with an available 'down' port.
            #We will label this as 'methyl_start', again for consistency
            #with longer chain molecules.

            if n == 1:
                self.add(CH3_down(), 'methyl_start')
            if n > 1:
                self.add(Backbone(n=n-1, cap_start_mol=CH2(),
                          cap_start_name= 'methyl_start', cap_start_port = 'up',
                          cap_end_mol = CH3_down(), cap_end_name='methyl_end',
                          cap_end_port= 'down'))

class Alcohol(mb.Compound):
    """
        create a linear alcohol molecule .
        
        Parameters
        ----------
        your_argument: int
        n: int, total number of carbon atoms, default=1
        cap_start: bool, should the start of the molecule be capped
        """
    def __init__(self, n=1, cap_start=True):
        super(Alcohol, self).__init__()
        
        if n < 1:
            raise ValueError('n must be 1 or more')
        if cap_start:
           self.add(Backbone(n=n, cap_start_mol=CH3(),
                                  cap_start_name= 'methyl_start', cap_start_port = 'up',
                                  cap_end_mol = OH(), cap_end_name='OH_end',
                                  cap_end_port= 'down'))
        else:
            self.add(Backbone(n=n, cap_start_mol=CH2(),
                              cap_start_name= 'methyl_start', cap_start_port = 'up',
                              cap_end_mol = OH(), cap_end_name='OH_end',
                              cap_end_port= 'down'))

class Acid(mb.Compound):
    """
        create a linear acid molecule, .
        
        Parameters
        ----------
        your_argument: int
        n: int, total number of carbon atoms, default=1
        cap_start: bool, should the start of the molecule be capped
        """
    def __init__(self, n=1, cap_start=True):
        super(Acid, self).__init__()
        if n < 1:
            raise ValueError('n must be 1 or more')
        if cap_start:
            if n ==1:
                self.add(Methanol())
            if n > 1:
                self.add(Backbone(n=n-1, cap_start_mol=CH3(),
                                  cap_start_name= 'methyl_start', cap_start_port = 'up',
                                  cap_end_mol = COOH(), cap_end_name='COOH_end',
                                  cap_end_port= 'down'))
        else:
            if n ==1:
                self.add(COOH())
            if n > 1:
                self.add(Backbone(n=n-1, cap_start_mol=CH2(),
                                  cap_start_name= 'methyl_start', cap_start_port = 'up',
                                  cap_end_mol = COOH(), cap_end_name='COOH_end',
                                  cap_end_port= 'down'))



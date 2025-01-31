import iDEA as idea
import matplotlib.pyplot as plt
import numpy as np

s = idea.system.systems.atom

a1 = idea.methods.interacting.solve(s, k=9,allstates=True)
excitations = [0,1,2,3,4,5,6,7,8,9]
for excitation in excitations:
    a = idea.methods.interacting.solve(s, k=excitation, stopprint=True)
    print(f"Excitation {excitation},  Sum of difference of full wavefunction: {np.sum(abs(a1.allfull[...,excitation])-abs(a.full))}")
    print(f"Excitation {excitation},  Difference of energy:                   {a1.allenergy[excitation]-a.energy}")

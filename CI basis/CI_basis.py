import numpy as np
import iDEA as idea
import matplotlib.pyplot as plt
import pickle
import tqdm

def innerproduct(state1,state2,system1,system2):    
    return abs(np.sum(state1*state2)*system1.dx*system2.dx)

file = open("doublestate.system","rb")
system_a = pickle.load(file)
file.close()
file = open("doublestate.system","rb")
system_b = pickle.load(file)
file.close()

DE_state = idea.state.load_many_body_state("doublestate.state")
system_a.electrons="u"
system_b.electrons="u"
max_excitation = 4

single_states_a = np.zeros((max_excitation+1,300),dtype=np.float32)
single_states_b = np.zeros((max_excitation+1,300),dtype=np.float32)
for i in tqdm.tqdm(range(0,max_excitation+1)):
    single_states_a[i] = idea.methods.interacting.solve(system_a,k=i,stopprint="True").space.real
    single_states_b[i] = idea.methods.interacting.solve(system_b,k=i,stopprint="True").space.real

basis_set = np.zeros((max_excitation+1,max_excitation+1,300,300),dtype=np.float32)
coefficients = np.zeros((max_excitation+1,max_excitation+1),dtype=np.float32)
basis_set_name = np.empty((max_excitation+1,max_excitation+1),dtype=object)
sign = np.sign(DE_state[150,0,155,0])
contructed_state = np.zeros((300,300),dtype=np.float32)
completeness = 0

for i in range(0,max_excitation+1):
    for j in range(0,max_excitation+1):
        basis_set_name[i][j] = f"up {i}, down {j}"
        basis_set[i][j] = (1/np.sqrt(2))*(np.outer(single_states_a[i],single_states_b[j])-np.outer(single_states_b[j],single_states_a[i]))
        #basis_set[i][j] = np.outer(single_states_b[j],single_states_a[i])
        if np.sign(basis_set[i][j][150][155])!=sign:
            basis_set[i][j] = -basis_set[i][j]
        
        coefficients[i][j] = innerproduct(DE_state[:,0,:,0],basis_set[i][j],system_a,system_b)
        
        contructed_state = contructed_state + 0.5*coefficients[i][j]*basis_set[i][j]

        completeness = completeness + 0.5*(coefficients[i][j])**2

flat_coeff = coefficients.flatten()
flat_names = basis_set_name.flatten()
sort_index = np.argsort(flat_coeff)
for i in range(0,(max_excitation+1)**2):
        print(f"Basis state {flat_names[sort_index][i]}: coefficient {flat_coeff[sort_index][i]}, contribution {((flat_coeff[sort_index][i])**2)*100}%")

print(f"{completeness*100}% Complete")

plt.imshow(contructed_state, cmap="seismic", vmax=0.75, vmin=-0.75, extent=[-20, 20, 20, -20], aspect=1)
plt.xlabel("x, position of electron 1 (Bohrs)")
plt.ylabel("x', poisition of electron 2 (Bohrs)")
plt.colorbar()
plt.xlim([-20,20])
plt.ylim([-20,20])
plt.show()
plt.close()

plt.imshow(DE_state[:,0,:,0], cmap="seismic", vmax=0.75, vmin=-0.75, extent=[-20, 20, 20, -20], aspect=1)
plt.xlabel("x, position of electron 1 (Bohrs)")
plt.ylabel("x', poisition of electron 2 (Bohrs)")
plt.colorbar()
plt.xlim([-20,20])
plt.ylim([-20,20])
plt.show()
plt.close()

plt.imshow(DE_state[:,0,:,0]-contructed_state, cmap="seismic", vmax=0.75, vmin=-0.75, extent=[-20, 20, 20, -20], aspect=1)
plt.xlabel("x, position of electron 1 (Bohrs)")
plt.ylabel("x', poisition of electron 2 (Bohrs)")
plt.colorbar()
plt.xlim([-20,20])
plt.ylim([-20,20])
plt.show()
plt.close()

"""
plt.imshow(basis[16], cmap="seismic", vmax=0.75, vmin=-0.75, extent=[-20, 20, 20, -20], aspect=1)
plt.xlabel("x, position of electron 1 (Bohrs)")
plt.ylabel("x', poisition of electron 2 (Bohrs)")
plt.colorbar()
plt.xlim([-20,20])
plt.ylim([-20,20])
plt.show()
plt.close()
"""
import iDEA as idea

atom = idea.system.systems.atom

state = idea.methods.interacting.solve(atom, k=0)

idea.state.save_many_body_state(state,"teststate.state")

test = idea.state.load_many_body_state("teststate.state")

print(test.space.shape)

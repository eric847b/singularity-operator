from groq_singularity import SingularityGroq
sg = SingularityGroq(auto_iter=True)
def evolve(prompt): return sg.call(f'Evolve: {prompt}')
print(evolve('Full Singularity with multi-AI swarm'))
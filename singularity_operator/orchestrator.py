# Orchestrator v0.3.0 - Multi-provider AI routing + HubRuntime metrics live
# Health-driven model selection, cost awareness, proposal persistence

from singularity_operator.groq_wrapper import call_ai

print('Orchestrator v0.3.0 - All AI calls via free provider router')

def route_ai(prompt):
    return call_ai(prompt)  # Auto multi-provider

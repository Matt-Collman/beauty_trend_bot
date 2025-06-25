from agents import Agent, Runner

agent = Agent(name="TestAgent", instructions="You are a helpful assistant.")

result = Runner.run_sync(agent, "Hello, world!")
print(result.final_output)

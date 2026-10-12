# Simulation

Built in weeks 4-5. Plan:

- `strategies.py`: the four procurement strategies (reactive single source, advance procurement, diversified sourcing, reserved extra capacity)
- `run_simulation.py`: Monte Carlo runs for each strategy, demand scenario, and uncertainty level
- `decision_map.py`: averages the runs and draws the 3x3 decision map

Each run records delay in months, total cost, and whether the deadline was met.

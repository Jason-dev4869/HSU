# Example for Resource Allocation Problem
from ortools.linear_solver import pywraplp

def resource_allocation():
    profits = [100, 200, 150]
    resources_required = [50, 70, 80]
    total_resources = 300
    
    solver = pywraplp.Solver.CreateSolver('GLOP')

    x = [solver.IntVar(0.0, solver.infinity(), f'x_{i}') for i in range(len(profits))]

    solver.Add(sum(resources_required[i] * x[i] for i in range(len(profits))) <= total_resources)

    objective = solver.Objective()
    for i in range(len(profits)):
        objective.SetCoefficient(x[i], profits[i])
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Maximum Profit: ', objective.Value())
        for i in range(len(profits)):
            print(f'Resources allocated to project {i}: {x[i].solution_value()}')
    else:
        print('No optimal solution found')

resource_allocation()

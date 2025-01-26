from ortools.linear_solver import pywraplp

def solve_linear_programming():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    if not solver:
        print('Khong the tao solver!')
        return

    x = solver.IntVar(0.0, solver.infinity(), 'x')
    y = solver.IntVar(0.0, solver.infinity(), 'y')

    solver.Maximize(3 * x + 4 * y)
    
    solver.Add(x + 2 * y <= 14)
    solver.Add(3 * x - y >= 0)
    solver.Add(x - y <= 2)

    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print('Giai phap toi uu:')
        print(f'x = {x.solution_value()}')
        print(f'y = {y.solution_value()}')
        print(f'Gia tri cua ham muc tieu = {solver.Objective().Value()}')
    else:
        print('Khong co giai phap toi uu.')

solve_linear_programming()
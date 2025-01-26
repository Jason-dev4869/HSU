from ortools.linear_solver import pywraplp

def solve_coexistence(C):
    # C là ma trận thông tin: C[i][j] = số lượng thức ăn cần cho loài j khi sử dụng nguồn thức ăn i
    solver = pywraplp.Solver.CreateSolver('SCIP')

    if not solver:
        print('Khong the tao solver!')
        return

    # Tạo các biến quyết định cho Toad, Salamander, Caecilian
    x = [solver.IntVar(0.0, 1000.0, f'loai_{i}') for i in range(3)]

    # Hàm mục tiêu: Tối đa hóa sự tồn tại của các loài (tối đa hóa x1 + x2 + x3)
    solver.Maximize(x[0] + x[1] + x[2])

    # Ràng buộc:
    solver.Add(2 * x[0] + 1 * x[1] + 1 * x[2] <= C[0][3])  # Worms
    solver.Add(1 * x[0] + 3 * x[1] + 2 * x[2] <= C[1][3])  # Crickets
    solver.Add(1 * x[0] + 2 * x[1] + 3 * x[2] <= C[2][3])  # Flies

    # Ràng buộc giới hạn số lượng tối đa cho mỗi loài
    solver.Add(x[0] <= C[0][0])  # Max Toad
    solver.Add(x[1] <= C[1][0])  # Max Salamander
    solver.Add(x[2] <= C[2][0])  # Max Caecilian

    # Giải bài toán
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Giai phap toi uu:')
        print(f'Toad: {x[0].solution_value()}')
        print(f'Salamander: {x[1].solution_value()}')
        print(f'Caecilian: {x[2].solution_value()}')
        print(f'Ham muc tieu: {solver.Objective().Value()}')
    else:
        print('Khong co giai phap toi uu.')

C = [
    [1000, 1000, 1000, 1500],
    [1000, 1000, 1000, 3000],
    [1000, 1000, 1000, 5000]
]

solve_coexistence(C)
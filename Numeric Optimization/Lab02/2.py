from ortools.sat.python import cp_model

def project_scheduling():
    jobs = [(0, 4), (1, 3), (2, 2)]
    precedence = [(0, 1), (1, 2)]

    model = cp_model.CpModel()

    start_times = []
    for job_id, duration in jobs:
        start_times.append(model.NewIntVar(0, sum(duration for _, duration in jobs), f'start_{job_id}'))

    for (job_1, job_2) in precedence:
        model.Add(start_times[job_1] + jobs[job_1][1] <= start_times[job_2])

    makespan = model.NewIntVar(0, sum(duration for _, duration in jobs), 'makespan')
    for job_id, duration in jobs:
        model.Add(makespan >= start_times[job_id] + duration)
    
    model.Minimize(makespan)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print(f"Optimal Project Completion Time: {solver.Value(makespan)}")
        for job_id, duration in jobs:
            print(f"Job {job_id} starts at: {solver.Value(start_times[job_id])}")
    else:
        print('No optimal solution found')

project_scheduling()

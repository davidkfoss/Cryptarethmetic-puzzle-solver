from ortools.sat.python import cp_model
def solve_cryptarithmetic_puzzle():
    model = cp_model.CpModel()
    
    base = 10
    
    # Define the variables for the letters
    v = model.NewIntVar(0, base - 1, 'V')
    i = model.NewIntVar(0, base - 1, 'I')
    s = model.NewIntVar(0, base - 1, 'S')
    m = model.NewIntVar(0, base - 1, 'M')
    a = model.NewIntVar(0, base - 1, 'A')
    p = model.NewIntVar(0, base - 1, 'P')
    h = model.NewIntVar(0, base - 1, 'H')
    e = model.NewIntVar(0, base - 1, 'E')
    n = model.NewIntVar(0, base - 1, 'N')
    l = model.NewIntVar(0, base - 1, 'L')
    
    # Define constraints
    model.AddAllDifferent([v, i, s, m, a, p, h, e, n, l])  # All letters must have different values
    
    # Define the equation: VISMA + API + AI + SAAS = HEAVEN
    model.Add(
        v * 10000 + i * 1000 + s * 100 + m * 10 + a +
        a * 100 + p * 10 + i +
        a * 10 + i +
        s * 1000 + a * 100 + a * 10 + s
        == h * 100000 + e * 10000 + a * 1000 + v * 100 + e * 10 + n
    )
    model.Add(m != 2)
    model.Add(a != 1)
    
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter([v, i, s, m, a, p, h, e, n, l])
    solver.parameters.enumerate_all_solutions = True
    
    status = solver.Solve(model, solution_printer)
    
    if status == cp_model.OPTIMAL:
        print(f"Solution found: 31203 = {''.join([str(solution_printer.solution_letters[str(var)]) for var in [3,1,2,0,3]])}")
    else:
        print("No solution found.")

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.solution_letters = {}

    def on_solution_callback(self):
        self.__solution_count += 1
        if self.__solution_count == 1:
            print("Solutions:")
        for var in self.__variables:
            print(f"{var} = {self.Value(var)}", end=", ")
            if self.Value(var) == 3 or self.Value(var) == 1 or self.Value(var) == 2 or self.Value(var) == 0:
                self.solution_letters[str(self.Value(var))] = var
        print()

    def solution_count(self):
        return self.__solution_count

if __name__ == '__main__':
    solve_cryptarithmetic_puzzle()

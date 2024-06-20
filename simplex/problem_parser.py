class ProblemParser:

    def __init__(self, filename=None, str_problem=None):
        self.filename = filename
        self.str_problem = str_problem
        self.lines = []
        self.objective = []
        self.constraints = []
        self.decision_vars = []
        self.problem_type = 0
        self.init()

    def init(self):
        self.lines = self.retrieve_problem_lines()
        self.objective = self.retrieve_objective()
        self.problem_type = self.retrieve_problem_type()
        self.constraints = self.retrieve_constraints()
        self.decision_vars = self.retrieve_decision_vars()

    def retrieve_problem_lines(self):
        # Read the file and split by '\n'
        if self.str_problem != None:
            return self.str_problem.split("\n")
        else:
            with open(self.filename, mode="r", newline="\n") as file:
                self.str_problem = file.read()
                return self.str_problem.split("\n")

    def retrieve_objective(self):
        return self.lines[0]

    def retrieve_constraints(self):
        return self.lines[1:]

    def retrieve_problem_type(self):
        return 1 if self.objective.split()[0].lower() == "max" else -1

    def retrieve_decision_vars(self):
        return [item.split(".")[1] for item in self.objective.split()[1:]]
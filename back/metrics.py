import ast

def non_blanc_lines(code: str) -> int:
    return sum(1 for line in code.split('\n') if line.strip() != '')

def get_variable_names(code_ast: ast.AST) -> list[str]:
    variable_names = []

    class VariableNameExtractor(ast.NodeVisitor):
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                variable_names.append(node.id)
            self.generic_visit(node)

    extractor = VariableNameExtractor()
    extractor.visit(code_ast)
    return variable_names

def average_variable_length(code_ast: ast.AST) -> float:
    variable_names = get_variable_names(code_ast)
    if not variable_names:
        return 0
    total_length = sum(len(name) for name in variable_names)
    average_length = total_length / len(variable_names)
    return average_length

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.func_calls = []
        self.decision_complexity = 0
        self.declaration_statements = 0
        self.executable_statements = 0
        self.arcs = 0
        self.decision_count = 0
        self.decision_spans = []
        self.knot_count = 0
        self.loop_count = 0
        self.exit_count = 0
        self.node_count = 0
        self.nesting_level = 0
        self.max_nesting_level = 0
        self.independent_paths = 0
        self.control_statements = 0
        self.structure_breaches = 0
        self.current_nesting = 0
    
    def visit_FunctionDef(self, node):
        self.declaration_statements += 1
        self.current_nesting += 1
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_Assign(self, node):
        self.declaration_statements += 1
        self.generic_visit(node)
    
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.func_calls.append(node.func.id)
        self.executable_statements += 1
        self.generic_visit(node)
    
    def visit_If(self, node):
        self.decision_complexity += 1
        self.decision_count += 1
        self.executable_statements += 1
        self.control_statements += 1
        self.current_nesting += 1
        self.max_nesting_level = max(self.max_nesting_level, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_For(self, node):
        self.decision_complexity += 1
        self.loop_count += 1
        self.executable_statements += 1
        self.control_statements += 1
        self.current_nesting += 1
        self.max_nesting_level = max(self.max_nesting_level, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_While(self, node):
        self.decision_complexity += 1
        self.loop_count += 1
        self.executable_statements += 1
        self.control_statements += 1
        self.current_nesting += 1
        self.max_nesting_level = max(self.max_nesting_level, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_Expr(self, node):
        self.executable_statements += 1
        self.generic_visit(node)
    
    def visit_Return(self, node):
        self.exit_count += 1
        self.generic_visit(node)
    
    def analyze(self, code_ast):
        self.visit(code_ast)
        
        total_func_calls = len(self.func_calls)
        unique_func_calls = len(set(self.func_calls))
        avg_complexity = self.decision_complexity / total_func_calls if total_func_calls else 0
        
        self.independent_paths = self.decision_complexity + 1
        self.arcs = self.node_count + self.decision_complexity
        
        if self.decision_count > 0:
            avg_decision_span = sum(self.decision_spans) / self.decision_count
        else:
            avg_decision_span = 0

        return {
            "total_func_calls": total_func_calls,
            "unique_func_calls": unique_func_calls,
            "avg_complexity_of_decisions": avg_complexity,
            "num_declaration_statements": self.declaration_statements,
            "num_executable_statements": self.executable_statements,
            "num_arcs": self.arcs,
            "num_decisions": self.decision_count,
            "avg_decision_span": avg_decision_span,
            "num_knots": self.knot_count,
            "num_loops": self.loop_count,
            "num_exits": self.exit_count,
            "num_nodes": self.node_count,
            "avg_nesting_level": self.max_nesting_level,
            "num_independent_paths": self.independent_paths,
            "num_control_statements": self.control_statements,
            "num_structure_breaches": self.structure_breaches,
        }

class Metrics:
    def __init__(self, code: str) -> None:
        code_ast = ast.parse(code)

        analyzer = CodeAnalyzer()
        analysis_results = analyzer.analyze(code_ast)

        # Layout
        self.non_blanc_lines = non_blanc_lines(code)
        self.avg_var_length = average_variable_length(code_ast)
        
        # Expressions
        self.total_func_calls = analysis_results["total_func_calls"]
        self.unique_func_calls = analysis_results["unique_func_calls"]
        self.avg_complexity_of_decisions = analysis_results["avg_complexity_of_decisions"]
        self.num_declaration_statements = analysis_results["num_declaration_statements"]
        self.num_executable_statements = analysis_results["num_executable_statements"]

        # Control flow
        self.num_arcs = analysis_results["num_arcs"]
        self.num_decisions = analysis_results["num_decisions"]
        self.avg_decision_span = analysis_results["avg_decision_span"]
        self.num_knots = analysis_results["num_knots"]
        self.num_loops = analysis_results["num_loops"]
        self.num_exits = analysis_results["num_exits"]
        self.num_nodes = analysis_results["num_nodes"]
        self.avg_nesting_level = analysis_results["avg_nesting_level"]
        self.num_independent_paths = analysis_results["num_independent_paths"]
        self.num_control_statements = analysis_results["num_control_statements"]
        self.num_structure_breaches = analysis_results["num_structure_breaches"]
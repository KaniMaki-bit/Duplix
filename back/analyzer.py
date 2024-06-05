from pythonparser import diagnostic, source, lexer
from typing import Dict, Tuple, Any, List
import ast
import difflib as dl

PYTHON_VERSION = (3,6)
PARAMETERIZABLE_TYPES = {
    "float", 
    "int", 
    "strdata", 
    "ident"
}
BUILT_INT_FUNCTIONS = {
    "abs",
    "aiter",
    "all",
    "anext",
    "any",
    "ascii",
    "bin",
    "bool",
    "breakpoint",
    "bytearray",
    "bytes",
    "callable",
    "chr",
    "classmethod",
    "compile",
    "complex",
    "delattr",
    "dict",
    "dir",
    "divmod",
    "enumerate",
    "eval",
    "exec",
    "filter",
    "float",
    "format",
    "frozenset",
    "getattr",
    "globals",
    "hasattr",
    "hash",
    "help",
    "hex",
    "id",
    "input",
    "int",
    "isinstance",
    "issubclass",
    "iter",
    "len",
    "list",
    "locals",
    "map",
    "max",
    "memoryview",
    "min",
    "next",
    "object",
    "oct",
    "open",
    "ord",
    "pow",
    "print",
    "property",
    "range",
    "repr",
    "reversed",
    "round",
    "set",
    "setattr",
    "slice",
    "sorted",
    "staticmethod",
    "str",
    "sum",
    "super",
    "tuple",
    "type",
    "vars",
    "zip",
    "__import__"
}
PARAMETERIZED_REPLACEMENT = "P"
MIN_MATCH_BLOCK_SIZE = 10
DELTAS = {
    "Numero de lineas no vacias": 5,
    "Longitud promedio de variables": 2,

    "Llamadas a funciones": 5,
    "Llamadas unicas a funciones": 2,
    "Complejidad promedio de decisiones": 2,
    "Declaraciones declarativas": 2,
    "Declaraciones ejecutables": 5,

    "Arcos": 2,
    "Decisiones": 2,
    "Promedio de lapso de decisiones": 5,
    "Nudos": 2,
    "Ciclos": 2,
    "Salidas": 2,
    "Nodos": 2,
    "Promedio de anidación": 2,
    "Caminos independientes": 100,
    "Declaraciones de control": 2,
    "Violaciones de estructura": 2
}

def non_blanc_lines(code: str) -> int:
    return sum(1 for line in code.split('\n') if line.strip() != '')

def get_variable_names(code_ast: ast.AST) -> List[str]:
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

class Archivos:
    def __init__(self, archivos: Dict[str, str]) -> None:
        self.archivos = {matricula: Archivo(matricula, codigo) for matricula, codigo in archivos.items()}
        self.comparaciones = dict()
        self.heatmap = dict()

        for matricula1, archivo1 in self.archivos.items():
            if matricula1 not in self.comparaciones:
                self.comparaciones[matricula1] = dict()
            if matricula1 not in self.heatmap:
                self.heatmap[matricula1] = dict()
            for matricula2, archivo2 in self.archivos.items():
                comparacion_ = comparar_archivos(archivo1, archivo2)
                self.comparaciones[matricula1][matricula2] = comparacion_
                if matricula1 == matricula2:
                    self.heatmap[matricula1][matricula2] = 1
                    continue
                self.heatmap[matricula1][matricula2] = round(comparacion_['similitud'], 2)

    def estudiantes(self) -> List[str]:
        return [matricula for matricula in self.archivos]

    def comparacion(self, id_1: str, id_2: str):
        comparacion_ = self.comparaciones[id_1][id_2]
        print(comparacion_)
        return comparacion_

class Archivo:
    def __init__(self, id: str, code: str) -> None:
        self.id = id
        self.code = code
        self.metrics = Metrics(code)
        self.tokens = code_tokens(code)
        self.parameterized_tokens = parameterized_tokens(self.tokens)

    def __repr__(self) -> str:
        return f"Archivo({self.id}, {self.code})"
    
def comparar_archivos(archivo1: Archivo, archivo2: Archivo):
    codigo1, codigo2, block_ratio = dup(archivo1, archivo2)
    deltas, deltas_clasificacion, deltas_ratio = metrics_deltas(archivo1.metrics, archivo2.metrics)

    return {
        "codigo": {
            archivo1.id: codigo1,
            archivo2.id: codigo2,
            "similitud": block_ratio
        },
        "metricas": {
            "deltas": deltas,
            "clasificacion": deltas_clasificacion,
            "similitud": deltas_ratio
        },
        "similitud": (block_ratio * 0.6) + (deltas_ratio * 0.4)
    }

def delta(a, b) -> float:
    return abs(a - b)

def metrics_deltas(metric_1: Metrics, metric_2: Metrics):
    deltas = {
        "layout": {
            "Numero de lineas no vacias": {
                "delta": delta(metric_1.non_blanc_lines, metric_2.non_blanc_lines),
                "archivo 1": metric_1.non_blanc_lines,
                "archivo 2": metric_2.non_blanc_lines
            },
            "Longitud promedio de variables": {
                "delta": delta(metric_1.avg_var_length, metric_2.avg_var_length),
                "archivo 1": round(metric_1.avg_var_length, 2),
                "archivo 2": round(metric_2.avg_var_length, 2)
            }
        },
        "expresiones": {
            "Llamadas a funciones": {
                "delta": delta(metric_1.total_func_calls, metric_2.total_func_calls),
                "archivo 1": metric_1.total_func_calls,
                "archivo 2": metric_2.total_func_calls
            },
            "Llamadas unicas a funciones": {
                "delta": delta(metric_1.unique_func_calls, metric_2.unique_func_calls),
                "archivo 1": metric_1.unique_func_calls,
                "archivo 2": metric_2.unique_func_calls
            },
            "Complejidad promedio de decisiones": {
                "delta": delta(metric_1.avg_complexity_of_decisions, metric_2.avg_complexity_of_decisions),
                "archivo 1": metric_1.avg_complexity_of_decisions,
                "archivo 2": metric_2.avg_complexity_of_decisions
            },
            "Declaraciones declarativas": {
                "delta": delta(metric_1.num_declaration_statements, metric_2.num_declaration_statements),
                "archivo 1": metric_1.num_declaration_statements,
                "archivo 2": metric_2.num_declaration_statements
            },
            "Declaraciones ejecutables": {
                "delta": delta(metric_1.num_executable_statements, metric_2.num_executable_statements),
                "archivo 1": metric_1.num_executable_statements,
                "archivo 2": metric_2.num_executable_statements
            }
        },
        "flujo de control": {
            "Arcos": {
                "delta": delta(metric_1.num_arcs, metric_2.num_arcs),
                "archivo 1": metric_1.num_arcs,
                "archivo 2": metric_2.num_arcs
            },
            "Decisiones": {
                "delta": delta(metric_1.num_decisions, metric_2.num_decisions),
                "archivo 1": metric_1.num_decisions,
                "archivo 2": metric_2.num_decisions
            },
            "Promedio de lapso de decisiones": {
                "delta": delta(metric_1.avg_decision_span, metric_2.avg_decision_span),
                "archivo 1": metric_1.avg_decision_span,
                "archivo 2": metric_2.avg_decision_span
            },
            "Nudos": {
                "delta": delta(metric_1.num_knots, metric_2.num_knots),
                "archivo 1": metric_1.num_knots,
                "archivo 2": metric_2.num_knots
            },
            "Ciclos": {
                "delta": delta(metric_1.num_loops, metric_2.num_loops),
                "archivo 1": metric_1.num_loops,
                "archivo 2": metric_2.num_loops
            },
            "Salidas": {
                "delta": delta(metric_1.num_exits, metric_2.num_exits),
                "archivo 1": metric_1.num_exits,
                "archivo 2": metric_2.num_exits
            },
            "Nodos": {
                "delta": delta(metric_1.num_nodes, metric_2.num_nodes),
                "archivo 1": metric_1.num_nodes,
                "archivo 2": metric_2.num_nodes
            },
            "Promedio de anidación": {
                "delta": delta(metric_1.avg_nesting_level, metric_2.avg_nesting_level),
                "archivo 1": metric_1.avg_nesting_level,
                "archivo 2": metric_2.avg_nesting_level
            },
            "Caminos independientes": {
                "delta": delta(metric_1.num_independent_paths, metric_2.num_independent_paths),
                "archivo 1": metric_1.num_independent_paths,
                "archivo 2": metric_2.num_independent_paths
            },
            "Declaraciones de control": {
                "delta": delta(metric_1.num_control_statements, metric_2.num_control_statements),
                "archivo 1": metric_1.num_control_statements,
                "archivo 2": metric_2.num_control_statements
            },
            "Violaciones de estructura": {
                "delta": delta(metric_1.num_structure_breaches, metric_2.num_structure_breaches),
                "archivo 1": metric_1.num_structure_breaches,
                "archivo 2": metric_2.num_structure_breaches
            }
        }
    }

    metrics_type_classification = dict()

    for metrics_type in deltas:
        iguales, similares, diferentes = 0, 0, 0

        for metric in deltas[metrics_type]:
            delta_ = deltas[metrics_type][metric]['delta']

            if delta_ <= DELTAS[metric]:
                if deltas[metrics_type][metric]['archivo 1'] == deltas[metrics_type][metric]['archivo 2']:
                    deltas[metrics_type][metric]['clasificacion'] = "Iguales"
                    iguales += 1
                else:
                    deltas[metrics_type][metric]['clasificacion'] = "Similares"
                    similares += 1
            else:
                deltas[metrics_type][metric]['clasificacion'] = "Diferentes"
                diferentes += 1

        if similares == 0 and diferentes == 0:
            metrics_type_classification[metrics_type] = "Iguales"
        elif similares > 0 and diferentes == 0:
            metrics_type_classification[metrics_type] = "Similares"
        elif diferentes > 0:
            metrics_type_classification[metrics_type] = "Diferentes"

    
    deltas_clasificacion, deltas_ratio = "Similares", 0.5

    if metrics_type_classification['layout'] == "Similares" and metrics_type_classification['expresiones'] == "Iguales" and metrics_type_classification['flujo de control'] == "Iguales":
        deltas_clasificacion = "Layouts similar"
        deltas_ratio = 0.9
    elif metrics_type_classification['layout'] == "Diferentes" and metrics_type_classification['expresiones'] == "Iguales" and metrics_type_classification['flujo de control'] == "Iguales":
        deltas_clasificacion = "Layouts diferentes"
        deltas_ratio = 0.7
    elif metrics_type_classification['expresiones'] == "Similares" and metrics_type_classification['flujo de control'] == "Iguales":
        deltas_clasificacion = "Expresiones similares"
        deltas_ratio = 0.5
    elif metrics_type_classification['expresiones'] == "Diferentes" and metrics_type_classification['flujo de control'] == "Iguales":
        deltas_clasificacion = "Expresiones diferentes"
        deltas_ratio = 0.3
    elif metrics_type_classification['flujo de control'] == "Similares":
        deltas_clasificacion = "Flujos de control similares"
        deltas_ratio = 0.1
    elif metrics_type_classification['flujo de control'] == "Diferentes":
        deltas_clasificacion = "Flujos de control diferentes"
        deltas_ratio = 0.0

    return deltas, deltas_clasificacion, deltas_ratio

def _insert(source_str: str, insert_str: str, pos: int) -> str:
    return source_str[:pos] + insert_str + source_str[pos:]

def code_tokens(code_str: str) -> List[lexer.Token]:
    """
    Toma el codigo de un archivo y regresa una lista de sus `lexer.Token`
    """
    buffer = source.Buffer(code_str)
    engine = diagnostic.Engine()

    tokens = [token
        for token in lexer.Lexer(
            buffer,
            PYTHON_VERSION,
            engine
        )
    ]

    return tokens

def parameterize_token(token: lexer.Token) -> Tuple[str, Any]:
    """
    Toma un `lexer.Token` y regresa una tupla en donde [0] es el tipo (str) y [1] el valor (Any)
    """
    parameterized_token = (token.kind, token.value)

    if token.kind in PARAMETERIZABLE_TYPES:
        if not((token.kind == "ident") and (token.value in BUILT_INT_FUNCTIONS)): # No parametrizar built-in functions
            parameterized_token = (token.kind, PARAMETERIZED_REPLACEMENT)

    return parameterized_token

def parameterized_tokens(tokens: List[lexer.Token]) -> List[Tuple[str, Any]]:
    """
    Dada una lista de Tokens, conserva unicamente el tipo y valor de los tokens.
    Tambien, parametriza los tokens de cierto tipo (float, int, strdata, ident), cambiando su valor a 'P'
    Se regresa una lista de tuplas que representan los tokens, [0] (str) representa el tipo de token y [1] (any) su valor
    """
    return [parameterize_token(token) for token in tokens]

def matching_blocks(sequence1: List, sequence2: List, min_block_size: int) -> Tuple[List[dl.Match], float]:
    """
    Regresa todos los bloques identicos entre ambas secuencias cuya longitud sea mayor o igual a `min_block_size` y similaridad (0 - 1)
    """
    matcher = dl.SequenceMatcher(None, sequence1, sequence2)
    min_len = min(len(sequence1), len(sequence2))
    blocks_len = 0

    blocks = []

    for block in matcher.get_matching_blocks():
        if block.size >= min_block_size:
            blocks.append(block)
            blocks_len += block.size

    ratio = blocks_len / min_len

    return blocks, ratio

def mark_code(file1: Archivo, file2: Archivo, matches: List[dl.Match]) -> Tuple[str, str]:
    corrimiento_str1, corrimiento_str2 = 0, 0
    code1_str, code2_str = file1.code, file2.code

    for index, match in enumerate(matches):
        a = match.a
        b = match.b
        n = match.size

        str_start_index_1 = file1.tokens[a].loc.begin_pos
        str_end_index_1 = file1.tokens[a + n - 1].loc.end_pos

        str_start_index_2 = file2.tokens[b].loc.begin_pos
        str_end_index_2 = file2.tokens[b + n - 1].loc.end_pos

        left_mark = f"(Inicio de bloque {index + 1})"
        right_mark = f"(Fin de bloque {index + 1})"

        code1_str = _insert(code1_str, left_mark, str_start_index_1 + corrimiento_str1)
        corrimiento_str1 += len(left_mark)
        code1_str = _insert(code1_str, right_mark, str_end_index_1 + corrimiento_str1)
        corrimiento_str1 += len(right_mark)

        code2_str = _insert(code2_str, left_mark, str_start_index_2 + corrimiento_str2)
        corrimiento_str2 += len(left_mark)
        code2_str = _insert(code2_str, right_mark, str_end_index_2 + corrimiento_str2)
        corrimiento_str2 += len(right_mark)

    return code1_str, code2_str

def dup(file1: Archivo, file2: Archivo) -> Tuple[str, str, float]:
    """
    Dados 2 archivos, regresa el codigo de estos tras agregar las marcas de los bloques de plagio al igual que el ratio de similitud
    """
    matching_blocks_, ratio = matching_blocks(file1.parameterized_tokens, file2.parameterized_tokens, MIN_MATCH_BLOCK_SIZE)
    marked_file1_code, marked_file2_code = mark_code(file1, file2, matching_blocks_)

    return marked_file1_code, marked_file2_code, ratio

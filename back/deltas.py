from metrics import Metrics

# (https://www.sdml.cs.kent.edu/library/Mayrand96.pdf)
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
                "archivo 1": metric_1.avg_var_length,
                "archivo 2": metric_2.avg_var_length
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

            if delta_ == DELTAS[metric]:
                deltas[metrics_type][metric]['clasificacion'] = "Iguales"
                iguales += 1
            elif delta_ < DELTAS[metric]:
                deltas[metrics_type][metric]['clasificacion'] = "Similares"
                similares += 1
            elif delta_ > DELTAS[metric]:
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
from pythonparser import diagnostic, source, lexer
from typing import Tuple, Any
import difflib as dl
from archivos import Archivo

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
MIN_MATCH_BLOCK_SIZE = 1

def _insert(source_str: str, insert_str: str, pos: int) -> str:
    return source_str[:pos] + insert_str + source_str[pos:]

def code_tokens(code_str: str) -> list[lexer.Token]:
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

def parameterized_tokens(tokens: list[lexer.Token]) -> list[Tuple[str, Any]]:
    """
    Dada una lista de Tokens, conserva unicamente el tipo y valor de los tokens.
    Tambien, parametriza los tokens de cierto tipo (float, int, strdata, ident), cambiando su valor a 'P'
    Se regresa una lista de tuplas que representan los tokens, [0] (str) representa el tipo de token y [1] (any) su valor
    """
    return [parameterize_token(token) for token in tokens]

def matching_blocks(sequence1: list, sequence2: list, min_block_size: int) -> Tuple[list[dl.Match], float]:
    """
    Regresa todos los bloques identicos entre ambas secuencias cuya longitud sea mayor o igual a `min_block_size` y similaridad (0 - 1)
    """
    matcher = dl.SequenceMatcher(None, sequence1, sequence2)
    return [block for block in matcher.get_matching_blocks() if block.size >= min_block_size], matcher.ratio

def mark_code(file1: Archivo, file2: Archivo, matches: list[dl.Match]) -> Tuple[str, str]:
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

        left_mark = "{{{"
        right_mark = f"}}}}}}{index}"

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
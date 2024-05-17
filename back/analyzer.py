from pythonparser import diagnostic, source, lexer
import difflib as dl
from models import *

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
JUNK_TOKENS = {
    ('newline', None)
}

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

def parameterize_token(token: lexer.Token) -> Token:
    """
    Toma un `lexer.Token` y regresa un `models.Token`, parametrizando su valor (si aplica)
    """
    parameterized_token = Token(token.kind, token.value)

    if token.kind in PARAMETERIZABLE_TYPES:
        if not((token.kind == "ident") and (token.value in BUILT_INT_FUNCTIONS)): # No parametrizar built-in functions
            parameterized_token = Token(token.kind, PARAMETERIZED_REPLACEMENT)

    return parameterized_token

def parameterized_tokens(tokens: list[lexer.Token]) -> list[Token]:
    """
    Dada una lista de Tokens, conserva unicamente el tipo y valor de los tokens.
    Tambien, parametriza los tokens de cierto tipo (float, int, strdata, ident), cambiando su valor a 'P'
    Se regresa una lista de tuplas que representan los tokens, [0] (str) representa el tipo de token y [1] (any) su valor
    """
    return [parameterize_token(token) for token in tokens]

def matching_blocks(sequence1: list, sequence2: list, min_block_size: int) -> list[dl.Match]:
    """
    Regresa todos los bloques identicos entre ambas secuencias cuya longitud sea mayor o igual a `min_block_size`
    """
    matcher = dl.SequenceMatcher(None, sequence1, sequence2)
    return [block for block in matcher.get_matching_blocks() if block.size >= min_block_size]

code1 = open("test_files/test1.py").read()
code2 = open("test_files/test2.py").read()

t1 = code_tokens(code1)
pt1 = parameterized_tokens(t1)

t2 = code_tokens(code2)
pt2 = parameterized_tokens(t2)

blocks = matching_blocks(pt1, pt2, 1)
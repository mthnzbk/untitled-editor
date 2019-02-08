from PyQt5.Qsci import QsciLexerCustom


class PythonLexer(QsciLexerCustom):

    styles = {
        "Default": 0,
        "Comment": 1,
        "Keyword": 2,
        "String": 3,
        "Number": 4,
        "Pragma": 5,
        "Operator": 6,
        "Unsafe": 7,
        "Type": 8,
    }

    keyword_list = [
        "False",
        "None",
        "True",
        "and",
        "as",
        "assert",
        "async",
        "await",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "nonlocal",
        "not",
        "or",
        "pass",
        "raise",
        "return",
        "try",
        "while",
        "with",
        "yield",
    ]


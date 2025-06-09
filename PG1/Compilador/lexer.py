import ply.lex as lex

# Palabras reservadas
reserved = {
    '.section': 'SECTION',
    '.word': 'WORD',
    '.text': 'TEXT',
    '.data': 'DATA',
    '.vault': 'VAULT',
    'MOV': 'MOV',
    'MOVI': 'MOVI',
    'ADD': 'ADD',
    'ADDI': 'ADDI',
    'SUB': 'SUB',
    'SUBI': 'SUBI',
    'MUL': 'MUL',
    'MULI': 'MULI',
    'XOR': 'XOR',
    'XORI': 'XORI',
    'XOR3': 'XOR3',
    'SHL': 'SHL',
    'SHR': 'SHR',
    'BSHL': 'BSHL',
    'BSHR': 'BSHR',
    'BSTRH': 'BSTRH',
    'BSTRL': 'BSTRL',
    'LDR': 'LDR',
    'LDRI': 'LDRI',
    'STR': 'STR',
    'STRI': 'STRI',
    'CMP': 'CMP',
    'CMPI': 'CMPI',
    'BEQ': 'BEQ',
    'BNE': 'BNE',
    'BLT': 'BLT',
    'BGT': 'BGT',
    'JUMP': 'JUMP',
    'NOP': 'NOP',
    'END': 'END'
}

tokens = [
    'LABEL_DEF', 'LABEL',
    'REGISTER', 'BKEY',
    'IMMEDIATE', 'COMMA', 
    'NEWLINE', 'COLON', 
    'COMMENT', 'EQUALS',
] + list(set(reserved.values()))

t_EQUALS = r'='
t_COMMA = r','
t_COLON = r':'

def t_SECTION(t):
    r'\.section'
    return t

def t_TEXT(t):
    r'\.text'
    return t

def t_DATA(t):
    r'\.data'
    return t

def t_VAULT(t):
    r'\.vault'
    return t

def t_WORD(t):
    r'\.word'
    return t

def t_REGISTER(t):
    r'[Rr][0-9]+'
    t.value = t.value.upper()  # opcional para normalizar a mayúscula
    return t

def t_BKEY(t):
    r'[Kk][0-3]'
    t.value = t.value.upper()
    return t

def t_IMMEDIATE(t):
    r'0x[0-9a-fA-F]+|\#-?\d+|-?\d+'
    val = t.value
    if val.startswith('#'):
        t.value = int(val[1:])
    elif val.startswith('0x') or val.startswith('-0x'):
        t.value = int(val, 16)
    else:
        t.value = int(val)
    return t

def t_LABEL_DEF(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*:'
    t.value = t.value[:-1]  # eliminar el ':'
    return t

def t_LABEL(t):
    r'[A-Za-z_][\w_]*'
    upper_val = t.value.upper()
    if upper_val in reserved:
        t.type = reserved[upper_val]
        t.value = upper_val
    else:
        t.type = 'LABEL'
    return t

def t_COMMENT(t):
    r'\@.*'
    pass  # ignorar comentarios

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()


if __name__ == "__main__":
    with open("tea_decrypt.txt", "r") as f:
        data = f.read()

    lexer.input(data)

    current_line = -1
    tokens_en_linea = []

    while True:
        tok = lexer.token()
        if not tok:
            # imprimir lo último pendiente
            if tokens_en_linea:
                print(f"Line {current_line}:", " | ".join(tokens_en_linea))
            break

        if tok.lineno != current_line:
            # imprimir línea anterior si hay
            if tokens_en_linea:
                print(f"Line {current_line}:", " | ".join(tokens_en_linea))
            # iniciar nueva línea
            current_line = tok.lineno
            tokens_en_linea = []

        tokens_en_linea.append(f"{tok.type:<12} {tok.value}")


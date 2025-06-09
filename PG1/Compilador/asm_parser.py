import ply.yacc as yacc
from lexer import tokens

instructions = []

def p_program(p):
    '''program : sections'''
    p[0] = p[1]

def p_sections(p):
    '''sections : section
                | section sections'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_section(p):
    '''section : SECTION section_type NEWLINE content'''
    p[0] = (p[2], p[4])

def p_section_type(p):
    '''section_type : TEXT
                    | DATA
                    | VAULT'''
    p[0] = p[1]

def p_content(p):
    '''content : content line
               | line'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_line(p):
    '''line : instruction
            | word_directive
            | LABEL_DEF
            | NEWLINE'''
    p[0] = p[1]

def p_word_directive(p):
    '''word_directive : LABEL_DEF WORD IMMEDIATE_LIST'''
    p[0] = ('word', p[1], p[3])

def p_IMMEDIATE_LIST(p):
    '''IMMEDIATE_LIST : IMMEDIATE
                      | IMMEDIATE COMMA IMMEDIATE_LIST'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_instruction(p):
    '''instruction : MOV REGISTER COMMA REGISTER
                   | MOVI REGISTER COMMA IMMEDIATE
                   | ADD REGISTER COMMA REGISTER COMMA REGISTER
                   | ADDI REGISTER COMMA REGISTER COMMA IMMEDIATE
                   | SUB REGISTER COMMA REGISTER COMMA REGISTER
                   | SUBI REGISTER COMMA REGISTER COMMA IMMEDIATE
                   | MUL REGISTER COMMA REGISTER COMMA REGISTER
                   | MULI REGISTER COMMA REGISTER COMMA IMMEDIATE
                   | XOR REGISTER COMMA REGISTER COMMA REGISTER
                   | XORI REGISTER COMMA REGISTER COMMA IMMEDIATE
                   | XOR3 REGISTER COMMA REGISTER COMMA REGISTER COMMA REGISTER
                   | SHL REGISTER COMMA REGISTER COMMA IMMEDIATE
                   | SHR REGISTER COMMA REGISTER COMMA IMMEDIATE
                   | BSHL REGISTER COMMA REGISTER COMMA BKEY COMMA IMMEDIATE
                   | BSHR REGISTER COMMA REGISTER COMMA BKEY COMMA IMMEDIATE
                   | BSTRH BKEY COMMA IMMEDIATE
                   | BSTRL BKEY COMMA IMMEDIATE
                   | LDR REGISTER COMMA REGISTER
                   | LDR REGISTER COMMA REGISTER COMMA IMMEDIATE
                   | LDRI REGISTER COMMA IMMEDIATE
                   | LDRI REGISTER COMMA EQUALS LABEL
                   | STR REGISTER COMMA REGISTER
                   | STR REGISTER COMMA REGISTER COMMA IMMEDIATE
                   | STRI REGISTER COMMA IMMEDIATE
                   | STRI REGISTER COMMA EQUALS LABEL
                   | CMP REGISTER COMMA REGISTER
                   | CMPI REGISTER COMMA IMMEDIATE
                   | BEQ LABEL
                   | BNE LABEL
                   | BLT LABEL
                   | BGT LABEL
                   | JUMP LABEL
                   | NOP
                   | END'''
    p[0] = tuple(p[1:])

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        print("Error de sintaxis al final del archivo")

parser = yacc.yacc()

def parsed_program(data):
    result = parser.parse(data)
    return result

if __name__ == "__main__":
    with open("tea_encrypt.txt", "r") as f:
        data = f.read()

    result = parsed_program(data)
    print("Parse result:")
    for section_type, content in result:
        print(f"Section: {section_type}")
        for line in content:
            print("  ", line)

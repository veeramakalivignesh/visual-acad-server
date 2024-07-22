import re
import ast

def process_for_bracket(line, b_open, b_close):
    num = 1
    for i in range(len(line)-1):
        if line[len(line)-i-2] == b_open:
            num -= 1
        elif line[len(line)-i-2] == b_close:
            num += 1
        if num == 0:
            return line[:len(line)-i-1] + '\"' + line[len(line)-i-1:-1] + '\"' + b_close
    return None 


def fix_mermaid(mermaid):
    lines = mermaid.split('\n')
    new_lines = []
    for line in lines:
        if len(line) >1 and line[-2:] == 'LR':
            line = line[:-2] + 'TD'
        if len(line) > 0 and line[-1] == '}':
            new_line =  process_for_bracket(line, '{', '}')
        elif len(line) > 0 and line[-1] == ')':
            new_line =  process_for_bracket(line, '(', ')')
        elif len(line) > 0 and line[-1] == ']':
            new_line =  process_for_bracket(line, '[', ']')
        else:
            new_line = line
        new_lines.append(new_line)

    return '\n'.join(new_lines)

def get_script(code):
    is_fun = False
    code_lines = []
    for line in code.split('\n'):
        if line[:4] == 'def ' or line[:4] == 'def\t':
            is_fun = True
        elif len(line)>0 and is_fun and line[0] != ' ' and line[0]!= '\t':
            is_fun = False
        if not is_fun:
            code_lines.append(line)
    script = '\n'.join(code_lines)
    return script

class FunctionExtractorRemover(ast.NodeTransformer):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        # Store the function definition
        self.functions.append(node)
        # Remove the function definition from the AST
        return None

def snip_code(code_split, start_line, end_line):
    return "\n".join(code_split[start_line-1:end_line])

def extract_skeleton(code_split, func_indices):
    func_index_set = set()
    for start, end in func_indices:
        for i in range(start -1, end):
            func_index_set.add(i)
    new_split = []
    for i, line in enumerate(code_split):
        if i not in func_index_set:
            new_split.append(line)
    return "\n".join(new_split)


def parse_code(code):
    # Parse the code into an AST
    global tree 
    tree = ast.parse(code)

    code_split = code.split('\n')

    # Create an instance of the transformer
    transformer = FunctionExtractorRemover()

    # Transform the tree (this also fills the functions list)
    new_tree = transformer.visit(tree)
    
    # Fix missing locations
    ast.fix_missing_locations(new_tree)
    
    code_list = []
    func_indices = []
    for func in transformer.functions:
        func_indices.append((func.lineno,func.end_lineno))
        code_list.append({
            "name": func.name,
            "code": snip_code(code_split, func.lineno, func.end_lineno)
        })
    
    skeleton = ast.unparse(new_tree)
    if skeleton != '':
        code_list = [{
            "name": "skeleton",
            "code": extract_skeleton(code_split, func_indices)
        }] + code_list
    
    return code_list
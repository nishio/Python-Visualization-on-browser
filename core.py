import json
import dis
import compiler
import parser
import ast
from opcode import *
from opcode import __all__ as _opcodes_all

def disassemble(co):
    """Disassemble a code object."""
    lines = []
    code = co.co_code
    labels = dis.findlabels(code)
    linestarts = dict(dis.findlinestarts(co))
    n = len(code)
    i = 0
    extended_arg = 0
    free = None
    while i < n:
        c = code[i]
        op = ord(c)
        data = {"raw_op": op}
        if i in linestarts:
            data["line_no"] = linestarts[i]
        else:
            data["line_no"] = None

        if i in labels:
            data["in_labels"] = True
        else:
            data["in_labels"] = False

        data["i"] = i
        data["opname"] = opname[op]
        data["hex"] = "%02X" % op
        i = i + 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i + 1]) * 256 + extended_arg
            extended_arg = 0
            data["hex"] += " %02X %02X" % (ord(code[i]), ord(code[i + 1]))
            i = i + 2
            if op == EXTENDED_ARG:
                extended_arg = oparg * 65536L
            data["raw_arg"] = oparg
            if op in hasconst:
                data['arg'] = {"value": repr(co.co_consts[oparg]), "type": "const"}
            elif op in hasname:
                data['arg'] =  {"value": co.co_names[oparg], "type": "name"}
            elif op in hasjrel:
                data['arg'] =  {"value": repr(i + oparg), "type": "jump_relative"}
            elif op in haslocal:
                data['arg'] =  {"value": co.co_varnames[oparg], "type": "local_name"}
            elif op in hascompare:
                data['arg'] =  {"value": cmp_op[oparg], "type": "compare"}
            elif op in hasfree:
                if free is None:
                    free = co.co_cellvars + co.co_freevars
                data['arg'] =  {"value": cmp_op[oparg], "type": "free_variable"}

        lines.append(data)
    return json.dumps(lines)

def to_bytecode(code):
    return disassemble(compiler.compile(code, "<string>", "exec"))

def to_ast(code):
    tree = ast.parse(code)
    s = ast.dump(tree)
    # make better print

def to_syntax_tree(code):
    st = parser.suite("1 + 2")
    tpl = st.totuple()
    # TODO: find my old blog entry

def _test():
    import doctest
    doctest.testmod()
    print to_bytecode("1+2")

if __name__ == "__main__":
    _test()

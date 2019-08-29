rules = {}
rules[0] = "(+[])"
rules[1] = "(+!![])"
rules["0x"] = "+[]"
rules["1x"] = "+!![]"
rules[""] = "[]"
rules["0"] = rules[0] + "+" +rules[""]
rules["1"] = rules[1] + "+" +rules[""]
rules["2"] = "("+"+!![]"*2 + ")+" +rules[""]
rules["3"] = "("+"+!![]"*3 + ")+" +rules[""]
rules["4"] = "("+"+!![]"*4 + ")+" +rules[""]
rules["5"] = "("+"+!![]"*5 + ")+" +rules[""]
rules["6"] = "("+"+!![]"*6 + ")+" +rules[""]
rules["7"] = "("+"+!![]"*7 + ")+" +rules[""]
rules["8"] = "("+"+!![]"*8 + ")+" +rules[""]
rules["9"] = "("+"+!![]"*9 + ")+" +rules[""]

rules['undefined'] = "[][[]]+[]"
rules['false'] = "![]+[]"
rules['true'] = "!![]+[]"
rules['[object Object]'] = "[]+{}"
rules["NaN"] = "+{}+[]"


def to_string(s):
    return '['+s+']' + '[+[]]'
        
def get_index(idx):
    if idx == 0:
        s_idx = rules["0x"]
    elif idx == 1:
        s_idx = rules["1x"]
    elif idx < 10:
        s_idx = rules["1x"]*idx
    else:
        l = int((str(idx)[0]),10)
        r = int((str(idx)[1]),10)
        if r == 0:
            s_r = rules["0x"]
        else:
            s_r = rules["1x"] * r
        s_l = rules["1x"] * l
        s_idx = '+(['+s_l+']+['+s_r+'])'
    return s_idx

def index_str(s, idx):
    return to_string(s)+'['+get_index(idx)+']'

rules['a'] = index_str(rules['false'],1)
rules['b'] = index_str(rules['[object Object]'],2)
rules['c'] = index_str(rules['[object Object]'],5)
rules['d'] = index_str(rules['undefined'],2)
rules['e'] = index_str(rules['true'],3)
rules['f'] = index_str(rules['false'],0)
rules['g'] = None
rules['h'] = None # btoa("r4a")[3]
rules['i'] = index_str(rules['undefined'],5)
rules['j'] = index_str(rules['[object Object]'],3)
rules['k'] = None
rules['l'] = index_str(rules['false'],2)
rules['m'] = None
rules['n'] = index_str(rules['undefined'],1)
rules['o'] = index_str(rules['[object Object]'],1)
rules['p'] = None
rules['q'] = None
rules['r'] = index_str(rules['true'],1)
rules['s'] = index_str(rules['false'],3)
rules['t'] = index_str(rules['true'],0)
rules['u'] = index_str(rules['undefined'],0)
rules['v'] = None
rules['w'] = None
rules['x'] = None
rules['y'] = None
rules['z'] = None
rules['A'] = None
rules['B'] = None
rules['C'] = None # btoa("0 f") = "MCBm"
#eval("btoa(+[]+[[]+{}][+[]][+!![]+!![]+!![]+!![]+!![]+!![]+!![]]+[![]+[]][+[]][+[]])");
#"MCBm"

rules['D'] = None
rules['E'] = None
rules['F'] = None
rules['G'] = None
rules['H'] = None
rules['I'] = None
rules['J'] = None
rules['K'] = None
rules['L'] = None
rules['M'] = None
rules['N'] = index_str(rules['NaN'], 0)
rules['O'] = index_str(rules['[object Object]'],8)
rules['P'] = None
rules['Q'] = None
rules['R'] = None
rules['S'] = None
rules['T'] = None
rules['U'] = None
rules['V'] = None
rules['W'] = None
rules['X'] = None
rules['Y'] = None
rules['Z'] = None
rules['['] = index_str(rules['[object Object]'],0)
rules[']'] = index_str(rules['[object Object]'], 14)
rules['('] = None
rules[')'] = None
rules['='] = None
rules['<'] = None
rules['>'] = None
rules[';'] = None
rules[','] = None
rules[':'] = None
rules['.'] = "(+(+!+[]+[+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+[!+[]+!+[]]+[+[]])+[])[+!+[]]"
rules[' '] = index_str(rules['[object Object]'],7)

def build_string(s):
    res = []
    for c in s:
        if rules[c] == None:
            print "Complex chr", c
            return None
        res.append(rules[c])
    return "+".join(res)

rules['constructor'] = build_string("constructor")
rules['sort'] = build_string("sort")	

def get_function(j_name):
    return "[][%s]" % (j_name)
	
def get_function_str(j_name):
    return "%s+[]" % (get_function(j_name))
	
def get_constructor(varx):
    # returns something like []['sort']['constructor']
    return "%s[%s]" % (varx, rules['constructor']) 

rules['('] = index_str(get_function_str(rules['sort']),13)
rules[')'] = index_str(get_function_str(rules['sort']),14)

def index_only(s, idx):
    return "%s[%s]" % (s, get_index(idx))

rules['F'] = index_only("("+get_constructor(get_function(rules['sort']))+"+[])", 9)
rules['v'] = index_only("("+get_constructor(get_function(rules['sort']))+"+[])", 31)
	
# (+[]+[])['constructor'] String.constructor
rules['S'] = index_only("("+get_constructor("("+rules["0x"]*2+")")+"+[])", 9)
rules['g'] = index_only("("+get_constructor("("+rules["0x"]*2+")")+"+[])", 14)

# (+[])['constructor'] Number.constructor
rules['N'] = index_only("("+get_constructor(rules[0])+"+[])", 9)
rules['m'] = index_only("("+get_constructor(rules[0])+"+[])", 11)

rules['/'] = "(+[]+[])[[[][[]]+[]][+[]][+!![]+!![]+!![]+!![]+!![]]+[!![]+[]][+[]][+[]]+[![]+[]][+[]][+!![]]+[![]+[]][+[]][+!![]+!![]]+[[][[]]+[]][+[]][+!![]+!![]+!![]+!![]+!![]]+[[]+{}][+[]][+!![]+!![]+!![]+!![]+!![]]+[![]+[]][+[]][+!![]+!![]+!![]]]()[+!![]+!![]+!![]+!![]+!![]]" # (+[]+[])["italics"]()

rules['"'] = "(+[]+[])[[![]+[]][+[]][+[]]+[[]+{}][+[]][+!![]]+[[][[]]+[]][+[]][+!![]]+[!![]+[]][+[]][+[]]+[[]+{}][+[]][+!![]+!![]+!![]+!![]+!![]]+[[]+{}][+[]][+!![]]+[![]+[]][+[]][+!![]+!![]]+[[]+{}][+[]][+!![]]+[!![]+[]][+[]][+!![]]]()[+([+!![]]+[+!![]+!![]])]" #("")["fontcolor"]()[12] 

def execute_js(js_str):
    js = "(%s)()" % js_str
    return get_constructor(get_function(rules['sort'])) + js

rules['C'] = index_only(execute_js(build_string('return btoa("0 f")')),1)

rules['h'] = index_only(execute_js(build_string('return btoa("r4a")')),3)

rules[','] = execute_js(build_string('return String.fromCharCode(44)'))


#print execute_js(build_string("alert(2)"))	

#print execute_js(build_string('console.log(String.fromCharCode(115,101,32,118,105,101,110,101,32,109,97,116,114,105,120,32,52))'))

def arbitrary_js(jscode):
    ords = ",".join([str(ord(_)) for _ in jscode])
    jscode = "eval(String.fromCharCode(%s))" % ords
    return execute_js(build_string(jscode))

arbitrary_js("alert(1)")
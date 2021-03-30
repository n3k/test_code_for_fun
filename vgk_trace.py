import pykd

#addr = pykd.reg("rsp")
#value = pykd.loadBytes(addr,16)
#print(hex(addr), value)
#register = "rsp"
#print(pykd.dbgCommand("dq {}".format(register)))


class InstructionQueue:
    """
    Maintains a list of <size> items
    """
    def __init__(self, size):
        self.queue = []
        self.size = size

    def add(self, item):
        if len(self.queue) == self.size:
            self.queue.pop(0)
        self.queue.append(item)

x64_registers = [
    "rax",
    "rcx",
    "rbx",
    "rdx",
    "r8",
    "r9",
    "r10",
    "r11",
    "r12",
    "r13",
    "r14",
    "r15",
    "rsi",
    "rdi"
]

def get_current_intruction_parts():
    disasm_line = pykd.disasm().instruction()
    parts = disasm_line.split()[2:]
    return parts

def get_current_intruction_address():
    disasm_line = pykd.disasm().instruction()
    address = disasm_line.split()[0]
    return int(address.replace("`",""), 0x10)

def get_module_base(module_name):
    res = pykd.dbgCommand('dd {} L?1'.format(module_name))
    return int(res.split()[0].replace("`",""), 0x10)

def get_module_range(module_name):
    res = pykd.dbgCommand('lm m {}'.format(module_name))
    return int(res.split("\n")[1].split()[1].replace("`",""), 0x10)

def relative_format(addr):
    if addr < 0:
        raise Exception("address cannot be negative")
    return "{}+{}".format(MODULE_NAME, hex(addr))

def is_in_module_range(address):
    if address >= MODULE_BASE and address <= MODULE_RANGE:
        return True
    return False


def trace_calls_jmps_rets():
    fout = open("c:\\users\\public\\temp.txt", "wb")
    real_counter = 0
    total_ins_counter = 0
    while real_counter < 20000:
        total_ins_counter += 1
        ins_addr = get_current_intruction_address()
        ins_parts = get_current_intruction_parts()

        #if not is_in_module_range(ins_addr):
        #    #print("OUTSIDE:: {} - {}".format(hex(ins_addr), ins_parts))
        #    pykd.trace()
        #    continue

        relative_addr = ins_addr - MODULE_BASE
        #print("INSIDE:: {} - {}".format(hex(ins_addr), ins_parts))
        actual_ins = ins_parts[0]
        if actual_ins == "jmp":
            real_counter += 1
            opnd = ins_parts[1]
            if opnd in x64_registers:
                #target = pykd.dbgCommand("dq {} L?1".format(opnd)).split()[1].strip("`")
                target = pykd.reg(opnd)
                if not is_in_module_range(target):
                    print("{}: {} | JMP {} (to other module)".format(real_counter, hex(ins_addr), hex(target)))
                else:
                    target = target - MODULE_BASE
                    print("{}: {} | JMP {} -> {}".format(real_counter, relative_format(relative_addr),opnd, relative_format(target)))

        elif actual_ins == "call":
            real_counter += 1
            if is_in_module_range(ins_addr):
                print("{}: ".format(real_counter), hex(ins_addr), ins_parts)

        elif actual_ins == "retn" or actual_ins == "ret":
            # check if previous instruction was a push
            real_counter += 1
            prev_ins = instruction_queue.queue[-1]
            prev_ins_parts = prev_ins.split()[2:]
            if prev_ins_parts[0] == "push":
                pushed_reg = prev_ins_parts[1]
                target = pykd.reg(pushed_reg)
                if not is_in_module_range(target):
                    print("{}: {} | RET {} (to other module)".format(real_counter, hex(target)))
                else:
                    target = target - MODULE_BASE
                    print("{}: {} | RET {}".format(real_counter, relative_format(relative_addr), relative_format(target)))

        instruction_queue.add(pykd.disasm().instruction())
        pykd.trace()

    fout.close()

    

instruction_queue = InstructionQueue(200)

MODULE_NAME = "vgk.sys"
OFFSET_DRIVER_ENTRY = "0x22000"
MODULE_BASE = get_module_base(MODULE_NAME)
MODULE_RANGE = get_module_range(MODULE_NAME[:-4])

# Set breakpoints
#pykd.dbgCommand('bc *')
#pykd.dbgCommand('bp ' + MODULE_NAME + ' +' + OFFSET_DRIVER_ENTRY)
#"r @$t0 = rcx; pt; .printf \"Allocation: %llx \\n\", rax; .printf \"Size: %08x \\n\", $t0;"
#pykd.dbgCommand('ba e 1 nt!ExAllocatePool "r; pt; dd rax L?1; g"')# ".printf \"Size: %08x \\n\", dwo(poi(esp+8)+C);"')
#pykd.dbgCommand('ba e 1 nt!ExAllocatePoolWithTag "r; pt; dd rax L?1; g"')



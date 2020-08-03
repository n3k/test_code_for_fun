from app.bytecode import *

class VirtualMachine:

    # Set trace of instructions for debugging purposes
    @property
    def trace(self):
        return self._trace
    @trace.setter
    def trace(self, v):
        self._trace = v

    def __init__(self, code, start, data_size, stack_size=200):
        self.code_mem = code
        self.data_mem = [0 for _ in range(data_size)]
        self.stack_mem = [0 for _ in range(stack_size)]
        self.trace = False

        # Setup registers
        self.ip = start
        self.sp = -1 # starts at minus one because we push before we increment this. (so
        self.fp = 0

    def fetch(self):
        op = self.code_mem[self.ip]
        self.ip += 1
        return op

    def push(self, v):
        self.sp += 1
        self.stack_mem[self.sp] = v

    def pop(self):
        v = self.stack_mem[self.sp]
        self.sp -= 1
        return v

    def disassemble(self, opcode):
        curr_instruction = opcodes[opcode]
        if curr_instruction.nargs == 1:
            fmt = "::Instruction (ip={}): {} - Opnd: {}".format(self.ip-1, curr_instruction.name, self.code_mem[self.ip])
        elif curr_instruction.nargs == 2:
            fmt = "::Instruction (ip={}): {} - Opnds: {} - {}".format(self.ip-1, curr_instruction.name,
                                                            self.code_mem[self.ip],
                                                            self.code_mem[self.ip+1])
        else:
            fmt = "::Instruction (ip={}): {}".format(self.ip-1, curr_instruction.name)
        print(fmt)

        # Print Stack
        print("::Stack memory: ", self.stack_mem[:self.sp+1])
        print(":::: SP: {}   FP: {}".format(self.sp, self.fp))
        # Print Data Mem
        print("::Data memory: ", self.data_mem)
        return

    def cpu(self):
        while self.ip < len(self.code_mem):
            op = self.fetch()
            if self.trace:
                self.disassemble(op)

            if op == HALT:
                return
            elif op == ICONST:
                v1 = self.fetch()
                self.push(v1)
            elif op == PRINT:
                v1 = self.pop()
                print(v1)
            elif op == GLOAD:
                addr = self.fetch()
                v = self.data_mem[addr]
                self.push(v)
            elif op == GSTORE:
                v = self.pop()
                addr = self.fetch()
                self.data_mem[addr] = v
            elif op == LOAD:
                offset = self.fetch()
                v = self.stack_mem[self.fp + offset]
                self.push(v)
            elif op == STORE:
                offset = self.fetch()
                v = self.pop()
                self.stack_mem[self.fp + offset] = v
            elif op == IADD:
                v1 = self.pop()
                v2 = self.pop()
                res = v1 + v2
                self.push(res)
            elif op == ISUB:
                v1 = self.pop()
                v2 = self.pop()
                res = v2 - v1
                self.push(res)
            elif op == IMUL:
                v1 = self.pop()
                v2 = self.pop()
                res = v1 * v2
                self.push(res)
            elif op == ILT:
                v1 = self.pop()
                v2 = self.pop()
                if v2 < v1:
                    self.push(1)
                else:
                    self.push(0)
            elif op == IEQ:
                v1 = self.pop()
                v2 = self.pop()
                if v2 == v1:
                    self.push(1)
                else:
                    self.push(0)
            elif op == BRF:
                addr = self.fetch()
                v1 = self.pop()
                if v1 == 0:
                    self.ip = addr
            elif op == BRT:
                addr = self.fetch()
                v1 = self.pop()
                if v1 == 1:
                    self.ip = addr
            elif op == BR:
                addr = self.fetch()
                self.ip = addr
            elif op == CALL:
                addr = self.fetch()
                n_params = self.fetch()
                self.push(n_params)
                self.push(self.fp)
                self.push(self.ip)
                self.fp = self.sp
                self.ip = addr
            elif op == RET:
                result = self.pop() # pop result value
                self.sp = self.fp
                ret_addr = self.pop()
                self.fp = self.pop()
                n_params = self.pop()
                for i in range(n_params):
                    self.pop()
                self.push(result) # push result to the the top of the stack
                self.ip = ret_addr
            else:
                print("::ERROR: unknown instruction {} at ip={}".format(op, self.ip-1))
                return



def first_test():
    code_test = [
        ICONST, 1337,
        PRINT,
        ICONST, 11,
        PRINT,
        HALT
    ]
    vm = VirtualMachine(code_test, 0, 0)
    vm.cpu()

def second_test():
    code_test = [
        ICONST, 1337,
        GSTORE, 0,
        GLOAD, 0,
        PRINT,
        ICONST, 11,
        PRINT,
        HALT
    ]
    vm = VirtualMachine(code_test, start=0, data_size=10)
    vm.trace = True
    vm.cpu()


def factorial_bytecode(n):
    fact_fn = 0
    main_addr = 22
    return main_addr, [
        # IF N < 2 RETURN 1
        LOAD, ARG_0,
        ICONST, 2,
        ILT,
        BRF, 10,
        ICONST, 1,
        RET,

        # Return FACT(N - 1) * N
        LOAD, ARG_0,
        ICONST, 1,
        ISUB,
        CALL, fact_fn, 1,
        LOAD, ARG_0,
        IMUL,
        RET,

        # MAIN (+22)
        ICONST, n,
        CALL, fact_fn, 1,
        PRINT,
        HALT
    ]

if __name__ == "__main__":
    main_addr, code = factorial_bytecode(5)
    vm = VirtualMachine(code, start=main_addr, data_size=10)
    #vm.trace = True
    vm.cpu()

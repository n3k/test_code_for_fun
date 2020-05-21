#include <windows.h>
#pragma pack(1)


// FogInject.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>

#define TRAMPOLINE_BYTES 5


PVOID g_OriginalFunction;
PVOID g_HookFunction;
BYTE FunctionOriginalOpcodes[TRAMPOLINE_BYTES];
BYTE JmpOpcodes[TRAMPOLINE_BYTES];


CRITICAL_SECTION g_CS_Hook1007;
PVOID pfnOriginalFunction1007;


__declspec(noinline) void insertHook(LPVOID hookFunction, LPVOID originalFunction, BYTE *oldBytes, BYTE *jmpBytes)
{
	DWORD oldProtect = 0;
	// 32-bit API Hooking
	BYTE tempJMP[TRAMPOLINE_BYTES] = { 0xE9, 0xDE, 0xAD, 0xBE, 0xEF }; // JMP 0xDEADBEEF
	memcpy(jmpBytes, tempJMP, TRAMPOLINE_BYTES);
	DWORD JMPSize = ((DWORD)hookFunction - (DWORD)originalFunction - 5);
	VirtualProtect((LPVOID)originalFunction, TRAMPOLINE_BYTES, PAGE_EXECUTE_READWRITE, &oldProtect);
	memcpy(oldBytes, originalFunction, TRAMPOLINE_BYTES);
	memcpy(&jmpBytes[1], &JMPSize, 4);

	memcpy(originalFunction, jmpBytes, TRAMPOLINE_BYTES);
}


__declspec(noinline) int install_hook(PVOID originalFunction, PVOID hookFunction) {
	if (originalFunction == NULL) {
		return -1;
	}
	
	g_OriginalFunction = originalFunction;
	g_HookFunction = hookFunction;

	insertHook(
		hookFunction,
		originalFunction,
		FunctionOriginalOpcodes,
		JmpOpcodes
	);

	return 0;
}

unsigned int send_count = 0;
char g_buff[] = "\xff\x51\x8c\x00\x13\x3b\x3f\x41\x00\x01\x0e\x01\x26"
"\xd7\x1b\x03\x02\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00\x18"
"\x00\x00\x00\x0e\xe6\x2c\x01\x00\x00\x00\x00\xf7\x04\x24\x8f\xec"
"\xc5\x69\xbb\x38\x57\x5e\xac\x7c\xd3\x01\xe6\xfc\x6c\x27\x25"
"\x1a\x00\x00\x00\x19\x00\x00\x00\x0c\x52\x28\x01\x00\x00\x00"
"\x00\x56\xcb\x12\x1c\xf9\x66\x0f\x60\xf2\xe5\xf6\xd0\xad\x48"
"\xac\x9f\x38\x47\xea\xb6\x47\x61\x6d\x65\x2e\x65\x78\x65\x20"
"\x30\x33\x2f\x33\x31\x2f\x31\x36\x20\x30\x31\x3a\x30\x39\x3a"
"\x30\x31\x20\x33\x35\x39\x30\x31\x32\x30\x00\x44\x34\x72\x74"
"\x68\x4e\x33\x6b\x00";

void *tsocket;
void *tbuff;
int tlen;
int retValue;
int __declspec(naked) Hook1007(void) // void *socket, void *buffer, int len
{
	__asm {		
		push ebp;
		mov ebp, esp;
		mov tsocket, ecx;
		mov tbuff, edx;
		mov eax, [ebp + 8];
		mov tlen, eax;
		pushad;
	}
	//EnterCriticalSection(&g_CS_Hook1007);

	memcpy(pfnOriginalFunction1007, FunctionOriginalOpcodes, TRAMPOLINE_BYTES);
	// If there's a succesfully running log file handler.
	

	//__debugbreak();
	if (send_count == 3) {		
		__asm {			
			lea edx, [g_buff];
			mov ecx, tsocket;
			mov eax, 0x8C;
			push eax;
			mov eax, pfnOriginalFunction1007;
			call eax;
			mov retValue, eax;
			mov eax, send_count;
			inc eax;
			mov send_count, eax;			
		}		
		//LeaveCriticalSection(&g_CS_Hook1007);
		__asm {
			jmp waittag;
		}
	}
	__asm {
		mov edx, tbuff;
		mov ecx, tsocket;
		mov eax, tlen;
		push eax;
		mov eax, pfnOriginalFunction1007;
		call eax;
		mov retValue, eax;
		mov eax, send_count;
		inc eax;
		mov send_count, eax;
	}

	// Finally, set the hook back, and restablish the original protection.
	memcpy(pfnOriginalFunction1007, JmpOpcodes, TRAMPOLINE_BYTES);

	//LeaveCriticalSection(&g_CS_Hook1007);
	__asm {
	waittag:
		popad;
		mov esp, ebp;
		pop ebp;
		mov eax, retValue;
		ret 4;
	}	
}


HINSTANCE hL2 = 0;

int main()
{
	//__debugbreak();
	hL2 = LoadLibraryA(".\\Fog.dll");
	InitializeCriticalSection(&g_CS_Hook1007);
	if (!hL2) return FALSE;
	pfnOriginalFunction1007 = GetProcAddress(hL2, MAKEINTRESOURCEA(10007));
	install_hook(pfnOriginalFunction1007, Hook1007);
	
	return 1;
}



HINSTANCE hLThis = 0;
HINSTANCE hL = 0;
FARPROC p[38] = { 0 };

BOOL WINAPI DllMain(HINSTANCE hInst, DWORD reason, LPVOID)
{
	if (reason == DLL_PROCESS_ATTACH)
	{
		hLThis = hInst;
		hL = LoadLibraryA(".\\D2Net_orig.dll");
		if (!hL) return false;


		p[0] = GetProcAddress(hL, MAKEINTRESOURCEA(10000));
		p[1] = GetProcAddress(hL, MAKEINTRESOURCEA(10001));
		p[2] = GetProcAddress(hL, MAKEINTRESOURCEA(10002));
		p[3] = GetProcAddress(hL, MAKEINTRESOURCEA(10003));
		p[4] = GetProcAddress(hL, MAKEINTRESOURCEA(10004));
		p[5] = GetProcAddress(hL, MAKEINTRESOURCEA(10005));
		p[6] = GetProcAddress(hL, MAKEINTRESOURCEA(10006));
		p[7] = GetProcAddress(hL, MAKEINTRESOURCEA(10007));
		p[8] = GetProcAddress(hL, MAKEINTRESOURCEA(10008));
		p[9] = GetProcAddress(hL, MAKEINTRESOURCEA(10009));
		p[10] = GetProcAddress(hL, MAKEINTRESOURCEA(10010));
		p[11] = GetProcAddress(hL, MAKEINTRESOURCEA(10011));
		p[12] = GetProcAddress(hL, MAKEINTRESOURCEA(10012));
		p[13] = GetProcAddress(hL, MAKEINTRESOURCEA(10013));
		p[14] = GetProcAddress(hL, MAKEINTRESOURCEA(10014));
		p[15] = GetProcAddress(hL, MAKEINTRESOURCEA(10015));
		p[16] = GetProcAddress(hL, MAKEINTRESOURCEA(10016));
		p[17] = GetProcAddress(hL, MAKEINTRESOURCEA(10017));
		p[18] = GetProcAddress(hL, MAKEINTRESOURCEA(10018));
		p[19] = GetProcAddress(hL, MAKEINTRESOURCEA(10019));
		p[20] = GetProcAddress(hL, MAKEINTRESOURCEA(10020));
		p[21] = GetProcAddress(hL, MAKEINTRESOURCEA(10021));
		p[22] = GetProcAddress(hL, MAKEINTRESOURCEA(10022));
		p[23] = GetProcAddress(hL, MAKEINTRESOURCEA(10023));
		p[24] = GetProcAddress(hL, MAKEINTRESOURCEA(10024));
		p[25] = GetProcAddress(hL, MAKEINTRESOURCEA(10025));
		p[26] = GetProcAddress(hL, MAKEINTRESOURCEA(10026));
		p[27] = GetProcAddress(hL, MAKEINTRESOURCEA(10027));
		p[28] = GetProcAddress(hL, MAKEINTRESOURCEA(10028));
		p[29] = GetProcAddress(hL, MAKEINTRESOURCEA(10029));
		p[30] = GetProcAddress(hL, MAKEINTRESOURCEA(10030));
		p[31] = GetProcAddress(hL, MAKEINTRESOURCEA(10031));
		p[32] = GetProcAddress(hL, MAKEINTRESOURCEA(10032));
		p[33] = GetProcAddress(hL, MAKEINTRESOURCEA(10033));
		p[34] = GetProcAddress(hL, MAKEINTRESOURCEA(10034));
		p[35] = GetProcAddress(hL, MAKEINTRESOURCEA(10035));
		p[36] = GetProcAddress(hL, MAKEINTRESOURCEA(10036));
		p[37] = GetProcAddress(hL, MAKEINTRESOURCEA(10037));

		main();

	}
	if (reason == DLL_PROCESS_DETACH)
	{
		FreeLibrary(hL);
	}

	return 1;
}

// ___XXX___1
extern "C" __declspec(naked) void __stdcall __E__0__()
{
	__asm
	{
		jmp p[0 * 4];
	}
}

// ___XXX___2
extern "C" __declspec(naked) void __stdcall __E__1__()
{
	__asm
	{
		jmp p[1 * 4];
	}
}

// ___XXX___3
extern "C" __declspec(naked) void __stdcall __E__2__()
{
	__asm
	{
		jmp p[2 * 4];
	}
}

// ___XXX___4
extern "C" __declspec(naked) void __stdcall __E__3__()
{
	__asm
	{
		jmp p[3 * 4];
	}
}

// ___XXX___5
extern "C" __declspec(naked) void __stdcall __E__4__()
{
	__asm
	{
		jmp p[4 * 4];
	}
}

// ___XXX___6
extern "C" __declspec(naked) void __stdcall __E__5__()
{
	__asm
	{
		jmp p[5 * 4];
	}
}

// ___XXX___7
extern "C" __declspec(naked) void __stdcall __E__6__()
{
	__asm
	{
		jmp p[6 * 4];
	}
}

// ___XXX___8
extern "C" __declspec(naked) void __stdcall __E__7__()
{
	__asm
	{
		jmp p[7 * 4];
	}
}

// ___XXX___9
extern "C" __declspec(naked) void __stdcall __E__8__()
{
	__asm
	{
		jmp p[8 * 4];
	}
}

// ___XXX___10
extern "C" __declspec(naked) void __stdcall __E__9__()
{
	__asm
	{
		jmp p[9 * 4];
	}
}

// ___XXX___11
extern "C" __declspec(naked) void __stdcall __E__10__()
{
	__asm
	{
		jmp p[10 * 4];
	}
}

// ___XXX___12
extern "C" __declspec(naked) void __stdcall __E__11__()
{
	__asm
	{
		jmp p[11 * 4];
	}
}

// ___XXX___13
extern "C" __declspec(naked) void __stdcall __E__12__()
{
	__asm
	{
		jmp p[12 * 4];
	}
}

// ___XXX___14
extern "C" __declspec(naked) void __stdcall __E__13__()
{
	__asm
	{
		jmp p[13 * 4];
	}
}

// ___XXX___15
extern "C" __declspec(naked) void __stdcall __E__14__()
{
	__asm
	{
		jmp p[14 * 4];
	}
}

// ___XXX___16
extern "C" __declspec(naked) void __stdcall __E__15__()
{
	__asm
	{
		jmp p[15 * 4];
	}
}

// ___XXX___17
extern "C" __declspec(naked) void __stdcall __E__16__()
{
	__asm
	{
		jmp p[16 * 4];
	}
}

// ___XXX___18
extern "C" __declspec(naked) void __stdcall __E__17__()
{
	__asm
	{
		jmp p[17 * 4];
	}
}

// ___XXX___19
extern "C" __declspec(naked) void __stdcall __E__18__()
{
	__asm
	{
		jmp p[18 * 4];
	}
}

// ___XXX___20
extern "C" __declspec(naked) void __stdcall __E__19__()
{
	__asm
	{
		jmp p[19 * 4];
	}
}

// ___XXX___21
extern "C" __declspec(naked) void __stdcall __E__20__()
{
	__asm
	{
		jmp p[20 * 4];
	}
}

// ___XXX___22
extern "C" __declspec(naked) void __stdcall __E__21__()
{
	__asm
	{
		jmp p[21 * 4];
	}
}

// ___XXX___23
extern "C" __declspec(naked) void __stdcall __E__22__()
{
	__asm
	{
		jmp p[22 * 4];
	}
}

// ___XXX___24
extern "C" __declspec(naked) void __stdcall __E__23__()
{
	__asm
	{
		jmp p[23 * 4];
	}
}

// ___XXX___25
extern "C" __declspec(naked) void __stdcall __E__24__()
{
	__asm
	{
		jmp p[24 * 4];
	}
}

// ___XXX___26
extern "C" __declspec(naked) void __stdcall __E__25__()
{
	__asm
	{
		jmp p[25 * 4];
	}
}

// ___XXX___27
extern "C" __declspec(naked) void __stdcall __E__26__()
{
	__asm
	{
		jmp p[26 * 4];
	}
}

// ___XXX___28
extern "C" __declspec(naked) void __stdcall __E__27__()
{
	__asm
	{
		jmp p[27 * 4];
	}
}

// ___XXX___29
extern "C" __declspec(naked) void __stdcall __E__28__()
{
	__asm
	{
		jmp p[28 * 4];
	}
}

// ___XXX___30
extern "C" __declspec(naked) void __stdcall __E__29__()
{
	__asm
	{
		jmp p[29 * 4];
	}
}

// ___XXX___31
extern "C" __declspec(naked) void __stdcall __E__30__()
{
	__asm
	{
		jmp p[30 * 4];
	}
}

// ___XXX___32
extern "C" __declspec(naked) void __stdcall __E__31__()
{
	__asm
	{
		jmp p[31 * 4];
	}
}

// ___XXX___33
extern "C" __declspec(naked) void __stdcall __E__32__()
{
	__asm
	{
		jmp p[32 * 4];
	}
}

// ___XXX___34
extern "C" __declspec(naked) void __stdcall __E__33__()
{
	__asm
	{
		jmp p[33 * 4];
	}
}

// ___XXX___35
extern "C" __declspec(naked) void __stdcall __E__34__()
{
	__asm
	{
		jmp p[34 * 4];
	}
}

// ___XXX___36
extern "C" __declspec(naked) void __stdcall __E__35__()
{
	__asm
	{
		jmp p[35 * 4];
	}
}

// ___XXX___37
extern "C" __declspec(naked) void __stdcall __E__36__()
{
	__asm
	{
		jmp p[36 * 4];
	}
}

// ___XXX___38
extern "C" __declspec(naked) void __stdcall __E__37__()
{
	__asm
	{
		jmp p[37 * 4];
	}
}


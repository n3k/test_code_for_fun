// GetFullPathName.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <windows.h>
#include <subauth.h>


#define DECLARE_UNICODE_STRING_SIZE(_var, _size) \
WCHAR _var ## _buffer[_size]; \
UNICODE_STRING _var = { 0, _size * sizeof(WCHAR) , _var ## _buffer }

typedef struct _RTL_RELATIVE_NAME {
	UNICODE_STRING RelativeName;
	HANDLE         ContainingDirectory;
	void*          CurDirRef;
} RTL_RELATIVE_NAME, *PRTL_RELATIVE_NAME;

typedef BOOLEAN (NTAPI *_RtlDosPathNameToRelativeNtPathName_U) (
	_In_       PCWSTR DosFileName,
	_Out_      PUNICODE_STRING NtFileName,
	_Out_opt_  PWSTR* FilePath,
	_Out_opt_  PRTL_RELATIVE_NAME RelativeName
);

_RtlDosPathNameToRelativeNtPathName_U RtlDosPathNameToRelativeNtPathName_U = NULL;

void convert_to_nt_path(WCHAR *pIn, PUNICODE_STRING NtFileName) {
	RtlDosPathNameToRelativeNtPathName_U = (_RtlDosPathNameToRelativeNtPathName_U)
		GetProcAddress(GetModuleHandleA("ntdll.dll"), "RtlDosPathNameToRelativeNtPathName_U");

	RtlDosPathNameToRelativeNtPathName_U(pIn, NtFileName, NULL, NULL);
}

int main(int argc, char *argv[])
{
	if (argc < 2)
		return 0;

	WCHAR inBuff[4096] = { 0 };
	WCHAR outFullPathName[4096] = { 0 };

	DECLARE_UNICODE_STRING_SIZE(outNtName, 4096);
	
	swprintf(inBuff, 4096, L"%hs", argv[1]);

	GetFullPathNameW(inBuff, 4096, outFullPathName, NULL);

	printf("-> %S\n", outFullPathName);

	convert_to_nt_path(outFullPathName, &outNtName);

	printf("-> %S\n", outNtName.Buffer);
    return 0;
}


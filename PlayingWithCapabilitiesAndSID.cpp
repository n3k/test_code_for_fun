// PlayingWithCapabilitiesAndSID.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <windows.h>
#include <userenv.h>
#include <sddl.h>

#pragma comment(lib, "Userenv.lib")
#pragma comment(lib, "Advapi32.lib")

void delete_container_profile(WCHAR *containerName) {
	HRESULT hr = DeleteAppContainerProfile(containerName);
	if (hr != S_OK) {
		printf("DeleteAppContainerProfile call failed!\n");
	}
}

int main()
{
	PSID appContainerSid = { 0 };
	WCHAR pszAppContainerName[] = L"MyFirstAppContainer_012312591";

	//delete_container_profile(pszAppContainerName);

	HRESULT hr = CreateAppContainerProfile(
		pszAppContainerName,
		pszAppContainerName,
		pszAppContainerName, 
		NULL,
		NULL,
		&appContainerSid);

	if (hr != S_OK) {
		printf("CreateAppContainerProfile call failed!\n");
		hr = DeriveAppContainerSidFromAppContainerName(pszAppContainerName, &appContainerSid);
		if (hr != S_OK) {
			printf("DeriveAppContainerSidFromAppContainerName call failed!\n");
			exit(-1);
		}
	}
	//////////////////////////////////

	STARTUPINFOEX si = { 0 };
	si.StartupInfo.cb = sizeof(si);
	PROCESS_INFORMATION pi = {0};

	SIZE_T size;
	SECURITY_CAPABILITIES sc = { 0 };
	sc.AppContainerSid = appContainerSid;

	InitializeProcThreadAttributeList(NULL, 1, 0, &size);
	BYTE *buffer = (BYTE *)HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, size);
	si.lpAttributeList = (LPPROC_THREAD_ATTRIBUTE_LIST)buffer;
	InitializeProcThreadAttributeList(si.lpAttributeList, 1, 0, &size);

	UpdateProcThreadAttribute(si.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES, &sc, sizeof(sc), NULL, NULL);

	WCHAR exeName[] = L"c:\\windows\\system32\\notepad.exe";
	BOOL fSuccess = CreateProcessW(NULL, exeName, NULL, NULL, FALSE,
		EXTENDED_STARTUPINFO_PRESENT, NULL, NULL,
		(LPSTARTUPINFO)&si, &pi);
	printf("Process created?: %d\n", fSuccess);

	PWSTR ppszPath = NULL;
	LPWSTR stringSID = NULL;
	ConvertSidToStringSidW(appContainerSid, &stringSID);
	printf("AppContainer SID: %S\n", stringSID);

	GetAppContainerFolderPath(stringSID, &ppszPath);
	printf("AppContainer Folder: %S\n", ppszPath);

	//////////////////////////////////
	LocalFree(stringSID);
	CoTaskMemFree(ppszPath);
	HeapFree(GetProcessHeap(), 0, buffer);
	FreeSid(appContainerSid);
	//delete_container_profile(pszAppContainerName);

    return 0;
}


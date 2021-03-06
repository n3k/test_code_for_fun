// unmanaged_clr.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>
#include <metahost.h>

/*
The hosting API enables unmanaged hosts to integrate the common language runtime (CLR) into their applications.
https://docs.microsoft.com/en-us/dotnet/framework/unmanaged-api/hosting/
https://www.codeproject.com/Articles/607352/Injecting-NET-Assemblies-Into-Unmanaged-Processes#LoadTheCLRFundamentals
*/
#pragma comment(lib, "mscoree.lib")

int main()
{
	ICLRMetaHost *metaHost = NULL;
	IEnumUnknown *runtime = NULL;
	HRESULT hr;

	if (CLRCreateInstance(CLSID_CLRMetaHost, IID_ICLRMetaHost, (LPVOID*)&metaHost) != S_OK) {
		printf("[x] Error: CLRCreateInstance(..)\n");
		return 2;
	}

	if (metaHost->EnumerateInstalledRuntimes(&runtime) != S_OK) {
		printf("[x] Error: EnumerateInstalledRuntimes(..)\n");
		return 2;
	}

	LPWSTR frameworkName = (LPWSTR)LocalAlloc(LPTR, 2048);
	if (frameworkName == NULL) {
		printf("[x] Error: malloc could not allocate\n");
		return 2;
	}

	// Enumerate through runtimes and show supported frameworks
	IUnknown *enumRuntime;
	ICLRRuntimeInfo *runtimeInfo;
	DWORD bytes;
	while (runtime->Next(1, &enumRuntime, 0) == S_OK) {
		if (enumRuntime->QueryInterface<ICLRRuntimeInfo>(&runtimeInfo) == S_OK) {
			if (runtimeInfo != NULL) {
				runtimeInfo->GetVersionString(frameworkName, &bytes);
				wprintf(L"[*] Supported Framework: %s\n", frameworkName);
			}
		}
	}

	//hr = metaHost->GetRuntime(L"v4.0.30319", IID_PPV_ARGS(&runtimeInfo));


	// For demo, we just use the last supported runtime
	ICLRRuntimeHost *runtimeHost;
	if (runtimeInfo->GetInterface(CLSID_CLRRuntimeHost, IID_ICLRRuntimeHost, (LPVOID*)&runtimeHost) != S_OK) {
		printf("[x] ..GetInterface(CLSID_CLRRuntimeHost...) failed\n");
		return 2;
	}

	// Start runtime, and load our assembly
	hr = runtimeHost->Start();	
	
	printf("[*] ======= Calling .NET Code =======\n\n");
	DWORD returnValue;
	if (hr = runtimeHost->ExecuteInDefaultAppDomain(
		L"D:\\Projects\\unmanaged_clr\\staged_assembly\\staged_assembly\\bin\\Release\\staged_assembly.dll",
		L"staged_assembly.Program",
		L"Xest",
		//L"EntryPoint",
		L"ASD",
		&returnValue
	) != S_OK) {
		printf("[x] Error: ExecuteInDefaultAppDomain(..) failed: %08x\n", hr);
		return 2;
	}
	printf("[*] ======= Done =======\n");
	printf("Result: %d\n", returnValue);

	runtimeInfo->Release();
	metaHost->Release();	
	runtimeHost->Release();
    return 0;
}


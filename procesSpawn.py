#https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw
#https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-process_information
#https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfoa

import ctypes

from ctypes.wintypes import HANDLE, DWORD, LPWSTR, WORD, LPBYTE #could also use the ctypes.c_ulong if you wanted
k_handle = ctypes.WinDLL("Kernel32.dll")

#While they are structs in C, you implement them as classes in python.
#he started by defining the structure from the create process doc that catches the return information
class PROCESS_INFORMATION(ctypes.Structure): #can be named anything you want.  Here we inherit from ctypes.Structure
    #we need to pass the info to the stuct, so we use a tuple/list known as _fields_
    _fields_ = [
        #create a tuple with the items we want
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessID", DWORD), 
        ("ddwThreadId", DWORD)
    ]

#to instantiate a process handler function, you just assign it to a variable
#p_handle = PROCESS_INFORMATION()
class STARTUPINFO(ctypes.Structure): 
    _fields_ = [
        #create a tuple with the items we want
        ("cb", DWORD),
        ("lpReserved", LPWSTR),
        ("lpDesktop", LPWSTR), 
        ("lpTitle", LPWSTR),        
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput", HANDLE),
        ("hStdError", DWORD),
    ]

#set up the parameters for the CreateProcessW
lpApplicationName = "C:\\Windows\\System32\\cmd.exe"
lpCommandLine = None
lpProcessAttributes = None
lpThreadAttributes = None
bInheritHandles = False
dwCreationFlags = 0x00000010 #flag for "Create new console"
lpEnvironment = None
lpCurrentDirectory = None
lpStartupInfo = STARTUPINFO()
lpProcessInformation = PROCESS_INFORMATION() #this is where the returned data is stored

#setup the startupinfo information 
lpStartupInfo.wShowWindow = 0x1
lpStartupInfo.dwFlags = 0x1

#execute the call
#parameter order matters, so stick to the API
response = k_handle.CreateProcessW(
    lpApplicationName,
    lpCommandLine,
    lpProcessAttributes,
    lpThreadAttributes,
    bInheritHandles, 
    dwCreationFlags,
    lpEnvironment,
    lpCurrentDirectory,
    ctypes.byref(lpStartupInfo), #passing a pointer to the structure
    ctypes.byref(lpProcessInformation)
)

if response > 0:
    print("Proc is running")
else:
    print("Failed.  Error Code: {0}".format(k_handle.GetLastError()))


#try to read info from the struct
print(lpProcessInformation.dwProcessID)
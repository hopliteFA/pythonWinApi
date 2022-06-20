#https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess
#https://docs.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights
#https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-

import ctypes

k_handle = ctypes.WinDLL("Kernel32.dll")

#ask the user for the PID for the process they want a handle to.  Convert to int and hex.
userPID = hex(int(input("Enter the PID you would like a handle to:  ")))
print(userPID)

#To assign the access rights, you would normally have to create a long list of hex with
#all the values you want OR'd together.  However, there is a shortcut to give you blanket 
#permissions of PROCESS_ALL_ACCESS.  It is actually listed in the API docs.

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFFF)

#setup the parameters for the OpenProcess call
dwDesiredAccess = PROCESS_ALL_ACCESS
bInheritHandle = False
#you get this from the PID of the process you want, but must convert it from dec to hex
dwProcessId = userPID

response = k_handle.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId)

print(response)

error = k_handle.GetLastError()

if error != 0:
    print ("Error Code: {0}".format(error))
    #exit(1)

if response <= 0:
    print("A handle was not created.")
else:
    print("A handle was created {}".format(response))
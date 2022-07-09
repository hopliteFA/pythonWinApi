#using the windows API and python, get a window and kill the process that owns it
#you will need 
#FindWindowA - User32.dll
#GetWIndowThreadProcessId - User32.dll
#OpenProcess - Kernel32.dll
#TerminateProcess 

import ctypes

user_handle = ctypes.WinDLL("User32.dll")
k_handle = ctypes.WinDLL("Kernel32.dll")

#set permissions
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFFF)

#******************GET THE WINDOWS HANDLE - FindWindowA***************************

lpClassName = None

#I had to cheat here and watch the video.  Since it expects a pointer, you have to look up 
#the ctypes constant using the github cheat sheet (cpython/Lib/ctypes/wintypes.py).  
#In this case LPCSTR requires you to call ctypes.c_char_p("input_string"). 
#Further, you can't pass the string directly until it is converted to utf-8
lpWindowName = ctypes.c_char_p(("Task Manager").encode('utf-8'))
print(lpWindowName)

windowHandle = user_handle.FindWindowA(lpClassName, lpWindowName)

if windowHandle == 0:
    print ("Failed to get window handle.  Error Code: {0}".format(k_handle.GetLastError()))
    exit(1)
else:
    print("Got Handle:  " + str(windowHandle))

#***********GET THE THREAD PROCESS ID - GetWIndowThreadProcessId ***************************

#call takes in a HWND (Window Handle) and a pointer variable to update; returns a DWORD pointer

lpdwProcessId = ctypes.c_ulong() #used the wintypes sheet from GH to get a DWORD to pass to the function call

#A lot to be desired in the course right now.  Since it expects a pointer, we have to pass the variable by reference
threadProcessID = user_handle.GetWindowThreadProcessId(windowHandle, ctypes.byref(lpdwProcessId))

if threadProcessID == 0:
    print ("Failed to get Thread ID.  Error Code: {0}".format(k_handle.GetLastError()))
    exit(1)
else:
    print("Got ThreadID:  " + str(threadProcessID))

#***********Open the process - OpenProcess  ***************************

dwDesiredAccess = PROCESS_ALL_ACCESS
bInheritHandle = False
dwProcessId = lpdwProcessId

hProcess = k_handle.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId)

error = k_handle.GetLastError()

if error != 0:
    print ("Failed to open process.  Error Code: {0}".format(error))
    #exit(1)
else:
    print("Successfully opened the process")

#***********Terminate the process - TerminateProcess  ***************************

#Takes a handle (hProcess) and a unit (uExitCode) and returns a bool

terminateResponse = k_handle.TerminateProcess(hProcess, 0) #set the exit code to 0 so the OS knows it was successful

terminateError = k_handle.GetLastError()


if terminateError != 0:
    print ("Failed to terminate the process.  Error Code: {0}".format(error))
    #exit(1)
else:
    print("Successfully terminated the process")
import ctypes

#how you import the dll that holds the the api call you want
user_handle = ctypes.WinDLL("User32.dll") #contains the MessageBox call
k_handle = ctypes.WinDLL("Kernel32.dll") #contains the GetLastError call for error handling

hWnd = None
lpText = "Hello World"
lpCaption = "Hello Students!"
uType = 0x00000001

#if you just want to run it, you can use user_handle.MessageBoxW(parameters)
#however, we want to catch the response and know what the user clicked
response = user_handle.MessageBoxW(hWnd, lpText, lpCaption, uType)

error = k_handle.GetLastError()

if error != 0:
    print("Error Code: (0)".format(error))
    exit(1)

if response == 1:
    print("The user clicked OK")
elif response == 2:
    print("The user clicked CANCEL")


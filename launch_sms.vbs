Set objShell = CreateObject("WScript.Shell")
strPath = objShell.CurrentDirectory
objShell.Run "pythonw.exe """ & strPath & "\sms.py""", 0, False

Set objShell = CreateObject("WScript.Shell")
strPath = objShell.CurrentDirectory & "\sms.py"
objShell.Run "python """ & strPath & """", 0, False

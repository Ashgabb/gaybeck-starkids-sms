' Gaybeck Starkids SMS - Silent Launcher
' This script runs the SMS application without showing any console windows

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this VBS file is located
strScriptPath = WScript.ScriptFullName
strScriptDir = objFSO.GetParentFolderName(strScriptPath)
strAppPath = objFSO.BuildPath(strScriptDir, "sms.py")

' Run the application with pythonw.exe (no console)
' 0 = hidden window, False = don't wait for completion
objShell.Run "pythonw.exe """ & strAppPath & """", 0, False


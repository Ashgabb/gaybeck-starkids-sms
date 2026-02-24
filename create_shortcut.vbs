Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\Gaybeck Starkids SMS.lnk"
strPath = oWS.CurrentDirectory
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "wscript.exe"
oLink.Arguments = """" & strPath & "\launch_sms.vbs"""
oLink.WorkingDirectory = strPath
oLink.Description = "Gaybeck Starkids School Management System"
oLink.IconLocation = strPath & "\sms_icon.ico"
oLink.Save
WScript.Echo "Desktop shortcut created successfully!"

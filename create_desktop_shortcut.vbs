' ============================================================================
' GAYBECK STARKIDS SMS - CREATE DESKTOP SHORTCUT
'
' If the desktop shortcut was not created during setup, run this file
' to manually create the shortcut
' ============================================================================

Set objWS = WScript.CreateObject("WScript.Shell")

' Get the folder where this script is located
strScriptPath = WScript.ScriptFullName
Set objFSO = CreateObject("Scripting.FileSystemObject")
strAppFolder = objFSO.GetParentFolderName(strScriptPath)

' Check if sms_icon.ico exists
If objFSO.FileExists(strAppFolder & "\sms_icon.ico") Then
    strIconPath = strAppFolder & "\sms_icon.ico"
Else
    strIconPath = ""
End If

' Get Desktop folder
strDesktop = objWS.SpecialFolders("Desktop")

' Create the shortcut
strShortcutPath = strDesktop & "\Gaybeck Starkids SMS.lnk"
Set objShortcut = objWS.CreateShortcut(strShortcutPath)

objShortcut.TargetPath = strAppFolder & "\launch_sms.bat"
objShortcut.WorkingDirectory = strAppFolder
objShortcut.Description = "Gaybeck Starkids School Management System"
objShortcut.WindowStyle = 1

' Set icon if it exists
If strIconPath <> "" Then
    objShortcut.IconLocation = strIconPath
End If

objShortcut.Save

' Show success message
MsgBox "Desktop shortcut created successfully!" & vbCrLf & vbCrLf & _
        "Look for 'Gaybeck Starkids SMS' on your desktop.", _
        vbInformation, "Shortcut Created"

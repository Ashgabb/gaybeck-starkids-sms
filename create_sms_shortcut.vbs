' ============================================================================
' GAYBECK STARKIDS SMS - CREATE DESKTOP SHORTCUT (Enhanced Version)
' 
' This script creates a desktop shortcut for the SMS application
' If run manually, it creates a shortcut on your desktop
' ============================================================================

On Error Resume Next

Set objWS = WScript.CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the folder where this script is located
strScriptPath = WScript.ScriptFullName
strAppFolder = objFSO.GetParentFolderName(strScriptPath)

' Check if the launcher batch file exists
If Not objFSO.FileExists(strAppFolder & "\sms_launcher.bat") Then
    WScript.Echo "Error: sms_launcher.bat not found in " & strAppFolder
    WScript.Quit 1
End If

' Resolve the icon path
strIconPath = ""
If objFSO.FileExists(strAppFolder & "\sms_icon.ico") Then
    strIconPath = strAppFolder & "\sms_icon.ico"
ElseIf objFSO.FileExists(strAppFolder & "\sms_icon.png") Then
    strIconPath = strAppFolder & "\sms_icon.png"
End If

' Get Desktop folder
strDesktop = objWS.SpecialFolders("Desktop")

' Check if shortcut already exists
strShortcutPath = strDesktop & "\Gaybeck Starkids SMS.lnk"
If objFSO.FileExists(strShortcutPath) Then
    iConfirm = MsgBox("Shortcut already exists. Do you want to replace it?", vbYesNo + vbQuestion, "Gaybeck SMS")
    If iConfirm <> vbYes Then
        WScript.Quit 0
    End If
    objFSO.DeleteFile strShortcutPath, True
End If

' Create the shortcut
On Error Resume Next
Set objShortcut = objWS.CreateShortcut(strShortcutPath)

With objShortcut
    .TargetPath = strAppFolder & "\sms_launcher.bat"
    .WorkingDirectory = strAppFolder
    .Description = "Gaybeck Starkids School Management System"
    .WindowStyle = 1  ' Normal window
    .Hotkey = ""  ' No hotkey by default
    
    ' Set icon if found
    If strIconPath <> "" Then
        .IconLocation = strIconPath
    End If
End With

objShortcut.Save

If Err.Number = 0 Then
    MsgBox "Desktop shortcut created successfully!" & vbCrLf & vbCrLf & _
            "✓ Look for 'Gaybeck Starkids SMS' on your desktop." & vbCrLf & _
            "✓ You can now launch the application from the desktop." & vbCrLf & vbCrLf & _
            "Working Directory: " & strAppFolder, _
            vbInformation, "Success"
    WScript.Quit 0
Else
    MsgBox "Failed to create shortcut:" & vbCrLf & Err.Description, _
            vbCritical, "Error"
    WScript.Quit 1
End If

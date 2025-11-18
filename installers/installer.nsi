; Gaybeck Starkids SMS Installer Script
; Version: 3.0.0
; Date: November 17, 2025
; Features: Auto version detection, upgrade/removal, dependency installation, icon setup

#include "MUI2.nsh"
#include "x64.nsh"
#include "LogicLib.nsh"

; Define constants
!define PRODUCT_NAME "Gaybeck Starkids SMS"
!define PRODUCT_VERSION "3.0.0"
!define PRODUCT_PUBLISHER "Gaybeck Starkids School"
!define PRODUCT_WEB_SITE "https://www.gaybeckstarkids.edu"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PYTHON_VERSION "3.13"
!define INSTALL_LOCATION "$PROGRAMFILES\${PRODUCT_NAME}"

; Name and file
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "Gaybeck_Starkids_SMS_v3.0.0_Setup.exe"
InstallDir "${INSTALL_LOCATION}"

; Settings
SetCompress off
ShowInstDetails show
ShowUninstDetails show
RequestExecutionLevel admin

; MUI Settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

; Variables
Var PythonExe
Var ExistingInstall
Var ExistingVersion
Var UpgradeChoice

; Functions
Function .onInit
  SetShellVarContext all
  
  ; Check for existing installation
  ReadRegStr $ExistingInstall "${PRODUCT_UNINST_ROOT_KEY}" "${PRODUCT_UNINST_KEY}" "InstallLocation"
  
  ${If} $ExistingInstall != ""
    ReadRegStr $ExistingVersion "${PRODUCT_UNINST_ROOT_KEY}" "${PRODUCT_UNINST_KEY}" "DisplayVersion"
    
    ; Show upgrade/remove dialog
    MessageBox MB_YESNOCANCEL "$(^NameDA) version $ExistingVersion is already installed.$\n$\nYes: Upgrade to ${PRODUCT_VERSION}$\nNo: Remove and perform clean install$\nCancel: Cancel installation" \
      IDYES UpgradeInstall IDNO RemoveInstall
    
    ; Cancel was clicked
    Abort "Installation cancelled by user"
    
    UpgradeInstall:
      StrCpy $UpgradeChoice "upgrade"
      Goto ContinueInit
    
    RemoveInstall:
      StrCpy $UpgradeChoice "remove"
      ; Execute uninstaller
      ExecWait '"$ExistingInstall\Uninstall.exe" /S'
      Sleep 2000
  ${EndIf}
  
  ContinueInit:
  ; Check for Python
  ${If} ${RunningX64}
    SetRegView 64
  ${EndIf}
  
  ReadRegStr $PythonExe HKLM "Software\Python\PythonCore\${PYTHON_VERSION}\InstallPath" ""
  ${If} $PythonExe == ""
    ReadRegStr $PythonExe HKCU "Software\Python\PythonCore\${PYTHON_VERSION}\InstallPath" ""
  ${EndIf}
  
  ${If} $PythonExe == ""
    MessageBox MB_OK "Python ${PYTHON_VERSION} is not installed. Please install Python ${PYTHON_VERSION} first from https://www.python.org"
    Abort "Python ${PYTHON_VERSION} required"
  ${EndIf}
FunctionEnd

Section "Install Application"
  SetOutPath "$INSTDIR"
  
  ; Copy application files
  File /r "sms.py"
  File /r "advanced_ai_analytics.py"
  File /r "requirements.txt"
  File /r "database\*.*"
  File /r "docs\*.*"
  File /r "scripts\*.*"
  File /r "logo.png"
  File /r "icon.ico"
  
  ; Create .venv if not exists
  ${If} $UpgradeChoice == "upgrade"
    DetailPrint "Skipping virtual environment (keeping existing)"
  ${Else}
    DetailPrint "Creating Python virtual environment..."
    nsExec::ExecToLog '"$PythonExe\python.exe" -m venv "$INSTDIR\.venv"'
  ${EndIf}
  
  ; Install dependencies
  DetailPrint "Installing Python dependencies..."
  nsExec::ExecToLog '"$INSTDIR\.venv\Scripts\pip.exe" install --upgrade pip'
  nsExec::ExecToLog '"$INSTDIR\.venv\Scripts\pip.exe" install -r "$INSTDIR\requirements.txt"'
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Write registry keys
  WriteRegStr "${PRODUCT_UNINST_ROOT_KEY}" "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr "${PRODUCT_UNINST_ROOT_KEY}" "${PRODUCT_UNINST_KEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr "${PRODUCT_UNINST_ROOT_KEY}" "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr "${PRODUCT_UNINST_ROOT_KEY}" "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr "${PRODUCT_UNINST_ROOT_KEY}" "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\icon.ico"
  WriteRegStr "${PRODUCT_UNINST_ROOT_KEY}" "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr "${PRODUCT_UNINST_ROOT_KEY}" "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
SectionEnd

Section "Create Desktop Shortcut"
  DetailPrint "Creating desktop shortcut..."
  
  ; Get desktop path
  SetShellVarContext all
  
  ; Create shortcut
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortCut "$DESKTOP\${PRODUCT_NAME}.lnk" \
    "$INSTDIR\.venv\Scripts\pythonw.exe" \
    '$INSTDIR\sms.py' \
    "$INSTDIR\icon.ico" \
    0 SW_SHOWNORMAL
  
  DetailPrint "Desktop shortcut created: $DESKTOP\${PRODUCT_NAME}.lnk"
SectionEnd

Section "Create Start Menu Shortcuts"
  DetailPrint "Creating Start Menu shortcuts..."
  
  SetShellVarContext all
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  
  ; Main application shortcut
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" \
    "$INSTDIR\.venv\Scripts\pythonw.exe" \
    '$INSTDIR\sms.py' \
    "$INSTDIR\icon.ico" \
    0 SW_SHOWNORMAL
  
  ; Documentation shortcut
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Documentation.lnk" \
    "$INSTDIR\docs\AI_FEATURES_GUIDE.md"
  
  ; Uninstall shortcut
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk" \
    "$INSTDIR\Uninstall.exe"
  
  DetailPrint "Start Menu shortcuts created"
SectionEnd

Section "Create Taskbar Shortcut"
  DetailPrint "Creating taskbar shortcut..."
  
  ; Pin to taskbar using registry/VBS (Windows 7+)
  ; Note: Taskbar pinning requires Windows API calls which aren't directly available in NSIS
  ; We'll create a batch script to handle this
  
  FileOpen $0 "$INSTDIR\PinToTaskbar.vbs" w
  FileWrite $0 "Set objArgs = WScript.Arguments$\r$\n"
  FileWrite $0 "Set objFSO = CreateObject('Scripting.FileSystemObject')$\r$\n"
  FileWrite $0 "Set objShell = CreateObject('Shell.Application')$\r$\n"
  FileWrite $0 "$\r$\n"
  FileWrite $0 "strPath = objArgs(0)$\r$\n"
  FileWrite $0 "$\r$\n"
  FileWrite $0 "Set objFolder = objShell.NameSpace(objFSO.GetParentFolderName(strPath))$\r$\n"
  FileWrite $0 "Set objFile = objFolder.ParseName(objFSO.GetBaseName(strPath) & '.lnk')$\r$\n"
  FileWrite $0 "$\r$\n"
  FileWrite $0 "Set colVerbs = objFile.Verbs$\r$\n"
  FileWrite $0 "For Each objVerb In colVerbs$\r$\n"
  FileWrite $0 "    If Replace(objVerb.Name, '&', '') = 'Pin to Taskbar' Then$\r$\n"
  FileWrite $0 "        objVerb.DoIt$\r$\n"
  FileWrite $0 "    End If$\r$\n"
  FileWrite $0 "Next$\r$\n"
  FileClose $0
  
  ; Execute VBS to pin to taskbar
  nsExec::ExecToLog 'cscript.exe "$INSTDIR\PinToTaskbar.vbs" "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk"'
  
  DetailPrint "Taskbar shortcut created"
SectionEnd

Section "Uninstall"
  ; Remove application files
  RMDir /r "$INSTDIR"
  
  ; Remove shortcuts
  RMDir /r "$SMPROGRAMS\${PRODUCT_NAME}"
  Delete "$DESKTOP\${PRODUCT_NAME}.lnk"
  
  ; Remove registry keys
  DeleteRegKey "${PRODUCT_UNINST_ROOT_KEY}" "${PRODUCT_UNINST_KEY}"
  
  MessageBox MB_OK "${PRODUCT_NAME} has been uninstalled successfully."
SectionEnd

; Section descriptions
LangString DESC_Install ${LANG_ENGLISH} "Install the application files and dependencies"
LangString DESC_Desktop ${LANG_ENGLISH} "Create a shortcut on the desktop"
LangString DESC_StartMenu ${LANG_ENGLISH} "Create shortcuts in the Start Menu"
LangString DESC_Taskbar ${LANG_ENGLISH} "Pin application to the taskbar"

; Assign descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
!insertmacro MUI_DESCRIPTION_TEXT ${Install} $(DESC_Install)
!insertmacro MUI_DESCRIPTION_TEXT ${Desktop} $(DESC_Desktop)
!insertmacro MUI_DESCRIPTION_TEXT ${StartMenu} $(DESC_StartMenu)
!insertmacro MUI_DESCRIPTION_TEXT ${Taskbar} $(DESC_Taskbar)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

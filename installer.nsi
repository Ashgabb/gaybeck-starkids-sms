; NSIS Installer Script for Gaybeck Starkids SMS
; Creates professional Windows installer (.exe)
; 
; Install NSIS from: https://nsis.sourceforge.io
; Then: makensis installer.nsi

!include "MUI2.nsh"
!include "x64.nsh"

; Application Information
!define APP_NAME "Gaybeck Starkids SMS"
!define APP_VERSION "2.0.3"
!define APP_PUBLISHER "Gaybeck Starkids School"
!define APP_URL "https://www.gaybeckstarkids.com"
!define APP_EXECUTABLE "GaybeckStarKidsSMS.exe"
!define INSTALL_SIZE 250000

; Installer Settings
Name "${APP_NAME} ${APP_VERSION}"
OutFile "GaybeckStarKidsSMS_Installer_${APP_VERSION}.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKCU "Software\${APP_NAME}" ""
RequestExecutionLevel admin

; MUI Settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "French"
!insertmacro MUI_LANGUAGE "German"
!insertmacro MUI_LANGUAGE "Spanish"

; Installer Section
Section "Install"
    SetOutPath "$INSTDIR"
    
    ; Copy application files
    File /r "dist\GaybeckStarKidsSMS\*.*"
    
    ; Create start menu shortcuts
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}" "" "$INSTDIR\${APP_EXECUTABLE}" 0
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
    
    ; Create desktop shortcut
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}" "" "$INSTDIR\${APP_EXECUTABLE}" 0
    
    ; Register uninstaller
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME} ${APP_VERSION}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "EstimatedSize" ${INSTALL_SIZE}
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

; Uninstaller Section
Section "Uninstall"
    ; Delete shortcuts
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    
    ; Delete files
    RMDir /r "$INSTDIR"
    
    ; Delete registry entries
    DeleteRegKey HKCU "Software\${APP_NAME}"
    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
SectionEnd

; Function to validate destination directory
Function .onVerifyInstDir
    IfFileExists "$INSTDIR\*.*" 0 +2
    Abort "This directory already contains ${APP_NAME}. Please choose another directory."
FunctionEnd

; Function to show read me
Function .onInstSuccess
    MessageBox MB_YESNO "Installation successful!$\n$\nWould you like to run ${APP_NAME} now?" IDNO +2
    Exec "$INSTDIR\${APP_EXECUTABLE}"
FunctionEnd

; ========================================================================
; NSIS Installer Script for Gaybeck Starkids SMS
; ========================================================================
; Creates a professional Windows installer (.exe) for non-technical users
;
; Installation Instructions:
;   1. Install NSIS from: https://nsis.sourceforge.io/download
;   2. Run: CREATE_INSTALLER.bat
;      OR
;   3. Run: makensis /V2 installer.nsi
;
; The script will create: GaybeckStarKidsSMS_Installer_2.0.3.exe
; ========================================================================

!include "MUI2.nsh"
!include "x64.nsh"
!include "LogicLib.nsh"

; ========================================================================
; APPLICATION INFORMATION
; ========================================================================
!define APP_NAME "Gaybeck Starkids SMS"
!define APP_VERSION "2.0.3"
!define APP_PUBLISHER "Gaybeck Starkids School"
!define APP_WEBSITE "https://www.gaybeckstarkids.com"
!define APP_EXECUTABLE "GaybeckStarKidsSMS.exe"
!define INSTALL_SIZE 250000
!define UNINSTALL_NAME "Uninstall $(^Name)"

; ========================================================================
; INSTALLER CONFIGURATION
; ========================================================================
Name "${APP_NAME} ${APP_VERSION}"
OutFile "GaybeckStarKidsSMS_Installer_${APP_VERSION}.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKCU "Software\${APP_NAME}" "InstallDir"

; Request admin privileges for Windows Vista and later
RequestExecutionLevel admin

; Compression ratio
SetCompress auto
SetCompressor /SOLID lzma
SetDatablockOptimize on

; ========================================================================
; VISUAL SETTINGS
; ========================================================================
; Modern UI with custom branding
!define MUI_ABORTWARNING
!define MUI_ICON "sms_icon.ico"
!define MUI_UNICON "sms_icon.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "logo.png"
!define MUI_WELCOMEFINISHPAGE_BITMAP "logo.png"

; Colors for modern look
!define MUI_TEXTCOLOR 000000
!define MUI_BGCOLOR FFFFFF

; ========================================================================
; MUI PAGES (Installation Wizard Pages)
; ========================================================================

; Welcome page
!insertmacro MUI_PAGE_WELCOME

; License agreement page
; !insertmacro MUI_PAGE_LICENSE "LICENSE.txt"

; Installation folder page
!insertmacro MUI_PAGE_DIRECTORY

; Installation progress page
!insertmacro MUI_PAGE_INSTFILES

; Finish page with run option
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APP_EXECUTABLE}"
!define MUI_FINISHPAGE_RUN_TEXT "Launch ${APP_NAME} now"
!define MUI_FINISHPAGE_LINK "Visit Website"
!define MUI_FINISHPAGE_LINK_LOCATION "${APP_WEBSITE}"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; ========================================================================
; LANGUAGE SUPPORT
; ========================================================================
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "French"
!insertmacro MUI_LANGUAGE "German"
!insertmacro MUI_LANGUAGE "Spanish"
!insertmacro MUI_LANGUAGE "Portuguese"
!insertmacro MUI_LANGUAGE "Russian"

; ========================================================================
; INSTALLER SECTION - Main Installation
; ========================================================================
Section "Install"
    SetOutPath "$INSTDIR"
    SetOverwrite ifnewer
    
    ; Display status message
    DetailPrint "Installing ${APP_NAME} ${APP_VERSION}..."
    
    ; Copy all application files from build output
    ${If} ${FileExists} "dist\GaybeckStarKidsSMS\*.*"
        File /r "dist\GaybeckStarKidsSMS\*.*"
        DetailPrint "Application files installed"
    ${Else}
        MessageBox MB_OK|MB_ICONEXCLAMATION \
            "Error: Application files not found in dist\GaybeckStarKidsSMS\$\nPlease run CREATE_INSTALLER.bat first."
        Abort "Installation failed"
    ${EndIf}
    
    ; Create database directory if it doesn't exist
    CreateDirectory "$INSTDIR\database"
    CreateDirectory "$INSTDIR\database_backups"
    CreateDirectory "$INSTDIR\backups"
    CreateDirectory "$INSTDIR\restore_points"
    
    ; Store installation folder for uninstaller
    WriteRegStr HKCU "Software\${APP_NAME}" "InstallDir" "$INSTDIR"
    
    ; Create Start Menu shortcuts
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" \
        "$INSTDIR\${APP_EXECUTABLE}" \
        "" \
        "$INSTDIR\${APP_EXECUTABLE}" \
        0 \
        SW_SHOWNORMAL \
        "" \
        "School Management System"
    
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall ${APP_NAME}.lnk" \
        "$INSTDIR\uninstall.exe" \
        "" \
        "$INSTDIR\uninstall.exe" \
        0
    
    ; Create Desktop shortcut (optional)
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" \
        "$INSTDIR\${APP_EXECUTABLE}" \
        "" \
        "$INSTDIR\${APP_EXECUTABLE}" \
        0 \
        SW_SHOWNORMAL
    
    ; Register with Windows Control Panel
    DetailPrint "Registering application with Windows..."
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "DisplayName" "${APP_NAME} ${APP_VERSION}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "DisplayVersion" "${APP_VERSION}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "URLInfoAbout" "${APP_WEBSITE}"
    WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
        "EstimatedSize" ${INSTALL_SIZE}
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    DetailPrint "Installation complete!"
SectionEnd

; ========================================================================
; UNINSTALLER SECTION
; ========================================================================
Section "Uninstall"
    DetailPrint "Removing ${APP_NAME}..."
    
    ; Delete Start Menu shortcuts
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Uninstall ${APP_NAME}.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    
    ; Delete Desktop shortcut
    Delete "$DESKTOP\${APP_NAME}.lnk"
    
    ; Delete installation directory
    RMDir /r "$INSTDIR"
    
    ; Remove registry entries
    DeleteRegKey HKCU "Software\${APP_NAME}"
    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    
    DetailPrint "Uninstallation complete!"
SectionEnd

; ========================================================================
; INITIALIZATION FUNCTION
; ========================================================================
Function .onInit
    ; Initialize installation
    SetShellVarContext all
    
    ; Check if running on Windows 7 or later
    ${If} ${IsWinVista}
    ${Else}
        MessageBox MB_OK|MB_ICONEXCLAMATION \
            "${APP_NAME} requires Windows Vista or later."
        Quit
    ${EndIf}
    
    ; Check available disk space (minimum 500 MB)
    ${DriveSpace} "$INSTDIR" /S=M /D=size
    ${If} $size < 500
        MessageBox MB_OK|MB_ICONEXCLAMATION \
            "Insufficient disk space. At least 500 MB is required."
        Quit
    ${EndIf}
FunctionEnd

; ========================================================================
; INSTALL VERIFICATION FUNCTION
; ========================================================================
Function .onVerifyInstDir
    ; Check if directory is empty before allowing installation
    ${If} ${FileExists} "$INSTDIR\${APP_EXECUTABLE}"
        MessageBox MB_YESNO \
            "${APP_NAME} appears to be already installed in this location.$\n$\nClick Yes to overwrite, or No to choose a different directory." \
            IDYES skip_check
        Abort
    skip_check:
    ${EndIf}
FunctionEnd

; ========================================================================
; POST-INSTALLATION FUNCTION
; ========================================================================
Function .onInstSuccess
    MessageBox MB_YESNO \
        "Installation completed successfully!$\n$\nWould you like to launch ${APP_NAME} now?" \
        IDNO skip_run
    
    Exec "$INSTDIR\${APP_EXECUTABLE}"
    skip_run:
FunctionEnd

; ========================================================================
; UNINSTALL INITIALIZATION
; ========================================================================
Function un.onInit
    MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 \
        "Are you sure you want to completely remove ${APP_NAME} and all its components?" \
        IDYES proceed_uninstall
    Abort
    proceed_uninstall:
FunctionEnd

; ========================================================================
; END OF INSTALLER SCRIPT
; ========================================================================

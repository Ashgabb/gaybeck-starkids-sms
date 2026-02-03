# Gaybeck Starkids SMS - Administrator Deployment Guide

## Overview

This guide helps IT administrators and tech-savvy staff deploy the Gaybeck Starkids SMS application to school computers.

---

## 🎯 Deployment Methods

### **Method 1: Single File Distribution (Simplest)**

```powershell
# For each user computer:
1. Copy: GaybeckStarKidsSMS_Installer_2.0.3.exe
2. Run the installer
3. Complete the wizard
```

**Time per computer:** 3-5 minutes  
**User complexity:** Minimal (point-and-click)

### **Method 2: Batch Deployment (Windows Domain)**

If your school uses Active Directory:

```batch
@echo off
REM Deploy to multiple computers on domain

REM Run on each computer (via GPO or remote script):
"\\server\installers\GaybeckStarKidsSMS_Installer_2.0.3.exe" /S
```

**Time per computer:** 2-3 minutes (automated)  
**Requires:** Domain admin access

### **Method 3: Network Share Installation**

```batch
REM Install from network share:
\\SchoolServer\Software\GaybeckStarKidsSMS_Installer_2.0.3.exe
```

---

## 📊 Deployment Checklist

### **Pre-Deployment**

- [ ] Create installer file (run `CREATE_INSTALLER.bat`)
- [ ] Test on 2-3 representative computers
- [ ] Verify database functionality
- [ ] Test all user roles (Admin, Teacher, Accountant)
- [ ] Create backup of working installation
- [ ] Document any custom configurations

### **Deployment**

- [ ] Copy installer to USB drives or network share
- [ ] Send deployment instructions to staff
- [ ] Monitor installation progress
- [ ] Create help desk ticket queue for support
- [ ] Track installation on all target computers

### **Post-Deployment**

- [ ] Verify successful installation on all computers
- [ ] Conduct user training sessions
- [ ] Monitor error logs in first week
- [ ] Provide IT support contact information
- [ ] Schedule follow-up meetings

---

## 🔧 Installation Command Reference

### **Interactive Installation**
```cmd
GaybeckStarKidsSMS_Installer_2.0.3.exe
```

### **Silent Installation** (No prompts)
```cmd
GaybeckStarKidsSMS_Installer_2.0.3.exe /S /D=C:\Program Files\Gaybeck Starkids SMS
```

### **Installation with Log File**
```cmd
GaybeckStarKidsSMS_Installer_2.0.3.exe /S /D=C:\Program Files\Gaybeck Starkids SMS /O "install.log"
```

---

## 📝 Network Deployment Script

### **Deploy to Multiple Computers (PowerShell)**

```powershell
# deployment.ps1
# Prerequisites: Run as Administrator

$installerPath = "\\SchoolServer\Installers\GaybeckStarKidsSMS_Installer_2.0.3.exe"
$computers = @(
    "COMPUTER01",
    "COMPUTER02",
    "COMPUTER03",
    "COMPUTER04",
    "COMPUTER05"
)

foreach ($computer in $computers) {
    Write-Host "Installing on $computer..." -ForegroundColor Yellow
    
    # Create session to remote computer
    $session = New-PSSession -ComputerName $computer
    
    # Copy installer
    Copy-Item -Path $installerPath -Destination "C:\Temp\" -ToSession $session
    
    # Run installer
    Invoke-Command -Session $session -ScriptBlock {
        & "C:\Temp\GaybeckStarKidsSMS_Installer_2.0.3.exe" /S /D="C:\Program Files\Gaybeck Starkids SMS"
        Start-Sleep -Seconds 60  # Wait for installation
    }
    
    # Verify installation
    $installed = Invoke-Command -Session $session -ScriptBlock {
        Test-Path "C:\Program Files\Gaybeck Starkids SMS\GaybeckStarKidsSMS.exe"
    }
    
    if ($installed) {
        Write-Host "✓ Installation successful on $computer" -ForegroundColor Green
    } else {
        Write-Host "✗ Installation failed on $computer" -ForegroundColor Red
    }
    
    # Cleanup
    Remove-PSSession -Session $session
}

Write-Host "Deployment complete!" -ForegroundColor Green
```

**Usage:**
```powershell
powershell -ExecutionPolicy Bypass -File deployment.ps1
```

---

## 🛡️ Security Considerations

### **Installation Permissions**

The installer requires:
- **Local Administrator rights** (to install in Program Files)
- **Windows 7 or later**

To allow standard users to install:
1. Create a shared installer folder: `\\SchoolServer\Installers\`
2. Grant read access to all users
3. Have administrator pre-stage the installation
4. Or use Group Policy for enterprise deployment

### **Data Protection**

After installation, ensure:
- [ ] Database folder access is restricted
- [ ] Regular backups are scheduled
- [ ] Antivirus software is configured to exclude database
- [ ] Windows Firewall allows local database access

### **Network Installation**

If hosting on network share:
- Use `\\ServerName\Share\installer.exe` (not mapped drives)
- Verify network connectivity before deployment
- Consider local copy to improve speed

---

## 🚨 Rollback Plan

### **If Installation Fails**

1. **Uninstall:**
   ```cmd
   GaybeckStarKidsSMS_Installer_2.0.3.exe /un
   OR
   Control Panel → Programs → Uninstall a program → Gaybeck Starkids SMS
   ```

2. **Restore backup:**
   - If database backup exists, restore from backup directory
   - Copy previous working database if available

3. **Retry Installation:**
   - Clear installation directory
   - Ensure sufficient disk space (500+ MB)
   - Check for antivirus interference
   - Run with administrator privileges

---

## 📈 Scaling Deployment

### **Small School (1-5 computers)**
- **Time:** 1-2 hours (manual installation on each)
- **Method:** Direct USB or file sharing
- **Support:** Email or phone support sufficient

### **Medium School (5-20 computers)**
- **Time:** 2-4 hours (batch installation)
- **Method:** Network share + PowerShell script
- **Support:** Create help desk queue, email support

### **Large School (20+ computers)**
- **Time:** 4-8 hours (full domain deployment)
- **Method:** Group Policy, WSUS, or MDM
- **Support:** 24/7 help desk recommended

---

## 📞 Deployment Support

### **Common Issues**

| Issue | Solution |
|-------|----------|
| "Administrator rights required" | Run installer as admin (right-click → Run as administrator) |
| "Python not found" | Ensure Python 3.13+ is installed on build computer only |
| "Installation path invalid" | Use full path: `C:\Program Files\Gaybeck Starkids SMS` |
| "Database locked" | Ensure application is closed on all other computers |
| "Disk space insufficient" | Free up 500 MB before installation |

### **Getting Support**

1. Check application logs: `C:\Program Files\Gaybeck Starkids SMS\logs\`
2. Review Windows Event Viewer for errors
3. Contact system administrator
4. Review installation guide for troubleshooting

---

## 📋 Documentation to Share with Users

When deploying, include:
- [ ] `INSTALLATION_FOR_USERS.md` (user-friendly guide)
- [ ] Quick reference card with login credentials
- [ ] Help desk contact information
- [ ] Password reset procedure
- [ ] Backup instruction card

---

## 🔄 Update Deployment

### **Rolling Out New Versions**

1. **Test new version** on non-production machine
2. **Create new installer** with `CREATE_INSTALLER.bat`
3. **Backup current database** on all machines
4. **Run new installer** (it will update existing installation)
5. **Verify functionality** on each machine
6. **Provide release notes** to users

### **Version Rollback**

If new version has issues:
1. Restore database backup
2. Uninstall current version
3. Install previous version
4. Test before resuming normal operations

---

## 📊 Deployment Report Template

```
DEPLOYMENT REPORT - Gaybeck Starkids SMS
=========================================

Date Deployed: _______________
Deployed By: _______________
Version: 2.0.3

Computers Deployed:
- COMPUTER01: Success / Fail
- COMPUTER02: Success / Fail
- COMPUTER03: Success / Fail
- COMPUTER04: Success / Fail
- COMPUTER05: Success / Fail

Total Deployed: _____
Successful: _____
Failed: _____
Success Rate: _____%

Issues Encountered:
1. _________________________________
2. _________________________________
3. _________________________________

Lessons Learned:
_________________________________
_________________________________

Next Steps:
_________________________________
_________________________________

Approved By: _______________
Date: _______________
```

---

## 🎓 User Training Guide

### **Pre-Training Setup**

1. Create user accounts (Admin, Teachers, Accountants)
2. Test login with each role
3. Prepare sample data (students, classes, fees)
4. Set up printer for report generation

### **Training Schedule Recommendation**

| Phase | Duration | Content |
|-------|----------|---------|
| **Week 1** | 2 hours | Basic navigation, login, interface tour |
| **Week 2** | 2 hours | Student management, fee collection |
| **Week 3** | 2 hours | Attendance, reports, backups |
| **Week 4** | 2 hours | Advanced features, troubleshooting |

### **Documentation for Users**

- Video tutorials (optional)
- Quick reference cards (print-friendly)
- Help desk contact info
- Troubleshooting guide

---

## 📞 Support Escalation

### **Level 1: Help Desk (School IT)**
- Password resets
- Installation issues
- Basic troubleshooting

### **Level 2: System Administrator**
- Database issues
- Network/connectivity
- Advanced configuration

### **Level 3: Application Support**
- Feature requests
- Bug reports
- Custom development

---

**Deployment Date:** _______________  
**Deployment Manager:** _______________  
**Support Contact:** _______________  
**Backup Location:** _______________  

---

*Last Updated: February 3, 2026*

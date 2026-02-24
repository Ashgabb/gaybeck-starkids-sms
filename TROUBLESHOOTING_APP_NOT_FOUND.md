# ⚠️ GAYBECK STARKIDS SMS - TROUBLESHOOTING: APP NOT FOUND

## Problem: "Setup completed but I can't find the application or desktop icon"

If `setup.bat` ran successfully but you can't see the app on your desktop, follow these solutions:

---

## ✅ SOLUTION 1: Quick Manual Launch

### Step 1: Open the Application Folder
- Open **File Explorer** (Windows folder icon on taskbar or press Windows+E)
- Navigate to: `Desktop` → `Gaybeck SMS` → `gaybeck-starkids-sms`

### Step 2: Find and Run the Launcher
- Look for the file: **`launch_sms.bat`**
- **Double-click it** to launch the application

### Step 3: Application Should Open
- The app will start
- Login screen will appear
- You're ready to use it!

---

## ✅ SOLUTION 2: Create Desktop Shortcut Manually

If you want a desktop icon, do this:

### Step 1: Locate Desktop Shortcut Creator
- Go back to the `gaybeck-starkids-sms` folder
- Look for: **`create_desktop_shortcut.vbs`**

### Step 2: Run the Shortcut Creator
- **Double-click** `create_desktop_shortcut.vbs`
- A small window might appear - click OK
- You should see a success message

### Step 3: Check Your Desktop
- Minimize windows or go to desktop
- Look for **"Gaybeck Starkids SMS"** icon
- **Double-click it** to launch the app

---

## ✅ SOLUTION 3: Re-run Setup

If neither solution works, run setup again:

### Step 1: Go Back to Application Folder
- Navigate to `Desktop` → `Gaybeck SMS` → `gaybeck-starkids-sms`
- Look for **`setup.bat`**

### Step 2: Run Setup Again
- **Right-click** `setup.bat`
- Select **"Run as Administrator"**
- Wait for it to complete

### Step 3: Try Desktop Icon Again
- After setup completes, check desktop for **"Gaybeck Starkids SMS"** icon
- If still not there, use Solution 2 above

---

## ✅ SOLUTION 4: Create Shortcut Manually in Windows

### Step 1: Create Shortcut
- Minimize all windows (see your desktop)
- **Right-click** on empty desktop space
- Select: **New** → **Shortcut**

### Step 2: Point to Application
- In the location box, type (or copy-paste):
  ```
  C:\Users\YOUR_USERNAME\Desktop\Gaybeck SMS\gaybeck-starkids-sms\launch_sms.bat
  ```
  *(Replace YOUR_USERNAME with your Windows username)*

### Step 3: Name It
- Name it: **Gaybeck Starkids SMS**
- Click **Finish**

### Step 4: Customize Icon (Optional)
- **Right-click** the new shortcut
- Select **Properties**
- Click **Change Icon**
- Navigate to the folder and select **sms_icon.ico**
- Click OK twice

### Step 5: Launch!
- **Double-click** the new shortcut to start the app

---

## ❓ COMMON REASONS APP CAN'T BE FOUND

| Reason | Solution |
|--------|----------|
| Setup didn't complete | Run setup.bat again |
| Shortcut creation failed | Use `create_desktop_shortcut.vbs` |
| Wrong folder | Verify you're in gaybeck-starkids-sms folder |
| Python not installed | Run setup.bat again |
| File permissions issue | Run setup as Administrator |

---

## 🔍 VERIFY INSTALLATION

### Check If Files Are There

1. **Open File Explorer**
2. Go to your gaybeck-starkids-sms folder
3. Look for these files:
   - ✓ `sms.py` (main application)
   - ✓ `launch_sms.bat` (launcher)
   - ✓ `create_desktop_shortcut.vbs` (shortcut creator)
   - ✓ `setup.bat` (setup script)
   - ✓ `sms_icon.ico` (application icon)
   - ✓ `school_management.db` (data file)

**If all files are there:** Setup was successful!  
**If files are missing:** Re-download or re-extract the package

---

## 📱 QUICK DESKTOP ICON TUTORIAL

### Creating Icon Using File Explorer

1. Go to: `C:\Users\[YourUsername]\Desktop\Gaybeck SMS\gaybeck-starkids-sms`
2. Right-click **`launch_sms.bat`**
3. Select **Send To** → **Desktop (create shortcut)**
4. Go to your desktop
5. Right-click the new shortcut
6. Select **Properties**
7. Click **Change Icon**
8. Select **sms_icon.ico** from the folder
9. Click **OK** twice

**Result:** Professional-looking icon on your desktop! 🎉

---

## ✨ RUNNING THE APP WITHOUT ICON

If you can't create the icon (no worries!), you can still use the app:

**Always available:**
- Go to: `Desktop` → `Gaybeck SMS` → `gaybeck-starkids-sms`
- Double-click **`launch_sms.bat`**
- App launches every time

This method works just as well, it just takes one extra click.

---

## 🆘 STILL HAVING ISSUES?

### Contact Support
- **Email:** support@gaybeckstarkids.com
- **Phone:** +233 XXX XXX XXX
- **Tell them:** Where you're stuck and which solution you tried

### Include This Information
- Screenshot of your error (if any)
- Folder where you extracted files
- Which solution attempts you've tried
- Your Windows version (Windows 10, 11, etc.)

---

## ✅ VERIFICATION CHECKLIST

Before contacting support, verify:

- [ ] I extracted ALL files from the package
- [ ] I ran setup.bat and it completed successfully
- [ ] I see "INSTALLATION COMPLETE" message
- [ ] Files exist in the gaybeck-starkids-sms folder
- [ ] I have administrator rights on my computer
- [ ] I tried at least one solution above
- [ ] I checked file locations carefully
- [ ] I restarted my computer (helps sometimes!)

---

## 🎉 SUCCESS!

Once you can launch the app:

1. ✅ Double-click `launch_sms.bat` (or the desktop icon)
2. ✅ Wait for login screen
3. ✅ Login with: **admin** / **admin123**
4. ✅ You're in! Follow QUICK_REFERENCE.md next

---

**Remember:** The most direct way to launch is always:  
**gaybeck-starkids-sms** folder → **launch_sms.bat** → Double-click

This works 100% of the time if Python is installed correctly.

**Need help? We're here!** support@gaybeckstarkids.com

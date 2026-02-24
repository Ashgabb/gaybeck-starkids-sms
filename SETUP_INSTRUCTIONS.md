# 🎓 GAYBECK STARKIDS SMS - SETUP INSTRUCTIONS

## For Non-Technical Users

Welcome! These instructions will guide you through setting up Gaybeck Starkids SMS on your computer.

**Time Required:** 10-15 minutes  
**Technical Level:** No experience needed

---

## ✅ BEFORE YOU START

Make sure you have:
- [ ] This folder on your computer
- [ ] Internet connection (for initial setup only)
- [ ] Administrator access to your computer
- [ ] Windows 7 or newer (for Windows systems)

---

## 🚀 QUICK START (Recommended)

### Step 1: Run the Setup File
1. **Look for the file named `setup.bat`** in this folder
2. **Double-click on it** to run the automated setup
3. **Wait** for it to complete (you'll see messages on the screen)
4. The setup will handle everything automatically!

### Step 2: Launch the Application
1. **Look for `launch_sms.bat`** in this folder
2. **Double-click it** to start the application
3. The application will open automatically

**That's it! You're done.** 🎉

---

## 📋 MANUAL SETUP (If Automated Setup Doesn't Work)

### Step 1: Install Python
1. Go to `https://www.python.org/downloads/`
2. Download **Python 3.13** (the latest version)
3. Run the installer
4. **IMPORTANT:** Check the box that says "Add Python to PATH"
5. Click "Install Now"
6. Wait for installation to complete

### Step 2: Set Up the Application
1. Open **Command Prompt** (search for "cmd" on your computer)
2. Copy and paste this command:
   ```
   cd C:\Users\YOUR_USERNAME\Desktop\Gaybeck SMS\gaybeck-starkids-sms
   ```
   *(Replace YOUR_USERNAME with your actual Windows username)*

3. Copy and paste this command:
   ```
   python -m pip install -r requirements.txt
   ```
4. Wait for it to finish (may take 2-5 minutes)

### Step 3: Run the Application
1. In the same Command Prompt, type:
   ```
   python sms.py
   ```
2. The application will open

---

## 🔑 LOGIN INFORMATION

### Default Admin Account
- **Username:** admin
- **Password:** admin123

### Default Teacher Account
- **Username:** teacher1
- **Password:** teacher123

**⚠️ IMPORTANT:** Change these passwords immediately after first login!

---

## 🎯 FIRST TIME SETUP

When you launch the application for the first time:

1. **Login** using the credentials above
2. **Go to Settings** (bottom of menu)
3. **Create your admin account** with your own username and password
4. **Add your teachers** in the Teachers section
5. **Add your classes** in the Classes section
6. **Start using the system!**

---

## ❓ COMMON ISSUES

### Issue: "Python is not recognized"
**Solution:**
- You didn't install Python OR
- You didn't check "Add Python to PATH" during installation
- **Fix:** Reinstall Python and make sure to check that box

### Issue: "Requirements not found" or "Module not found"
**Solution:**
- Make sure you ran the pip install command
- **Fix:** Run this command again:
  ```
  python -m pip install -r requirements.txt
  ```

### Issue: "Database error"
**Solution:**
- First time setup issue (normal)
- **Fix:** Just restart the application, it will initialize automatically

### Issue: Application won't open
**Solution:**
- Make sure Python is installed correctly
- **Fix:** 
  1. Open Command Prompt
  2. Type: `python --version`
  3. If it shows a version number, Python is installed correctly
  4. Try running setup again

### Issue: "Port already in use"
**Solution:**
- Another instance is running
- **Fix:** Close all instances and restart

---

## 📞 NEED HELP?

If you encounter any issues:

1. **Read the error message carefully** - it usually tells you what's wrong
2. **Try restarting** the application
3. **Check your internet connection**
4. **Contact technical support** with a screenshot of any error

---

## 🔐 IMPORTANT SECURITY NOTES

1. **Change default passwords immediately** after installation
2. **Keep your database file safe** (school_management.db)
3. **Make regular backups** of your data
4. **Only run the application on trusted networks**
5. **Don't share admin credentials** with unauthorized people

---

## 📊 WHAT'S INCLUDED

Your Gaybeck Starkids SMS includes:

✅ Student Management  
✅ Attendance Tracking  
✅ Fee Management  
✅ Grading & Assessment  
✅ **AI Assessment Generation** (Create exams in minutes!)  
✅ Financial Management  
✅ Teacher Management  
✅ Analytics & Insights  
✅ And much more!

---

## 🎓 GETTING STARTED GUIDE

### For Administrators:
1. Login with admin account
2. Go to **Teachers** section and add your teachers
3. Go to **Classes** section and create your classes
4. Assign teachers to classes
5. Add students to classes
6. You're ready to use the system!

### For Teachers:
1. Login with your teacher account
2. Go to **Dashboard** to see your class
3. Go to **Attendance** to mark daily attendance
4. Go to **Grades** to enter student grades
5. Go to **AI Assessments** to create exams (🎉 Our best feature!)
6. View analytics to understand class performance

### For Finance Staff:
1. Login (ask admin for credentials)
2. Go to **Financial Management**
3. Track fee payments
4. View financial reports
5. Generate receipts for parents

---

## 🚀 NEXT STEPS

After installation:

1. **Back up your data** regularly
2. **Train your staff** on the system
3. **Start using the AI Assessment** feature (teachers love it!)
4. **Monitor the analytics** to understand your school's performance
5. **Explore all features** to maximize the value

---

## 📱 SYSTEM REQUIREMENTS

**Minimum Requirements:**
- Windows 7 or newer (or Mac/Linux)
- 4 GB RAM
- 500 MB free disk space
- Python 3.8 or newer (installed automatically)

**Recommended Requirements:**
- Windows 10 or newer
- 8 GB RAM
- 2 GB free disk space
- Modern internet browser (for optional parent portal)

---

## ⚙️ TROUBLESHOOTING CHECKLIST

Before contacting support, check:
- [ ] Python is installed (type `python --version` in CMD)
- [ ] You're in the correct folder
- [ ] You have admin rights on your computer
- [ ] Requirements were installed (`python -m pip install -r requirements.txt`)
- [ ] No other instance is running
- [ ] You have internet connection for initial setup
- [ ] Default database wasn't corrupted

---

## 📞 CONTACT & SUPPORT

For technical support:
- 📧 Email: support@gaybeckstarkids.com
- 📱 Phone: +233 XXX XXX XXX
- 🌐 Website: www.gaybeckstarkids.com

---

## ✨ CONGRATULATIONS!

You've successfully set up Gaybeck Starkids SMS!

You now have access to:
- Complete school management system
- Advanced AI assessment tools
- Real-time analytics
- Financial management
- And much more!

**Enjoy the system and good luck with your school! 🎓**

---

**Version:** 2.0  
**Last Updated:** February 24, 2026  
**For Support:** Contact Gaybeck Starkids team

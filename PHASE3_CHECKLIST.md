# Phase 3.3 - Build & Installation Checklist

## ✅ Pre-Build Checklist

- [ ] **Java (JDK) Installed**
  - Run: `java -version`
  - Expected: Java 8+ or JDK 11 LTS
  
- [ ] **Android SDK Installed**
  - Check: `C:\Users\YourUser\AppData\Local\Android\Sdk` exists
  - Or wherever you installed Android Studio SDK
  
- [ ] **Android NDK r25b Installed**
  - Check: Extracted `android-ndk-r25b-windows.zip`
  - Default location: `C:\Android\ndk\android-ndk-r25b`
  
- [ ] **Buildozer Installed**
  - Run: `pip list | findstr buildozer`
  - Expected: buildozer package listed
  
- [ ] **30+ GB Free Disk Space**
  - Check: File Explorer → Properties
  - C: drive should have 30GB+ available
  
- [ ] **USB Cable Available**
  - Have a USB-A to USB-C or micro-USB cable
  
- [ ] **Android Device Available**
  - Any phone/tablet with Android 5.0+ (API 21+)

---

## 🔧 Configuration Phase (5 minutes)

### Step 1: Configure SDK/NDK Paths

```bash
cd e:\MobileApp_Paulina
python configure_android_paths.py --auto
```

- [ ] Script runs without errors
- [ ] Detects Android SDK path
- [ ] Detects Android NDK path
- [ ] buildozer.spec updated

**If auto-detect fails**, use manual:
```bash
python configure_android_paths.py \
  --sdk "C:\Users\YourUser\AppData\Local\Android\Sdk" \
  --ndk "C:\Android\ndk\android-ndk-r25b"
```

---

## ✔️ Verification Phase (1 minute)

### Step 2: Verify Environment

```bash
python verify_android_env.py
```

**Expected output**:
```
[1/5] Checking Java (JDK)... ✅ Java is installed
[2/5] Checking Android SDK... ✅ Android SDK is installed
[3/5] Checking Android NDK... ✅ Android NDK is installed
[4/5] Checking Buildozer... ✅ Buildozer is installed
[5/5] Checking Disk Space... ✅ Sufficient disk space

Passed: 5/5
🎉 All checks passed! Ready to build APK.
```

- [ ] All 5 checks passed ✅
- [ ] No error messages
- [ ] No ⚠️  warnings

**If any check fails**: Fix the issue before proceeding!

---

## 🏗️ Build Phase (5-15 minutes)

### Step 3: Build Debug APK

```bash
python build_apk.py --type debug
```

**During build**:
- [ ] Terminal shows progress messages
- [ ] No error messages appear
- [ ] Building continues for 5-15 minutes (first time longer)

**Expected output at end**:
```
✅ APK build successful! (12.5 minutes)

📦 APK Location: bin/workhours-1.0.0-debug.apk
   Size: 85.3MB
```

- [ ] APK file exists: `bin/workhours-1.0.0-debug.apk`
- [ ] File size is 80-100 MB (normal range)
- [ ] Build took reasonable time
- [ ] No errors in output

**If build fails**:
- [ ] Read error message carefully
- [ ] Common issues:
  - SDK path incorrect → run `configure_android_paths.py` again
  - NDK path incorrect → verify `android-ndk-r25b` folder name
  - Out of disk space → free up 30GB
  - Java not in PATH → restart PowerShell/CMD after JDK install

---

## 📱 Device Preparation (5 minutes)

### Step 4A: Connect Device

- [ ] Plug phone into computer via USB cable
- [ ] Phone screen should show "Allow USB debugging?" prompt
- [ ] Check "Always allow from this computer"
- [ ] Tap "Allow"

### Step 4B: Enable USB Debugging (if not already done)

On your phone:
1. [ ] Open Settings
2. [ ] Scroll to "About Phone"
3. [ ] Find "Build Number" field
4. [ ] **Tap "Build Number" 7 times** (until Developer Mode enabled)
5. [ ] Go back to Settings
6. [ ] Find "Developer Options" (now visible)
7. [ ] Tap "Developer Options"
8. [ ] Enable "USB Debugging" toggle
9. [ ] Enable "Install via USB" (if available)

### Step 4C: Verify Connection

```bash
adb devices -l
```

**Expected output**:
```
List of attached devices
emulator-5554          device

----- Devices -----
emulator-5554          device usb:340000000 ...
```

- [ ] Your device is listed
- [ ] Status shows "device" (not "offline" or "unauthorized")
- [ ] Device ID visible (emulator-XXXX or XXXXXXXXXXXX)

**If device shows "unauthorized"**:
- [ ] Check phone screen for authorization prompt
- [ ] Tap "Allow" again
- [ ] Run: `adb kill-server`
- [ ] Run: `adb start-server`
- [ ] Retry: `adb devices`

---

## 📥 Installation Phase (2 minutes)

### Step 5: Install APK on Device

```bash
python install_apk.py
```

**Script will**:
- [ ] Find connected device
- [ ] Locate latest APK in `bin/` folder
- [ ] Install APK on device
- [ ] Show installation progress

**Expected output**:
```
✅ Found adb
✅ Found 1 device(s):
   1. emulator-5554 (selected)
📦 Installing APK: bin/workhours-1.0.0-debug.apk
   Size: 85.3MB
$ adb install -r bin/workhours-1.0.0-debug.apk
Success

✅ APK installed successfully!
🎉 Ready to use! Launch 'WorkHours' app on your device.
```

- [ ] Installation completes successfully
- [ ] No error messages
- [ ] App appears in device app list

---

## 🧪 Testing Phase (10 minutes)

### Step 6: Test App Functionality

On your phone:
1. [ ] Open "App Drawer"
2. [ ] Find "WorkHours" app
3. [ ] Tap to launch

**First launch**:
- [ ] App starts without crashing
- [ ] Main screen displays (Dashboard/Home)
- [ ] Bottom navigation buttons visible

**Create Profile** (if not exists):
- [ ] Tap "Settings" or profile button
- [ ] Enter name: Test User
- [ ] Tap "Save"
- [ ] Profile created successfully

**Log Work Hours**:
- [ ] Go to "Entry" or "Add Hours" screen
- [ ] Select date: Today
- [ ] Select type: Work
- [ ] Enter hours: 8
- [ ] Tap "Save"
- [ ] Entry appears in Dashboard

**Check Dashboard**:
- [ ] View monthly stats
- [ ] See last 7 days entries
- [ ] Refresh button works
- [ ] Numbers are correct

**Generate Report**:
- [ ] Go to "Report" screen
- [ ] Select month/year
- [ ] Tap "Generate PDF"
- [ ] PDF appears in system notifications
- [ ] PDF is readable

**Change Theme**:
- [ ] Go to "Theme" screen
- [ ] Select different theme
- [ ] Colors change immediately
- [ ] Theme persists on restart

### Test Results

- [ ] All basic features work
- [ ] No crashes during testing
- [ ] Database saves data
- [ ] PDF generation works
- [ ] Theme switching works
- [ ] No errors in console (if visible)

---

## 📊 Final Validation

### Step 7: Confirm Success

- [ ] APK built: ✅
- [ ] APK installed: ✅
- [ ] App launches: ✅
- [ ] Features work: ✅
- [ ] Data persists: ✅
- [ ] No crashes: ✅

**Status**: Phase 3.3 COMPLETE ✅

---

## 🚀 Next Steps

After successful completion:

1. [ ] Close the test app on phone
2. [ ] Disconnect USB cable (optional)
3. [ ] Verify app still works offline
4. [ ] Take screenshots for Google Play (later)
5. [ ] **Type in terminal**: `kontynuuj phase3.4`
6. [ ] Continue to Phase 3.4: Google Play Deployment

---

## 📞 Troubleshooting

### Issue: "Configure script fails"
```
❌ SDK path does not exist
```
**Solution**:
- Verify Android SDK location
- Check if path has spaces (needs quotes)
- Manually run: `python configure_android_paths.py --sdk "C:\path\to\sdk" --ndk "C:\path\to\ndk"`

### Issue: "Verify script has ❌ checks"
```
❌ Java not found in PATH
```
**Solution**:
- Java not installed or not in PATH
- Install JDK from https://www.oracle.com/java/technologies/downloads/
- Restart PowerShell/CMD after installation
- Verify: `java -version`

### Issue: "Build fails with errors"
```
ERROR: ... SDK not found
```
**Solution**:
- SDK/NDK paths in buildozer.spec incorrect
- Run `python configure_android_paths.py --auto` again
- Verify paths exist: open File Explorer and navigate there
- Common issues: spaces in path, wrong drive letter

### Issue: "Device not found"
```
❌ No connected devices found
```
**Solution**:
- Check USB cable connection
- Enable USB Debugging on phone
- Authorize device (look for prompt on phone)
- Run: `adb kill-server && adb start-server`
- Retry: `adb devices`

### Issue: "Installation fails"
```
FAILURE [INSTALL_FAILED_...]
```
**Solution**:
- Not enough space on device
- Uninstall old version: `adb uninstall org.workhours`
- Device not authorized (check phone screen)
- Try again: `python install_apk.py`

### Issue: "App crashes on launch"
**Solution**:
- Check Android version (need API 21+)
- Check permissions enabled
- Check logcat: `adb logcat | findstr WorkHours`
- Report issue with full error log

---

## 📝 Notes

```
Date Started: _______________
Device Used: _______________
Date Completed: _______________
Issues Encountered: _______________
Overall Result: _______________
```

---

## ✨ Success Celebration!

When all checks are complete:

🎊 **You have successfully:**
- ✅ Configured Android build system
- ✅ Built APK from Kivy Python code
- ✅ Installed app on real Android device
- ✅ Tested all features on mobile
- ✅ Completed Phase 3.3!

**Achievement Unlocked**: 🏆 Native Android Developer

---

*Phase 3.3 Checklist - Build & Installation*
*Last Updated: February 4, 2026*
*Total Estimated Time: 30 minutes - 1 hour*

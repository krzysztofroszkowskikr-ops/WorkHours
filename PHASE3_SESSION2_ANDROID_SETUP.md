# 📱 Phase 3.2 - Android SDK/NDK Setup Instructions

## 🔍 Current Status

**Date**: February 4, 2026  
**Phase**: 3.2 - Android SDK/NDK Installation & Configuration  
**Status**: ⏳ MANUAL SETUP REQUIRED  

---

## ⚠️ Important Note

Building APK on Windows requires:
1. **Java Development Kit (JDK)** - for build tools
2. **Android SDK** - Android development libraries
3. **Android NDK** - C/C++ compilation tools

These are **large downloads** (10-20GB total) and require **30GB+ free disk space**.

---

## 📋 Step-by-Step Setup Guide

### Step 1: Check Java Installation

#### Option A: Check System Java
```powershell
# In PowerShell, check if Java is installed
java -version

# If installed, you'll see something like:
# openjdk version "11.0.13" 2021-10-19
# OpenJDK Runtime Environment (build 11.0.13+8)
```

#### Option B: If Java Not Installed
Download from: https://www.oracle.com/java/technologies/downloads/

Choose:
- **JDK 11 or JDK 8** (LTS versions are safest)
- **Windows x64 Installer**

Install with default settings.

---

### Step 2: Download Android SDK

#### Option A: Use Android Studio (Easiest)
1. Go to: https://developer.android.com/studio
2. Download **Android Studio** for Windows
3. Run installer
4. During setup, let it install:
   - Android SDK
   - SDK Platform API 31
   - Android SDK Build-Tools

**Installation Path**: Usually `C:\Users\<YourUser>\AppData\Local\Android\Sdk`

#### Option B: Manual Command-Line SDK Manager
If you prefer command-line only:
1. Download Android SDK Tools from: https://developer.android.com/tools/sdkmanager
2. Follow instructions in guide

**Recommended Path**: `C:\Android\sdk`

---

### Step 3: Download Android NDK

1. Go to: https://developer.android.com/ndk/downloads
2. Download **NDK r25b** (specific version for stability)
   - Choose **Windows (64-bit)**
   - File: `android-ndk-r25b-windows.zip` (~650MB)

3. Extract to: `C:\Android\ndk\r25b`
   - Or your preferred location (path will be added to buildozer.spec)

**Installation Path Example**: `C:\Android\ndk\android-ndk-r25b`

---

### Step 4: Update buildozer.spec

After installing SDK and NDK, update `buildozer.spec`:

```ini
[buildozer]

# Add these lines (replace paths with YOUR actual paths):
android_sdk_path = C:\Users\<YourUser>\AppData\Local\Android\Sdk
android_ndk_path = C:\Android\ndk\android-ndk-r25b

# Or if using Android Studio:
android_sdk_path = C:\Users\<YourUser>\AppData\Local\Android\Sdk
android_ndk_path = C:\Android\ndk\android-ndk-r25b
```

**Important**: Use forward slashes or double backslashes in paths!

---

## ✅ Verification Checklist

After installation, verify everything is in place:

### Check 1: Java
```powershell
java -version
# Should output version info, not "command not found"
```

### Check 2: Android SDK
```powershell
# Check if SDK manager exists
Get-Item "C:\Users\<YourUser>\AppData\Local\Android\Sdk\tools\bin\sdkmanager.bat"
# Or your SDK path
```

### Check 3: Android NDK
```powershell
# Check if NDK exists
Get-Item "C:\Android\ndk\android-ndk-r25b\ndk-build.cmd"
# Or your NDK path
```

### Check 4: Buildozer Config
```powershell
cd e:\MobileApp_Paulina
# Check that paths in buildozer.spec are valid
Get-Content buildozer.spec | Select-String "android_sdk_path|android_ndk_path"
```

---

## 🛠️ Installation Sizes & Times

| Component | Size | Download Time | Installation Time |
|-----------|------|----------------|-------------------|
| JDK 11 | ~200MB | 5-10 min | 5 min |
| Android Studio | ~900MB | 20-30 min | 15 min |
| Android SDK Extras | ~3GB | 30-60 min | 10 min |
| Android NDK r25b | ~650MB | 15-20 min | 5 min |
| **TOTAL** | **~5GB** | **1-2 hours** | **30 min** |

---

## 📝 Common Issues & Solutions

### Issue 1: "java: command not found"
**Solution**: JDK not installed or not in PATH
- Install JDK from oracle.com
- After install, restart PowerShell
- Test with `java -version`

### Issue 2: "sdkmanager not found"
**Solution**: Android SDK not properly installed
- Download from Android Studio
- Make sure SDK platform API 31 is installed
- Check path matches buildozer.spec

### Issue 3: "NDK build tools not found"
**Solution**: NDK r25b not extracted to correct location
- Download NDK r25b specifically (not r26)
- Extract to exact path in buildozer.spec
- Path must have `android-ndk-r25b` folder name

### Issue 4: "Path contains spaces"
**Solution**: Buildozer doesn't like spaces in paths
- Use `C:\Android\` not `C:\Program Files\Android\`
- Use forward slashes: `C:/Android/ndk/r25b`

---

## 🚀 After Setup Complete

Once all three are installed:

1. Update `buildozer.spec` with SDK/NDK paths
2. Test buildozer is ready:
   ```powershell
   cd e:\MobileApp_Paulina
   buildozer android debug --help
   # Should show help without errors
   ```

3. Then build APK:
   ```powershell
   buildozer android debug
   # Will take 5-15 minutes on first run
   # APK will be in: bin/workhours-1.0.0-debug.apk
   ```

---

## 📚 Official Resources

- **JDK**: https://www.oracle.com/java/technologies/downloads/
- **Android Studio**: https://developer.android.com/studio
- **Android NDK**: https://developer.android.com/ndk/downloads
- **Buildozer Docs**: https://buildozer.readthedocs.io/

---

## ⏱️ Next Steps

### Timeline for Phase 3.2

1. **Install JDK** (10 min)
   - Download & run installer
   - Verify with `java -version`

2. **Install Android Studio** (30 min)
   - Download & install
   - Let SDK install automatically

3. **Download Android NDK r25b** (20 min)
   - Download from Google
   - Extract to `C:\Android\ndk\`

4. **Update buildozer.spec** (5 min)
   - Add SDK and NDK paths
   - Save file

5. **Verify Installation** (5 min)
   - Check all paths exist
   - Test `buildozer android debug --help`

**Total Time**: ~1-1.5 hours

---

## 🎯 Success Criteria

Phase 3.2 is complete when:

- [x] JDK installed and verified (`java -version` works)
- [x] Android SDK installed with API 31
- [x] Android NDK r25b downloaded and extracted
- [x] buildozer.spec updated with correct paths
- [x] All paths verified to exist
- [x] `buildozer android debug --help` works without errors

---

## ❓ Questions?

If you encounter issues:

1. Check the error message carefully
2. Verify paths in buildozer.spec are correct
3. Make sure you have 30GB+ free disk space
4. Try reinstalling the problematic component

---

**Status**: ⏳ **Awaiting Manual Installation**

After completing these steps, report back and we'll proceed to Phase 3.3 - APK Build!

**Next Command**: `kontynuuj build apk` (after installation complete)


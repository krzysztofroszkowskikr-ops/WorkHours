# DEPENDENCIES MATRIX & REQUIREMENTS
## WorkHours Purple v1.0

---

## 1. PYTHON DEPENDENCIES - COMPLETE LIST

### 1.1 Core Dependencies Matrix

| Package | Version | Purpose | Min Version | Max Version | License |
|---------|---------|---------|-------------|-------------|---------|
| **kivy** | 2.3.0 | UI Framework (cross-platform) | 2.2.0 | 3.0.0 | MIT |
| **kivymd** | 0.104.2 | Material Design components | 0.104.0 | 1.0.0 | MIT |
| **python-dateutil** | 2.8.2 | Date/time parsing & manipulation | 2.8.0 | 3.0.0 | Apache 2.0 |
| **reportlab** | 4.0.7 | PDF generation library | 4.0.0 | 5.0.0 | BSD |
| **plyer** | 2.1.0 | Native API access (notifications, camera, etc) | 2.0.0 | 3.0.0 | MIT |
| **pyjnius** | 1.5.2 | Java/Android integration | 1.4.0 | 2.0.0 | MIT |
| **pillow** | 10.0.1 | Image processing (PDF, icons) | 9.0.0 | 11.0.0 | PIL License |

### 1.2 Development Dependencies

| Package | Version | Purpose | License |
|---------|---------|---------|---------|
| **pytest** | 7.4.2 | Unit testing framework | MIT |
| **pytest-cov** | 4.1.0 | Code coverage reports | MIT |
| **pytest-mock** | 3.11.1 | Mocking library for tests | MIT |
| **black** | 23.9.1 | Code formatter | MIT |
| **flake8** | 6.1.0 | Linter (PEP8 compliance) | MIT |
| **mypy** | 1.5.1 | Static type checker | MIT |
| **buildozer** | 1.4.11 | APK builder for Kivy | MIT |

### 1.3 Optional/Conditional Dependencies

| Package | Version | When Used | Purpose |
|---------|---------|-----------|---------|
| **Cython** | 0.29.36 | Android build | Compilation optimization |
| **android** | 0.4.4 | Android runtime | Android-specific APIs |

---

## 2. requirements.txt

```txt
# Core Framework
kivy==2.3.0
kivymd==0.104.2

# Date/Time Handling
python-dateutil==2.8.2

# PDF Generation
reportlab==4.0.7
Pillow==10.0.1

# Android/Native APIs
plyer==2.1.0
pyjnius==1.5.2

# Development (dev-only)
# Uncomment for development:
# pytest==7.4.2
# pytest-cov==4.1.0
# pytest-mock==3.11.1
# black==23.9.1
# flake8==6.1.0
# mypy==1.5.1
# buildozer==1.4.11
```

**Install:**
```bash
pip install -r requirements.txt
```

---

## 3. ANDROID REQUIREMENTS

### 3.1 minSdkVersion vs targetSdkVersion

```
minSdkVersion: 26      # Android 8.0 Oreo (Dec 2017)
targetSdkVersion: 35   # Android 15 (2024+)
```

**Rationale for target 35:**
- ✅ Support latest Android features
- ✅ Required by Google Play (as of Nov 2024)
- ✅ Android 16 ready (backward compatible)
- ✅ Scoped storage compliance
- ✅ Latest security patches

### 3.2 Required Permissions

```xml
<!-- AndroidManifest.xml (Buildozer generates) -->

<!-- File I/O -->
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />

<!-- Notifications -->
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

<!-- Alarms (for reminders) -->
<uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />

<!-- Android 13+ permission for notifications -->
<uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" 
    android:maxSdkVersion="30" />
```

**In buildozer.spec:**
```ini
[app]
permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,POST_NOTIFICATIONS,SCHEDULE_EXACT_ALARM
```

### 3.3 Android Features Required

```ini
[app]
# Minimal features - low device compatibility barrier
android.features = android.hardware.screen.portrait

# No need for:
# - Camera
# - GPS
# - Bluetooth
# - NFC
# - etc.
```

---

## 4. SYSTEM REQUIREMENTS (Developer Machine)

### 4.1 Windows Development Setup

```
OS: Windows 10/11
Python: 3.9+ (3.11 recommended)
Java: JDK 11+ (needed for Buildozer)
Android SDK: API 26+ (installed by buildozer)
Gradle: 7.0+ (managed by buildozer)
RAM: 8GB minimum (16GB recommended)
Disk: 20GB for SDK/NDK
```

### 4.2 Linux/Mac Development

```
OS: Ubuntu 20.04+ / macOS 11+
Python: 3.9+ (3.11 recommended)
Java: JDK 11+ (apt: openjdk-11-jdk)
Android SDK: Latest
Cython: pip install cython
```

---

## 5. OPTIONAL INTEGRATIONS

### 5.1 Cloud Backup (v1.2+)

```python
# For optional cloud sync:
# google-cloud-storage==2.10.0
# firebase-admin==6.2.0
```

### 5.2 Analytics (v1.2+)

```python
# For optional app analytics:
# google-analytics-python-api==4.10.0
```

---

## 6. DEPENDENCY COMPATIBILITY MATRIX

### Python Version Support

```
Python 3.9   ✅ Full support (legacy compatible)
Python 3.10  ✅ Full support
Python 3.11  ✅ Recommended (latest stable)
Python 3.12  ⚠️ Beta support (Kivy 2.3+)
Python 3.13  ❌ Not yet (await Kivy 2.4)
```

### Kivy / KivyMD Compatibility

```
Kivy 2.2 + KivyMD 0.103  ⚠️ Legacy (deprecated)
Kivy 2.3 + KivyMD 0.104  ✅ RECOMMENDED (stable)
Kivy 2.4 (beta) + KivyMD 0.105 (beta) ⚠️ Future
```

---

## 7. BUILDOZER CONFIGURATION

### 7.1 buildozer.spec (Excerpt)

```ini
[app]
# Application metadata
title = WorkHours Purple
package.name = workhours
package.domain = org.workhours

# Source code
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Version
version = 1.0.0

# Requirements
requirements = python3,kivy,kivymd,reportlab,plyer,pyjnius,pillow,python-dateutil

# Permissions
permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,POST_NOTIFICATIONS,SCHEDULE_EXACT_ALARM

# App icon & presplash
icon.filename = assets/icons/app_icon.png
presplash.filename = assets/icons/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1
```

### 7.2 Building APK

```bash
# Install buildozer (one-time)
pip install buildozer

# Build debug APK
buildozer android debug

# Build release APK (requires signing key)
buildozer android release

# Deploy to connected device
buildozer android debug deploy run

# Clean build
buildozer android clean
```

---

## 8. VIRTUAL ENVIRONMENT SETUP

### 8.1 Create venv

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 8.2 Install dependencies

```bash
# Install core
pip install -r requirements.txt

# Optional: install dev tools
pip install pytest pytest-cov black flake8 mypy buildozer
```

---

## 9. DEPENDENCY ANALYSIS

### 9.1 Total Size Impact

```
Kivy + KivyMD:        ~50 MB
ReportLab:            ~15 MB
Other dependencies:   ~20 MB
Python runtime:       ~50 MB
──────────────────────────────
Total APK (debug):    ~135 MB
Total APK (release):  ~45 MB (after ProGuard shrinking)
```

### 9.2 No External Network Required

- ✅ All dependencies bundled in APK
- ✅ No remote API calls (offline-first)
- ✅ Optional: future cloud sync (v1.2+)

### 9.3 Known Issues & Workarounds

| Issue | Package | Workaround |
|-------|---------|-----------|
| Slow startup | Kivy | Use Cython compilation (buildozer handles) |
| PDF memory leak | ReportLab | Explicit garbage collection in PDFService |
| Android 14+ scoped storage | Plyer | Request runtime permissions |
| PyJNI compatibility | PyJNI | Tested on API 26-35 ✅ |

---

## 10. UPGRADE STRATEGY

### Minor Version Updates (Safe)

```bash
# Safe to update patch versions
pip install --upgrade "reportlab==4.0.*"
pip install --upgrade "pillow==10.0.*"
```

### Major Version Updates (Test Required)

```bash
# Test in isolated environment first
python -m venv test_venv
pip install "kivy==2.4.0"  # Major version jump
# Run full test suite
pytest
```

---

## 11. DEPENDENCY LOCK FILE (Optional)

### 11.1 requirements-lock.txt

```txt
# Exact pinned versions for production builds
kivy==2.3.0
kivymd==0.104.2
python-dateutil==2.8.2
reportlab==4.0.7
pillow==10.0.1
plyer==2.1.0
pyjnius==1.5.2

# Generated: 2026-02-04
# Run: pip install -r requirements-lock.txt
```

**Generate:**
```bash
pip freeze > requirements-lock.txt
```

---

## 12. SECURITY & LICENSE COMPLIANCE

### Licenses Used:

```
MIT License:
  - Kivy
  - KivyMD
  - Plyer
  - PyJNI
  - python-dateutil
  - Black
  - Flake8
  - MyPy

BSD License:
  - ReportLab

PIL License:
  - Pillow

Apache 2.0:
  - python-dateutil (dual)
```

✅ **All licenses are permissive** — safe for commercial use

### Vulnerability Check

```bash
# Check for known vulnerabilities
pip install safety
safety check
```

---

## 13. NEXT STEPS

1. **Setup venv & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Configure Buildozer** (for Android build)
   ```bash
   pip install buildozer
   buildozer android debug
   ```

3. **Install dev tools** (for development)
   ```bash
   pip install pytest black flake8 mypy
   ```

---

**NEXT:** Theme System (Opcja A+B+Animations)

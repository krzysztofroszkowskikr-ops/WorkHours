#!/usr/bin/env python3
"""
Verify Android Build Environment

Checks if all required tools are installed and configured correctly
for buildozer Android APK builds.

Usage:
    python verify_android_env.py
"""

import os
import sys
import subprocess
from pathlib import Path


def check_java():
    """Check if Java is installed"""
    print("\n[1/5] Checking Java (JDK)...")
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("  ✅ Java is installed")
            # Extract version
            version_line = result.stderr.split('\n')[0]
            print(f"     {version_line}")
            return True
        else:
            print("  ❌ Java not found")
            return False
    except FileNotFoundError:
        print("  ❌ Java not found in PATH")
        print("     Action: Install JDK from https://www.oracle.com/java/technologies/downloads/")
        return False
    except Exception as e:
        print(f"  ❌ Error checking Java: {e}")
        return False


def check_android_sdk(sdk_path):
    """Check if Android SDK is installed"""
    print("\n[2/5] Checking Android SDK...")
    
    if not sdk_path:
        print("  ⚠️  SDK_PATH not set in buildozer.spec")
        print("     Action: Set android_sdk_path in buildozer.spec")
        return False
    
    sdk_dir = Path(sdk_path)
    
    if not sdk_dir.exists():
        print(f"  ❌ SDK path does not exist: {sdk_path}")
        print("     Action: Download Android SDK from https://developer.android.com/studio")
        return False
    
    # Check for SDK Manager
    sdkmanager = sdk_dir / "tools" / "bin" / "sdkmanager.bat"
    if not sdkmanager.exists():
        sdkmanager = sdk_dir / "cmdline-tools" / "latest" / "bin" / "sdkmanager.bat"
    
    if sdkmanager.exists():
        print("  ✅ Android SDK is installed")
        print(f"     Path: {sdk_path}")
        return True
    else:
        print(f"  ⚠️  SDK Manager not found in: {sdk_path}")
        print("     This might be OK if SDK was installed via Android Studio")
        return True  # Don't fail, might still work


def check_android_ndk(ndk_path):
    """Check if Android NDK is installed"""
    print("\n[3/5] Checking Android NDK...")
    
    if not ndk_path:
        print("  ⚠️  NDK_PATH not set in buildozer.spec")
        print("     Action: Set android_ndk_path in buildozer.spec")
        return False
    
    ndk_dir = Path(ndk_path)
    
    if not ndk_dir.exists():
        print(f"  ❌ NDK path does not exist: {ndk_path}")
        print("     Action: Download Android NDK r25b from https://developer.android.com/ndk/downloads")
        return False
    
    # Check for ndk-build
    ndk_build = ndk_dir / "ndk-build.cmd"
    if not ndk_build.exists():
        ndk_build = ndk_dir / "ndk-build"
    
    if ndk_build.exists():
        print("  ✅ Android NDK is installed")
        print(f"     Path: {ndk_path}")
        return True
    else:
        print(f"  ⚠️  ndk-build not found in: {ndk_path}")
        print("     Action: Make sure NDK r25b is properly extracted")
        return False


def check_buildozer():
    """Check if buildozer is installed"""
    print("\n[4/5] Checking Buildozer...")
    try:
        result = subprocess.run(
            ["buildozer", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 or "buildozer" in result.stderr.lower():
            print("  ✅ Buildozer is installed")
            return True
        else:
            print("  ❌ Buildozer not found")
            return False
    except FileNotFoundError:
        print("  ❌ Buildozer not found in PATH")
        print("     Action: Run: pip install buildozer")
        return False
    except Exception as e:
        print(f"  ⚠️  Error checking Buildozer: {e}")
        return False


def check_disk_space():
    """Check if there's enough disk space"""
    print("\n[5/5] Checking Disk Space...")
    try:
        import shutil
        
        # Get free space in home directory
        stat = shutil.disk_usage(Path.home())
        free_gb = stat.free / (1024**3)
        
        if free_gb < 30:
            print(f"  ⚠️  Low disk space: {free_gb:.1f}GB free (need 30GB)")
            print("     Action: Free up at least 30GB")
            return False
        else:
            print(f"  ✅ Sufficient disk space: {free_gb:.1f}GB free")
            return True
    except Exception as e:
        print(f"  ⚠️  Error checking disk space: {e}")
        return True  # Don't fail, might still work


def parse_buildozer_spec(spec_path="buildozer.spec"):
    """Parse buildozer.spec for SDK/NDK paths"""
    print(f"\n[0/5] Reading buildozer.spec...")
    
    if not Path(spec_path).exists():
        print(f"  ❌ File not found: {spec_path}")
        return None, None
    
    sdk_path = None
    ndk_path = None
    
    with open(spec_path, 'r') as f:
        for line in f:
            if line.startswith("android_sdk_path"):
                sdk_path = line.split("=", 1)[1].strip()
                # Remove quotes if present
                sdk_path = sdk_path.strip("'\"")
            elif line.startswith("android_ndk_path"):
                ndk_path = line.split("=", 1)[1].strip()
                # Remove quotes if present
                ndk_path = ndk_path.strip("'\"")
    
    if sdk_path:
        print(f"  SDK path from spec: {sdk_path}")
    else:
        print("  ⚠️  android_sdk_path not found in buildozer.spec")
    
    if ndk_path:
        print(f"  NDK path from spec: {ndk_path}")
    else:
        print("  ⚠️  android_ndk_path not found in buildozer.spec")
    
    return sdk_path, ndk_path


def main():
    """Main verification function"""
    print("=" * 60)
    print("Android Build Environment Verification")
    print("=" * 60)
    
    # Parse buildozer.spec
    sdk_path, ndk_path = parse_buildozer_spec()
    
    # Run checks
    results = {
        "Java (JDK)": check_java(),
        "Android SDK": check_android_sdk(sdk_path),
        "Android NDK": check_android_ndk(ndk_path),
        "Buildozer": check_buildozer(),
        "Disk Space": check_disk_space(),
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All checks passed! Ready to build APK.")
        print("\nNext step: buildozer android debug")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

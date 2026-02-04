#!/usr/bin/env python3
"""
Configure Android SDK/NDK Paths in buildozer.spec

Updates buildozer.spec with correct paths after manual SDK/NDK installation.

Usage:
    python configure_android_paths.py --sdk <path> --ndk <path>
    
    Examples:
    python configure_android_paths.py --sdk "C:\\Users\\YourUser\\AppData\\Local\\Android\\Sdk" --ndk "C:\\Android\\ndk\\android-ndk-r25b"
    python configure_android_paths.py --auto
"""

import sys
import os
import argparse
from pathlib import Path


def find_android_sdk_auto():
    """Try to find Android SDK in common locations"""
    common_paths = [
        Path.home() / "AppData" / "Local" / "Android" / "Sdk",  # Android Studio default
        Path("C:\\") / "Android" / "Sdk",
        Path("C:\\") / "Android" / "android-sdk",
        Path.home() / "Android" / "Sdk",
    ]
    
    for path in common_paths:
        if path.exists():
            print(f"Found Android SDK at: {path}")
            return str(path)
    
    return None


def find_android_ndk_auto():
    """Try to find Android NDK in common locations"""
    common_paths = [
        Path("C:\\") / "Android" / "ndk" / "android-ndk-r25b",
        Path.home() / "AppData" / "Local" / "Android" / "Sdk" / "ndk",
        Path("C:\\") / "Android" / "android-ndk-r25b",
        Path.home() / "Android" / "ndk" / "android-ndk-r25b",
    ]
    
    for path in common_paths:
        if path.exists():
            # Check if it's the r25b version
            if "r25b" in str(path) or (path / "source.properties").exists():
                print(f"Found Android NDK at: {path}")
                return str(path)
    
    return None


def validate_sdk_path(path):
    """Validate that SDK path is valid"""
    sdk_dir = Path(path)
    
    if not sdk_dir.exists():
        print(f"❌ SDK path does not exist: {path}")
        return False
    
    # Check for key SDK directories
    required = ["platforms", "build-tools"]
    for req in required:
        if not (sdk_dir / req).exists():
            print(f"⚠️  Missing {req} in SDK path")
    
    print(f"✅ SDK path valid: {path}")
    return True


def validate_ndk_path(path):
    """Validate that NDK path is valid"""
    ndk_dir = Path(path)
    
    if not ndk_dir.exists():
        print(f"❌ NDK path does not exist: {path}")
        return False
    
    # Check for key NDK files
    if not (ndk_dir / "ndk-build.cmd").exists() and not (ndk_dir / "ndk-build").exists():
        print(f"⚠️  ndk-build not found in NDK path")
    
    print(f"✅ NDK path valid: {path}")
    return True


def update_buildozer_spec(sdk_path, ndk_path, spec_file="buildozer.spec"):
    """Update buildozer.spec with new SDK/NDK paths"""
    
    if not Path(spec_file).exists():
        print(f"❌ buildozer.spec not found: {spec_file}")
        return False
    
    # Read current spec
    with open(spec_file, 'r') as f:
        lines = f.readlines()
    
    # Update paths
    sdk_found = False
    ndk_found = False
    updated_lines = []
    
    for line in lines:
        if line.startswith("android_sdk_path"):
            updated_lines.append(f"android_sdk_path = {sdk_path}\n")
            sdk_found = True
        elif line.startswith("android_ndk_path"):
            updated_lines.append(f"android_ndk_path = {ndk_path}\n")
            ndk_found = True
        else:
            updated_lines.append(line)
    
    # If not found, add them in the [app] section
    if not sdk_found or not ndk_found:
        # Find [app:android] section
        app_android_idx = None
        for i, line in enumerate(updated_lines):
            if line.startswith("[app:android]"):
                app_android_idx = i
                break
        
        if app_android_idx is not None:
            if not sdk_found:
                updated_lines.insert(app_android_idx + 1, f"android_sdk_path = {sdk_path}\n")
            if not ndk_found:
                updated_lines.insert(app_android_idx + (2 if not sdk_found else 1), 
                                   f"android_ndk_path = {ndk_path}\n")
    
    # Write back
    with open(spec_file, 'w') as f:
        f.writelines(updated_lines)
    
    print(f"✅ Updated {spec_file}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Configure Android SDK/NDK paths")
    parser.add_argument("--sdk", help="Android SDK path")
    parser.add_argument("--ndk", help="Android NDK path")
    parser.add_argument("--auto", action="store_true", help="Auto-detect SDK/NDK paths")
    parser.add_argument("--spec", default="buildozer.spec", help="buildozer.spec file path")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Android SDK/NDK Configuration")
    print("=" * 60)
    
    sdk_path = args.sdk
    ndk_path = args.ndk
    
    # Auto-detect if requested
    if args.auto:
        print("\n[AUTO-DETECT MODE]")
        if not sdk_path:
            sdk_path = find_android_sdk_auto()
        if not ndk_path:
            ndk_path = find_android_ndk_auto()
    
    # If still not found, ask user
    if not sdk_path:
        print("\n❌ Android SDK path not found")
        print("\nTo find your SDK path:")
        print("  1. Open Android Studio")
        print("  2. Settings → Appearance & Behavior → System Settings → Android SDK")
        print("  3. Copy the Android SDK Location")
        sdk_path = input("\nEnter Android SDK path: ").strip()
    
    if not ndk_path:
        print("\n❌ Android NDK path not found")
        print("\nTo find your NDK path:")
        print("  1. Extract android-ndk-r25b-windows.zip")
        print("  2. Enter the extracted directory path")
        ndk_path = input("\nEnter Android NDK path: ").strip()
    
    # Remove quotes if user added them
    sdk_path = sdk_path.strip("'\"")
    ndk_path = ndk_path.strip("'\"")
    
    print("\n[VALIDATION]")
    sdk_valid = validate_sdk_path(sdk_path)
    ndk_valid = validate_ndk_path(ndk_path)
    
    if sdk_valid and ndk_valid:
        print("\n[UPDATE]")
        update_buildozer_spec(sdk_path, ndk_path, args.spec)
        print("\n✅ Configuration complete!")
        print("\nNext step: python verify_android_env.py")
        return 0
    else:
        print("\n❌ Please fix the paths above")
        return 1


if __name__ == "__main__":
    sys.exit(main())

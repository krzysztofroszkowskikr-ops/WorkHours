#!/usr/bin/env python3
"""
Install APK on Android Device

Automated installation using adb with device detection.

Usage:
    python install_apk.py
    python install_apk.py --device <device_id>
    python install_apk.py --apk <path/to/apk>
"""

import sys
import subprocess
import argparse
from pathlib import Path
import time


def find_adb():
    """Find adb executable"""
    common_paths = [
        Path.home() / "AppData" / "Local" / "Android" / "Sdk" / "platform-tools" / "adb.exe",
        Path("C:\\") / "Android" / "Sdk" / "platform-tools" / "adb.exe",
        Path.home() / "Android" / "Sdk" / "platform-tools" / "adb.exe",
    ]
    
    for path in common_paths:
        if path.exists():
            return str(path)
    
    # Try to find in PATH
    try:
        result = subprocess.run(
            ["where", "adb"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    return None


def run_adb_command(adb_path, args):
    """Run adb command"""
    cmd = [adb_path] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timeout"
    except Exception as e:
        return False, str(e)


def list_devices(adb_path):
    """List connected devices"""
    success, output = run_adb_command(adb_path, ["devices", "-l"])
    
    if not success:
        print("❌ Failed to list devices")
        return []
    
    devices = []
    for line in output.split('\n'):
        line = line.strip()
        if line and not line.startswith('List') and not line.startswith('*'):
            parts = line.split()
            if len(parts) >= 2:
                device_id = parts[0]
                status = parts[1]
                if status == "device":
                    devices.append(device_id)
    
    return devices


def install_apk(adb_path, apk_path, device_id=None):
    """Install APK on device"""
    
    apk_file = Path(apk_path)
    if not apk_file.exists():
        print(f"❌ APK not found: {apk_path}")
        return False
    
    print(f"\n📦 Installing APK: {apk_path}")
    print(f"   Size: {apk_file.stat().st_size / (1024*1024):.1f}MB")
    
    # Build adb install command
    cmd = ["install", "-r"]  # -r = replace existing
    if device_id:
        cmd = ["-s", device_id] + cmd
    cmd.append(str(apk_path))
    
    print(f"\n$ adb {' '.join(cmd)}")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        process = subprocess.Popen(
            [adb_path] + cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Stream output
        for line in iter(process.stdout.readline, ''):
            if line:
                print(line.rstrip())
        
        returncode = process.wait()
        elapsed = time.time() - start_time
        
        print("=" * 60)
        
        if returncode == 0:
            print(f"\n✅ APK installed successfully! ({elapsed/60:.1f} minutes)")
            return True
        else:
            print(f"\n❌ Installation failed (exit code: {returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def find_latest_apk():
    """Find latest built APK"""
    bin_dir = Path("bin")
    if not bin_dir.exists():
        return None
    
    apk_files = list(bin_dir.glob("*.apk"))
    if not apk_files:
        return None
    
    # Return most recent
    return max(apk_files, key=lambda p: p.stat().st_mtime)


def main():
    parser = argparse.ArgumentParser(description="Install APK on Android device")
    parser.add_argument("--apk", help="APK file path")
    parser.add_argument("--device", help="Target device ID")
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("INSTALL APK ON ANDROID DEVICE")
    print("=" * 60)
    
    # Find adb
    adb_path = find_adb()
    if not adb_path:
        print("❌ adb not found in PATH")
        print("\nTo fix this:")
        print("  1. Install Android SDK via Android Studio")
        print("  2. Or manually set Android SDK path in environment")
        return 1
    
    print(f"\n✅ Found adb: {adb_path}")
    
    # Find APK
    apk_path = args.apk
    if not apk_path:
        print("\nSearching for latest APK...")
        latest_apk = find_latest_apk()
        if latest_apk:
            apk_path = str(latest_apk)
            print(f"✅ Found: {apk_path}")
        else:
            print("❌ No APK found in bin/")
            print("\nUsage: python install_apk.py --apk <path/to/apk>")
            print("Or first run: python build_apk.py")
            return 1
    
    # List devices
    print("\n[DETECTING DEVICES]")
    devices = list_devices(adb_path)
    
    if not devices:
        print("❌ No connected devices found")
        print("\nPlease:")
        print("  1. Connect Android device via USB")
        print("  2. Enable 'Developer Mode' on device (tap Build Number 7 times)")
        print("  3. Enable 'USB Debugging' in Developer Options")
        print("  4. Authorize USB connection on device")
        return 1
    
    print(f"✅ Found {len(devices)} device(s):")
    for i, dev in enumerate(devices, 1):
        marker = " (selected)" if i == 1 and not args.device else ""
        print(f"   {i}. {dev}{marker}")
    
    # Select device
    target_device = args.device or devices[0]
    if target_device not in devices:
        print(f"❌ Device not found: {target_device}")
        return 1
    
    print(f"\n📱 Target device: {target_device}")
    
    # Install
    if install_apk(adb_path, apk_path, target_device):
        print(f"\n🎉 Ready to use! Launch 'WorkHours' app on your device.")
        return 0
    else:
        print("\n⚠️  Installation failed. Check messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

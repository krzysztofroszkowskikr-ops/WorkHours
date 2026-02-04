#!/usr/bin/env python3
"""
Build Android APK for WorkHours App

Streamlined APK build with progress tracking and error handling.

Usage:
    python build_apk.py [--debug|--release]
    python build_apk.py --debug         # Build debug APK
    python build_apk.py --release       # Build release APK (requires signing)
"""

import sys
import subprocess
import argparse
from pathlib import Path
import time


def check_prerequisites():
    """Check if all prerequisites are met"""
    print("\n" + "=" * 60)
    print("CHECKING PREREQUISITES")
    print("=" * 60)
    
    checks = {
        "buildozer.spec exists": Path("buildozer.spec").exists(),
        "src/app.py exists": Path("src").exists() and Path("src/app.py").exists(),
        "src/main.py exists": Path("src").exists() and Path("src/main.py").exists(),
    }
    
    all_ok = True
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
        if not result:
            all_ok = False
    
    return all_ok


def run_command(cmd, description=""):
    """Run a command and capture output"""
    print(f"\n{'━' * 60}")
    if description:
        print(f"[{description}]")
    print(f"$ {' '.join(cmd)}")
    print('━' * 60)
    
    try:
        process = subprocess.Popen(
            cmd,
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
        return returncode == 0, returncode
        
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False, 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, 1


def clean_build():
    """Clean previous build artifacts"""
    print("\n" + "=" * 60)
    print("CLEANING PREVIOUS BUILD")
    print("=" * 60)
    
    cleanup_dirs = [".buildozer", "bin"]
    
    for dir_name in cleanup_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"Removing {dir_name}...")
            # Use system command to remove directory
            import shutil
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Removed {dir_name}")
            except Exception as e:
                print(f"⚠️  Could not remove {dir_name}: {e}")
        else:
            print(f"⚠️  {dir_name} not found (skipping)")


def build_apk(build_type="debug"):
    """Build APK using buildozer"""
    
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed!")
        return False
    
    print("\n" + "=" * 60)
    print(f"BUILDING {build_type.upper()} APK")
    print("=" * 60)
    
    start_time = time.time()
    
    # Build command
    cmd = ["buildozer", "android", build_type]
    
    success, returncode = run_command(
        cmd,
        description=f"Buildozer {build_type.upper()} Build"
    )
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("BUILD RESULT")
    print("=" * 60)
    
    if success:
        print(f"✅ APK build successful! ({elapsed/60:.1f} minutes)")
        
        # Find APK file
        bin_dir = Path("bin")
        apk_files = list(bin_dir.glob("*.apk")) if bin_dir.exists() else []
        
        if apk_files:
            apk_path = apk_files[-1]  # Get latest
            apk_size = apk_path.stat().st_size / (1024 * 1024)
            print(f"\n📦 APK Location: {apk_path}")
            print(f"   Size: {apk_size:.1f}MB")
            
            if build_type == "debug":
                print(f"\n🚀 Next steps:")
                print(f"   1. Connect Android device via USB")
                print(f"   2. Enable Developer Mode & USB Debugging on device")
                print(f"   3. Run: adb install -r {apk_path}")
                print(f"   4. Or: python install_apk.py")
        
        return True
    else:
        print(f"❌ APK build failed (exit code: {returncode})")
        print(f"   Duration: {elapsed/60:.1f} minutes")
        print(f"\n   Check error messages above for details")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Build Android APK for WorkHours App"
    )
    parser.add_argument(
        "--type",
        choices=["debug", "release"],
        default="debug",
        help="Build type (default: debug)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean previous build before building"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("WORKHOURS - ANDROID APK BUILD")
    print("=" * 60)
    
    if args.clean:
        clean_build()
    
    success = build_apk(args.type)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

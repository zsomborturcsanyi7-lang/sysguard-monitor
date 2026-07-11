import subprocess
import sys
import os

def run_command(cmd, check=True):
    """Run a shell command"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0 and check:
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("ERROR: Python 3.7 or higher required!")
        return False
    return True

def install_package(package):
    """Install a Python package"""
    print(f"Installing {package}...")
    return run_command(f"{sys.executable} -m pip install {package}")

def main():
    print("=" * 50)
    print("SysGuard Installer")
    print("=" * 50)
    
    # Check Python
    if not check_python_version():
        return
    
    # Upgrade pip
    print("\nUpgrading pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip", check=False)
    
    # Required packages
    packages = [
        "psutil",      # System monitoring
        "requests",    # For potential API calls
        "colorama",    # Colored console output (optional)
    ]
    
    # Install packages
    success = True
    for package in packages:
        if not install_package(package):
            print(f"Failed to install {package}")
            success = False
    
    if success:
        print("\n" + "=" * 50)
        print("Installation completed successfully!")
        print("\nNext steps:")
        print("1. Edit config/config.json with your settings")
        print("2. Run: python sysguard.py")
        print("3. Or try simple version: python sysguard_simple.py")
        print("=" * 50)
    else:
        print("\nInstallation had errors. Some packages may not be installed.")
    
    # Create a requirements.txt file
    print("\nCreating requirements.txt...")
    with open("requirements.txt", "w") as f:
        for package in packages:
            f.write(f"{package}\n")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
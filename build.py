import os
import subprocess
import sys

def build_executable():
    print("Building Medieval Chess executable...")
    
    # Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    build_command = [
        "pyinstaller",
        "--name=MedievalChess",
        "--onefile",
        "--windowed",
        "--add-data=images;images",  # Include images folder
        "medieval-chess.py"
    ]
    
    # Run the build command
    try:
        subprocess.check_call(build_command)
        print("\nBuild completed successfully!")
        print("\nThe executable can be found in the 'dist' folder.")
        print("You can run 'MedievalChess.exe' from there.")
    except subprocess.CalledProcessError as e:
        print(f"\nError during build: {e}")
        return False
    
    return True

if __name__ == "__main__":
    build_executable() 
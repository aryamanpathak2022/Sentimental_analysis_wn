import subprocess
import sys
import os

def setup_environment():
    # Create a virtual environment
    subprocess.run(['python', '-m', 'venv', 'venv'], check=True)
    
    # Activate the virtual environment
    activate_script = 'venv\\Scripts\\activate' if os.name == 'nt' else 'venv/bin/activate'
    subprocess.run([activate_script], shell=True, check=True)

    # Install the dependencies
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)

def run_scripts():
    subprocess.run(['python', 'preprocessing.py'], check=True)
    subprocess.run(['python', 'main.py'], check=True)
    # Add more scripts as needed

def deactivate_environment():
    # Deactivate the virtual environment
    subprocess.run(['deactivate'], shell=True, check=True)

def main():
    setup_environment()
    run_scripts()
    deactivate_environment()
    print("Script execution completed.")

if __name__ == "__main__":
    main()

import subprocess
import sys
import os

def run_command(command, cwd="."):
    print(f"Executing: {command} in {cwd}")
    try:
        subprocess.run(command, cwd=cwd, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Check Failed: {command}")
        sys.exit(1)

def main():
    print("🚀 Starting Production Release Automation...")
    
    # 0. Enforce Production Environment
    print("\n🌍 Enforcing Production Environment...")
    try:
        # Import the switcher module properly or execute it
        # Since it's in a sibling dir, let's use subprocess to be safe and consistent
        subprocess.run("python3 scripts/switch_env.py prod", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to switch to Production Environment. Aborting.")
        sys.exit(1)

    # 1. Backend Pre-Flight

    print("\n🔍 verifying Backend Health...")
    # Compile python files to check for syntax errors
    run_command("python3 -m compileall -q app", cwd="backend")
    print("✅ Backend Syntax OK")

    # 2. Frontend Pre-Flight
    print("\n🔍 Verifying Frontend Health...")
    # Run build to check for compilation/lint errors
    # We use 'npm run build' as the gold standard for 'ready for production'
    run_command("npm run build", cwd=".")
    print("✅ Frontend Build OK")

    # 3. Git Operations
    print("\n📦 Pushing to Git...")
    
    # Get Commit Message
    if len(sys.argv) > 1:
        message = sys.argv[1]
    else:
        # Ask user if interactive, else default
        message = "Release: Automated Production Push"
    
    # Check status
    changes = subprocess.getoutput("git status --porcelain")
    if not changes:
        print("⚠️  No changes detected. Pushing anyway (to sync remote)...")
        run_command("git push origin main")
    else:
        run_command("git add .")
        run_command(f'git commit -m "{message}"')
        run_command("git push origin main")

    print("\n✨ Release Complete! Code is Live on GitHub.")
    print("   -> Railway will deploy Backend")
    print("   -> Vercel will deploy Frontend")

if __name__ == "__main__":
    main()

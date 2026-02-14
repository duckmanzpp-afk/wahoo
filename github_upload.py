#!/usr/bin/env python3
"""
🚀 GitHub Upload Helper
Auto-setup Git and upload to GitHub
"""

import subprocess
import os
import sys

def run_cmd(cmd, description=""):
    """Run command and show status"""
    print(f"\n▶️  {description}")
    print(f"   $ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"   ✅ Success")
        if result.stdout:
            print(f"   {result.stdout.strip()[:100]}")
        return True
    else:
        print(f"   ❌ Error: {result.stderr.strip()[:100]}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 GITHUB UPLOAD HELPER".center(60))
    print("="*60 + "\n")
    
    # Check git
    print("1️⃣  Checking Git...")
    result = subprocess.run("git --version", shell=True, capture_output=True)
    if result.returncode != 0:
        print("   ❌ Git not found!")
        print("   💡 Install: https://git-scm.com/download/win")
        return 1
    print("   ✅ Git found")
    
    # Get user info
    print("\n2️⃣  Configure Git")
    name = input("   Your Name: ").strip()
    email = input("   Your Email: ").strip()
    
    if not name or not email:
        print("   ❌ Name and email required")
        return 1
    
    run_cmd(f'git config --global user.name "{name}"', f"Set user name to '{name}'")
    run_cmd(f'git config --global user.email "{email}"', f"Set user email to '{email}'")
    
    # Get GitHub URL
    print("\n3️⃣  GitHub Repository")
    repo_url = input("   Enter GitHub repo URL: ").strip()
    
    if not repo_url.startswith("http") and not repo_url.startswith("git@"):
        print("   ❌ Invalid URL")
        return 1
    
    # Initialize repo
    print("\n4️⃣  Initialize Git Repository")
    
    if os.path.exists(".git"):
        print("   ⚠️  Repository already initialized")
    else:
        run_cmd("git init", "Initialize git repository")
    
    # Add all files
    print("\n5️⃣  Add Files")
    run_cmd("git add .", "Stage all files")
    
    # Commit
    print("\n6️⃣  Create Initial Commit")
    commit_msg = """Initial commit: Viral Video Generator System

- 4-Component Architecture (Audio, Content, Vision, Rendering)
- YouTube download support
- Auto-device detection (CPU/GPU)
- Mock analysis fallback
- Quick start scripts included"""
    
    run_cmd(f'git commit -m "{commit_msg}"', "Create initial commit")
    
    # Add remote
    print("\n7️⃣  Add GitHub Remote")
    run_cmd(f"git remote rm origin 2>nul || true", "Remove existing remote (if any)")
    run_cmd(f'git remote add origin "{repo_url}"', f"Add remote: {repo_url}")
    
    # Set main branch
    print("\n8️⃣  Set Main Branch")
    run_cmd("git branch -M main", "Rename branch to main")
    
    # Push
    print("\n9️⃣  Push to GitHub")
    print("   💡 You may be asked for credentials...")
    if run_cmd(f"git push -u origin main", "Push to GitHub"):
        print("\n" + "="*60)
        print("✅ UPLOAD SUCCESSFUL!".center(60))
        print("="*60)
        print(f"\n🎉 Repository: {repo_url}")
        print("   Share with: git clone", repo_url.replace("https://", "").replace(".git", ""))
        print("\n✨ Ready to let others use your Viral Video Generator!\n")
        return 0
    else:
        print("\n⚠️  Push failed - check credentials and try again")
        print("   Help: https://github.com/GITHUB_UPLOAD.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())

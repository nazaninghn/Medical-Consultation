#!/usr/bin/env python3
"""
Quick GitHub Update Script
Simple one-command update for GP Medical Assistant
"""

import subprocess
import sys
from datetime import datetime

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def quick_update():
    """Quick update to GitHub"""
    print("🚀 Quick GitHub Update - GP Medical Assistant")
    print("=" * 45)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Quick commit message
    commit_msg = f"🔄 Update GP Medical Assistant - {timestamp}"
    
    print("📦 Adding all changes...")
    if not run_command("git add ."):
        return False
    
    print("💾 Committing changes...")
    if not run_command(f'git commit -m "{commit_msg}"'):
        print("ℹ️  No changes to commit")
    
    print("🚀 Pushing to GitHub...")
    if not run_command("git push origin main"):
        return False
    
    print("✅ Successfully updated GitHub!")
    return True

if __name__ == "__main__":
    try:
        if quick_update():
            print("🎉 Your GP Medical Assistant is updated on GitHub!")
        else:
            print("❌ Update failed")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Update cancelled")
        sys.exit(1)
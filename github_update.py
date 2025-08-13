#!/usr/bin/env python3
"""
GitHub Update Script for GP Medical Assistant
Automated script to update GitHub repository with all changes
"""

import os
import subprocess
import sys
from datetime import datetime

class GitHubUpdater:
    """Automated GitHub repository updater"""
    
    def __init__(self):
        self.repo_path = os.getcwd()
        self.changes_detected = False
        
    def run_git_command(self, command):
        """Run a git command and return the result"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=self.repo_path
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def check_git_status(self):
        """Check current git status"""
        print("🔍 Checking Git status...")
        success, stdout, stderr = self.run_git_command("git status --porcelain")
        
        if success:
            if stdout.strip():
                self.changes_detected = True
                print("✅ Changes detected in repository")
                return True
            else:
                print("ℹ️  No changes detected")
                return False
        else:
            print(f"❌ Error checking git status: {stderr}")
            return False
    
    def show_changes(self):
        """Show what changes will be committed"""
        print("\n📋 Changes to be committed:")
        print("=" * 40)
        
        # Show modified files
        success, stdout, stderr = self.run_git_command("git status --porcelain")
        if success:
            lines = stdout.strip().split('\n')
            for line in lines:
                if line.strip():
                    status = line[:2]
                    filename = line[3:]
                    
                    if status == "??":
                        print(f"📄 NEW FILE: {filename}")
                    elif status == " M":
                        print(f"✏️  MODIFIED: {filename}")
                    elif status == "A ":
                        print(f"➕ ADDED: {filename}")
                    elif status == "D ":
                        print(f"🗑️  DELETED: {filename}")
                    else:
                        print(f"🔄 CHANGED: {filename}")
    
    def add_all_changes(self):
        """Add all changes to git staging"""
        print("\n📦 Adding all changes to staging...")
        
        # Add all files
        success, stdout, stderr = self.run_git_command("git add .")
        
        if success:
            print("✅ All changes added to staging area")
            return True
        else:
            print(f"❌ Error adding changes: {stderr}")
            return False
    
    def create_commit_message(self):
        """Create a comprehensive commit message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        commit_message = f"""🚀 Major Update: Complete GP Medical Assistant Enhancement

🎯 New Features Added:
- 🤗 Multiple AI model support (Hugging Face, Ollama, Free APIs)
- 🧠 RAG (Retrieval-Augmented Generation) system with medical knowledge base
- 🎨 Enhanced responsive UI with luxury design
- 🎤 Speech-to-speech functionality (voice input/output)
- 📁 File upload and processing (images, documents, audio)
- 🌐 Multiple deployment options (Render, Railway, Vercel, Docker)

🤖 AI Models Supported:
- Google Gemini (premium)
- Zephyr-7B, Mistral-7B, Llama2-7B, OpenChat-3.5 (free)
- Ollama local models (privacy-focused)
- Free API services (Together AI, Groq, Perplexity)

🧠 RAG System:
- Medical knowledge base with 7 comprehensive documents
- FAISS vector database for semantic search
- Evidence-based medical responses
- Expandable knowledge management

🎨 Frontend Enhancements:
- Modern responsive design with 5 breakpoints
- Luxury color scheme (gold, navy, emerald)
- Smooth animations and transitions
- Voice recording and playback
- File drag-and-drop interface
- Mobile-optimized touch controls

🚀 Deployment Ready:
- Multiple cloud platform support
- Docker containerization
- Environment-based configuration
- Production-ready setup

📚 Documentation:
- Comprehensive guides for all features
- Component location mapping
- Deployment instructions
- RAG system documentation

👩‍💻 Developed by Nazanin
Updated: {timestamp}"""

        return commit_message
    
    def commit_changes(self):
        """Commit changes with comprehensive message"""
        print("\n💾 Committing changes...")
        
        commit_message = self.create_commit_message()
        
        # Escape quotes in commit message
        escaped_message = commit_message.replace('"', '\\"')
        
        success, stdout, stderr = self.run_git_command(f'git commit -m "{escaped_message}"')
        
        if success:
            print("✅ Changes committed successfully")
            return True
        else:
            print(f"❌ Error committing changes: {stderr}")
            return False
    
    def push_to_github(self):
        """Push changes to GitHub"""
        print("\n🚀 Pushing to GitHub...")
        
        success, stdout, stderr = self.run_git_command("git push origin main")
        
        if success:
            print("✅ Successfully pushed to GitHub!")
            print("🌐 Your repository is now updated")
            return True
        else:
            print(f"❌ Error pushing to GitHub: {stderr}")
            return False
    
    def show_repository_info(self):
        """Show repository information"""
        print("\n📊 Repository Information:")
        print("=" * 30)
        
        # Get remote URL
        success, stdout, stderr = self.run_git_command("git remote get-url origin")
        if success:
            repo_url = stdout.strip()
            print(f"🔗 Repository URL: {repo_url}")
        
        # Get current branch
        success, stdout, stderr = self.run_git_command("git branch --show-current")
        if success:
            branch = stdout.strip()
            print(f"🌿 Current Branch: {branch}")
        
        # Get last commit
        success, stdout, stderr = self.run_git_command("git log -1 --oneline")
        if success:
            last_commit = stdout.strip()
            print(f"📝 Last Commit: {last_commit}")
    
    def update_repository(self):
        """Complete repository update process"""
        print("🚀 GP Medical Assistant - GitHub Update")
        print("=" * 50)
        
        # Check if we're in a git repository
        if not os.path.exists('.git'):
            print("❌ Not a git repository. Please run 'git init' first.")
            return False
        
        # Check for changes
        if not self.check_git_status():
            print("ℹ️  Repository is already up to date!")
            self.show_repository_info()
            return True
        
        # Show what will be changed
        self.show_changes()
        
        # Confirm with user
        print(f"\n❓ Do you want to commit and push these changes? (y/n): ", end="")
        confirmation = input().lower().strip()
        
        if confirmation != 'y':
            print("❌ Update cancelled by user")
            return False
        
        # Add all changes
        if not self.add_all_changes():
            return False
        
        # Commit changes
        if not self.commit_changes():
            return False
        
        # Push to GitHub
        if not self.push_to_github():
            return False
        
        # Show final repository info
        self.show_repository_info()
        
        print("\n🎉 GitHub repository updated successfully!")
        print("🌟 Your GP Medical Assistant is now live on GitHub with all enhancements!")
        
        return True

def main():
    """Main function"""
    updater = GitHubUpdater()
    
    try:
        success = updater.update_repository()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Update cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
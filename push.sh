#!/bin/bash

# EdgeForge Push Script
# This script helps push the EdgeForge project to GitHub

set -e  # Exit on error

echo "================================================================"
echo "EdgeForge - GitHub Push Script"
echo "================================================================"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    echo "Please run this script from the EdgeForge directory"
    exit 1
fi

# Show current status
echo "📊 Current Git Status:"
git status --short
echo ""

# Show commits ready to push
echo "📝 Commits ready to push:"
git log origin/main..HEAD --oneline
echo ""

# Confirm with user
read -p "🚀 Ready to push to GitHub? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Pushing to origin/main..."
    
    # Attempt push
    if git push origin main; then
        echo ""
        echo "✅ Successfully pushed to GitHub!"
        echo ""
        echo "Repository: https://github.com/financecommander/musical-fishstick"
        echo ""
        echo "Next steps:"
        echo "  1. Visit the repository on GitHub"
        echo "  2. Verify files are present"
        echo "  3. Test installation: pip install git+https://github.com/financecommander/musical-fishstick.git"
    else
        echo ""
        echo "❌ Push failed!"
        echo ""
        echo "Common solutions:"
        echo "  1. Check GitHub credentials: git credential-helper"
        echo "  2. Use SSH instead: git remote set-url origin git@github.com:financecommander/musical-fishstick.git"
        echo "  3. Generate Personal Access Token: https://github.com/settings/tokens"
        echo "  4. Manual push: gh auth login && git push origin main"
        exit 1
    fi
else
    echo "❌ Push cancelled"
    exit 0
fi

#!/bin/bash
# Script to push EduLingua Pro to GitHub

echo "🚀 Pushing EduLingua Pro to GitHub"
echo "=================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Add all files
echo "📝 Adding all files..."
git add .

# Check what will be committed
echo ""
echo "📋 Files to be committed:"
git status --short | head -20

# Commit
echo ""
echo "💾 Creating commit..."
git commit -m "Initial commit: EduLingua Pro - Complete NLP Language Learning Platform

Features:
- Full-stack AI-powered language learning platform
- Advanced NLP models (T5, Pegasus, Sentence-BERT)
- Grammar correction and rephrasing
- Text analytics and evaluation metrics
- Interactive chatbot and dialog practice
- Progress tracking and gamification
- Dark mode UI with modern design
- Comprehensive evaluation dashboard"

# Set main branch
git branch -M main

echo ""
echo "✅ Local repository ready!"
echo ""
echo "📤 Next steps:"
echo "1. Create a new repository on GitHub: https://github.com/new"
echo "2. Copy the repository URL"
echo "3. Run these commands (replace YOUR_USERNAME and REPO_NAME):"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "   git push -u origin main"
echo ""
echo "Or if using SSH:"
echo "   git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git"
echo "   git push -u origin main"
echo ""


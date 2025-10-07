#!/bin/bash

# GRNLITE Production Deployment Script
# Run this to deploy to production

echo "🚀 GRNLITE Production Deployment"
echo "================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Not in GRNLITE project directory"
    exit 1
fi

echo "📝 Step 1: Checking git status..."
git status

echo ""
echo "📦 Step 2: Adding all changes..."
git add .

echo ""
echo "💾 Step 3: Committing changes..."
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Production deployment: $(date '+%Y-%m-%d %H:%M')"
fi
git commit -m "$commit_msg"

echo ""
echo "🚀 Step 4: Pushing to production..."
git push origin main

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "📋 Next steps:"
echo "1. Check Render dashboard: https://dashboard.render.com"
echo "2. Verify environment variables are set:"
echo "   - JWT_SECRET"
echo "   - JWT_REFRESH_SECRET" 
echo "   - DJANGO_SECRET_KEY"
echo "3. Monitor deployment logs"
echo "4. Test your app at: https://grnlite.onrender.com"
echo ""
echo "🔍 Useful commands:"
echo "  ./prod-deploy.sh status  - Check deployment status"
echo "  ./prod-deploy.sh logs    - View deployment logs"
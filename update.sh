#!/bin/bash
# Simple script to update and deploy from macOS/Linux
# Usage: ./update.sh "Your update message"

msg="${1:-Update content}"

echo ""
echo "=== Pit Wall Auto-Deploy ==="
echo ""
echo "Staging data/content.json..."
git add data/content.json

echo "Committing..."
git commit -m "Update: $msg"

if [ $? -ne 0 ]; then
  echo ""
  echo "No changes to commit. Exiting."
  exit 0
fi

echo "Pushing to main..."
git push origin main

if [ $? -eq 0 ]; then
  echo ""
  echo "✓ Update deployed successfully!"
  echo "Your site will refresh in ~30 seconds."
  echo ""
else
  echo ""
  echo "✗ Push failed. Check your git setup."
  exit 1
fi

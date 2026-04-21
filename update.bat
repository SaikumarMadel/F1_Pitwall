@echo off
REM Simple script to update and deploy from Windows
REM Usage: run-update.bat "Your update message"

setlocal enabledelayedexpansion

if "%1"=="" (
  set "msg=Update content"
) else (
  set "msg=%1"
)

echo.
echo === Pit Wall Auto-Deploy ===
echo.
echo Staging data/content.json...
git add data/content.json

echo Committing...
git commit -m "Update: %msg%"

if %errorlevel% neq 0 (
  echo.
  echo No changes to commit. Exiting.
  exit /b 0
)

echo Pushing to main...
git push origin main

if %errorlevel% equ 0 (
  echo.
  echo ✓ Update deployed successfully!
  echo Your site will refresh in ~30 seconds.
  echo.
) else (
  echo.
  echo ✗ Push failed. Check your git setup.
  exit /b 1
)

endlocal

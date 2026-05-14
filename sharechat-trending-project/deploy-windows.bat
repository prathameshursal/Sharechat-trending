@echo off
echo ==========================================
echo  ShareChat Trending Tags - Windows Deploy
echo ==========================================
echo.

node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Install from https://nodejs.org
    pause
    exit /b 1
)

vercel --version >nul 2>&1
if errorlevel 1 (
    echo Installing Vercel CLI...
    npm install -g vercel
)

echo.
echo [1/3] Logging into Vercel...
vercel login

echo.
echo [2/3] Deploying to production...
vercel --prod

echo.
echo [3/3] Done! Copy the URL above.
echo.
pause

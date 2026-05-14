# ShareChat Trending Tags - Windows Deploy
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  ShareChat Trending Tags - Deploy Tool" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

try {
    $nodeVersion = node --version
    Write-Host "[OK] Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js not found!" -ForegroundColor Red
    Read-Host "Press Enter"
    exit 1
}

try {
    $vercelVersion = vercel --version
    Write-Host "[OK] Vercel CLI: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "[INFO] Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
}

Write-Host ""
Write-Host "[Step 1/3] Logging into Vercel..." -ForegroundColor Cyan
vercel login

Write-Host ""
Write-Host "[Step 2/3] Deploying..." -ForegroundColor Cyan
vercel --prod

Write-Host ""
Write-Host "[Step 3/3] Complete!" -ForegroundColor Green
Write-Host "Copy the URL above for your submission." -ForegroundColor Green
Read-Host "Press Enter"

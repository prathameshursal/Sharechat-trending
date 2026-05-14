# Windows Deployment Guide

## Prerequisites (Install First)

### 1. Install Node.js
1. Go to https://nodejs.org
2. Download LTS version
3. Run installer -> Next -> Next -> Finish
4. Verify in CMD:
   ```
   node --version
   npm --version
   ```

### 2. Install Vercel CLI
```cmd
npm install -g vercel
```

### 3. Install Git
1. Go to https://git-scm.com/download/win
2. Download and install
3. Verify:
   ```cmd
   git --version
   ```

---

## Deploy to Vercel (2 minutes)

### Step 1: Open Project Folder
```cmd
cd C:\Users\YourName\Downloads\sharechat-trending
```

### Step 2: Login to Vercel
```cmd
vercel login
```
- Opens browser -> click "Continue"

### Step 3: Deploy
```cmd
vercel --prod
```
- "Set up and deploy?" -> Y
- "Which scope?" -> Press Enter
- "Link to existing project?" -> N
- "Project name?" -> sharechat-trending
- Copy the URL!

---

## Push to GitHub

```cmd
cd C:\Users\YourName\Downloads\sharechat-trending
git init
git add .
git commit -m "Initial commit"
```

Then go to https://github.com/new, create repo, and push:
```cmd
git remote add origin https://github.com/YOURNAME/sharechat-trending.git
git branch -M main
git push -u origin main
```

---

## Record Loom Video

1. Install Loom from https://loom.com
2. Open your deployed URL in Chrome
3. Press Ctrl+Shift+L (or click Loom extension)
4. Record 2-minute walkthrough
5. Copy Loom URL

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| Deploy | vercel --prod |
| Push to GitHub | git push origin main |
| Open prototype | Double-click index.html |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "vercel not recognized" | npm install -g vercel |
| "git not recognized" | Reinstall Git, check "Add to PATH" |
| Hindi text shows boxes | Use Chrome/Edge |
| Deployment fails | Check internet, try vercel --force |

---

## Submission Checklist

- [ ] Deployed URL (Vercel/Netlify)
- [ ] GitHub repo URL
- [ ] Loom video URL (2 min)
- [ ] Screenshot attached

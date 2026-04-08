# 🚀 Deployment Guide - ResumeIQ

Make your **ResumeIQ** externally accessible to anyone! Follow these steps to deploy to **Vercel** for free.

## **Step 1: Create Environment Files**

### Frontend (.env.local)
```bash
# frontend/.env.local
VITE_API_URL=http://localhost:5000/api
```

### Frontend Production (.env.production)
```bash
# frontend/.env.production
VITE_API_URL=https://your-project-name.vercel.app/api
```

## **Step 2: Deploy to Vercel**

### Option A: Using Vercel CLI (Recommended)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy your project:**
   ```bash
   cd c:\Arnav\Etc\Blueprint\Project
   vercel
   ```

4. **Follow the prompts:**
   - Confirm project name
   - Select framework: **Other**
   - Select build directory: `frontend/dist`
   - Accept all defaults

### Option B: Using GitHub (Auto Deploy)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **Go to [vercel.com](https://vercel.com)**

3. **Click "New Project"**

4. **Import your GitHub repository**

5. **Set Environment Variables:**
   - Go to **Project Settings → Environment Variables**
   - Add: `VITE_API_URL` = `https://your-project-name.vercel.app/api`

6. **Click Deploy**

## **Step 3: Set Vercel Environment Variables**

After deployment, set these in Vercel Dashboard:

1. Go to **Project Settings → Environment Variables**

2. Add for **Production**:
   - Name: `VITE_API_URL`
   - Value: `https://your-project-name.vercel.app/api`

3. Your backend will be accessible at: `https://your-project-name.vercel.app/_/backend/`

## **Step 4: Update Backend API Base URL**

Once deployed, update the frontend to use the production API URL:

1. In `frontend/.env.production`, set:
   ```
   VITE_API_URL=https://your-project-name.vercel.app/api
   ```

2. Redeploy:
   ```bash
   vercel --prod
   ```

## **Step 5: Test External Access**

Visit your deployed app:
- 🌐 **Frontend**: https://your-project-name.vercel.app
- 📡 **API Health**: https://your-project-name.vercel.app/api

Anyone can now access your app from anywhere! 🎉

## **Troubleshooting**

### API Calls Failing?
- Check `vite.config.js` has the correct build output
- Verify `VITE_API_URL` is set in Vercel environment variables
- Check backend logs in Vercel dashboard

### CORS Errors?
- Backend already has CORS enabled ✅
- If issues persist, check `backend/app.py` CORS configuration

### Cannot Deploy?
- Make sure `vercel.json` is correct
- Check that `backend/requirements.txt` exists
- Verify both `frontend/package.json` and `backend/app.py` are present

## **Your App URLs After Deployment**

- **Frontend**: `https://your-project-name.vercel.app`
- **Backend API**: `https://your-project-name.vercel.app/api`
- **Share Link**: Share the frontend URL with anyone!

---

**Questions?** Check Vercel docs: https://vercel.com/docs

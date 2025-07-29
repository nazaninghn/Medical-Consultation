# 🚀 Deploy GP Medical Assistant to Vercel via GitHub

## 📋 Prerequisites
- GitHub account
- Vercel account (free)
- Google Gemini API key

## 🔧 Step-by-Step Deployment

### 1. **Push to GitHub**

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: GP Medical Assistant"

# Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/yourusername/gp-medical-assistant.git

# Push to GitHub
git push -u origin main
```

### 2. **Connect to Vercel**

1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with your GitHub account
3. Click **"New Project"**
4. **Import** your GitHub repository
5. Select **"gp-medical-assistant"** repository

### 3. **Configure Environment Variables**

In Vercel dashboard:
1. Go to **Settings** → **Environment Variables**
2. Add the following variable:
   - **Name**: `GOOGLE_API_KEY`
   - **Value**: Your Google Gemini API key
   - **Environment**: Production, Preview, Development

### 4. **Deploy**

1. Click **"Deploy"** button
2. Wait for build to complete (2-3 minutes)
3. Your app will be live at: `https://your-project-name.vercel.app`

## 🔧 Build Configuration

Vercel will automatically:
- ✅ Detect Python Flask app
- ✅ Install dependencies from `api/requirements.txt`
- ✅ Configure serverless functions
- ✅ Set up routing

## 🌐 Features Available on Vercel

✅ **Text Chat** - Full medical consultation  
✅ **Modern UI** - Responsive design  
✅ **File Upload** - Images, documents, audio  
✅ **Voice Recording** - Browser-based recording  
⚠️ **Audio Responses** - Limited (serverless constraints)  
✅ **Mobile Support** - Full responsive design  

## 🔧 Troubleshooting

### Build Errors
- Check `api/requirements.txt` for dependency issues
- Verify Python version compatibility

### Runtime Errors
- Check environment variables are set
- Verify Google API key is valid
- Check function timeout limits

### File Upload Issues
- Files are stored in `/tmp` (temporary)
- Large files may timeout
- Consider using external storage for production

## 📱 Post-Deployment

After successful deployment:
1. Test all features
2. Share your live URL
3. Monitor usage in Vercel dashboard
4. Set up custom domain (optional)

## 🔒 Security Notes

- ✅ API keys are secure in Vercel environment
- ✅ Files are temporarily stored
- ✅ HTTPS enabled by default
- ✅ CORS configured properly

## 🚀 Your Live App

Once deployed, your GP Medical Assistant will be available at:
`https://your-project-name.vercel.app`

Enjoy your modern medical consultation app! 🩺✨
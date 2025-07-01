# 🚀 Streamlit Community Cloud Deployment Guide

**@author SaltyHeart**

Complete guide for deploying Trad-Chem LLM to Streamlit Community Cloud.

## 📋 Pre-Deployment Checklist

### ✅ Required Files Present:
- `app.py` - Main Streamlit application
- `requirements.txt` - Dependencies (optimized for cloud)
- `config.py` - Configuration with secrets support
- `.streamlit/config.toml` - Streamlit configuration
- `.streamlit/secrets.toml.example` - Secret template
- `utils/` - Core handlers and utilities
- `Trad-Chem/` - Database directory with JSON file

### ✅ API Key Ready:
- Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🔧 Step-by-Step Deployment

### 1. Prepare Repository

1. **Fork this repository** to your GitHub account
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Trad-Chem-LLM.git
   cd Trad-Chem-LLM
   ```

3. **Verify all files** are present and committed:
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

### 2. Deploy to Streamlit Cloud

1. **Go to [Streamlit Cloud](https://share.streamlit.io)**
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Configure your app**:
   - **Repository**: `your-username/Trad-Chem-LLM`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL (optional)

### 3. Configure Secrets

1. **In Streamlit Cloud**, go to your app settings
2. **Navigate to "Secrets"** tab
3. **Add your secrets**:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key_here"
   ```
4. **Save** the secrets

### 4. Deploy

1. **Click "Deploy"**
2. **Wait** for deployment to complete (usually 2-5 minutes)
3. **Your app will be live** at the provided URL

## 🔍 Verification Steps

### After Deployment:

1. **✅ App loads successfully**
2. **✅ Gemini API status shows connected**
3. **✅ TradChem database status shows loaded**
4. **✅ Chat functionality works**
5. **✅ Database search works**

### Test Queries:
- "What is turmeric used for?"
- "Show me SMILES notation for curcumin"
- "List Ayurvedic medicines"

## 🛠️ Troubleshooting

### Common Issues:

#### 1. API Key Not Working
- **Problem**: "Gemini API key not configured"
- **Solution**: Check secrets are properly set in Streamlit Cloud settings
- **Format**: Ensure no extra spaces or quotes around the key

#### 2. Database Not Loading
- **Problem**: "TradChem database file not found"
- **Solution**: Verify `Trad-Chem/tradchem/data/tradchem_database.json` exists
- **Check**: File should be ~5KB with 4 medicine entries

#### 3. Import Errors
- **Problem**: Module import failures
- **Solution**: Check `requirements.txt` has all dependencies
- **Verify**: No local-only packages or development dependencies

#### 4. Deployment Timeout
- **Problem**: App takes too long to start
- **Solution**: Reduce dependencies in `requirements.txt`
- **Optimize**: Remove unused imports from `app.py`

## 📊 Performance Optimization

### For Better Performance:

1. **Minimal Dependencies**: Only essential packages in `requirements.txt`
2. **Efficient Imports**: Use selective imports
3. **Caching**: Utilize `@st.cache_data` for database loading
4. **Resource Management**: Optimize API calls

### Monitoring:

- **Check logs** in Streamlit Cloud dashboard
- **Monitor resource usage** in app settings
- **Track API quotas** in Google AI Studio

## 🔒 Security Best Practices

### API Key Security:
- ✅ Never commit API keys to repository
- ✅ Use Streamlit secrets management
- ✅ Rotate keys regularly
- ✅ Monitor API usage

### App Security:
- ✅ No sensitive data in logs
- ✅ Validate user inputs
- ✅ Rate limiting (if needed)
- ✅ Regular dependency updates

## 🔄 Updates and Maintenance

### Updating Your App:

1. **Make changes** to your local repository
2. **Test locally**:
   ```bash
   streamlit run app.py
   ```
3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push origin main
   ```
4. **Auto-deployment**: Streamlit Cloud will automatically redeploy

### Monitoring:
- Check app health regularly
- Monitor API usage quotas
- Update dependencies as needed
- Backup important configurations

## 📞 Support

### If You Need Help:

1. **Check logs** in Streamlit Cloud dashboard
2. **Review this guide** for common solutions
3. **Test locally** to isolate cloud-specific issues
4. **Contact support** through Streamlit Community forums

### Useful Links:
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)
- [Google AI Studio](https://makersuite.google.com/app/apikey)
- [Streamlit Community Forum](https://discuss.streamlit.io)

---

🚀 **Your Trad-Chem LLM is now ready for the cloud!** 

**Deployment Time**: ~5-10 minutes  
**Expected Performance**: Fast, responsive, reliable  
**Cost**: Free tier available on Streamlit Cloud  

Happy deploying! 🎉 
# 📝 MCQ Question Generator

An intelligent web application that generates multiple choice questions (MCQ) from uploaded study materials with detailed explanations for each answer.

## ✨ Features

- 📄 **Multiple File Formats**: Supports PDF, TXT, and DOCX files
- 🤖 **AI-Powered**: Uses OpenAI GPT to generate high-quality questions
- 📚 **Smart Explanations**: Each answer includes a brief explanation
- 🎨 **Beautiful UI**: Modern, user-friendly interface built with Streamlit
- 💾 **Export Questions**: Download generated questions as JSON
- 📱 **PWA Ready**: Can be installed as a mobile app
- 🌐 **Deployable**: Easy deployment to web and Android

## 🚀 Quick Start

### Local Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   streamlit run app.py
   ```
   Or double-click `run_app.bat`

3. **Get OpenAI API Key** (optional but recommended):
   - Visit https://platform.openai.com/api-keys
   - Create an account and generate an API key

## 📖 How to Use

1. **Upload your study material**:
   - Click "Choose a file" in the sidebar
   - Select a PDF, TXT, or DOCX file

2. **Configure settings**:
   - Enter your OpenAI API key (optional)
   - Select the number of questions you want (1-20)

3. **Generate questions**:
   - Click "Generate Questions" button
   - Wait for the AI to process your content

4. **Review and learn**:
   - Read each question and options
   - Check the explanation under each answer
   - Download questions as JSON if needed

## 🌐 Deploy as Website

### Streamlit Cloud (Easiest - Free)

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Sign in with GitHub
4. Click "New app" → Select repository → Deploy
5. ✅ Done! Your app is live

**See `WEB_DEPLOYMENT.md` for detailed instructions**

## 📱 Deploy as Android App

### Using PWABuilder

1. Deploy your website first (see above)
2. Go to https://www.pwabuilder.com
3. Enter your website URL
4. Click "Build My PWA" → Android
5. Download APK
6. Upload to Google Play Console

**See `GOOGLE_PLAY_GUIDE_AR.md` for detailed instructions**

## 📚 Deployment Guides

- **Quick Start**: `QUICK_START.md` - Fast deployment guide
- **Web Deployment**: `WEB_DEPLOYMENT.md` - Detailed web hosting guide
- **Google Play**: `GOOGLE_PLAY_GUIDE_AR.md` - Complete Android deployment
- **Full Guide**: `DEPLOYMENT_GUIDE.md` - Comprehensive deployment guide
- **Arabic Guide**: `تعليمات_النشر.md` - دليل شامل بالعربية

## 🎯 Use Cases

- **Students**: Generate practice questions from your notes
- **Teachers**: Create quizzes from course materials
- **Self-Learning**: Test your understanding of any document
- **Exam Preparation**: Practice with questions from your study materials

## 💡 Tips

- **Better results**: Use well-structured documents with clear content
- **API Key**: For best results, use OpenAI API key (GPT-3.5-turbo)
- **File size**: Works best with documents under 10,000 characters per chunk
- **Question quality**: More detailed source material = better questions

## 🔧 Technical Details

- **Framework**: Streamlit
- **AI Model**: OpenAI GPT-3.5-turbo (optional)
- **File Processing**: PyPDF2, python-docx
- **PWA Support**: manifest.json, service-worker.js
- **Language**: English

## 📁 Project Structure

```
mcq_generator/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── manifest.json         # PWA manifest
├── Procfile             # Heroku deployment
├── .streamlit/          # Streamlit config
├── pages/               # Additional pages
├── public/              # Static files
└── *.md                 # Documentation
```

## 📝 License

Free to use for educational purposes.

## 🤝 Contributing

Feel free to improve and customize this project for your needs!

---

**Made with ❤️ for students and educators**


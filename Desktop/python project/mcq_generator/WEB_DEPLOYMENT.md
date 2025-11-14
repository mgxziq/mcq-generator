# 🌐 دليل نشر الموقع على الويب

## الطريقة الأسهل: Streamlit Cloud (مجاني) ⭐

### الخطوات:

#### 1. إنشاء حساب GitHub
- اذهب إلى https://github.com
- أنشئ حساب جديد
- أنشئ مستودع جديد باسم `mcq-generator`

#### 2. رفع الكود على GitHub

افتح Terminal في مجلد `mcq_generator`:

```bash
# تهيئة Git
git init

# إضافة الملفات
git add .

# حفظ التغييرات
git commit -m "Initial commit: MCQ Generator app"

# ربط مع GitHub
git remote add origin https://github.com/YOUR_USERNAME/mcq-generator.git

# رفع الكود
git branch -M main
git push -u origin main
```

#### 3. النشر على Streamlit Cloud

1. اذهب إلى: https://streamlit.io/cloud
2. سجل دخول بحساب GitHub
3. اضغط **"New app"**
4. اختر:
   - **Repository:** mcq-generator
   - **Branch:** main
   - **Main file path:** app.py
5. اضغط **"Deploy"**
6. ✅ موقعك جاهز!

**الرابط سيكون:** `https://mcq-generator-YOUR_USERNAME.streamlit.app`

---

## طرق أخرى للنشر

### Heroku

1. تثبيت Heroku CLI
2. تسجيل الدخول:
   ```bash
   heroku login
   ```
3. إنشاء تطبيق:
   ```bash
   heroku create your-app-name
   ```
4. النشر:
   ```bash
   git push heroku main
   ```

### Render.com

1. اذهب إلى https://render.com
2. سجل دخول بحساب GitHub
3. اضغط "New Web Service"
4. اختر المستودع
5. الإعدادات:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

### Railway

1. اذهب إلى https://railway.app
2. سجل دخول بحساب GitHub
3. اضغط "New Project"
4. اختر "Deploy from GitHub repo"
5. اختر المستودع
6. ✅ جاهز!

---

## إضافة نطاق مخصص (Custom Domain)

### Streamlit Cloud:
- Settings → Custom domain
- أضف نطاقك

### Heroku:
```bash
heroku domains:add www.yourdomain.com
```

---

## SSL/HTTPS

جميع المنصات المذكورة توفر HTTPS تلقائياً! ✅

---

## تحديث التطبيق

بعد أي تغييرات:

```bash
git add .
git commit -m "Update app"
git push
```

سيتم تحديث الموقع تلقائياً!

---

**أسهل طريقة: Streamlit Cloud - مجاني وسهل! 🚀**


Here’s a fresh, professional, and developer-friendly README for your AI Meme & Poster Creator project — tailored for your setup and goals:

---

# 🖼️ AI Meme & Poster Creator (Base44 Integration)

A lightweight, AI-powered meme/poster generator built with **Python + Gradio**, designed for fast local use and seamless integration with the **Base44 API**.

---

## 🚀 Features

- 🖼️ Upload images or paste image URLs  
- ✏️ Add top/bottom text with custom font size, color, and alignment  
- 👀 Preview before saving  
- 💾 Save creations to Base44 via API  
- 🖼️ Built-in gallery to view, edit, and manage saved memes/posters  
- 🧠 Works 100% locally — no external hosting or rate-limit issues

---

## 🔧 Requirements

- Windows 10 or higher  
- Python 3.11+  
- A valid **Base44 API Key** and **App ID**

---

## ⚙️ Setup Instructions (Windows)

###  Clone or open the folder
```bash
cd "C:\Users\Sushe\Dropbox\My PC (LAPTOP-C6A7PQLG)\Desktop\ai-meme-poster"
```

###  Install dependencies
```bash
pip install -r requirements.txt
```



###  Run the app
```bash
app.py
```

---

## 🌐 Access Locally

Once running, open your browser and visit:

```
http://127.0.0.1:7860/
```

> ⚠️ This link works only on your machine. To share your app with others, consider deploying it via:
- Gradio Share
- Local network IP
- Cloud platforms like Render, Hugging Face Spaces, or Heroku

---

## 📁 Folder Structure

```
ai-meme-poster/
├── app.py
├── utils/
│   ├── base44_api.py
│   ├── image_tools.py
├── assets/
│   └── default_templates/
├── gallery/
├── requirements.txt
└── .env
```

---

## 🧪 Testing

- ✅ Upload sample images from `assets/default_templates/`  
- ✅ Try both URL and upload modes  
- ✅ Save to Base44 and verify in gallery

---

## 🙌 Credits

Built by CSK with ❤️ for meme lovers, poster designers, and API tinkerers.


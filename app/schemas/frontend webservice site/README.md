# 🚀 Ramadan Helper - Frontend

**A beautiful Islamic web application for Ramadan with prayer times, Duas, videos, and AI chat.**

---

## 📁 Project Structure

```
📦 Frontend Project
├── 📄 app.html              ← Main application (start here!)
├── 📄 package.json          ← Dependencies
├── 📄 .env.example          ← Environment template
│
├── 📂 src/                  ← Source code
│   ├── components/          ← Vue components
│   ├── pages/               ← Page components
│   ├── styles/              ← CSS files
│   ├── utils/               ← Helper functions
│   └── main.ts              ← Entry point
│
├── 📂 config/               ← Configuration files
│   ├── vite.config.ts       ← Vite configuration
│   ├── tailwind.config.js   ← Tailwind CSS config
│   ├── tsconfig.json        ← TypeScript config
│   └── postcss.config.js    ← PostCSS config
│
├── 📂 public/               ← Static files
│   ├── index.html           ← HTML template
│   └── demo.html            ← Demo page
│
└── 📂 docs/                 ← Documentation
    ├── 📂 GETTING_STARTED/  ← For new users (quick start)
    ├── 📂 GUIDES/           ← Detailed guides
    ├── 📂 REFERENCE/        ← Technical reference
    └── 📂 FINAL/            ← Project summaries
```

---

## 🎯 Quick Start

### 1. **Start the Application**
```bash
# Open in browser (fastest way)
Double-click: app.html
```

### 2. **For Development**
```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm build
```

### 3. **Explore the App**
- 🏠 **Home** - Dashboard and overview
- 💬 **Ask AI** - Chat with AI assistant
- 📿 **Dua Generator** - Generate Islamic prayers
- 📺 **Islamic Videos** - Search and watch videos
- 💬 **Chat** - Chat functionality
- 👨‍🕌 **Imams** - Scholar profiles
- 📜 **History** - View history

---

## 📚 Documentation

### **Getting Started (New Users)**
→ See: `docs/GETTING_STARTED/`
- Quick start guides
- Setup instructions
- Common questions

### **Development Guides**
→ See: `docs/GUIDES/`
- Feature development
- Building and setup
- Troubleshooting

### **Technical Reference**
→ See: `docs/REFERENCE/`
- API integration guide
- Project structure
- Technical details

### **Project Summary**
→ See: `docs/FINAL/`
- Completion summaries
- Verification steps
- Final documentation

---

## 🛠️ Technologies

- **Frontend:** Vanilla JavaScript, Tailwind CSS, HTML5
- **Build:** Vite
- **Styling:** Tailwind CSS, PostCSS
- **Backend:** FastAPI (separate project)
- **API:** RESTful API integration

---

## 📋 Features

✅ **7 Interactive Pages**
- Home dashboard with statistics
- AI-powered chat assistant
- Dua generator with customization
- Video search and playback
- Chat functionality
- Scholar profiles
- History tracking

✅ **YouTube Integration**
- Search Islamic videos
- Import and save videos
- Relevance scoring
- Video management

✅ **Beautiful UI**
- Responsive design
- Modern interface
- Dark/Light modes
- Smooth animations

---

## 🔗 Connect to Backend

The app connects to your FastAPI backend at:
```
http://localhost:8000/api
```

Make sure the backend is running before using video features!

---

## 📝 Environment

Create `.env` file:
```
VITE_API_URL=http://localhost:8000/api
```

---

## 🎨 Customization

- **Colors:** Edit Tailwind config in `config/tailwind.config.js`
- **Content:** Modify pages in `src/pages/`
- **Functions:** Update logic in `src/utils/`

---

## 🚀 Production Build

```bash
npm run build
```

Outputs to `dist/` folder - ready for deployment!

---

## 📞 Support

Check the appropriate docs folder:
- Lost? → `docs/REFERENCE/` (find your guide)
- New? → `docs/GETTING_STARTED/`
- Building? → `docs/GUIDES/`
- Summary? → `docs/FINAL/`

---

**Made with ❤️ for Ramadan**

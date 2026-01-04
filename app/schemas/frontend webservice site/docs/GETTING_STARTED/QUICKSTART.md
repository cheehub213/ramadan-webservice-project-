# Frontend Quick Start Guide

## 🚀 Getting Started

This is a complete React + TypeScript frontend for the Ramadan Assistant. Everything is configured and ready to run!

## 📋 What's Included

✅ **5 Complete Pages:**
1. **Home** - Landing page with feature overview
2. **Dua Generator** - Create personalized duas in English & Arabic
3. **Chat with Imams** - Real-time messaging with Islamic scholars
4. **Find Imams** - Search and discover Islamic scholars
5. **History** - Track all your generated duas and feedback

✅ **Complete API Integration:**
- All endpoints configured in `src/services/api.ts`
- Axios HTTP client ready to use
- Error handling and loading states

✅ **Professional UI/UX:**
- Tailwind CSS with Islamic green theme
- Responsive design (mobile-friendly)
- RTL support for Arabic
- Smooth transitions and hover effects

✅ **TypeScript:** Full type safety throughout

## 🛠️ Setup Instructions

### Step 1: Install Dependencies
```bash
npm install
```
This installs:
- React & React-DOM
- React Router for navigation
- Axios for API calls
- Tailwind CSS for styling
- TypeScript for type safety
- Vite build tools

### Step 2: Start Development Server
```bash
npm run dev
```

You'll see:
```
VITE v5.0.8  ready in 123 ms

➜  Local:   http://localhost:5173/
➜  press h to show help
```

### Step 3: Open in Browser
Visit: **http://localhost:5173/**

## ✨ Features Walkthrough

### Home Page
- **Email Input**: Enter your email to get started
- **Feature Cards**: Quick access to all features
- **About Section**: Learn about the app

### Dua Generator
1. Select a problem category (8 categories available)
2. Describe your situation
3. Click "Generate My Dua"
4. Receive bilingual dua (English + Arabic)
5. Get usage instructions
6. Submit helpful/not helpful feedback

**Example Categories:**
- Fear & Anxiety
- Financial Hardship
- Health Issues
- Family Problems
- Career Guidance
- Spiritual Growth
- Relationship Issues
- Personal Challenges

### Chat with Imams
1. **Available Imams**: See list of scholars
2. **Start New Chat**: Select imam + topic
3. **Real-time Messages**: Send/receive messages
4. **Chat History**: Access previous conversations

### Find Imams
1. **Browse All**: See all available imams
2. **Search**: Filter by name or expertise
3. **Availability**: Check who's online
4. **Quick Chat**: Start conversation immediately

### History
1. **Filter Options**: All / Helpful / Not Helpful
2. **View Details**: See original context and duas
3. **Bilingual Duas**: Both English and Arabic
4. **Feedback Notes**: Your previous notes

## 📁 Project Structure Explained

```
src/
├── pages/                    # All page components
│   ├── Home.tsx             # Landing page
│   ├── DuaGenerator.tsx      # Main feature
│   ├── ChatWithImams.tsx     # Chat interface
│   ├── SearchImams.tsx       # Scholar search
│   └── History.tsx           # Past duas
│
├── services/
│   └── api.ts               # API calls (Axios)
│
├── App.tsx                  # Navigation & routing
├── main.tsx                 # Entry point
└── index.css                # Global styles
```

## 🔌 API Connection

The frontend connects to your backend on `http://127.0.0.1:8001`

**Make sure your backend is running!**

All API calls go through `src/services/api.ts`:
- Dua endpoints (generate, history, feedback, etc.)
- Chat endpoints (messages, conversations, etc.)
- Imam endpoints (list, register, etc.)

## 🎨 Customization

### Change Color Theme
Edit `tailwind.config.js`:
```js
extend: {
  colors: {
    islamic: '#047857',      // Change primary color
    'islamic-light': '#10b981',
  }
}
```

### Add New Pages
1. Create file in `src/pages/NewPage.tsx`
2. Add route in `App.tsx`
3. Add navigation link in header

### Modify API Endpoints
All endpoints are in `src/services/api.ts` - easy to update!

## 🚀 Build & Deploy

### Build for Production
```bash
npm run build
```
Creates optimized files in `dist/` folder

### Deploy Options
- **Vercel**: Zero-config, just push to git
- **Netlify**: Drag-and-drop deploy
- **Docker**: Dockerfile ready to use
- **Any web host**: Copy `dist/` contents

## 🐛 Troubleshooting

### Backend Not Connecting?
- Ensure backend runs on `http://127.0.0.1:8001`
- Check browser console for errors (F12)
- Verify API endpoints in `src/services/api.ts`

### Styling Issues?
- Tailwind CSS might need rebuild
- Try: `npm run dev` restart

### TypeScript Errors?
- All types are pre-configured
- Errors show in VS Code with quick fixes

## 📚 Technology Stack

| Tool | Purpose | Version |
|------|---------|---------|
| React | UI Library | 18.2 |
| TypeScript | Type Safety | 5.3 |
| Vite | Build Tool | 5.0 |
| React Router | Navigation | 6.20 |
| Axios | HTTP Client | 1.6 |
| Tailwind CSS | Styling | 3.4 |
| PostCSS | CSS Processing | 8.4 |

## ✅ Next Steps

1. **Start the app**: `npm run dev`
2. **Test each page**: Click through the UI
3. **Generate a dua**: Fill form and test
4. **Check console**: F12 to see API responses
5. **Customize**: Add your branding/colors

## 📞 Support

All features are fully integrated with the backend API:
- ✅ Dua generation with bilingual support
- ✅ Chat messaging system
- ✅ Imam management
- ✅ History tracking
- ✅ Feedback system

Everything is ready to use - just start the app!

## 🙏 Notes

- The app is fully responsive (mobile-friendly)
- RTL support built-in for Arabic text
- All API errors are handled gracefully
- Loading states show during API calls
- Type-safe throughout with TypeScript

---

**Ready to launch?** → `npm run dev`

**May Allah bless this effort! 🌙**

# Ramadan Helper Frontend

A modern React + TypeScript frontend for the Ramadan Decision Assistant web service. This application provides a user-friendly interface for:

- **🕋 Personalized Dua Generation** - AI-powered duas in both English and Arabic
- **💬 Chat with Islamic Scholars** - Real-time conversations with learned imams
- **🔍 Find Imams** - Search and connect with Islamic scholars
- **📚 Dua History** - Track and manage your past duas and feedback

## Tech Stack

- **React 18.2** - UI framework
- **TypeScript 5.3** - Type-safe JavaScript
- **Vite 5.0** - Fast build tool and dev server
- **React Router 6.20** - Client-side routing
- **Axios 1.6** - HTTP client
- **Tailwind CSS 3.4** - Utility-first CSS framework
- **PostCSS** - CSS processing

## Prerequisites

- Node.js 18+ and npm 9+
- Backend API running on `http://127.0.0.1:8001`

## Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Create environment file:**
```bash
cp .env.example .env.local
```

3. **Start the development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Project Structure

```
src/
├── pages/              # Page components
│   ├── Home.tsx       # Landing page
│   ├── DuaGenerator.tsx    # Dua generation page
│   ├── ChatWithImams.tsx   # Chat interface
│   ├── SearchImams.tsx     # Imam search
│   └── History.tsx         # Dua history
├── components/        # Reusable components (expandable)
├── services/
│   └── api.ts         # API service layer & Axios configuration
├── App.tsx            # Main app component with routing
├── main.tsx           # React entry point
└── index.css          # Global styles with Tailwind
```

## Available Scripts

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint TypeScript
npm run lint
```

## Features

### 1. Home Page
- Landing page with feature overview
- Email input for user identification
- Navigation to all features

### 2. Dua Generator
- Select from 8 problem categories
- Provide context for personalized duas
- Receive bilingual duas (English + Arabic)
- Get usage instructions
- Submit feedback (helpful/not helpful)

### 3. Chat with Imams
- View available Islamic scholars
- Start new conversations
- Real-time messaging interface
- Access conversation history
- Track read/unread messages

### 4. Find Imams
- Browse all available imams
- View expertise and availability status
- Search by name or specialty
- Quick access to chat

### 5. Dua History
- View all generated duas
- Filter by helpful/not helpful
- See original context and date
- Access bilingual versions
- Review feedback notes

## API Integration

The frontend communicates with the backend API via Axios. All endpoints are defined in `src/services/api.ts`:

### Dua Endpoints
- `POST /api/v1/dua/generate` - Generate bilingual dua
- `GET /api/v1/dua/history/{email}` - Get user history
- `GET /api/v1/dua/categories` - Get problem categories
- `POST /api/v1/dua/feedback` - Submit feedback
- `GET /api/v1/dua/{id}` - Get single dua
- `GET /api/v1/dua/stats/helpful` - Get statistics

### Chat Endpoints
- `POST /api/v1/chat/conversations` - Create conversation
- `GET /api/v1/chat/conversations/user/{email}` - Get user chats
- `GET /api/v1/chat/conversations/{id}` - Get conversation
- `POST /api/v1/chat/conversations/{id}/messages` - Send message
- `GET /api/v1/chat/conversations/{id}/messages` - Get messages
- `PUT /api/v1/chat/messages/read` - Mark as read
- `PUT /api/v1/chat/imam/{id}/availability` - Set availability
- `GET /api/v1/chat/imam/{id}/availability` - Check availability

### Imam Endpoints
- `GET /api/v1/imam/list` - Get all imams
- `GET /api/v1/imam/{id}` - Get imam details
- `POST /api/v1/imam/register` - Register new imam

## Styling

The app uses **Tailwind CSS** with a custom Islamic green color scheme:

- Primary color: `#047857` (Islamic Green)
- Light variant: `#10b981` (Light Islamic Green)

Custom utility classes available:
- `.btn-primary` - Primary action button
- `.btn-secondary` - Secondary action button
- `.card` - Card container with hover effect

RTL support is built-in for Arabic language display.

## State Management

Currently using React component state with props. For larger apps, consider adding:
- Zustand (lightweight state management)
- Redux Toolkit
- Context API with useReducer

## Deployment

### Build for Production
```bash
npm run build
```

Output will be in the `dist/` directory.

### Deployment Options

1. **Vercel (Recommended for Vite)**
   - Zero-config deployment
   - Automatic previews for PR
   - Edge functions support

2. **Netlify**
   - Simple drag-and-drop
   - Continuous deployment via git

3. **Docker**
   ```dockerfile
   FROM node:18 AS build
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci
   COPY . .
   RUN npm run build

   FROM nginx:alpine
   COPY --from=build /app/dist /usr/share/nginx/html
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

4. **Traditional Server**
   - Copy `dist/` to your web server
   - Configure server to serve `index.html` for all routes (SPA)

## Development Notes

### Adding New Pages
1. Create new component in `src/pages/`
2. Add route in `src/App.tsx`
3. Update navigation in header

### Adding New API Endpoints
1. Add method in `src/services/api.ts`
2. Use in components via service import
3. Handle loading and error states

### Styling New Components
- Use Tailwind classes for styling
- Leverage custom utility classes
- Maintain RTL compatibility for Arabic

## Troubleshooting

### API Connection Issues
- Ensure backend is running on `http://127.0.0.1:8001`
- Check browser console for CORS errors
- Verify API endpoints in `src/services/api.ts`

### Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Hot Module Replacement (HMR) Issues
- HMR is configured in `vite.config.ts`
- If experiencing issues, try hard refresh (Ctrl+Shift+R)

## Contributing

1. Create a feature branch
2. Make changes following code style
3. Test in development
4. Submit pull request

## License

Islamic Educational Purpose - All Rights Reserved

## Support

For issues or feature requests, please open an issue in the project repository.

---

**Happy coding! May Allah accept our efforts. Ameen.** 🌙

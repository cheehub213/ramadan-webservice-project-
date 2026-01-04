# Frontend Development Guide

## 📖 Development Workflow

This guide helps you understand and extend the frontend application.

## Architecture Overview

```
Frontend (React + TypeScript)
    ↓
    ├── App Router (React Router 6)
    │   └── Navigation Header with Language Toggle
    │
    ├── Pages (5 main features)
    │   ├── Home - Landing page
    │   ├── DuaGenerator - Create personalized duas
    │   ├── ChatWithImams - Real-time messaging
    │   ├── SearchImams - Scholar directory
    │   └── History - Track duas
    │
    └── Services
        └── API Layer (Axios)
             ↓
    Backend API (http://127.0.0.1:8001)
```

## 🔧 Development Setup

### Prerequisites
- Node.js 18+ with npm
- VS Code (recommended)
- Backend running on http://127.0.0.1:8001

### Initial Setup
```bash
npm install
npm run dev
```

## 📱 Component Structure

### Pages

#### 1. **Home.tsx** (Landing Page)
```tsx
interface HomeProps {
  language: 'en' | 'ar'
  email: string
  setEmail: (email: string) => void
}
```
**Features:**
- Email input validation
- Feature cards with navigation
- About section
- Responsive grid layout

**Key Elements:**
- Hero section with title
- Email input with Get Started button
- 3 feature cards (clickable)
- About section with description

#### 2. **DuaGenerator.tsx** (Main Feature)
```tsx
interface DuaGeneratorProps {
  language: 'en' | 'ar'
  email: string
}
```
**Features:**
- Category selection (8 categories)
- Context input textarea
- Bilingual dua display (EN + AR)
- Usage instructions
- Feedback buttons

**State Management:**
- `selectedCategory` - Active category
- `context` - User's situation description
- `generatedDua` - API response with bilingual dua
- `loading` - API call state
- `error` - Error messages

**API Call:**
```ts
await duaService.generateDua(email, category, context)
```

#### 3. **ChatWithImams.tsx** (Messaging)
```tsx
interface ChatWithImamsProps {
  language: 'en' | 'ar'
  email: string
}
```
**Features:**
- Available imams list
- Conversation history
- Real-time messaging
- Message status tracking

**Key Components:**
- Imam selection panel (left)
- Chat display area (center)
- Message input (bottom)
- Conversation history

**API Calls:**
- `imamService.getImams()` - Load imams
- `chatService.getUserConversations(email)` - Get history
- `chatService.createConversation()` - Start chat
- `chatService.sendMessage()` - Send message

#### 4. **SearchImams.tsx** (Scholar Directory)
```tsx
interface SearchImamsProps {
  language: 'en' | 'ar'
}
```
**Features:**
- Search by name or expertise
- Filter results in real-time
- Availability status badges
- Card-based layout

**API Call:**
```ts
await imamService.getImams()
```

#### 5. **History.tsx** (Dua Tracking)
```tsx
interface HistoryProps {
  language: 'en' | 'ar'
  email: string
}
```
**Features:**
- View all generated duas
- Filter by helpful/not helpful
- Bilingual dua display
- Context and date information
- Feedback notes

**Filtering:**
- All duas
- Only helpful
- Only not helpful

**API Call:**
```ts
await duaService.getDuaHistory(email)
```

## 🌐 API Service Layer

All API calls are centralized in `src/services/api.ts`:

```ts
// Service structure
export const duaService = {
  generateDua: async (email, category, context) => {...},
  getDuaHistory: async (email) => {...},
  // ... more methods
}

export const chatService = {
  createConversation: async (email, imamId, topic) => {...},
  sendMessage: async (conversationId, message, senderType) => {...},
  // ... more methods
}

export const imamService = {
  getImams: async () => {...},
  getImamById: async (imamId) => {...},
  // ... more methods
}
```

### Adding New API Calls

1. **Define in service:**
```ts
export const duaService = {
  // ... existing methods
  newMethod: async (params) => {
    const response = await api.post('/dua/endpoint', { params })
    return response.data
  }
}
```

2. **Use in component:**
```tsx
const handleClick = async () => {
  try {
    const result = await duaService.newMethod(params)
    // Handle result
  } catch (error) {
    setError('Failed to...')
  }
}
```

## 🎨 Styling with Tailwind CSS

### Custom Utilities
```css
/* index.css */
.btn-primary {
  @apply bg-islamic hover:bg-islamic-light text-white font-semibold py-2 px-4 rounded-lg transition duration-200;
}

.card {
  @apply bg-white rounded-lg shadow p-6 hover:shadow-lg transition duration-200;
}
```

### Color Scheme
```js
// tailwind.config.js
colors: {
  islamic: '#047857',
  'islamic-light': '#10b981',
  // ... standard colors
}
```

### Responsive Design
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* 1 col on mobile, 2 on tablet, 3 on desktop */}
</div>
```

### RTL Support
```tsx
<div className={language === 'ar' ? 'rtl' : 'ltr'}>
  {/* Content */}
</div>
```

## 🌍 Internationalization (i18n)

Currently using inline ternary operators for English/Arabic:

```tsx
<h1>
  {language === 'en' ? 'English Title' : 'العنوان بالعربية'}
</h1>
```

### Better i18n (Future Enhancement)
Consider using `react-i18next`:

```bash
npm install i18next react-i18next
```

```tsx
import { useTranslation } from 'react-i18next'

function Component() {
  const { t } = useTranslation()
  return <h1>{t('title')}</h1>
}
```

## 📡 State Management

### Current Approach
- React component state with `useState`
- Props drilling for global state
- Local component state for forms

### Future Enhancement Options

**Option 1: Zustand (Recommended)**
```bash
npm install zustand
```

```ts
// src/store/useStore.ts
import create from 'zustand'

export const useStore = create((set) => ({
  email: '',
  language: 'en',
  setEmail: (email) => set({ email }),
  setLanguage: (lang) => set({ language: lang }),
}))
```

**Option 2: Context API**
```tsx
export const AppContext = createContext()

function Provider({ children }) {
  const [email, setEmail] = useState('')
  return (
    <AppContext.Provider value={{ email, setEmail }}>
      {children}
    </AppContext.Provider>
  )
}
```

## 🧪 Testing

### Setup Testing (Future)
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

### Example Test
```ts
// Home.test.tsx
import { render, screen } from '@testing-library/react'
import Home from './pages/Home'

test('renders welcome heading', () => {
  render(<Home language="en" email="" setEmail={() => {}} />)
  const heading = screen.getByText(/Welcome to Ramadan/i)
  expect(heading).toBeInTheDocument()
})
```

## 🚀 Performance Optimization

### Current Optimizations
- React.StrictMode for development warnings
- Conditional rendering to reduce DOM nodes
- CSS classes for styling (no inline styles)

### Future Optimizations

**Code Splitting**
```tsx
import { Suspense, lazy } from 'react'

const DuaGenerator = lazy(() => import('./pages/DuaGenerator'))

<Suspense fallback={<div>Loading...</div>}>
  <DuaGenerator />
</Suspense>
```

**Image Optimization**
- Use WebP format
- Lazy load images
- Optimize initial load

**Caching**
- Cache API responses
- Implement service worker

## 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit `.env` files
   - Use `.env.example` as template
   - Keep API URLs in environment

2. **API Security**
   - Validate all inputs
   - Sanitize outputs
   - Use HTTPS in production
   - Implement request/response validation

3. **Error Handling**
   - Don't expose sensitive errors to users
   - Log errors securely
   - Show user-friendly messages

## 📚 Adding New Features

### Example: Add Email Validation
```tsx
// In Home.tsx
const isValidEmail = (email: string) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

<button
  disabled={!isValidEmail(email)}
  className="btn-primary disabled:opacity-50"
>
  Get Started
</button>
```

### Example: Add Loading Skeleton
```tsx
// Reusable component
function Skeleton() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-4 bg-gray-300 rounded w-3/4"></div>
      <div className="h-4 bg-gray-300 rounded"></div>
      <div className="h-4 bg-gray-300 rounded w-5/6"></div>
    </div>
  )
}
```

## 🐛 Debugging

### Browser DevTools
- **Console**: Check for errors and logs
- **Network**: Monitor API calls
- **React DevTools**: Inspect component props/state
- **Lighthouse**: Performance audits

### Common Issues

**CORS Errors**
- Backend needs to allow frontend origin
- Vite proxy is configured in `vite.config.ts`

**State Not Updating**
- Check component re-renders
- Verify event handlers
- Use React DevTools to inspect

**Styling Issues**
- Tailwind might need rebuild
- Clear browser cache
- Check class names in DevTools

## 📝 Code Style

### Naming Conventions
- Components: PascalCase (Home.tsx)
- Functions: camelCase (handleClick)
- Constants: UPPER_SNAKE_CASE (API_URL)
- Files: kebab-case for utility files

### Best Practices
```tsx
// Good
const [isLoading, setIsLoading] = useState(false)
const handleGenerateDua = async () => { }

// Avoid
const [loading, setLoading] = useState(false)
const generateDua = () => { }
```

## 🚢 Deployment Checklist

- [ ] Remove console.logs
- [ ] Update environment variables
- [ ] Test all pages
- [ ] Check API endpoints
- [ ] Verify error handling
- [ ] Test on mobile
- [ ] Run `npm run build`
- [ ] Deploy to host

## 📞 Helpful Resources

- **React**: https://react.dev
- **TypeScript**: https://www.typescriptlang.org
- **Tailwind CSS**: https://tailwindcss.com
- **Vite**: https://vitejs.dev
- **Axios**: https://axios-http.com
- **React Router**: https://reactrouter.com

---

**Happy coding! For questions, check the code comments or README.** 🚀

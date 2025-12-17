# Enterprise RAG Platform - Frontend

A modern React TypeScript frontend application for the Enterprise RAG Platform, built with Chakra UI and React Query.

## 🚀 Features

- **Authentication**: Login and registration with JWT token management
- **Document Management**: Upload, view, and manage documents
- **AI Chat Interface**: Chat with your documents using RAG (Retrieval Augmented Generation)
- **Admin Dashboard**: Analytics and user management (admin only)
- **User Profile**: Manage your account settings
- **Real-time Updates**: React Query for efficient data fetching and caching
- **Responsive Design**: Mobile-friendly UI with Chakra UI

## 🛠️ Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **Chakra UI** - Component library
- **React Query (TanStack Query)** - Data fetching and state management
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Zustand** - Lightweight state management (if needed)

## 📦 Installation

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Setup

1. **Install dependencies**:

```bash
npm install
```

2. **Configure environment variables**:

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

3. **Start the development server**:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Layout.tsx       # Main layout wrapper
│   │   └── ProtectedRoute.tsx  # Route guard component
│   ├── contexts/            # React contexts
│   │   └── AuthContext.tsx  # Authentication context
│   ├── hooks/               # Custom React hooks
│   │   ├── useChat.ts       # Chat-related hooks
│   │   └── useDocuments.ts  # Document-related hooks
│   ├── pages/               # Page components
│   │   ├── Admin.tsx        # Admin dashboard
│   │   ├── Chat.tsx         # Chat interface
│   │   ├── Dashboard.tsx    # Main dashboard
│   │   ├── Documents.tsx    # Document management
│   │   ├── Login.tsx        # Login page
│   │   ├── Profile.tsx      # User profile
│   │   └── Register.tsx     # Registration page
│   ├── services/            # API service layer
│   │   ├── admin.service.ts
│   │   ├── api.ts           # Axios instance
│   │   ├── auth.service.ts
│   │   ├── chat.service.ts
│   │   ├── documents.service.ts
│   │   └── organizations.service.ts
│   ├── types/               # TypeScript type definitions
│   │   └── index.ts
│   ├── App.tsx              # Main app component
│   └── main.tsx             # Entry point
├── index.html               # HTML template
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 🔧 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🎯 Key Features Explained

### Authentication Flow

The app uses JWT-based authentication with automatic token refresh:

1. User logs in via `/login`
2. Access and refresh tokens are stored in localStorage
3. Axios interceptor automatically adds the token to requests
4. Token is refreshed automatically when expired
5. User is redirected to login if refresh fails

### API Integration

All API calls go through the centralized API client (`src/services/api.ts`), which:

- Adds authentication headers
- Handles token refresh
- Provides error handling
- Supports request/response interceptors

### State Management

- **React Query**: Server state management (API data)
- **React Context**: Global client state (auth, user)
- **Component State**: Local UI state

### Protected Routes

Routes are protected using the `ProtectedRoute` component:

```tsx
<ProtectedRoute requireAdmin>
  <AdminPage />
</ProtectedRoute>
```

## 🎨 UI Components

The app uses Chakra UI components with:

- Responsive design
- Dark mode support (built-in)
- Accessible components
- Consistent theming

## 📡 API Endpoints Used

- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/refresh` - Token refresh
- `GET /users/me` - Get current user
- `GET /documents/` - List documents
- `POST /documents/upload` - Upload document
- `DELETE /documents/{id}` - Delete document
- `GET /chat/conversations` - List conversations
- `POST /chat/chat` - Send chat message
- `GET /admin/*` - Admin endpoints

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000/api/v1` |

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.

### Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Deploy to Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod
```

## 🧪 Testing

```bash
# Run tests (to be implemented)
npm test
```

## 📝 Code Style

The project uses:

- ESLint for code linting
- TypeScript for type checking
- Prettier for code formatting (recommended)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Ensure TypeScript compiles without errors
4. Test your changes
5. Submit a pull request

## 📄 License

This project is part of the Enterprise RAG Platform.

## 🐛 Known Issues

- Streaming chat responses not yet implemented (uses regular POST)
- Profile update functionality placeholder
- Mobile sidebar needs improvement

## 🔮 Future Enhancements

- [ ] Real-time streaming for chat responses
- [ ] File preview before upload
- [ ] Advanced document search
- [ ] User settings page
- [ ] Organization management UI
- [ ] Dark mode toggle
- [ ] Internationalization (i18n)
- [ ] Progressive Web App (PWA) support

## 📞 Support

For issues and questions, please contact the development team or create an issue in the repository.


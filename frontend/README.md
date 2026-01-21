# Miscrits Nexus Frontend

A modern React frontend for the Miscrits Nexus project, built with Vite and featuring a clean, responsive interface for browsing Miscrits data, moves database, and relics calculator.

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation & Running
1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:5173](http://localhost:5173) in your browser

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
├── src/                   # Source code
│   ├── assets/           # Images, icons, etc.
│   ├── App.jsx           # Main application component
│   ├── App.css           # Main application styles
│   ├── index.css         # Global styles
│   └── main.jsx          # Application entry point
├── .gitignore            # Git ignore rules
├── eslint.config.js      # ESLint configuration
├── index.html            # HTML template
├── package.json          # Dependencies and scripts
├── README.md             # This file
└── vite.config.js        # Vite configuration
```

## 🎨 Features & Components

### Current Features
- **Tab-based Navigation**: Switch between Miscrits Database, Moves Database, and Relics Calculator
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI**: Clean interface with gradient backgrounds and smooth animations
- **Placeholder Sections**: Ready-to-implement areas for each major feature

### Main Components

#### App.jsx
The main application component featuring:
- State management for active tab navigation
- Three main sections: Miscrits, Moves, and Relics
- Responsive tab interface
- Clean component structure ready for expansion

#### App.css
Custom styling includes:
- Modern gradient header design
- Responsive tab navigation
- Smooth animations and transitions
- Mobile-first responsive breakpoints
- Professional color scheme (#667eea theme)

## 🛠 Technology Stack

- **React 19.2.0** - Latest React with modern features
- **Vite 7.2.4** - Fast build tool and dev server
- **Axios** - HTTP client for API calls (ready for backend integration)
- **React Router DOM** - Routing capabilities (installed for future use)
- **ESLint** - Code linting and quality assurance

## 📦 Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server at http://localhost:5173 |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint to check code quality |

## 🔧 VS Code Integration

### Installed Extensions
- **ESLint** - JavaScript/React code linting
- **HTML CSS Support** - Enhanced HTML/CSS IntelliSense

### VS Code Tasks
The project includes predefined VS Code tasks (`.vscode/tasks.json` in root):
- **Start React Dev Server** - Launch development server
- **Build React App** - Create production build

Access via: `Ctrl+Shift+P` → "Tasks: Run Task"

## 🎯 Ready for Development

The frontend is structured to connect with your existing backend:

### Backend Integration Points
- **Miscrits Database**: Ready to fetch from `/api/miscrits` endpoint
- **Moves Database**: Prepared for `/api/moves` data integration  
- **Relics Calculator**: Set up for `/api/relics` API calls

### File Structure for Expansion
```
src/
├── components/           # Reusable UI components (to be created)
├── pages/               # Page-level components (to be created)
├── services/            # API service functions (to be created)
├── hooks/               # Custom React hooks (to be created)
└── utils/               # Utility functions (to be created)
```

## 🔗 Backend Connection

The frontend is designed to work with your Python backend located in `../backend/`. Key integration points:

1. **Database Files**: Ready to display data from:
   - `../data/miscrit_database.csv`
   - `../data/moves_database.csv`
   - `../data/miscrit_relics.csv`

2. **Scraper Integration**: Can trigger and display results from:
   - `../backend/scraper/miscrit_scraper.py`
   - `../backend/scraper/miscrit_updater.py`

## 🎨 Design System

### Colors
- Primary: `#667eea` (Purple-blue gradient start)
- Secondary: `#764ba2` (Purple gradient end)
- Background: Dynamic with backdrop blur effects
- Text: Responsive dark/light theme ready

### Layout
- **Mobile-first** responsive design
- **Tab-based** navigation for easy content switching
- **Card-based** content layout for data display
- **Gradient backgrounds** for modern aesthetic

## 🚀 Next Steps

1. **Create API Services**: Set up axios services to connect with backend
2. **Build Components**: Create reusable components for data display
3. **Add Routing**: Implement React Router for multi-page navigation
4. **Data Integration**: Connect with CSV data and database endpoints
5. **State Management**: Add Redux or Context API for complex state
6. **Testing**: Add Jest and React Testing Library

## 📋 Development Workflow

1. **Start Development**: `npm run dev`
2. **Make Changes**: Edit files in `src/`
3. **Hot Reload**: Changes appear instantly in browser
4. **Build Production**: `npm run build` when ready to deploy
5. **Preview**: `npm run preview` to test production build

## 🐛 Troubleshooting

### Common Issues
- **Port 5173 in use**: Vite will automatically try the next available port
- **Module not found**: Run `npm install` to ensure all dependencies are installed
- **ESLint errors**: Check `eslint.config.js` for configuration issues

### VS Code Issues
- **Extensions not working**: Reload VS Code window
- **Tasks not appearing**: Check `.vscode/tasks.json` exists in project root

---

**Created**: January 2, 2026  
**Framework**: React + Vite  
**Ready for**: Backend integration and feature development

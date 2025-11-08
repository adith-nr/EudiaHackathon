# EudiaHackathon - Shopify Analytics & Pricing Intelligence Platform

A full-stack application combining React frontend, Express.js backend, and FastAPI AI agents for intelligent Shopify store analytics and competitive pricing recommendations.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Frontend      │    │   Backend        │    │   FastAPI           │
│   (React/Vite)  │◄──►│   (Express.js)   │◄──►│   (AI Agents)       │
│   Port: 5173    │    │   Port: 4000     │    │   Port: 8000        │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
```

### 🎯 Core Features

- **📊 Analytics Dashboard**: Real-time Shopify store performance metrics
- **🤖 AI-Powered Pricing**: Competitive pricing recommendations using market analysis  
- **🔐 Authentication**: Secure user management with Clerk
- **📈 Product Analytics**: Detailed product performance insights
- **🛒 Shopify Integration**: Direct integration with Shopify Admin API
- **⚡ Real-time Data**: Live order and inventory tracking

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v16+) and **npm/pnpm**
- **Python** (3.8+) with **pip**
- **Shopify Store** with Admin API access
- **API Keys**: Shopify Access Token, Gemini API key

### 1. Clone & Install

```bash
git clone https://github.com/adith-nr/EudiaHackathon.git
cd EudiaHackathon

# Install all dependencies
npm install --prefix backend
npm install --prefix frontend
pip install -r fastapi/requirements.txt  # Create if needed
```

### 2. Environment Configuration

Create `.env` files in each service:

**Backend (.env)**:
```env
PORT=4000
SHOPIFY_STORE=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_access_token
NODE_ENV=development
```

**FastAPI (.env)**:
```env
SHOPIFY_STORE=your-store.myshopify.com
ACCESS_TOKEN=your_access_token
GEMINI_API_KEY=your_gemini_api_key
SERPAPI_KEY=your_serpapi_key
HOST=127.0.0.1
PORT=8000
```

**Frontend (.env)**:
```env
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_key
VITE_API_BASE_URL=http://localhost:4000
VITE_FASTAPI_URL=http://localhost:8000
```

### 3. Launch All Services

**🎯 One-Click Launch:**
```bash
# Windows
start-all-services.bat

# Or individually:
start-frontend.bat    # React dev server
start-backend.bat     # Express API
start-fastapi.bat     # Python AI agents
```

**🔧 Manual Launch:**
```bash
# Terminal 1 - Frontend
cd frontend && npm run dev

# Terminal 2 - Backend  
cd backend && npm run dev

# Terminal 3 - FastAPI
cd fastapi && python -m uvicorn server:app --reload
```

### 4. Access Applications

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:4000
- **FastAPI Docs**: http://localhost:8000/docs
- **Analytics API**: http://localhost:8000/analytics

## 📁 Project Structure

```
EudiaHackathon/
├── 📱 frontend/                 # React + Vite application
│   ├── src/
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   ├── ProductDetailsPage.jsx
│   │   │   └── ProductAnalytics.jsx
│   │   ├── lib/api.js          # API client
│   │   └── App.jsx             # Main app + routing
│   └── package.json
├── 🔧 backend/                  # Express.js API server
│   ├── controllers/
│   │   ├── shopify.controller.js
│   │   └── webhook.controller.js
│   ├── routes/
│   │   ├── shopify.routes.js
│   │   └── webhook.routes.js
│   ├── middlewares/
│   ├── services/
│   └── index.js
├── 🤖 fastapi/                  # AI agents & analytics
│   ├── agents/
│   │   ├── AgentClasses.py     # PricingAgent, Analytics
│   │   ├── analytics.py        # Shopify data analytics
│   │   ├── pricing_agent.py    # Market analysis
│   │   ├── utils.py            # Data processing
│   │   └── test_pricing_data.json
│   └── server.py              # FastAPI main server
└── 📜 Batch Scripts/           # Windows automation
    ├── start-all-services.bat
    ├── start-frontend.bat
    ├── start-backend.bat
    └── start-fastapi.bat
```

## 🔗 API Endpoints

### Backend (Express.js) - Port 4000

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health check |
| POST | `/shopify/create` | Create Shopify product |
| POST | `/shopify/updateInventory` | Update product inventory |
| GET | `/shopify/order` | Fetch order data |
| POST | `/shopify/pord` | Get orders by product |
| GET | `/shopify/products` | List all products |

### FastAPI (AI Agents) - Port 8000

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | FastAPI health check |
| GET | `/analytics` | Shopify analytics data |
| POST | `/products_analyze` | AI pricing analysis |

**Product Analysis Request:**
```json
{
  "name": "LED String Lights",
  "description": "Waterproof LED lights for decoration",
  "minPrice": 50.0,
  "maxPrice": 200.0
}
```

## 🤖 AI Features

### Pricing Agent
- **Market Analysis**: Scrapes competitor data from Amazon
- **AI Recommendations**: Uses Google Gemini for intelligent pricing
- **Price Optimization**: Considers ratings, reviews, and market trends
- **Data Sources**: Amazon product data, competitor analysis

### Analytics Engine
- **Order Analytics**: Revenue, AOV, orders per day
- **Product Performance**: Top products by revenue
- **Data Processing**: Robust pandas-based data cleaning
- **Shopify Integration**: Real-time store data sync

## 🛠️ Technology Stack

### Frontend
- **React 19** + **Vite** - Modern UI framework
- **Clerk** - Authentication & user management  
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls

### Backend  
- **Express.js** - RESTful API server
- **Cors** - Cross-origin resource sharing
- **Dotenv** - Environment configuration
- **Zod** - Schema validation

### AI/Analytics
- **FastAPI** - High-performance Python API
- **Pandas** - Data analysis and processing
- **Google Gemini** - AI-powered insights
- **SerpAPI** - Web scraping for market data
- **Pydantic** - Data validation and serialization

## 🔧 Development

### Adding New Features

**Frontend Components:**
```bash
# Add new page
touch frontend/src/pages/NewPage.jsx

# Update routing in App.jsx
```

**Backend Endpoints:**
```bash
# Add controller
touch backend/controllers/new.controller.js

# Add route
touch backend/routes/new.routes.js

# Register in app.js
```

**AI Agents:**
```bash
# Add new agent class
touch fastapi/agents/NewAgent.py

# Register in server.py
```

### Database Integration
Currently using direct Shopify API calls. To add database persistence:

1. Choose database (PostgreSQL, MongoDB)
2. Add ORM (Prisma, SQLAlchemy)  
3. Create migration scripts
4. Update API endpoints

### Testing

```bash
# Backend tests
cd backend && npm test

# Frontend tests  
cd frontend && npm run test

# FastAPI tests
cd fastapi && python -m pytest
```

## 🚀 Deployment

### Production Environment

**Frontend (Vercel/Netlify):**
```bash
cd frontend
npm run build
# Deploy dist/ folder
```

**Backend (Railway/Heroku):**
```bash
cd backend  
npm run start
```

**FastAPI (Railway/AWS Lambda):**
```bash
cd fastapi
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port $PORT
```

### Docker Deployment

```dockerfile
# Create docker-compose.yml for multi-service deployment
services:
  frontend:
    build: ./frontend
    ports: [5173:5173]
  
  backend:  
    build: ./backend
    ports: [4000:4000]
    
  fastapi:
    build: ./fastapi  
    ports: [8000:8000]
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/adith-nr/EudiaHackathon/issues)
- **Feature Requests**: Use GitHub Issues with `enhancement` label
- **Questions**: Check existing issues or create new one

## 📊 Project Status

- ✅ **Frontend**: React app with authentication
- ✅ **Backend**: Express API with Shopify integration  
- ✅ **FastAPI**: AI agents and analytics
- ✅ **Automation**: Windows batch scripts
- 🔄 **In Progress**: Advanced analytics features
- 📋 **Planned**: Database integration, advanced AI features

---

**Built for EudiaHackathon** - Intelligent Shopify analytics and pricing automation platform.

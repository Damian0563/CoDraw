# Production Deployment Configuration

## Architecture Overview

```
┌─────────────┐
│    Nginx    │ (Reverse Proxy, SSL termination)
│   (Port 80  │
│    & 443)   │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌──────┐ ┌──────┐
│Frontend│ │ Backend │
│(Nginx) │ │(Daphne) │
│Port 80 │ │Port 8080│
└──────┘ └──────┘
   │       │
   └───────┘
       │
┌──────┴──────┐
│  Services   │
│ - MongoDB   │
│ - Redis     │
│ - Prometheus│
└─────────────┘
```

## Services

### Frontend (Vue.js)
- **Build Process**: Multi-stage Docker build
  - Stage 1: Node.js builds the production bundle (`npm run build`)
  - Stage 2: Nginx Alpine serves static files
- **Port**: 80 (internal)
- **Features**:
  - Gzip compression enabled
  - Static asset caching (1 year)
  - Client-side routing support (SPA)
  - Optimized for production

### Backend (Django/Daphne)
- **Server**: Daphne ASGI server
- **Port**: 8080 (internal)
- **Features**:
  - WebSocket support
  - ASGI application
  - Connected to MongoDB and Redis

### Nginx (Reverse Proxy)
- **Ports**: 80, 443 (external)
- **Responsibilities**:
  - SSL/TLS termination
  - Static file serving (via frontend container)
  - API request proxying to backend
  - WebSocket proxying to backend
  - Client max body size: 20MB

### Database & Cache
- **MongoDB**: Port 27017, persistent volume
- **Redis**: Port 6379, in-memory cache

### Monitoring
- **Prometheus**: Port 9090, metrics collection

## Environment Variables

### Frontend Build Args
- `VUE_APP_BASE_URL`: Backend API URL
- `VUE_APP_WS_URL`: WebSocket URL
- `VUE_APP_GTAG`: Google Analytics tag
- `VUE_APP_GOOGLE_ID`: Google OAuth client ID

### Backend Environment
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account JSON
- `GOOGLE_BUCKET`: GCS bucket name
- `MODE`: PROD
- MongoDB credentials

## Deployment Commands

### Build and Start
```bash
# Build all services
docker-compose build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Production Deployment
```bash
# Ensure .env.prod is configured
docker-compose -f docker-compose.yml up -d
```

## Key Changes from Development

1. **Frontend Build**: Uses `npm run build` instead of `npm run serve`
   - Creates optimized production bundle
   - No development server running
   - Static files served by nginx

2. **Multi-stage Build**: Reduces final image size
   - Build dependencies not included in final image
   - Only production artifacts and nginx

3. **Nginx Configuration**:
   - Added gzip compression
   - Static asset caching headers
   - SPA routing support (try_files)

4. **Port Changes**:
   - Frontend: 8000 (dev) → 80 (production nginx)

## SSL Configuration

SSL certificates are mounted from host:
- `/etc/letsencrypt/live/codrawapp.com/fullchain.pem`
- `/etc/letsencrypt/live/codrawapp.com/privkey.pem`

HTTP requests are automatically redirected to HTTPS.

## Security Considerations

1. All services run on internal Docker network
2. Only nginx exposes ports to the outside
3. SSL/TLS encryption for all traffic
4. MongoDB authentication enabled
5. No sensitive data in Docker images (use .env files)

## Troubleshooting

### Check Service Status
```bash
docker-compose ps
docker-compose logs <service-name>
```

### Rebuild Frontend
```bash
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### View Nginx Configuration
```bash
docker exec <nginx-container> nginx -T
```

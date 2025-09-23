# GRNLITE Keep-Alive Service

This document explains the keep-alive service implemented to prevent the Render free tier from sleeping.

## Overview

The keep-alive service consists of two components:
1. **Integrated Keep-Alive (`keepAlive.js`)** - Runs within your main Node.js server
2. **Standalone Keep-Alive (`standalone-keepalive.js`)** - Runs as a separate service

## How It Works

### The Problem
Render's free tier puts applications to sleep after 15 minutes of inactivity. This means:
- Your app becomes unavailable until the next request
- Users experience slow load times (cold starts)
- Background processes may not run consistently

### The Solution
The keep-alive service makes HTTP requests to your app every 14 minutes, ensuring it never goes to sleep.

## Deployment Options

### Option 1: Separate Keep-Alive Service (Recommended)

This option deploys two services on Render:
1. Your main Django/Python app
2. A separate Node.js service that pings your main app

**Advantages:**
- Independent scaling and monitoring
- Cleaner separation of concerns  
- If one service fails, the other continues running

**Configuration:**
The `render.yaml` file is already configured for this approach with two services:
- `GRNLITE`: Your main Python/Django application
- `GRNLITE-KeepAlive`: The Node.js keep-alive service

### Option 2: Integrated Keep-Alive

The keep-alive service runs within your main application server.

**To use this option:**
1. Update your Django application to also run the Node.js server
2. Modify the `render.yaml` to use a different start command
3. Ensure both Python and Node.js dependencies are installed

## Environment Variables

The keep-alive service uses these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `RENDER_EXTERNAL_URL` | Your app's Render URL | `https://grnlite.onrender.com` |
| `APP_URL` | Alternative app URL | Uses RENDER_EXTERNAL_URL |
| `HEALTH_ENDPOINT` | Endpoint to ping | `/` |
| `PING_INTERVAL` | Cron schedule | `*/14 * * * *` (every 14 minutes) |
| `REQUEST_TIMEOUT` | HTTP timeout in ms | `10000` (10 seconds) |
| `NODE_ENV` | Environment mode | `production` |

## Files Added/Modified

### New Files
- `keepAlive.js` - Integrated keep-alive service module
- `standalone-keepalive.js` - Standalone keep-alive service
- `KEEP_ALIVE_README.md` - This documentation

### Modified Files
- `package.json` - Added dependencies (`node-cron`, `axios`) and scripts
- `server.js` - Added health check endpoint and keep-alive integration
- `render.yaml` - Updated deployment configuration

## Dependencies Added

```json
{
  "axios": "^1.6.0",
  "node-cron": "^3.0.3"
}
```

## API Endpoints Added

### GET /api/health-check
Returns server health status and keep-alive statistics.

**Response:**
```json
{
  "status": "OK",
  "timestamp": "2025-09-23T...",
  "uptime": 1234.567,
  "keepAlive": {
    "isActive": true,
    "lastPing": "2025-09-23T...",
    "successCount": 42,
    "errorCount": 1,
    "successRate": "97.67%"
  },
  "message": "Server is running and healthy"
}
```

### GET /api/keep-alive-status
Returns only the keep-alive service statistics.

## Deployment Steps

1. **Push your code** to your GitHub repository
2. **Deploy to Render** using the updated `render.yaml`
3. **Verify deployment** by checking both services are running:
   - Main app: `https://your-app.onrender.com`
   - Keep-alive logs: Check the GRNLITE-KeepAlive service logs
4. **Monitor performance** through the `/api/health-check` endpoint

## Monitoring

### Check Keep-Alive Status
Visit: `https://your-app.onrender.com/api/health-check`

### Check Logs
1. Go to your Render dashboard
2. Select the "GRNLITE-KeepAlive" service
3. View the logs to see ping attempts and success/failure rates

### Expected Log Output
```
🚀 GRNLITE Keep-Alive Service Starting...
📍 Target URL: https://grnlite.onrender.com/
⏰ Ping Interval: Every 14 minutes
⏱️  Request Timeout: 10000ms

🔄 Ping #1 - Mon Sep 23 2025 14:30:00 GMT+0000 (UTC)
✅ SUCCESS - Status: 200, Time: 234ms
📊 Server Response: {"status": "OK", ...}
📈 Stats: 1/1 successful (100.0%)
```

## Troubleshooting

### Keep-Alive Service Not Starting
1. Check the service logs in Render dashboard
2. Verify environment variables are set correctly
3. Ensure `RENDER_EXTERNAL_URL` matches your actual app URL

### High Failure Rate
1. Check your main app's health and responsiveness
2. Verify the health endpoint is accessible
3. Check for network issues or timeouts

### App Still Going to Sleep
1. Verify the keep-alive service is making requests every 14 minutes
2. Check that requests are reaching your main application
3. Ensure the ping interval is less than 15 minutes

## Cost Considerations

- **Render Free Tier**: Both services use free tier resources
- **Request Limits**: Keep-alive makes ~100 requests per day
- **Bandwidth**: Minimal impact (small JSON responses)

## Security Notes

- Keep-alive requests include a unique User-Agent for identification
- Health check endpoints expose minimal system information
- No authentication required for health checks (by design)

## Alternative Solutions

If you prefer not to use a separate keep-alive service:

1. **External Monitoring Services**:
   - UptimeRobot (free tier available)
   - Pingdom
   - StatusCake

2. **Scheduled Services**:
   - GitHub Actions with cron
   - External VPS with cron job
   - AWS Lambda with CloudWatch Events

3. **Upgrade to Paid Tier**:
   - Render paid tiers don't sleep
   - More reliable for production applications

## Contributing

To improve the keep-alive service:
1. Modify the ping interval in `standalone-keepalive.js`
2. Add additional health checks
3. Implement retry logic for failed pings
4. Add email notifications for extended downtime

---

For questions or issues, check the service logs first, then review this documentation.
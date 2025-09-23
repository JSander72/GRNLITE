const cron = require('node-cron');
const axios = require('axios');

// Configuration
const APP_URL = process.env.RENDER_EXTERNAL_URL || 'https://your-app-name.onrender.com';
const KEEP_ALIVE_ENDPOINT = '/api/health-check'; // We'll create this endpoint
const INTERVAL = '*/14 * * * *'; // Every 14 minutes

/**
 * Keep alive service to prevent Render free tier from going to sleep
 * Makes a request every 14 minutes to keep the service active
 */
class KeepAliveService {
    constructor() {
        this.isActive = false;
        this.lastPing = null;
        this.successCount = 0;
        this.errorCount = 0;
    }

    /**
     * Start the keep-alive cron job
     */
    start() {
        if (this.isActive) {
            console.log('Keep-alive service is already running');
            return;
        }

        console.log('🚀 Starting keep-alive service...');
        console.log(`📍 Target URL: ${APP_URL}${KEEP_ALIVE_ENDPOINT}`);
        console.log(`⏰ Schedule: Every 14 minutes`);
        
        // Schedule the cron job
        this.cronJob = cron.schedule(INTERVAL, async () => {
            await this.ping();
        }, {
            scheduled: false,
            timezone: "America/New_York"
        });

        this.cronJob.start();
        this.isActive = true;
        
        console.log('✅ Keep-alive service started successfully');
        
        // Make an initial ping after 1 minute to test the setup
        setTimeout(() => {
            this.ping();
        }, 60000);
    }

    /**
     * Stop the keep-alive service
     */
    stop() {
        if (this.cronJob) {
            this.cronJob.stop();
            this.isActive = false;
            console.log('🛑 Keep-alive service stopped');
        }
    }

    /**
     * Make a ping request to keep the service alive
     */
    async ping() {
        try {
            const startTime = Date.now();
            const response = await axios.get(`${APP_URL}${KEEP_ALIVE_ENDPOINT}`, {
                timeout: 10000, // 10 second timeout
                headers: {
                    'User-Agent': 'KeepAlive-Service/1.0'
                }
            });
            
            const responseTime = Date.now() - startTime;
            this.lastPing = new Date();
            this.successCount++;
            
            console.log(`✅ Keep-alive ping successful [${this.successCount}/${this.successCount + this.errorCount}]`);
            console.log(`   Status: ${response.status}, Response time: ${responseTime}ms`);
            console.log(`   Last ping: ${this.lastPing.toLocaleString()}`);
            
        } catch (error) {
            this.errorCount++;
            console.error(`❌ Keep-alive ping failed [${this.successCount}/${this.successCount + this.errorCount}]:`);
            
            if (error.response) {
                console.error(`   Status: ${error.response.status} ${error.response.statusText}`);
            } else if (error.request) {
                console.error(`   Network error: ${error.code || error.message}`);
            } else {
                console.error(`   Error: ${error.message}`);
            }
            
            console.error(`   Target: ${APP_URL}${KEEP_ALIVE_ENDPOINT}`);
        }
    }

    /**
     * Get service statistics
     */
    getStats() {
        return {
            isActive: this.isActive,
            lastPing: this.lastPing,
            successCount: this.successCount,
            errorCount: this.errorCount,
            successRate: this.successCount + this.errorCount > 0 
                ? ((this.successCount / (this.successCount + this.errorCount)) * 100).toFixed(2) + '%'
                : '0%'
        };
    }
}

// Create and export the service instance
const keepAliveService = new KeepAliveService();

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🔄 Received SIGINT, stopping keep-alive service...');
    keepAliveService.stop();
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n🔄 Received SIGTERM, stopping keep-alive service...');
    keepAliveService.stop();
    process.exit(0);
});

module.exports = keepAliveService;
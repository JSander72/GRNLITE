#!/usr/bin/env node

/**
 * Standalone Keep-Alive Service
 * This script runs independently to keep your Render app alive
 * by making HTTP requests every 14 minutes
 */

const cron = require('node-cron');
const axios = require('axios');

// Configuration from environment variables
const APP_URL = process.env.RENDER_EXTERNAL_URL || process.env.APP_URL || 'https://grnlite.onrender.com';
const HEALTH_ENDPOINT = process.env.HEALTH_ENDPOINT || '/api/health-check';
const PING_INTERVAL = process.env.PING_INTERVAL || '*/14 * * * *'; // Every 14 minutes
const TIMEOUT = parseInt(process.env.REQUEST_TIMEOUT) || 10000; // 10 seconds

console.log('🚀 GRNLITE Keep-Alive Service Starting...');
console.log(`📍 Target URL: ${APP_URL}${HEALTH_ENDPOINT}`);
console.log(`⏰ Ping Interval: Every 14 minutes`);
console.log(`⏱️  Request Timeout: ${TIMEOUT}ms`);
console.log('=' * 50);

let pingCount = 0;
let successCount = 0;
let errorCount = 0;
let lastPingTime = null;

/**
 * Perform a keep-alive ping
 */
async function performPing() {
    pingCount++;
    const startTime = Date.now();
    
    try {
        console.log(`\n🔄 Ping #${pingCount} - ${new Date().toLocaleString()}`);
        
        const response = await axios.get(`${APP_URL}${HEALTH_ENDPOINT}`, {
            timeout: TIMEOUT,
            headers: {
                'User-Agent': 'GRNLITE-KeepAlive/1.0',
                'Accept': 'application/json'
            },
            validateStatus: function (status) {
                return status < 500; // Accept any status code less than 500
            }
        });
        
        const responseTime = Date.now() - startTime;
        successCount++;
        lastPingTime = new Date();
        
        console.log(`✅ SUCCESS - Status: ${response.status}, Time: ${responseTime}ms`);
        
        if (response.data) {
            console.log(`📊 Server Response:`, JSON.stringify(response.data, null, 2));
        }
        
        // Calculate success rate
        const successRate = ((successCount / pingCount) * 100).toFixed(1);
        console.log(`📈 Stats: ${successCount}/${pingCount} successful (${successRate}%)`);
        
    } catch (error) {
        errorCount++;
        const responseTime = Date.now() - startTime;
        
        console.log(`❌ FAILED - Time: ${responseTime}ms`);
        
        if (error.response) {
            console.log(`   Server responded with ${error.response.status}: ${error.response.statusText}`);
        } else if (error.request) {
            console.log(`   Network error: ${error.code || error.message}`);
        } else {
            console.log(`   Request setup error: ${error.message}`);
        }
        
        const failureRate = ((errorCount / pingCount) * 100).toFixed(1);
        console.log(`📉 Stats: ${errorCount}/${pingCount} failed (${failureRate}%)`);
    }
}

/**
 * Start the keep-alive service
 */
function startKeepAliveService() {
    console.log('⏰ Scheduling keep-alive pings...');
    
    // Schedule the cron job
    const job = cron.schedule(PING_INTERVAL, performPing, {
        scheduled: true,
        timezone: "UTC"
    });
    
    console.log('✅ Keep-alive service started successfully!');
    console.log('🔄 Making initial ping in 30 seconds...');
    
    // Perform initial ping after 30 seconds
    setTimeout(performPing, 30000);
    
    // Handle graceful shutdown
    process.on('SIGINT', () => {
        console.log('\n\n🛑 Received SIGINT - Shutting down gracefully...');
        job.stop();
        console.log('📊 Final Stats:');
        console.log(`   Total Pings: ${pingCount}`);
        console.log(`   Successful: ${successCount}`);
        console.log(`   Failed: ${errorCount}`);
        console.log(`   Success Rate: ${pingCount > 0 ? ((successCount / pingCount) * 100).toFixed(1) : 0}%`);
        console.log('👋 Keep-alive service stopped. Goodbye!');
        process.exit(0);
    });
    
    process.on('SIGTERM', () => {
        console.log('\n\n🛑 Received SIGTERM - Shutting down gracefully...');
        job.stop();
        process.exit(0);
    });
    
    // Keep the process alive
    process.on('uncaughtException', (error) => {
        console.error('❌ Uncaught Exception:', error);
        process.exit(1);
    });
    
    process.on('unhandledRejection', (reason, promise) => {
        console.error('❌ Unhandled Rejection at:', promise, 'reason:', reason);
        process.exit(1);
    });
}

// Validate configuration
if (!APP_URL) {
    console.error('❌ ERROR: APP_URL or RENDER_EXTERNAL_URL environment variable is required');
    process.exit(1);
}

// Start the service
startKeepAliveService();
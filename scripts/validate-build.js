#!/usr/bin/env node

// Build validation script
console.log('🔍 Validating build environment...')

// Check Node.js version
const nodeVersion = process.version
console.log(`📦 Node.js version: ${nodeVersion}`)

// Load environment variables from .env file
require('dotenv').config()

// Check required environment variables
const requiredVars = [
  'NEXT_PUBLIC_PRIVY_APP_ID'
]

const missingVars = requiredVars.filter(varName => !process.env[varName])

if (missingVars.length > 0) {
  console.warn('⚠️ Missing environment variables:', missingVars)
  console.log('💡 This is okay for local development, but ensure these are set in production')
}

// Check memory availability
const memUsage = process.memoryUsage()
console.log('💾 Memory usage:', {
  rss: Math.round(memUsage.rss / 1024 / 1024) + 'MB',
  heapUsed: Math.round(memUsage.heapUsed / 1024 / 1024) + 'MB',
  heapTotal: Math.round(memUsage.heapTotal / 1024 / 1024) + 'MB'
})

console.log('✅ Build environment validation completed!')
#!/usr/bin/env node

// Build validation script
console.log('🔍 Validating build environment...')

// Check Node.js version
const nodeVersion = process.version
console.log(`📦 Node.js version: ${nodeVersion}`)

// Check required environment variables
const requiredVars = [
  'NODE_ENV',
  'NEXT_PUBLIC_PRIVY_APP_ID'
]

const missingVars = requiredVars.filter(varName => !process.env[varName])

if (missingVars.length > 0) {
  console.error('❌ Missing required environment variables:', missingVars)
  process.exit(1)
}

// Check memory availability
const memUsage = process.memoryUsage()
console.log('💾 Memory usage:', {
  rss: Math.round(memUsage.rss / 1024 / 1024) + 'MB',
  heapUsed: Math.round(memUsage.heapUsed / 1024 / 1024) + 'MB',
  heapTotal: Math.round(memUsage.heapTotal / 1024 / 1024) + 'MB'
})

console.log('✅ Build environment validation passed!')
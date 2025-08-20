/**
 * Secure Configuration Template for EXDEX Platform
 * 
 * SECURITY NOTICE: This file contains template configurations for secure deployment.
 * All sensitive values must be provided via environment variables or secure configuration
 * management systems. NEVER commit real credentials to version control.
 */

// Environment-based configuration loading
class SecureConfig {
    constructor() {
        this.config = {};
        this.loaded = false;
    }

    /**
     * Load configuration from secure sources
     * Priority: Environment Variables > Secure Config API > Defaults
     */
    async loadConfig() {
        try {
            // Load from environment variables (highest priority)
            this.config = {
                // API Endpoints - Use environment variables in production
                API_URL: process.env.EXDEX_API_URL || this.getSecureDefault('API_URL'),
                WS_URL: process.env.EXDEX_WS_URL || this.getSecureDefault('WS_URL'),
                
                // Security Configuration
                ENCRYPTION_ENABLED: process.env.ENCRYPTION_ENABLED === 'true' || true,
                AUDIT_LOGGING: process.env.AUDIT_LOGGING === 'true' || true,
                
                // Network Configuration
                SUPPORTED_NETWORKS: this.getSupportedNetworks(),
                
                // UI Configuration
                THEME: process.env.UI_THEME || 'dark',
                DEBUG_MODE: process.env.DEBUG_MODE === 'true' || false,
            };

            // Load additional config from secure API if available
            if (this.config.API_URL) {
                await this.loadRemoteConfig();
            }

            this.loaded = true;
            return this.config;
        } catch (error) {
            console.error('Failed to load secure configuration:', error);
            this.loadFallbackConfig();
        }
    }

    /**
     * Get secure default values - these should be safe for public repositories
     */
    getSecureDefault(key) {
        const defaults = {
            'API_URL': 'https://api.example.com', // Replace with your API
            'WS_URL': 'wss://ws.example.com',     // Replace with your WebSocket
        };
        return defaults[key] || null;
    }

    /**
     * Get supported blockchain networks (public information)
     */
    getSupportedNetworks() {
        return {
            ethereum: {
                name: 'Ethereum Mainnet',
                chainId: 1,
                rpcUrl: process.env.ETH_RPC_URL || 'https://mainnet.infura.io/v3/YOUR_PROJECT_ID',
                explorer: 'https://etherscan.io'
            },
            bsc: {
                name: 'Binance Smart Chain',
                chainId: 56,
                rpcUrl: process.env.BSC_RPC_URL || 'https://bsc-dataseed.binance.org/',
                explorer: 'https://bscscan.com'
            },
            polygon: {
                name: 'Polygon',
                chainId: 137,
                rpcUrl: process.env.POLYGON_RPC_URL || 'https://polygon-rpc.com/',
                explorer: 'https://polygonscan.com'
            }
        };
    }

    /**
     * Load additional configuration from secure remote API
     */
    async loadRemoteConfig() {
        try {
            const response = await fetch(`${this.config.API_URL}/config`, {
                headers: {
                    'Authorization': `Bearer ${process.env.CONFIG_API_TOKEN || ''}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const remoteConfig = await response.json();
                this.config = { ...this.config, ...remoteConfig };
            }
        } catch (error) {
            console.warn('Could not load remote configuration:', error.message);
            // Continue with local configuration
        }
    }

    /**
     * Fallback configuration for development/testing
     */
    loadFallbackConfig() {
        console.warn('Loading fallback configuration - some features may not work');
        this.config = {
            API_URL: 'http://localhost:3000',
            WS_URL: 'ws://localhost:3001',
            ENCRYPTION_ENABLED: false,
            AUDIT_LOGGING: false,
            SUPPORTED_NETWORKS: this.getSupportedNetworks(),
            THEME: 'dark',
            DEBUG_MODE: true,
        };
        this.loaded = true;
    }

    /**
     * Get configuration value with validation
     */
    get(key, defaultValue = null) {
        if (!this.loaded) {
            console.warn('Configuration not loaded yet. Call loadConfig() first.');
            return defaultValue;
        }
        return this.config[key] || defaultValue;
    }

    /**
     * Validate that all required configuration is present
     */
    validate() {
        const required = ['API_URL'];
        const missing = required.filter(key => !this.config[key]);
        
        if (missing.length > 0) {
            throw new Error(`Missing required configuration: ${missing.join(', ')}`);
        }
        return true;
    }
}

// Example wallet configuration (DEMO DATA ONLY - NOT FOR PRODUCTION)
class WalletConfigExample {
    /**
     * SECURITY WARNING: These are example values for demonstration only.
     * NEVER use these values in production. NEVER commit real wallet data.
     */
    static getExampleWalletData() {
        return {
            // Example wallet seeds (FAKE - for testing only)
            exampleSeeds: [
                {
                    name: 'Demo BTC Wallet',
                    seed: 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about',
                    network: 'testnet',
                    purpose: 'DEMO ONLY - NOT REAL'
                },
                {
                    name: 'Demo ETH Wallet', 
                    seed: 'test test test test test test test test test test test junk',
                    network: 'testnet',
                    purpose: 'DEMO ONLY - NOT REAL'
                }
            ],
            
            // Example addresses (testnet only)
            exampleAddresses: [
                {
                    name: 'Demo BTC Address',
                    address: 'tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx', // Bitcoin testnet
                    balance: '0.001 BTC (testnet)',
                    network: 'testnet'
                },
                {
                    name: 'Demo ETH Address',
                    address: '0x742d35Cc6634C0532925a3b8D42072cc70042B23', // Ethereum testnet
                    balance: '1.0 ETH (testnet)',
                    network: 'goerli'
                }
            ]
        };
    }
}

// Export configuration classes
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SecureConfig, WalletConfigExample };
} else {
    window.SecureConfig = SecureConfig;
    window.WalletConfigExample = WalletConfigExample;
}
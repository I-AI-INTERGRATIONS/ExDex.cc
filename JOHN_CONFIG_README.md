# JOHN.ini Configuration Guide

## Overview

The `JOHN.ini` file is the main configuration file for the ExDex.cc backend services. It centralizes all configuration parameters including blockchain settings, API keys, and feature flags.

## Setup Instructions

1. **Copy the example file:**
   ```bash
   cp JOHN.ini.example JOHN.ini
   ```

2. **Edit JOHN.ini** with your actual configuration values:
   - Replace all `YOUR_*` placeholders with actual API keys
   - Update `CHANGE_ME_*` security values with strong random strings
   - Adjust server settings for your deployment environment

3. **Keep it secure:**
   - Never commit `JOHN.ini` to version control (it's in `.gitignore`)
   - Only commit changes to `JOHN.ini.example` if adding new config options
   - Store production configurations in a secure secrets management system

## Configuration Sections

### [SERVER]
Basic server configuration including host, port, and CORS settings.

### [BLOCKCHAIN_BTC]
Bitcoin network configuration for wallet creation and transaction processing.

### [BLOCKCHAIN_ETH]
Ethereum network configuration including Infura URL and chain settings.

### [BLOCKCHAIN_LTC] / [BLOCKCHAIN_DOGE]
Litecoin and Dogecoin network configurations.

### [PAYMENT_COINPAYMENTS]
CoinPayments API integration for processing cryptocurrency payments.

### [PAYMENT_CARD]
Card payment processing configuration including BIN and PPC endpoint.

### [AI_SERVICES]
Local AI service configurations for ASR, TTS, and LLM integration.

### [LOGGING]
Logging configuration for operational security monitoring.

### [SECURITY]
Security-related settings. **CRITICAL:** Change all default values before deployment.

### [WALLET_KNOX]
Knox Wallet integration settings.

### [API_ENDPOINTS]
External API endpoints for blockchain explorers and data services.

### [FEATURES]
Feature flags to enable/disable specific functionality.

## Using Configuration in Code

To use this configuration in Python, you can use the `configparser` module:

```python
import configparser

config = configparser.ConfigParser()
config.read('JOHN.ini')

# Access configuration values
infura_url = config.get('BLOCKCHAIN_ETH', 'infura_url')
log_level = config.get('LOGGING', 'log_level')
enable_btc = config.getboolean('FEATURES', 'enable_btc')
```

## Security Best Practices

1. **Never hardcode secrets** - Always use the configuration file or environment variables
2. **Rotate keys regularly** - Update API keys and secrets periodically
3. **Use environment-specific configs** - Maintain separate configs for dev/staging/production
4. **Encrypt at rest** - Consider encrypting the configuration file on disk
5. **Audit access** - Monitor who accesses configuration files

## Environment Variables Override

Environment variables can override configuration file settings. For example:
- `INFURA_URL` environment variable overrides `[BLOCKCHAIN_ETH] infura_url`
- `COINPAYMENTS_PUBLIC_KEY` overrides `[PAYMENT_COINPAYMENTS] public_key`

This allows for flexible deployment in containerized environments.

## Troubleshooting

### Configuration file not found
Ensure `JOHN.ini` is in the same directory as the backend scripts or specify the full path.

### Invalid configuration values
Check that all required fields are filled and values are in the correct format.

### Permission denied
Ensure the configuration file has appropriate read permissions (recommended: 600).

## See Also

- `website/js/config-example.js` - Frontend configuration
- `website/backend/main.py` - Backend implementation
- `README.md` - Project overview

"""
Example integration of JOHN.ini configuration with the ExDex backend

This shows how to modify website/backend/main.py to use the configuration file
instead of hardcoded values or environment variables only.
"""

from fastapi import FastAPI
from config_loader import ExDexConfig
import os

# Initialize the configuration loader
# It will fall back to environment variables if config file is not found
try:
    config = ExDexConfig("JOHN.ini")
except FileNotFoundError:
    # In production, you would configure proper logging here
    # For this example, config will be None and env vars will be used
    config = None

app = FastAPI()

# Example: Get Infura URL from config with environment variable override
if config:
    INFURA_URL = config.get('BLOCKCHAIN_ETH', 'infura_url')
else:
    INFURA_URL = os.getenv('INFURA_URL', 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID')

# Example: Get server configuration
if config:
    SERVER_HOST = config.get('SERVER', 'host', '127.0.0.1')
    SERVER_PORT = config.getint('SERVER', 'port', 8000)
    DEBUG_MODE = config.getboolean('SERVER', 'debug', False)
else:
    SERVER_HOST = os.getenv('SERVER_HOST', '127.0.0.1')
    try:
        SERVER_PORT = int(os.getenv('SERVER_PORT', '8000'))
    except ValueError:
        SERVER_PORT = 8000  # Fallback to default if invalid
    DEBUG_MODE = os.getenv('DEBUG', 'false').lower() == 'true'

# Example: Get CoinPayments API keys
if config:
    COINPAYMENTS_PUBLIC = config.get('PAYMENT_COINPAYMENTS', 'public_key')
    COINPAYMENTS_PRIVATE = config.get('PAYMENT_COINPAYMENTS', 'private_key')
else:
    COINPAYMENTS_PUBLIC = os.getenv('COINPAYMENTS_PUBLIC_KEY')
    COINPAYMENTS_PRIVATE = os.getenv('COINPAYMENTS_PRIVATE_KEY')

# Example: Get feature flags
if config:
    ENABLE_BTC = config.getboolean('FEATURES', 'enable_btc', True)
    ENABLE_ETH = config.getboolean('FEATURES', 'enable_eth', True)
    ENABLE_AI_CHAT = config.getboolean('FEATURES', 'enable_ai_chat', True)
else:
    ENABLE_BTC = os.getenv('ENABLE_BTC', 'true').lower() == 'true'
    ENABLE_ETH = os.getenv('ENABLE_ETH', 'true').lower() == 'true'
    ENABLE_AI_CHAT = os.getenv('ENABLE_AI_CHAT', 'true').lower() == 'true'

# Example: Get logging configuration
if config:
    LOG_FILE = config.get('LOGGING', 'log_file', 'opsec_log.txt')
    LOG_LEVEL = config.get('LOGGING', 'log_level', 'INFO')
else:
    LOG_FILE = os.getenv('LOG_FILE', 'opsec_log.txt')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

@app.get("/config/info")
def get_config_info():
    """Endpoint to show which configuration source is being used"""
    return {
        "config_source": "JOHN.ini" if config else "environment_variables",
        "features": {
            "btc_enabled": ENABLE_BTC,
            "eth_enabled": ENABLE_ETH,
            "ai_chat_enabled": ENABLE_AI_CHAT
        },
        "server": {
            "host": SERVER_HOST,
            "port": SERVER_PORT,
            "debug": DEBUG_MODE
        }
    }

if __name__ == "__main__":
    import uvicorn
    print(f"Starting server on {SERVER_HOST}:{SERVER_PORT}")
    print(f"Configuration source: {'JOHN.ini' if config else 'environment variables'}")
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG_MODE)

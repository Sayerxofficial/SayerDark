import os
import json
from typing import Dict, List, Union

# Default configuration
DEFAULT_CONFIG = {
    'TOR_SOCKS_PROXY': {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    },
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'CHECK_INTERVAL': 600,
    'MAX_RETRIES': 3,
    'TIMEOUT': 30,
    'REQUEST_DELAY': 2,
    'MAX_DEPTH': 3,
    'MAX_PAGES': 100,
    'DATABASE_FILE': 'products.db',
    'BACKUP_DIR': 'backups',
    'LOG_FILE': 'sayerdark.log'
}

# Random user agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# Common HTML selectors
SELECTORS = {
    'product': [
        'div.product-container',
        'div.product',
        'article.item',
        'div.listing'
    ],
    'title': [
        'h1.title',
        'h2.name',
        'a.product-title',
        'span.title'
    ],
    'price': [
        'span.price',
        'div.amount',
        'span.product-price',
        'div.price'
    ]
}

def load_config(config_file: str = 'config.json') -> Dict:
    """Load configuration from file with validation"""
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            config = {}
        
        # Merge with defaults
        merged_config = DEFAULT_CONFIG.copy()
        merged_config.update(config)
        
        # Validate configuration
        validate_config(merged_config)
        
        return merged_config
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        return DEFAULT_CONFIG

def validate_config(config: Dict) -> bool:
    """Validate configuration values"""
    try:
        # Check required fields
        required_fields = ['TOR_SOCKS_PROXY', 'USER_AGENT', 'CHECK_INTERVAL']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required configuration field: {field}")
        
        # Validate numeric fields
        numeric_fields = ['CHECK_INTERVAL', 'MAX_RETRIES', 'TIMEOUT', 'REQUEST_DELAY', 'MAX_DEPTH', 'MAX_PAGES']
        for field in numeric_fields:
            if field in config and not isinstance(config[field], (int, float)):
                raise ValueError(f"Invalid numeric value for {field}")
        
        # Validate proxy configuration
        if not isinstance(config['TOR_SOCKS_PROXY'], dict):
            raise ValueError("Invalid TOR_SOCKS_PROXY configuration")
        
        return True
    except Exception as e:
        print(f"Configuration validation error: {str(e)}")
        return False

def save_config(config: Dict, config_file: str = 'config.json') -> bool:
    """Save configuration to file"""
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving configuration: {str(e)}")
        return False

# Load configuration
config = load_config()

# Export configuration values
TOR_SOCKS_PROXY = config['TOR_SOCKS_PROXY']
USER_AGENT = config['USER_AGENT']
CHECK_INTERVAL = config['CHECK_INTERVAL']
MAX_RETRIES = config['MAX_RETRIES']
TIMEOUT = config['TIMEOUT']
REQUEST_DELAY = config['REQUEST_DELAY']
MAX_DEPTH = config['MAX_DEPTH']
MAX_PAGES = config['MAX_PAGES']
DATABASE_FILE = config['DATABASE_FILE']
BACKUP_DIR = config['BACKUP_DIR']
LOG_FILE = config['LOG_FILE']

# List of keywords for search
KEYWORDS = [
    "product", "item", "price", "buy", "sell", "offer",
    "card", "transfer", "payment", "service", "market"
]

# List of common HTML elements for products
PRODUCT_SELECTORS = [
    "div.product", "div.item", "div.listing", "div.card",
    "div.product-container", "div.product-item", "div.product-box",
    "div.item-container", "div.listing-item", "div.card-item"
]

# List of common HTML elements for prices
PRICE_SELECTORS = [
    "span.price", "div.price", "span.amount", "div.amount",
    "span.cost", "div.cost", "span.value", "div.value",
    "span.currency", "div.currency"
]

# List of markets to crawl
MARKETS = {
    "market1": {
        "url": "http://l5keufi2jvz34eva7znc4we2e743kqn33o2qjxme2l7r6ylozpwsi2yd.onion",
        "parser": "market1"
    }
}

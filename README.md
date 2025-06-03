<<<<<<< HEAD
# SayerDark - Dark Web Market Monitor

A powerful and flexible tool for monitoring dark web markets, analyzing site structures, and tracking product prices.

## Features

- **Market Monitoring**: Track products and prices across multiple dark web markets
- **Site Mapping**: Extract and analyze site structures
- **Price History**: Track price changes over time
- **Tor Integration**: Built-in support for accessing .onion sites
- **Advanced Parsing**: Flexible HTML parsing with multiple selectors
- **Database Storage**: SQLite database for persistent data storage
- **NLP Analysis**: Basic text analysis for product descriptions

## Official Channel

Join our official Telegram channel for updates and support:
- [SayerX Channel](https://t.me/+J_4BNHpp0X9hODM0)

## Requirements

- Python 3.13+
- Tor Browser or Tor service running on port 9050
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SayerDark.git
cd SayerDark
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to customize:
- Tor proxy settings
- Crawling parameters
- User agents
- Product selectors
- Market URLs

## Usage

1. Start the program:
```bash
python sayerdark.py
```

2. Choose operation mode:
   - Product monitoring
   - Site structure analysis

3. Enter target URL:
   - Regular sites: http://example.com
   - Dark web: http://example.onion

## Project Structure

```
SayerDark/
├── sayerdark.py      # Main program
├── config.py         # Configuration settings
├── db.py            # Database operations
├── nlp_utils.py     # Text analysis utilities
├── requirements.txt # Dependencies
├── parsers/         # Market-specific parsers
│   └── market1.py   # Example market parser
└── venv/            # Virtual environment
```

## Database Schema

### Products Table
- id (PRIMARY KEY)
- market
- product_name
- price
- url
- last_seen
- first_seen
- price_history

### Markets Table
- id (PRIMARY KEY)
- name
- url
- last_check
- status
- error_count

## Security Considerations

- Always use Tor for accessing dark web sites
- Keep your Tor service updated
- Use random user agents
- Implement request delays
- Monitor error rates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes only. Users are responsible for complying with all applicable laws and regulations.
=======
# SayerDark
Know the content of dark Internet sites without entering the dark Internet to protect your privacy
>>>>>>> 85dc07c789761d79596e6e0a3bf1cf6c65d6b89f

# 🤖 Finance Trading AI Agent

An intelligent financial trading agent built with LangChain and LangGraph that provides comprehensive stock analysis, technical indicators, and market insights.

## 🚀 Features

- **Real-time Stock Data**: Get current prices, volume, and daily performance
- **Technical Analysis**: RSI, moving averages, support/resistance levels
- **Company Information**: Sector, industry, market cap, and financial metrics
- **Portfolio Analysis**: Track multiple holdings and calculate P&L
- **Market Movers**: Top gainers and losers tracking
- **Earnings Calendar**: Earnings dates and financial metrics
- **Financial News**: Real-time news and market analysis
- **Docker Support**: Containerized deployment

## 🛠️ Tech Stack

- **Python 3.11**
- **LangChain** - LLM framework
- **LangGraph** - Stateful applications
- **Anthropic Claude** - AI model
- **Tavily** - Search API
- **Yahoo Finance** - Stock data
- **Docker** - Containerization

## 📋 Prerequisites

- Python 3.11+
- Docker (optional)
- API Keys:
  - [Anthropic API Key](https://console.anthropic.com/)
  - [Tavily API Key](https://tavily.com/)

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd my-ai-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export ANTHROPIC_API_KEY='your-anthropic-key'
   export TAVILY_API_KEY='your-tavily-key'
   ```

4. **Run the agent**
   ```bash
   python main.py
   ```

### Docker Installation

1. **Build the Docker image**
   ```bash
   ./docker-run.sh build
   ```

2. **Run with Docker**
   ```bash
   ./docker-run.sh run
   ```

3. **Or use Docker Compose**
   ```bash
   docker-compose up --build
   ```

## 💬 Usage Examples

### Stock Price Information
```
💰 Ask about stocks: What's AAPL trading at?
```

### Technical Analysis
```
💰 Ask about stocks: Show me RSI and moving averages for TSLA
```

### Company Information
```
💰 Ask about stocks: Tell me about Microsoft
```

### Portfolio Analysis
```
💰 Ask about stocks: Analyze my portfolio: AAPL:100,MSFT:50,GOOGL:25
```

### Market Movers
```
💰 Ask about stocks: Show me today's top gainers
```

### Earnings Information
```
💰 Ask about stocks: When is NVDA's next earnings?
```

## 🛠️ Available Tools

| Tool | Description | Usage |
|------|-------------|-------|
| `get_stock_price` | Current stock price and performance | Stock symbol (e.g., 'AAPL') |
| `technical_analysis` | RSI, moving averages, support/resistance | Stock symbol |
| `company_info` | Company profile and fundamentals | Stock symbol |
| `portfolio_analysis` | Portfolio holdings and P&L | Format: 'AAPL:100,TSLA:50' |
| `market_movers` | Top gainers/losers | 'gainers' or 'losers' |
| `earnings_info` | Earnings calendar and metrics | Stock symbol |
| `search_financial_news` | Financial news and analysis | Search query |

## 🐳 Docker Commands

```bash
# Build image
./docker-run.sh build

# Run interactively
./docker-run.sh run

# Use Docker Compose
./docker-run.sh compose

# Stop containers
./docker-run.sh stop
```

## 📁 Project Structure

```
my-ai-agent/
├── main.py                 # Main application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── docker-run.sh          # Docker helper script
├── .dockerignore          # Docker ignore file
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
ANTHROPIC_API_KEY=your-anthropic-api-key
TAVILY_API_KEY=your-tavily-api-key
```

### API Keys Setup

1. **Anthropic API**: Get your key from [Anthropic Console](https://console.anthropic.com/)
2. **Tavily API**: Get your key from [Tavily](https://tavily.com/)

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Docker Production
```bash
docker build -t trading-agent .
docker run -d --name trading-agent trading-agent
```

### Docker Compose
```bash
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is a demonstration project for educational purposes. It is not financial advice. Always do your own research before making investment decisions.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/yourusername/my-ai-agent/issues) page
2. Create a new issue with detailed information
3. Include your Python version and error messages

## 🔄 Updates

Stay updated with the latest features and bug fixes by pulling from the main branch:

```bash
git pull origin main
```

---

**Happy Trading! 📈** 

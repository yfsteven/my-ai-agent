import getpass
import os
from langchain.chat_models import init_chat_model
from langchain.tools import Tool
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")

if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Enter API key for Tavily: ")

model = init_chat_model("claude-3-5-sonnet-latest", model_provider="anthropic")

search = TavilySearch(max_results=3)

memory = MemorySaver()

def get_stock_price(symbol):
    try:
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        hist = ticker.history(period="1d")
        
        if hist.empty:
            return f"Could not find data for {symbol}. Check if the symbol is correct."
        
        current_price = hist['Close'].iloc[-1]
        open_price = hist['Open'].iloc[-1]
        high_price = hist['High'].iloc[-1]
        low_price = hist['Low'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        
        prev_close = info.get('previousClose', current_price)
        change = current_price - prev_close
        change_percent = (change / prev_close) * 100
        
        return f"""
                📊 {symbol.upper()} Stock Info:
                💰 Current Price: ${current_price:.2f}
                📈 Change: ${change:.2f} ({change_percent:+.2f}%)
                🌅 Open: ${open_price:.2f}
                ⬆️ High: ${high_price:.2f}
                ⬇️ Low: ${low_price:.2f}
                📊 Volume: {volume:,}
                🏢 Company: {info.get('longName', 'N/A')}
                💼 Market Cap: ${info.get('marketCap', 0):,}
                """
    except Exception as e:
        return f"Error fetching data for {symbol}: {str(e)}"

def calculate_technical_indicators(symbol):
    try:
        ticker = yf.Ticker(symbol.upper())
        hist = ticker.history(period="6mo")
        
        if hist.empty:
            return f"Could not fetch historical data for {symbol}"
        
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
        sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
        current_price = hist['Close'].iloc[-1]
        
        recent_high = hist['High'].tail(20).max()
        recent_low = hist['Low'].tail(20).min()
        
        return f"""
                📈 Technical Analysis for {symbol.upper()}:
                🎯 RSI (14): {current_rsi:.2f} {'(Overbought)' if current_rsi > 70 else '(Oversold)' if current_rsi < 30 else '(Neutral)'}
                📊 SMA 20: ${sma_20:.2f} {'✅ Above' if current_price > sma_20 else '❌ Below'}
                📊 SMA 50: ${sma_50:.2f} {'✅ Above' if current_price > sma_50 else '❌ Below'}
                ⬆️ 20-day High: ${recent_high:.2f}
                ⬇️ 20-day Low: ${recent_low:.2f}
                💰 Current: ${current_price:.2f}
                """
    except Exception as e:
        return f"Error calculating indicators for {symbol}: {str(e)}"

def get_stock_info(symbol):
    try:
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        
        return f"""
                🏢 Company Profile for {symbol.upper()}:
                📛 Name: {info.get('longName', 'N/A')}
                🏭 Sector: {info.get('sector', 'N/A')}
                🔧 Industry: {info.get('industry', 'N/A')}
                👥 Employees: {info.get('fullTimeEmployees', 'N/A'):,}
                🌍 Country: {info.get('country', 'N/A')}
                💰 Market Cap: ${info.get('marketCap', 0):,}
                📊 P/E Ratio: {info.get('trailingPE', 'N/A')}
                💸 Dividend Yield: {info.get('dividendYield', 0)*100:.2f}%
                📝 Description: {info.get('longBusinessSummary', 'N/A')[:200]}...
                """
    except Exception as e:
        return f"Error fetching company info for {symbol}: {str(e)}"

def portfolio_analysis(holdings_input):
    try:
        holdings = {}
        for holding in holdings_input.split(','):
            symbol, shares = holding.strip().split(':')
            holdings[symbol.upper()] = int(shares)
        
        total_value = 0
        portfolio_data = []
        
        for symbol, shares in holdings.items():
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                position_value = current_price * shares
                total_value += position_value
                
                info = ticker.info
                prev_close = info.get('previousClose', current_price)
                change = current_price - prev_close
                change_percent = (change / prev_close) * 100
                daily_pnl = change * shares
                
                portfolio_data.append({
                    'symbol': symbol,
                    'shares': shares,
                    'price': current_price,
                    'value': position_value,
                    'change_pct': change_percent,
                    'daily_pnl': daily_pnl
                })
        
        portfolio_summary = f"💼 Portfolio Analysis:\n"
        portfolio_summary += f"💰 Total Portfolio Value: ${total_value:,.2f}\n\n"
        
        total_daily_pnl = 0
        for stock in portfolio_data:
            total_daily_pnl += stock['daily_pnl']
            portfolio_summary += f"📊 {stock['symbol']}: {stock['shares']} shares\n"
            portfolio_summary += f"   💰 ${stock['price']:.2f} x {stock['shares']} = ${stock['value']:,.2f}\n"
            portfolio_summary += f"   📈 Daily: {stock['change_pct']:+.2f}% (${stock['daily_pnl']:+.2f})\n\n"
        
        portfolio_summary += f"📊 Total Daily P&L: ${total_daily_pnl:+,.2f}\n"
        if total_value > 0:
            portfolio_summary += f"📈 Portfolio Daily Change: {(total_daily_pnl/total_value)*100:+.2f}%"
        else:
            portfolio_summary += f"📈 Portfolio Daily Change: N/A (no valid positions)"
        
        return portfolio_summary
    except Exception as e:
        return f"Error analyzing portfolio: {str(e)}. Format: 'AAPL:100,TSLA:50'"

def market_movers(move_type):
    try:
        popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC']
        
        movers = []
        for symbol in popular_stocks:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                current_price = info.get('currentPrice', 0)
                prev_close = info.get('previousClose', current_price)
                
                if prev_close > 0:
                    change_percent = ((current_price - prev_close) / prev_close) * 100
                    movers.append({
                        'symbol': symbol,
                        'change_pct': change_percent,
                        'price': current_price
                    })
            except Exception:
                continue
        
        if move_type.lower() == 'gainers':
            movers.sort(key=lambda x: x['change_pct'], reverse=True)
            title = "📈 Top Gainers Today:"
        else:
            movers.sort(key=lambda x: x['change_pct'])
            title = "📉 Top Losers Today:"
        
        result = f"{title}\n\n"
        for i, stock in enumerate(movers[:5]):
            result += f"{i+1}. {stock['symbol']}: {stock['change_pct']:+.2f}% (${stock['price']:.2f})\n"
        
        return result
    except Exception as e:
        return f"Error fetching market movers: {str(e)}"

def get_earnings_calendar(symbol):
    try:
        ticker = yf.Ticker(symbol.upper())
        calendar = ticker.calendar
        info = ticker.info
        
        earnings_info = f"📅 Earnings Info for {symbol.upper()}:\n\n"
        
        if calendar is not None and not calendar.empty:
            earnings_info += f"📊 Next Earnings Date: {calendar.index[0].strftime('%Y-%m-%d')}\n"
        
        earnings_info += f"💰 EPS (TTM): ${info.get('trailingEps', 'N/A')}\n"
        earnings_info += f"📈 EPS Estimate: ${info.get('forwardEps', 'N/A')}\n"
        earnings_info += f"📊 P/E Ratio: {info.get('trailingPE', 'N/A')}\n"
        earnings_info += f"🎯 PEG Ratio: {info.get('pegRatio', 'N/A')}\n"
        earnings_info += f"💸 Revenue (TTM): ${info.get('totalRevenue', 0):,}\n"
        
        return earnings_info
    except Exception as e:
        return f"Error fetching earnings data for {symbol}: {str(e)}"
    
def search_financial_news(query):
    try:
        search_results = search.invoke(f"{query} stock market finance news")
        
        if isinstance(search_results, str):
            return f"🔍 Search Results for '{query}':\n\n{search_results}"
        
        if not search_results:
            return f"No recent information found for: {query}"
        
        search_summary = f"🔍 Recent Information for '{query}':\n\n"
        
        for i, result in enumerate(search_results, 1):
            if isinstance(result, dict):
                title = result.get('title', 'No title')
                content = result.get('content', 'No content')[:200]
                url = result.get('url', 'No URL')
            else:
                title = f"Result {i}"
                content = str(result)[:200]
                url = "No URL"
            
            search_summary += f"{i}. {title}\n"
            search_summary += f"   📄 {content}...\n"
            search_summary += f"   🔗 Source: {url}\n\n"
        
        return search_summary
    except Exception as e:
        return f"Error searching for {query}: {str(e)}"

tools = [
    Tool(
        name="get_stock_price",
        description="Get current stock price and daily performance. Use ticker symbol like 'AAPL'",
        func=get_stock_price
    ),
    Tool(
        name="technical_analysis",
        description="Calculate technical indicators (RSI, moving averages, support/resistance). Use ticker symbol.",
        func=calculate_technical_indicators
    ),
    Tool(
        name="company_info",
        description="Get detailed company information, sector, industry, market cap. Use ticker symbol.",
        func=get_stock_info
    ),
    Tool(
        name="portfolio_analysis",
        description="Analyze portfolio holdings and calculate total value. Format: 'AAPL:100,TSLA:50,NVDA:25'",
        func=portfolio_analysis
    ),
    Tool(
        name="market_movers",
        description="Get top gainers or losers. Use 'gainers' or 'losers'",
        func=market_movers
    ),
    Tool(
        name="earnings_info",
        description="Get earnings calendar and financial metrics for a stock. Use ticker symbol.",
        func=get_earnings_calendar
    ),
    Tool(
        name="search_financial_news",
        description="Search for recent news, market analysis, or any financial information not available in other tools. Use for breaking news, analyst opinions, market trends, company developments.",
        func=search_financial_news
    )
]

agent_executor = create_react_agent(model, tools, checkpointer=memory)

def run_trading_agent():
    print("📈 Finance Trading Agent Ready!")
    print("\n🚀 Available Commands:")
    print("• Stock prices: 'What's AAPL trading at?'")
    print("• Technical analysis: 'Show me RSI and moving averages for TSLA'")
    print("• Company info: 'Tell me about Microsoft'")
    print("• Portfolio analysis: 'Analyze my portfolio: AAPL:100,MSFT:50,GOOGL:25'")
    print("• Market movers: 'Show me today's top gainers'")
    print("• Earnings: 'When is NVDA's next earnings?'")
    print("-" * 60)

    config = {"configurable": {"thread_id": "current_session"}}
    
    while True:
        user_input = input("\n💰 Ask about stocks (or 'quit'): ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Happy trading! 📊")
            break
        
        try:
            result = agent_executor.invoke({
                "messages": [{"role": "user", "content": user_input}]
            }, config)
            response = result['messages'][-1].content
            print(f"\n🤖 Trading Agent: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_trading_agent()
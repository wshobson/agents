---
name: sdk-automated-trading
description: Master Claude SDK for building automated trading systems with real-time signal generation, risk management, order execution, and performance monitoring. Covers algorithmic trading strategies, backtesting automation, and multi-timeframe analysis. Use when building trading bots, automating trading strategies, generating real-time signals, or developing systematic trading systems.
---

# Claude SDK Automated Trading Systems

Master the Claude SDK to build sophisticated automated trading systems with real-time signal generation, intelligent risk management, and systematic strategy execution.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Building automated trading bots and systems
- Developing algorithmic trading strategies
- Creating real-time trading signal generation
- Automating technical analysis and pattern recognition
- Implementing systematic risk management
- Building backtesting frameworks
- Creating multi-agent trading orchestration
- Developing market scanning and opportunity detection
- Automating trade execution and order management
- Building performance monitoring and reporting systems

## Core Concepts

### 1. Automated Trading System Architecture

**Core Components of Trading System**

A production-grade automated trading system built with Claude SDK:

```markdown
## Trading System Architecture

**Component 1: Market Data Pipeline**
- Real-time price feeds (WebFetch from APIs)
- Historical data collection (for backtesting)
- Data cleaning and normalization
- Multi-timeframe aggregation

**Component 2: Signal Generation Engine**
- Technical analysis (indicators, patterns)
- Multi-agent analysis (technical + fundamental)
- Confluence scoring (multiple signal agreement)
- Signal quality filtering

**Component 3: Risk Management**
- Position sizing algorithms
- Stop-loss automation
- Portfolio exposure limits
- Volatility-based risk scaling

**Component 4: Order Execution**
- Order generation and validation
- Broker API integration
- Order status monitoring
- Execution confirmation

**Component 5: Performance Monitoring**
- P&L tracking real-time
- Drawdown monitoring
- Strategy performance metrics
- Alert systems for anomalies
```

**SDK Tools for Trading Automation**

```markdown
## SDK Tool Usage in Trading

**WebFetch** - Real-time market data
```python
# Fetch real-time quote
WebFetch(
    url="https://api.alpaca.markets/v2/stocks/AAPL/quotes/latest",
    prompt="Get current bid, ask, last price for AAPL"
)

# Fetch technical indicators
WebFetch(
    url="https://api.tradingview.com/scan",
    prompt="Get RSI, MACD, Bollinger Bands for AAPL on 1-hour chart"
)
```

**Task** - Multi-agent trading coordination
```python
# Coordinate multiple analysts
Task(
    subagent_type="general-purpose",
    description="Generate trading signals",
    prompt="""
    Coordinate trading analysis:
    1. Technical analyst: Chart patterns, indicators
    2. Fundamental analyst: Earnings, news sentiment
    3. Risk specialist: Position sizing, stops
    Synthesize into trade recommendation
    """
)
```

**Bash** - Execute trading algorithms
```bash
# Run trading strategy
python strategies/mean_reversion.py --symbol AAPL --timeframe 1h --dry-run false

# Execute backtest
python backtest.py --strategy momentum --start 2024-01-01 --end 2025-11-09
```

**Read/Write** - Trading configuration and logs
```python
# Read strategy parameters
Read(file_path="config/strategy_params.json")

# Write trade log
Write(
    file_path="logs/trades_2025-11-09.json",
    content=trade_log
)
```
```

### 2. Real-Time Signal Generation

**Multi-Indicator Signal System**

Generate high-confidence trading signals using multiple indicators:

```markdown
## Real-Time Signal Generation Workflow

**Strategy:** Momentum breakout with confluence

**Step 1: Fetch Real-Time Data**
```python
# Get current market data
price_data = WebFetch(
    url="https://api.polygon.io/v2/aggs/ticker/AAPL/range/5/minute/2025-11-09/2025-11-09",
    prompt="Get 5-minute candles for today: OHLCV data"
)

# Get technical indicators
indicators = WebFetch(
    url="https://api.taapi.io/rsi?symbol=AAPL&interval=5m",
    prompt="Get RSI, MACD, and ATR for AAPL on 5-minute chart"
)
```

**Step 2: Calculate Signals**
```bash
# Run signal generation
Bash(command="python signals/momentum_breakout.py --symbol AAPL --timeframe 5m")
```

**momentum_breakout.py:**
```python
import pandas as pd
import talib

# Load price data
df = pd.read_json("data/AAPL_5m.json")

# Calculate indicators
df['RSI'] = talib.RSI(df['close'], timeperiod=14)
df['MACD'], df['MACD_signal'], _ = talib.MACD(df['close'])
df['BB_upper'], df['BB_middle'], df['BB_lower'] = talib.BBANDS(df['close'])
df['ATR'] = talib.ATR(df['high'], df['low'], df['close'])

# Current values
current = df.iloc[-1]
prev = df.iloc[-2]

# Signal conditions
signals = {
    'breakout': current['close'] > current['BB_upper'],
    'momentum': current['RSI'] > 60 and current['RSI'] < 75,
    'macd': current['MACD'] > current['MACD_signal'] and prev['MACD'] <= prev['MACD_signal'],
    'volume': current['volume'] > df['volume'].rolling(20).mean().iloc[-1] * 1.5
}

# Confluence score (4 signals)
score = sum(signals.values())

# Generate signal
if score >= 3:  # At least 3/4 signals agree
    signal = {
        'action': 'BUY',
        'symbol': 'AAPL',
        'price': current['close'],
        'confidence': score / 4,
        'stop_loss': current['close'] - (2 * current['ATR']),
        'take_profit': current['close'] + (3 * current['ATR']),
        'position_size': calculate_position_size(current['ATR'])
    }
    print(json.dumps(signal))
```

**Step 3: Multi-Agent Validation**
```python
# Validate signal with multiple agents
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Validate trading signal for AAPL BUY:
    - Technical analyst: Confirm chart pattern validity
    - News analyst: Check for negative news in last hour
    - Risk manager: Validate position size and stops

    Signal details: {signal}

    Provide: APPROVE or REJECT with reasoning
    """
)
```

**Output:**
```
🎯 Trading Signal Generated - 2025-11-09 14:35

Symbol: AAPL
Action: BUY
Price: $180.50
Confidence: 75% (3/4 signals)

Signal Breakdown:
✅ Breakout: Price above upper Bollinger Band ($180.25)
✅ Momentum: RSI at 68 (strong but not overbought)
✅ MACD: Bullish crossover just occurred
✅ Volume: 2.1x average (strong conviction)

Risk Management:
- Position size: 100 shares ($18,050)
- Stop loss: $176.50 (2 ATR below entry)
- Take profit: $186.50 (3 ATR above entry)
- Risk: $400 (2.2% of position)
- Reward: $600 (3.3% of position)
- R/R Ratio: 1.5:1

Multi-Agent Validation:
✅ Technical: Pattern confirmed, clean breakout
✅ News: No negative catalysts in last hour
✅ Risk: Position size within 2% portfolio limit

Decision: APPROVED - Execute trade
```
```

**Pattern Recognition Automation**

Automated chart pattern detection:

```markdown
## Automated Pattern Recognition

**SDK Workflow:**

**Step 1: Scan Market for Patterns**
```python
# Scan entire watchlist
watchlist = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'AMD', 'AMZN']

for symbol in watchlist:
    # Fetch chart data
    WebFetch(
        url=f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/2025-10-01/2025-11-09",
        prompt=f"Get daily OHLCV for {symbol} last 30 days"
    )

    # Detect patterns
    Bash(command=f"python patterns/detect_patterns.py --symbol {symbol} --data data/{symbol}_daily.json")
```

**detect_patterns.py:**
```python
import pandas as pd
import numpy as np

def detect_head_and_shoulders(df):
    """Detect head and shoulders pattern"""
    # Simplified pattern detection
    # (In production, use more sophisticated algorithms)

    peaks = []
    for i in range(5, len(df)-5):
        if df['high'].iloc[i] > df['high'].iloc[i-5:i].max() and \
           df['high'].iloc[i] > df['high'].iloc[i+1:i+6].max():
            peaks.append((i, df['high'].iloc[i]))

    # Check for H&S pattern
    if len(peaks) >= 3:
        left, head, right = peaks[-3:]
        if head[1] > left[1] and head[1] > right[1] and \
           abs(left[1] - right[1]) / left[1] < 0.02:  # Shoulders similar
            return {
                'pattern': 'Head and Shoulders',
                'bearish': True,
                'neckline': min(left[1], right[1]),
                'target': min(left[1], right[1]) - (head[1] - min(left[1], right[1]))
            }
    return None

# Load data
df = pd.read_json(f"data/{symbol}_daily.json")

# Detect patterns
patterns = []
if hs := detect_head_and_shoulders(df):
    patterns.append(hs)

# ... detect other patterns (triangles, flags, etc.)

if patterns:
    print(json.dumps(patterns))
```

**Step 2: Generate Trading Signals from Patterns**
```python
# Analyze detected patterns
Task(
    subagent_type="general-purpose",
    prompt="""
    Patterns detected in watchlist:
    - AAPL: Ascending triangle (bullish)
    - TSLA: Head and shoulders (bearish)
    - NVDA: Bull flag (bullish continuation)

    For each pattern:
    1. Validate pattern quality
    2. Calculate entry/exit levels
    3. Estimate probability of success
    4. Generate trade recommendations
    """
)
```

**Output:**
```
📊 Pattern Scan Results - 2025-11-09

Patterns Detected: 3

1. AAPL - Ascending Triangle (Bullish)
   Pattern Quality: 8/10
   Current Price: $180.50
   Breakout Level: $182.00
   Target: $189.00 (+4.8%)
   Stop Loss: $178.00 (-1.4%)
   Probability: 65%
   Recommendation: BUY on breakout above $182 with volume

2. TSLA - Head and Shoulders (Bearish)
   Pattern Quality: 7/10
   Current Price: $242.00
   Neckline: $238.00
   Target: $225.00 (-7.0%)
   Stop Loss: $246.00 (+1.7%)
   Probability: 60%
   Recommendation: SHORT on break below $238 with volume

3. NVDA - Bull Flag (Bullish Continuation)
   Pattern Quality: 9/10
   Current Price: $495.00
   Breakout Level: $498.00
   Target: $520.00 (+5.1%)
   Stop Loss: $488.00 (-1.4%)
   Probability: 70%
   Recommendation: BUY on breakout above $498

Priority: NVDA (highest quality pattern + probability)
```
```

### 3. Automated Risk Management

**Dynamic Position Sizing**

Volatility-based position sizing automation:

```markdown
## Volatility-Based Position Sizing

**Goal:** Size positions based on current market volatility

**SDK Workflow:**

**Step 1: Calculate Volatility**
```python
# Fetch historical data for volatility calculation
WebFetch(
    url="https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2025-10-01/2025-11-09",
    prompt="Get daily OHLCV for AAPL last 30 days for ATR calculation"
)

# Calculate ATR
Bash(command="python risk/calculate_atr.py --symbol AAPL --period 14")
```

**calculate_atr.py:**
```python
import pandas as pd
import talib

# Load data
df = pd.read_json("data/AAPL_daily.json")

# Calculate ATR
df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)

current_atr = df['ATR'].iloc[-1]
current_price = df['close'].iloc[-1]

# ATR as percentage of price
atr_pct = (current_atr / current_price) * 100

print(f"ATR: ${current_atr:.2f}")
print(f"ATR %: {atr_pct:.2f}%")
```

**Step 2: Calculate Position Size**
```python
# Calculate optimal position size
Bash(command="python risk/position_sizing.py --symbol AAPL --account-value 100000 --risk-pct 1.0")
```

**position_sizing.py:**
```python
import json

# Parameters
account_value = 100000  # $100K account
risk_per_trade = 0.01  # Risk 1% per trade
current_price = 180.50
atr = 4.00

# Position sizing formula:
# Position Size = (Account Value × Risk %) / (ATR × ATR Multiplier)
# Using 2 ATR for stop loss distance

stop_distance = 2 * atr  # $8.00
risk_amount = account_value * risk_per_trade  # $1,000

shares = int(risk_amount / stop_distance)  # 125 shares
position_value = shares * current_price  # $22,562

print(f"Position size: {shares} shares")
print(f"Position value: ${position_value:,.0f}")
print(f"Stop loss: ${current_price - stop_distance:.2f}")
print(f"Risk amount: ${risk_amount:,.0f}")
print(f"Portfolio %: {(position_value / account_value) * 100:.1f}%")
```

**Output:**
```
Position Sizing Calculation - AAPL

Account Value: $100,000
Risk per Trade: 1.0% ($1,000)

Volatility Metrics:
- ATR: $4.00 (2.2% of price)
- ATR Multiplier for Stop: 2x
- Stop Distance: $8.00

Position Sizing:
- Shares: 125
- Position Value: $22,562 (22.6% of portfolio)
- Entry Price: $180.50
- Stop Loss: $172.50 (-4.4%)
- Risk Amount: $1,000 (1% of account)

Validation:
✅ Position within 25% portfolio limit
✅ Risk exactly 1% of account
✅ Stop loss based on technical level (2 ATR)
```
```

**Automated Stop Loss Management**

Dynamic stop-loss adjustment system:

```markdown
## Trailing Stop Loss Automation

**SDK Workflow:**

**Monitor Positions Continuously**
```python
# monitor_positions.py
import time

while True:
    # Get current positions
    positions = Read(file_path="data/current_positions.json")

    for position in positions:
        # Fetch current price
        current_price = WebFetch(
            url=f"https://api.alpaca.markets/v2/stocks/{position['symbol']}/quotes/latest",
            prompt=f"Get current price for {position['symbol']}"
        )

        # Calculate unrealized P&L
        entry_price = position['entry_price']
        pnl_pct = (current_price - entry_price) / entry_price

        # Update trailing stop
        if pnl_pct > 0.05:  # If up >5%, activate trailing stop
            # Trail stop 3 ATR below current price
            WebFetch(
                url=f"https://api.polygon.io/v2/aggs/ticker/{position['symbol']}/prev",
                prompt=f"Get yesterday's ATR for {position['symbol']}"
            )

            new_stop = current_price - (3 * atr)

            # Only raise stop, never lower
            if new_stop > position['stop_loss']:
                # Update stop
                Bash(command=f"python trading/update_stop.py --symbol {position['symbol']} --new-stop {new_stop}")

                # Log update
                Write(
                    file_path=f"logs/stop_updates_{position['symbol']}.log",
                    content=f"{datetime.now()}: Updated stop from {position['stop_loss']} to {new_stop}\n"
                )

        # Check if stop hit
        if current_price <= position['stop_loss']:
            # Exit position
            Bash(command=f"python trading/exit_position.py --symbol {position['symbol']} --reason stop_loss")

    time.sleep(60)  # Check every minute
```

**Output:**
```
🛡️ Stop Loss Update - AAPL

Position Status:
- Entry: $180.50 (2025-11-09 14:35)
- Current: $189.25 (2025-11-10 10:15)
- P&L: +$8.75 (+4.8%) ✅

Stop Loss Management:
- Initial Stop: $172.50 (2 ATR below entry)
- Current ATR: $4.20
- New Trailing Stop: $176.65 (3 ATR below current)
- Update: $172.50 → $176.65 (raised by $4.15)

Protection:
- Locked in profit: $6.15 per share
- Risk: Only -$2.60 downside from current
- Upside: Unlimited (trailing stop follows price up)

Status: Stop updated, profit protected ✅
```
```

### 4. Backtesting Automation

**Comprehensive Backtesting Framework**

Automate strategy backtesting with historical data:

```markdown
## Backtesting Framework with SDK

**Strategy to Test:** RSI Mean Reversion

**Step 1: Fetch Historical Data**
```python
# Get historical data for multiple symbols
symbols = ['AAPL', 'MSFT', 'GOOGL']

for symbol in symbols:
    WebFetch(
        url=f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/2024-01-01/2025-11-09",
        prompt=f"Get daily OHLCV data for {symbol} for 2024-2025"
    )
```

**Step 2: Run Backtest**
```bash
# Execute backtest
Bash(command="python backtest/run_backtest.py --strategy rsi_mean_reversion --start 2024-01-01 --end 2025-11-09 --initial-capital 100000")
```

**run_backtest.py:**
```python
import backtrader as bt
import pandas as pd

class RSIMeanReversion(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('rsi_oversold', 30),
        ('rsi_overbought', 70),
        ('position_size', 0.95),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(
            self.data.close,
            period=self.params.rsi_period
        )

    def next(self):
        if not self.position:
            # Buy when RSI < 30 (oversold)
            if self.rsi < self.params.rsi_oversold:
                size = int((self.broker.get_cash() * self.params.position_size) / self.data.close[0])
                self.buy(size=size)
        else:
            # Sell when RSI > 70 (overbought)
            if self.rsi > self.params.rsi_overbought:
                self.close()

# Run backtest
cerebro = bt.Cerebro()
cerebro.addstrategy(RSIMeanReversion)

# Add data
for symbol in symbols:
    data = bt.feeds.PandasData(dataname=pd.read_json(f"data/{symbol}_daily.json"))
    cerebro.adddata(data, name=symbol)

# Set initial capital
cerebro.broker.setcash(100000.0)

# Run
initial_value = cerebro.broker.getvalue()
cerebro.run()
final_value = cerebro.broker.getvalue()

# Calculate metrics
total_return = (final_value - initial_value) / initial_value

print(f"Initial: ${initial_value:,.0f}")
print(f"Final: ${final_value:,.0f}")
print(f"Return: {total_return:.2%}")
```

**Step 3: Performance Analysis**
```python
# Analyze backtest results
Task(
    subagent_type="general-purpose",
    prompt="""
    Analyze backtest results:
    1. Calculate Sharpe ratio, max drawdown, win rate
    2. Compare to buy-and-hold benchmark
    3. Identify best/worst performing periods
    4. Recommend parameter optimizations
    """
)
```

**Output:**
```
📈 Backtest Results - RSI Mean Reversion Strategy

Test Period: 2024-01-01 to 2025-11-09 (23 months)
Initial Capital: $100,000

Performance Metrics:
- Final Value: $128,450
- Total Return: +28.5%
- Annualized Return: +14.8%
- Sharpe Ratio: 1.32
- Max Drawdown: -12.3%
- Win Rate: 58%
- Total Trades: 47
- Avg Win: +4.2%
- Avg Loss: -2.8%

vs Buy & Hold Benchmark:
- S&P 500 Return: +22.1%
- Strategy Alpha: +6.4%
- Volatility: 15.2% vs 18.5% (lower)
- Risk-Adjusted: Superior (higher Sharpe)

Performance by Period:
- Best Month: Mar 2024 (+8.2%)
- Worst Month: Aug 2024 (-5.1%)
- Consecutive Wins: 7 max
- Consecutive Losses: 4 max

Parameter Sensitivity:
- RSI oversold optimal: 30 (current)
- RSI overbought optimal: 70 (current)
- Period optimal: 14 days (current)

Recommendations:
✅ Strategy shows positive alpha
✅ Better risk-adjusted returns than benchmark
✅ Current parameters near optimal
🔴 Consider tighter stops to reduce max drawdown
🔴 Add trend filter to avoid whipsaws in strong trends

Decision: APPROVE for live trading with 25% of capital
```
```

### 5. Order Execution Automation

**Automated Order Management**

Execute and manage orders programmatically:

```markdown
## Order Execution Workflow

**Step 1: Validate Trade Signal**
```python
# Read pending signal
signal = Read(file_path="signals/pending/AAPL_BUY_20251109.json")

# Pre-trade validation
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Pre-trade checklist for {signal}:
    1. Sufficient buying power?
    2. Not exceeding position limits?
    3. No conflicting positions?
    4. Market hours open?
    5. Minimum R/R ratio met?
    Provide: GO or NO-GO
    """
)
```

**Step 2: Execute Order**
```bash
# Place order via broker API
Bash(command="python trading/place_order.py --signal signals/pending/AAPL_BUY_20251109.json")
```

**place_order.py:**
```python
import alpaca_trade_api as tradeapi
import json

# Load signal
with open("signals/pending/AAPL_BUY_20251109.json") as f:
    signal = json.load(f)

# Initialize Alpaca API
api = tradeapi.REST(
    key_id=os.getenv('ALPACA_API_KEY'),
    secret_key=os.getenv('ALPACA_SECRET_KEY'),
    base_url='https://paper-api.alpaca.markets'
)

# Place order
order = api.submit_order(
    symbol=signal['symbol'],
    qty=signal['quantity'],
    side='buy',
    type='limit',
    limit_price=signal['entry_price'],
    time_in_force='day',
    order_class='bracket',  # OCO order with stop & target
    stop_loss={'stop_price': signal['stop_loss']},
    take_profit={'limit_price': signal['take_profit']}
)

print(f"Order placed: {order.id}")
print(f"Status: {order.status}")
```

**Step 3: Monitor Order Status**
```python
# Monitor order fills
# monitor_orders.py
import time

while True:
    # Get pending orders
    orders = api.list_orders(status='open')

    for order in orders:
        # Check status
        updated_order = api.get_order(order.id)

        if updated_order.status == 'filled':
            # Order filled, log trade
            Write(
                file_path=f"logs/filled_orders_{updated_order.symbol}.log",
                content=json.dumps({
                    'symbol': updated_order.symbol,
                    'side': updated_order.side,
                    'qty': updated_order.filled_qty,
                    'price': updated_order.filled_avg_price,
                    'timestamp': updated_order.filled_at
                })
            )

            # Send notification
            Bash(command=f"python notify/send_telegram.py --message 'Order filled: {updated_order.symbol} {updated_order.side} {updated_order.filled_qty} @ {updated_order.filled_avg_price}'")

    time.sleep(30)  # Check every 30 seconds
```

**Output:**
```
✅ Order Executed - AAPL BUY

Order Details:
- Order ID: abc123
- Symbol: AAPL
- Side: BUY
- Quantity: 125 shares
- Order Type: Bracket (limit + stop + target)

Entry:
- Limit Price: $180.50
- Fill Price: $180.48 (saved $2.50!)
- Fill Time: 2025-11-09 14:36:12

Risk Management:
- Stop Loss: $172.50 (-4.4%)
- Take Profit: $186.50 (+3.3%)
- Risk: $1,000
- Reward: $750
- R/R: 0.75:1

Position Summary:
- Position Value: $22,560
- Portfolio %: 22.6%
- Buying Power Remaining: $77,440

Status: FILLED ✅
Notifications: Sent via Telegram
```
```

## References

### SDK Tools for Trading Automation

| Tool | Purpose | Trading Use Cases |
|------|---------|-------------------|
| **WebFetch** | Market data | Price quotes, indicators, news, economic data |
| **Task** | Multi-agent trading | Coordinate technical/fundamental/risk analysis |
| **Bash** | Execute strategies | Run Python/R trading algorithms, backtests |
| **Read** | Read files | Strategy configs, position data, signals |
| **Write** | Write files | Trade logs, performance reports, alerts |

### Trading System Patterns

**Pattern 1: Signal Generation Pipeline**
```
WebFetch (data) → Bash (indicators) → Task (multi-agent) → Write (signal)
```

**Pattern 2: Risk-Managed Execution**
```
Read (signal) → Task (validate) → Bash (position size) → Bash (execute)
```

**Pattern 3: Continuous Monitoring**
```
Loop: Read (positions) → WebFetch (prices) → Check (stops) → Bash (exit if triggered)
```

**Pattern 4: Backtesting Workflow**
```
WebFetch (historical) → Bash (backtest) → Task (analyze) → Write (report)
```

### Best Practices

✅ **Always backtest** - Never trade live without historical validation
✅ **Risk management first** - Define stops before entry
✅ **Position sizing** - Use volatility-based sizing
✅ **Diversification** - Don't put all capital in one trade
✅ **Log everything** - Detailed logs enable improvement
✅ **Paper trade first** - Test in simulated environment
✅ **Monitor performance** - Track and analyze all trades

### Critical Warnings

⚠️ **Trading involves significant risk** - Can lose entire investment
⚠️ **Past performance ≠ future results** - Backtests can overfit
⚠️ **Start small** - Begin with small position sizes
⚠️ **Use stop losses** - Always define maximum loss
⚠️ **Check regulations** - Comply with all trading regulations
⚠️ **Broker API limits** - Respect rate limits, test thoroughly
⚠️ **Market conditions change** - Strategies that worked may stop working

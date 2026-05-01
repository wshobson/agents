# Quantitative Trading

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `quant-analyst` | inherit | Build financial models, backtest trading strategies, and analyze market data. Implements risk metrics, portfolio opti... |
| `risk-manager` | inherit | Monitor portfolio risk, R-multiples, and position limits. Creates hedging strategies, calculates expectancy, and impl... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `backtesting-frameworks` | Build robust backtesting systems for trading strategies with proper handling of look-ahead bias, survivorship bias, and transaction costs... |
| `risk-metrics-calculation` | Calculate portfolio risk metrics including VaR, CVaR, Sharpe, Sortino, and drawdown analysis. Use when measuring portfolio risk, implemen... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Build financial models, backtest trading strategies, and analyze market data" → activates `quant-analyst`
- "Build robust backtesting systems for trading strategies with proper handling of look-ahead bias, survivorship bias, and transaction costs" → activates `backtesting-frameworks` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.

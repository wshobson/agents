"""
TraderNet API Integration Module
Интегрирует анализ портфеля с торговлей через TraderNet API
"""

import requests
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import pandas as pd


@dataclass
class TradeRecommendation:
    """Рекомендация по торговле"""
    ticker: str
    action: str  # SELL, BUY, TRIM, HOLD
    current_price: float
    quantity: int
    reason: str
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    priority: int = 1  # 1=highest, 5=lowest


class TraderNetClient:
    """
    Клиент для работы с TraderNet API
    Поддерживает аутентификацию по API Key + Secret
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.tradernet.global"):
        """
        Инициализация клиента TraderNet

        Args:
            api_key: API Key из TraderNet
            api_secret: API Secret из TraderNet
            base_url: Base URL для API (по умолчанию основной URL)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "X-API-Secret": api_secret,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Выполнить HTTP запрос к API

        Args:
            method: HTTP метод (GET, POST, DELETE)
            endpoint: Endpoint API без base_url
            **kwargs: Дополнительные параметры для requests

        Returns:
            JSON ответ от API
        """
        url = f"{self.base_url}/{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            raise

    def get_portfolio(self) -> Dict:
        """
        Получить текущий портфель

        Returns:
            Информация о портфеле с позициями
        """
        return self._request("GET", "portfolio")

    def get_positions(self) -> List[Dict]:
        """
        Получить список открытых позиций

        Returns:
            Список позиций с текущей информацией
        """
        portfolio = self.get_portfolio()
        return portfolio.get("positions", [])

    def get_quote(self, ticker: str) -> Dict:
        """
        Получить котировку по тикеру

        Args:
            ticker: Тикер акции (например, NVDA.US)

        Returns:
            Информация о цене и изменениях
        """
        return self._request("GET", f"quotes/{ticker}")

    def get_quotes_batch(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Получить котировки для нескольких тикеров

        Args:
            tickers: Список тикеров

        Returns:
            Словарь с котировками по каждому тикеру
        """
        quotes = {}
        for ticker in tickers:
            try:
                quotes[ticker] = self.get_quote(ticker)
            except Exception as e:
                print(f"⚠️ Failed to get quote for {ticker}: {e}")
                quotes[ticker] = None
        return quotes

    def send_order(self, ticker: str, action: str, quantity: int,
                   order_type: str = "market", price: Optional[float] = None,
                   stop_loss: Optional[float] = None,
                   take_profit: Optional[float] = None) -> Dict:
        """
        Отправить ордер на покупку/продажу

        Args:
            ticker: Тикер акции
            action: BUY или SELL
            quantity: Количество акций
            order_type: Тип ордера (market, limit)
            price: Цена для лимитного ордера
            stop_loss: Цена стоп-лосса
            take_profit: Цена тейк-профита

        Returns:
            Информация об ордере
        """
        payload = {
            "ticker": ticker,
            "action": action.upper(),
            "quantity": quantity,
            "order_type": order_type.lower(),
        }

        if order_type.lower() == "limit" and price:
            payload["price"] = price

        if stop_loss:
            payload["stop_loss"] = stop_loss

        if take_profit:
            payload["take_profit"] = take_profit

        return self._request("POST", "orders/send", json=payload)

    def cancel_order(self, order_id: str) -> Dict:
        """
        Отменить ордер

        Args:
            order_id: ID ордера

        Returns:
            Подтверждение отмены
        """
        return self._request("DELETE", f"orders/{order_id}")

    def get_orders(self, status: Optional[str] = None) -> List[Dict]:
        """
        Получить историю ордеров

        Args:
            status: Статус (open, closed, cancelled)

        Returns:
            Список ордеров
        """
        endpoint = "orders"
        if status:
            endpoint += f"?status={status}"
        return self._request("GET", endpoint).get("orders", [])


class PortfolioAnalyzer:
    """
    Анализ портфеля и генерация рекомендаций
    """

    def __init__(self, tradernet_client: TraderNetClient):
        self.client = tradernet_client

    def analyze_current_portfolio(self) -> Tuple[pd.DataFrame, Dict]:
        """
        Анализ текущего портфеля

        Returns:
            (DataFrame с позициями, Словарь со статистикой)
        """
        positions = self.client.get_positions()

        # Получить котировки для всех позиций
        tickers = [p["ticker"] for p in positions]
        quotes = self.client.get_quotes_batch(tickers)

        # Построить DataFrame
        data = []
        total_value = 0
        total_profit = 0

        for pos in positions:
            ticker = pos["ticker"]
            quote = quotes.get(ticker, {})

            quantity = pos.get("quantity", 0)
            current_price = quote.get("price", pos.get("current_price", 0))
            entry_price = pos.get("entry_price", 0)
            current_value = quantity * current_price
            entry_value = quantity * entry_price
            profit = current_value - entry_value
            profit_pct = (profit / entry_value * 100) if entry_value > 0 else 0

            data.append({
                "ticker": ticker,
                "quantity": quantity,
                "entry_price": entry_price,
                "current_price": current_price,
                "entry_value": entry_value,
                "current_value": current_value,
                "profit": profit,
                "profit_pct": profit_pct
            })

            total_value += current_value
            total_profit += profit

        df = pd.DataFrame(data)
        df["allocation_pct"] = (df["current_value"] / total_value * 100) if total_value > 0 else 0

        stats = {
            "total_value": total_value,
            "total_profit": total_profit,
            "total_profit_pct": (total_profit / (total_value - total_profit) * 100) if (total_value - total_profit) > 0 else 0,
            "positions_count": len(df),
            "avg_profit_pct": df["profit_pct"].mean() if len(df) > 0 else 0
        }

        return df, stats

    def generate_recommendations(self, df: pd.DataFrame) -> List[TradeRecommendation]:
        """
        Генерировать рекомендации на основе анализа портфеля

        Args:
            df: DataFrame с позициями

        Returns:
            Список рекомендаций
        """
        recommendations = []

        # Сортировать по размеру позиции и прибыльности
        df_sorted = df.sort_values("current_value", ascending=False)

        for idx, row in df_sorted.iterrows():
            ticker = row["ticker"]
            current_value = row["current_value"]
            allocation_pct = row["allocation_pct"]
            profit_pct = row["profit_pct"]
            quantity = int(row["quantity"])
            current_price = row["current_price"]

            # Правила для рекомендаций

            # 1. NVDA концентрация - триммировать
            if ticker == "NVDA.US" and allocation_pct > 25:
                trim_qty = int(quantity * 0.4)  # Продать 40% позиции
                recommendations.append(TradeRecommendation(
                    ticker=ticker,
                    action="TRIM",
                    current_price=current_price,
                    quantity=trim_qty,
                    reason=f"Концентрация {allocation_pct:.1f}% портфеля - критично выше норм 5-10%",
                    target_price=None,
                    stop_loss=None,
                    priority=1
                ))

            # 2. Убыточные позиции - закрыть
            if profit_pct < -15 and current_value < 1000:
                recommendations.append(TradeRecommendation(
                    ticker=ticker,
                    action="SELL",
                    current_price=current_price,
                    quantity=quantity,
                    reason=f"Убыточная позиция ({profit_pct:.1f}%) - loss harvesting для налогов",
                    target_price=None,
                    stop_loss=None,
                    priority=1
                ))

            # 3. Позиции с большой прибылью - частично закрыть
            if profit_pct > 150 and allocation_pct > 1:
                trim_qty = int(quantity * 0.5)  # Продать половину
                recommendations.append(TradeRecommendation(
                    ticker=ticker,
                    action="TRIM",
                    current_price=current_price,
                    quantity=trim_qty,
                    reason=f"Экстраординарная прибыль {profit_pct:.1f}% - закрепить прибыль",
                    target_price=None,
                    stop_loss=None,
                    priority=2
                ))

            # 4. PLTR высокая позиция - триммировать
            if ticker == "PLTR.US" and allocation_pct > 8:
                trim_qty = int(quantity * 0.25)
                recommendations.append(TradeRecommendation(
                    ticker=ticker,
                    action="TRIM",
                    current_price=current_price,
                    quantity=trim_qty,
                    reason=f"Позиция {allocation_pct:.1f}% - выше целевого 5%",
                    target_price=None,
                    stop_loss=None,
                    priority=2
                ))

        # Рекомендации по покупкам защитных инструментов
        # (Это должны быть реальные тикеры, доступные в вашем брокере)
        recommendations.extend([
            TradeRecommendation(
                ticker="BND.US",  # Vanguard Total Bond ETF
                action="BUY",
                current_price=0,  # Будет получена через API
                quantity=int(10000 / 80),  # ~$10,000
                reason="Добавить облигации (15% портфеля) для защиты",
                target_price=None,
                stop_loss=None,
                priority=3
            ),
            TradeRecommendation(
                ticker="GLD.US",  # Gold ETF
                action="BUY",
                current_price=0,
                quantity=int(5000 / 170),  # ~$5,000
                reason="Добавить золото (5% портфеля) как хеджирование",
                target_price=None,
                stop_loss=None,
                priority=3
            ),
        ])

        # Сортировать по приоритету
        return sorted(recommendations, key=lambda x: x.priority)


class TradingAutomation:
    """
    Автоматизация выполнения торговых операций
    """

    def __init__(self, tradernet_client: TraderNetClient, analyzer: PortfolioAnalyzer):
        self.client = tradernet_client
        self.analyzer = analyzer
        self.trade_log = []

    def execute_recommendation(self, rec: TradeRecommendation,
                              dry_run: bool = True) -> Dict:
        """
        Выполнить торговую рекомендацию

        Args:
            rec: Рекомендация
            dry_run: Если True, только показать, не выполнять

        Returns:
            Результат выполнения
        """
        result = {
            "ticker": rec.ticker,
            "action": rec.action,
            "quantity": rec.quantity,
            "executed": False,
            "order_id": None,
            "message": ""
        }

        if dry_run:
            result["message"] = f"[DRY RUN] {rec.action} {rec.quantity} {rec.ticker} @ {rec.current_price}"
            print(f"✓ {result['message']}")
            print(f"  Причина: {rec.reason}")
            return result

        try:
            # Определить тип ордера
            if rec.action in ["SELL", "TRIM"]:
                action = "SELL"
            else:
                action = "BUY"

            # Отправить ордер
            order_result = self.client.send_order(
                ticker=rec.ticker,
                action=action,
                quantity=rec.quantity,
                order_type="market",
                stop_loss=rec.stop_loss,
                take_profit=rec.take_profit
            )

            result["executed"] = True
            result["order_id"] = order_result.get("order_id")
            result["message"] = f"✓ Order executed: {action} {rec.quantity} {rec.ticker}"

            self.trade_log.append({
                "timestamp": datetime.now().isoformat(),
                "ticker": rec.ticker,
                "action": action,
                "quantity": rec.quantity,
                "reason": rec.reason,
                "order_id": result["order_id"]
            })

        except Exception as e:
            result["message"] = f"✗ Failed to execute: {str(e)}"

        print(result["message"])
        return result

    def execute_recommendations(self, recommendations: List[TradeRecommendation],
                                dry_run: bool = True,
                                max_priority: int = 2) -> List[Dict]:
        """
        Выполнить список рекомендаций по приоритету

        Args:
            recommendations: Список рекомендаций
            dry_run: Если True, только показать
            max_priority: Максимальный приоритет для выполнения (1=все, 2=только критические)

        Returns:
            Список результатов выполнения
        """
        results = []

        print("\n" + "="*80)
        print("ВЫПОЛНЕНИЕ ТОРГОВЫХ РЕКОМЕНДАЦИЙ")
        print("="*80)
        print(f"Режим: {'DRY RUN (тестирование)' if dry_run else 'LIVE TRADING'}")
        print(f"Максимальный приоритет: {max_priority}")
        print("="*80 + "\n")

        for rec in recommendations:
            if rec.priority <= max_priority:
                print(f"[Priority {rec.priority}] {rec.action} {rec.quantity} {rec.ticker}")
                print(f"Цена: ${rec.current_price:.2f} | Причина: {rec.reason}\n")

                result = self.execute_recommendation(rec, dry_run=dry_run)
                results.append(result)

        return results


# ============================================================================
# УТИЛИТЫ
# ============================================================================

def load_credentials_from_env() -> Tuple[str, str]:
    """
    Загрузить credentials из переменных окружения

    Returns:
        (api_key, api_secret)
    """
    api_key = os.getenv("TRADERNET_API_KEY")
    api_secret = os.getenv("TRADERNET_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError(
            "Установите переменные окружения TRADERNET_API_KEY и TRADERNET_API_SECRET"
        )

    return api_key, api_secret


def save_trading_log(automation: TradingAutomation, filepath: str):
    """
    Сохранить лог торговых операций

    Args:
        automation: Объект TradingAutomation
        filepath: Путь для сохранения JSON файла
    """
    with open(filepath, 'w') as f:
        json.dump(automation.trade_log, f, indent=2)
    print(f"✓ Trading log saved to {filepath}")


def print_portfolio_summary(df: pd.DataFrame, stats: Dict):
    """
    Вывести резюме портфеля
    """
    print("\n" + "="*80)
    print("АНАЛИЗ ПОРТФЕЛЯ")
    print("="*80)
    print(f"Общая стоимость: ${stats['total_value']:,.2f}")
    print(f"Совокупная прибыль: ${stats['total_profit']:,.2f} ({stats['total_profit_pct']:.2f}%)")
    print(f"Позиций: {stats['positions_count']}")
    print("="*80 + "\n")

    # Top 5 позиций
    print("TOP 5 ПОЗИЦИЙ:")
    print("-" * 80)

    top5 = df.nlargest(5, "current_value")[
        ["ticker", "quantity", "current_price", "current_value", "allocation_pct", "profit_pct"]
    ]

    for idx, row in top5.iterrows():
        print(f"{row['ticker']:12} | Qty: {row['quantity']:>6.0f} | "
              f"Price: ${row['current_price']:>8.2f} | "
              f"Value: ${row['current_value']:>12,.2f} | "
              f"Alloc: {row['allocation_pct']:>5.1f}% | "
              f"P&L: {row['profit_pct']:>7.2f}%")

    print("\n")


if __name__ == "__main__":
    print("TraderNet Integration Module loaded successfully")
    print("Используйте этот модуль для интеграции анализа портфеля с торговлей")

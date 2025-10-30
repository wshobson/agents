#!/usr/bin/env python3
"""
Простой скрипт для получения информации о портфеле из TraderNet API
БЕЗ каких-либо операций на бирже

Использование:
    python3 get_portfolio.py
    python3 get_portfolio.py --json
    python3 get_portfolio.py --csv portfolio.csv
"""

import sys
import json
import csv
import argparse
from datetime import datetime
from pathlib import Path

from tradernet_integration import TraderNetClient, load_credentials_from_env


def print_portfolio_pretty(df, stats):
    """Красивый вывод информации о портфеле"""
    print("\n" + "="*100)
    print("📊 ИНФОРМАЦИЯ О ПОРТФЕЛЕ")
    print("="*100)
    print(f"Дата/Время:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Общая стоимость: ${stats['total_value']:,.2f}")
    print(f"Совокупная прибыль: ${stats['total_profit']:,.2f} ({stats['total_profit_pct']:+.2f}%)")
    print(f"Позиций:        {stats['positions_count']}")
    print("="*100 + "\n")

    # Таблица позиций
    print("ПОЗИЦИИ:")
    print("-" * 100)
    print(f"{'Тикер':<12} {'Кол-во':>10} {'Цена':>10} {'Стоимость':>15} {'Доля':>8} {'Вход':>10} {'Прибыль':>12} {'%':>8}")
    print("-" * 100)

    for idx, row in df.iterrows():
        ticker = row['ticker']
        quantity = int(row['quantity'])
        current_price = row['current_price']
        current_value = row['current_value']
        allocation_pct = row['allocation_pct']
        entry_price = row['entry_price']
        profit = row['profit']
        profit_pct = row['profit_pct']

        # Цветовое обозначение прибыли (в консоли)
        profit_sign = "+" if profit >= 0 else ""

        print(f"{ticker:<12} {quantity:>10.0f} ${current_price:>9.2f} ${current_value:>14,.0f} {allocation_pct:>7.1f}% ${entry_price:>9.2f} {profit_sign}${profit:>10,.0f} {profit_pct:>+7.2f}%")

    print("-" * 100 + "\n")

    # Статистика по секторам/группам
    print("РАСПРЕДЕЛЕНИЕ ПО РАЗМЕРУ ПОЗИЦИЙ:")
    print("-" * 100)

    for idx, row in df.nlargest(10, 'current_value').iterrows():
        ticker = row['ticker']
        allocation_pct = row['allocation_pct']
        bar_length = int(allocation_pct / 2)  # Каждый % = 0.5 символа
        bar = "█" * bar_length

        print(f"{ticker:<12} {allocation_pct:>6.2f}% {bar}")

    print("="*100 + "\n")


def print_portfolio_json(df, stats):
    """Вывод в JSON формате"""
    output = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_value": float(stats['total_value']),
            "total_profit": float(stats['total_profit']),
            "total_profit_pct": float(stats['total_profit_pct']),
            "positions_count": stats['positions_count']
        },
        "positions": []
    }

    for idx, row in df.iterrows():
        output["positions"].append({
            "ticker": row['ticker'],
            "quantity": int(row['quantity']),
            "entry_price": float(row['entry_price']),
            "current_price": float(row['current_price']),
            "entry_value": float(row['entry_value']),
            "current_value": float(row['current_value']),
            "allocation_pct": float(row['allocation_pct']),
            "profit": float(row['profit']),
            "profit_pct": float(row['profit_pct'])
        })

    print(json.dumps(output, indent=2, ensure_ascii=False))


def save_portfolio_csv(df, filepath):
    """Сохранить портфель в CSV файл"""
    df.to_csv(filepath, index=False)
    print(f"✓ Портфель сохранен в {filepath}")


def main():
    """Главная функция"""

    parser = argparse.ArgumentParser(
        description="Получить информацию о портфеле из TraderNet API (БЕЗ операций на бирже)"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывести результат в JSON формате"
    )

    parser.add_argument(
        "--csv",
        type=str,
        help="Сохранить результат в CSV файл"
    )

    args = parser.parse_args()

    print("\n" + "="*100)
    print("🔗 TraderNet Portfolio Viewer (READ-ONLY)")
    print("="*100 + "\n")

    try:
        # Загрузить credentials
        print("🔑 Загружаю credentials...")
        api_key, api_secret = load_credentials_from_env()
        print("✓ Credentials загружены\n")

        # Подключиться к API
        print("🔗 Подключаюсь к TraderNet API...")
        client = TraderNetClient(api_key, api_secret)
        print("✓ Подключение установлено\n")

        # Получить портфель
        print("📊 Загружаю портфель...")

        positions = client.get_positions()
        print(f"✓ Получено {len(positions)} позиций\n")

        # Если позиций нет
        if not positions:
            print("⚠️  Портфель пуст или нет открытых позиций\n")
            return

        # Получить котировки
        print("💹 Загружаю текущие котировки...")
        tickers = [p["ticker"] for p in positions]
        quotes = client.get_quotes_batch(tickers)
        print(f"✓ Котировки загружены\n")

        # Построить DataFrame с анализом
        import pandas as pd
        data = []
        total_value = 0
        total_profit = 0

        for pos in positions:
            ticker = pos["ticker"]
            quote = quotes.get(ticker, {})

            quantity = pos.get("quantity", 0)
            current_price = quote.get("price", pos.get("current_price", 0)) if quote else pos.get("current_price", 0)
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
        df = df.sort_values("current_value", ascending=False)

        stats = {
            "total_value": total_value,
            "total_profit": total_profit,
            "total_profit_pct": (total_profit / (total_value - total_profit) * 100) if (total_value - total_profit) > 0 else 0,
            "positions_count": len(df),
            "avg_profit_pct": df["profit_pct"].mean() if len(df) > 0 else 0
        }

        # Вывести результаты
        if args.json:
            print_portfolio_json(df, stats)
        else:
            print_portfolio_pretty(df, stats)

        # Сохранить в CSV если нужно
        if args.csv:
            save_portfolio_csv(df, args.csv)

        # Финальный статус
        print("✓ ДАННЫЕ УСПЕШНО ЗАГРУЖЕНЫ (без операций на бирже)")
        print("="*100 + "\n")

    except KeyError as e:
        print(f"\n❌ Ошибка: Не установлены переменные окружения")
        print(f"Установите переменные:")
        print(f"  export TRADERNET_API_KEY='ваш_api_key'")
        print(f"  export TRADERNET_API_SECRET='ваш_api_secret'")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

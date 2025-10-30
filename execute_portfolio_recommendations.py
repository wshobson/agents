#!/usr/bin/env python3
"""
Скрипт для выполнения рекомендаций по портфелю через TraderNet API

Использование:
    # DRY RUN (тестирование, ничего не выполняется)
    python3 execute_portfolio_recommendations.py --dry-run

    # LIVE TRADING (реальное выполнение ордеров)
    python3 execute_portfolio_recommendations.py --execute --priority 2

Требуется:
    - Установить переменные окружения:
      export TRADERNET_API_KEY="your_api_key"
      export TRADERNET_API_SECRET="your_api_secret"
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Импортировать модуль интеграции
from tradernet_integration import (
    TraderNetClient,
    PortfolioAnalyzer,
    TradingAutomation,
    load_credentials_from_env,
    print_portfolio_summary,
    save_trading_log
)


def main():
    """Главная функция"""

    parser = argparse.ArgumentParser(
        description="Выполнить рекомендации по портфелю через TraderNet API"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Только показать рекомендации, ничего не выполнять (по умолчанию)"
    )

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Реально выполнить торговые операции (ОСТОРОЖНО!)"
    )

    parser.add_argument(
        "--priority",
        type=int,
        default=1,
        choices=[1, 2, 3, 4, 5],
        help="Максимальный приоритет рекомендаций для выполнения (1=все, 5=только критические)"
    )

    parser.add_argument(
        "--log",
        type=str,
        default="trading_log.json",
        help="Файл для сохранения лога операций"
    )

    args = parser.parse_args()

    # Определить режим
    dry_run = not args.execute
    if args.dry_run:
        dry_run = True

    print("\n" + "="*80)
    print("TRADERNET PORTFOLIO AUTOMATION")
    print("="*80)
    print(f"Режим: {'DRY RUN' if dry_run else 'LIVE TRADING'}")
    print(f"Приоритет: {args.priority}")
    print("="*80 + "\n")

    try:
        # Загрузить credentials
        print("🔑 Загружаю credentials из переменных окружения...")
        api_key, api_secret = load_credentials_from_env()
        print("✓ Credentials загружены\n")

        # Инициализировать клиент
        print("🔗 Подключаюсь к TraderNet API...")
        client = TraderNetClient(api_key, api_secret)
        print("✓ Подключение установлено\n")

        # Анализ портфеля
        print("📊 Анализирую текущий портфель...")
        analyzer = PortfolioAnalyzer(client)
        df, stats = analyzer.analyze_current_portfolio()
        print("✓ Анализ завершен\n")

        # Показать резюме
        print_portfolio_summary(df, stats)

        # Генерировать рекомендации
        print("💡 Генерирую торговые рекомендации...")
        recommendations = analyzer.generate_recommendations(df)

        print(f"✓ Сгенерировано {len(recommendations)} рекомендаций\n")

        # Показать рекомендации по приоритету
        print("="*80)
        print("ТОРГОВЫЕ РЕКОМЕНДАЦИИ")
        print("="*80)

        for i, rec in enumerate(recommendations, 1):
            print(f"\n[{i}] {rec.action} {rec.quantity} {rec.ticker}")
            print(f"    Цена: ${rec.current_price:.2f}")
            print(f"    Приоритет: {rec.priority}")
            print(f"    Причина: {rec.reason}")

            if rec.stop_loss:
                print(f"    Stop Loss: ${rec.stop_loss:.2f}")
            if rec.take_profit:
                print(f"    Take Profit: ${rec.take_profit:.2f}")

        # Выполнить рекомендации
        print("\n" + "="*80)
        automation = TradingAutomation(client, analyzer)
        results = automation.execute_recommendations(
            recommendations,
            dry_run=dry_run,
            max_priority=args.priority
        )

        # Сохранить лог
        if automation.trade_log:
            save_trading_log(automation, args.log)

        # Итоги
        print("\n" + "="*80)
        print("ИТОГИ")
        print("="*80)
        executed = sum(1 for r in results if r.get("executed"))
        print(f"Рекомендаций обработано: {len(results)}")
        print(f"Ордеров выполнено: {executed}")

        if dry_run:
            print("\n⚠️  ЭТО БЫЛ DRY RUN - РЕАЛЬНЫХ ОПЕРАЦИЙ НЕ ВЫПОЛНЕНО")
            print("\nДля реального выполнения используйте:")
            print("  python3 execute_portfolio_recommendations.py --execute --priority 2")
        else:
            print("\n✓ ЖИВАЯ ТОРГОВЛЯ ВЫПОЛНЕНА")

        print("="*80 + "\n")

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

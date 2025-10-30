# TraderNet API Integration Guide

Полное руководство по интеграции анализа портфеля с торговлей через TraderNet API

## Содержание
1. [Установка и Конфигурация](#установка-и-конфигурация)
2. [Получение API Credentials](#получение-api-credentials)
3. [Использование](#использование)
4. [Примеры](#примеры)
5. [Troubleshooting](#troubleshooting)

---

## Установка и Конфигурация

### 1. Установить зависимости

```bash
pip install requests pandas openpyxl
```

### 2. Получить API Credentials

#### Шаг 1: Войти в TraderNet

1. Перейти на https://tradernet.global
2. Войти в свой аккаунт

#### Шаг 2: Получить API Key и Secret

1. Перейти в **Settings** → **API**
2. Создать новый API Key:
   - Нажать **Create New API Key**
   - Дать имя: "Portfolio Automation"
   - Выбрать permissions:
     - ✅ Read Portfolio
     - ✅ Read Orders
     - ✅ Create Orders
     - ✅ Cancel Orders
     - ✅ Get Quotes
   - Нажать **Generate**

3. **СОХРАНИТЬ** значения:
   - **API Key**: начинается с `tr_` (например: `tr_abc123xyz...`)
   - **API Secret**: длинная строка (например: `secret_abc123xyz...`)

⚠️ **ВАЖНО:** Secret будет показан только один раз! Сохраните его в безопасном месте!

### 3. Установить переменные окружения

#### Вариант A: Временно для текущей сессии

```bash
export TRADERNET_API_KEY="tr_ваш_api_key"
export TRADERNET_API_SECRET="ваш_api_secret"
```

#### Вариант B: Постоянно в ~/.bashrc или ~/.zshrc

```bash
# Добавить в конец файла ~/.bashrc или ~/.zshrc
export TRADERNET_API_KEY="tr_ваш_api_key"
export TRADERNET_API_SECRET="ваш_api_secret"
```

Затем перезагрузить shell:
```bash
source ~/.bashrc  # или source ~/.zshrc
```

#### Вариант C: Через .env файл (рекомендуется)

1. Создать файл `.env` в каталоге проекта:

```bash
# .env
TRADERNET_API_KEY=tr_ваш_api_key
TRADERNET_API_SECRET=ваш_api_secret
```

2. Установить python-dotenv:

```bash
pip install python-dotenv
```

3. В начало скрипта добавить:

```python
from dotenv import load_dotenv
load_dotenv()
```

⚠️ **ВАЖНО:** Добавить `.env` в `.gitignore` чтобы не закоммитить secrets!

```bash
echo ".env" >> .gitignore
```

---

## Использование

### Синтаксис

```bash
python3 execute_portfolio_recommendations.py [OPTIONS]
```

### Опции

| Опция | Описание | Примечание |
|-------|---------|-----------|
| `--dry-run` | Только показать рекомендации (по умолчанию) | Безопасно для тестирования |
| `--execute` | Реально выполнить ордеры | ⚠️ Реальная торговля! |
| `--priority N` | Максимальный приоритет (1-5) | 1=все, 2=критические |
| `--log FILE` | Файл для лога операций | По умолчанию: `trading_log.json` |

### Режимы использования

#### 1. DRY RUN (тестирование)

```bash
# Показать все рекомендации (ничего не выполнится)
python3 execute_portfolio_recommendations.py --dry-run

# Показать только приоритет 1-2 (критические)
python3 execute_portfolio_recommendations.py --dry-run --priority 2
```

**Результат:** Увидите список операций, которые будут выполнены, но реально они не будут отправлены.

#### 2. LIVE TRADING (реальное выполнение)

```bash
# Выполнить только критические операции (приоритет 1-2)
python3 execute_portfolio_recommendations.py --execute --priority 2

# Выполнить все рекомендации
python3 execute_portfolio_recommendations.py --execute --priority 5
```

**ОСТОРОЖНО:** Эти команды реально выполнят ордеры на вашем счете!

---

## Примеры

### Пример 1: Первое тестирование

```bash
# Шаг 1: Проверить что credentials работают
python3 execute_portfolio_recommendations.py --dry-run

# Вывод должен быть:
# ✓ Credentials загружены
# ✓ Подключение установлено
# ✓ Анализ завершен
# ...список рекомендаций...
```

### Пример 2: Выполнение только критических операций

```bash
# Сначала тестируем
python3 execute_portfolio_recommendations.py --dry-run --priority 2

# Если выглядит хорошо - выполняем
python3 execute_portfolio_recommendations.py --execute --priority 2 --log critical_trades_2024.json
```

Это выполнит:
- Триммирование NVDA (слишком большая позиция)
- Закрытие убыточных позиций (tax loss harvesting)
- Триммирование PLTR

### Пример 3: Полная оптимизация с нескольких дней

```bash
# День 1: Выполнить критические операции
python3 execute_portfolio_recommendations.py --execute --priority 2 --log day1_trades.json

# День 2: Выполнить добавления облигаций и золота
python3 execute_portfolio_recommendations.py --execute --priority 3 --log day2_trades.json

# День 3: Выполнить прибыльные позиции
python3 execute_portfolio_recommendations.py --execute --priority 4 --log day3_trades.json
```

---

## Структура рекомендаций

Каждая рекомендация имеет приоритет:

| Приоритет | Тип | Описание |
|-----------|-----|---------|
| **1** | Критические | Немедленно: триммирование NVDA, закрытие убытков |
| **2** | Высокие | День 1-2: триммирование PLTR, закрытие экстремальных прибылей |
| **3** | Средние | День 3-5: добавление облигаций и золота |
| **4** | Низкие | День 5-7: прибыль-фиксация в других позициях |
| **5** | Опциональные | Неделя 2: мелкие оптимизации |

---

## Мониторинг и Логирование

### Просмотр логов операций

```bash
# Просмотр последних операций
cat trading_log.json | python3 -m json.tool

# Или красивый вывод
python3 << 'EOF'
import json
with open('trading_log.json') as f:
    trades = json.load(f)
    for trade in trades:
        print(f"{trade['timestamp']} - {trade['action']} {trade['quantity']} {trade['ticker']}")
        print(f"  Причина: {trade['reason']}")
EOF
```

### Проверка статуса ордеров

```python
from tradernet_integration import TraderNetClient, load_credentials_from_env

api_key, api_secret = load_credentials_from_env()
client = TraderNetClient(api_key, api_secret)

# Получить открытые ордеры
open_orders = client.get_orders(status="open")
for order in open_orders:
    print(f"{order['ticker']}: {order['quantity']} @ {order['price']}")

# Получить закрытые ордеры
closed_orders = client.get_orders(status="closed")
print(f"Всего закрытых ордеров: {len(closed_orders)}")
```

---

## Schedule Автоматизации (опционально)

Можете запускать рекомендации автоматически по расписанию:

### Использование cron (Linux/Mac)

```bash
# Редактировать crontab
crontab -e

# Добавить строку для запуска каждый понедельник в 9 AM
0 9 * * 1 /usr/bin/python3 /path/to/execute_portfolio_recommendations.py --execute --priority 2

# Или каждый день в 4 PM
0 16 * * * /usr/bin/python3 /path/to/execute_portfolio_recommendations.py --dry-run --priority 2 --log daily_check.json
```

### Использование Python scheduler

```python
import schedule
import time
from execute_portfolio_recommendations import main

# Запускать каждый понедельник в 9 AM
schedule.every().monday.at("09:00").do(lambda: main(['--execute', '--priority', '2']))

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Troubleshooting

### Проблема: "API Key not found"

```
❌ Ошибка: Не установлены переменные окружения
```

**Решение:**
```bash
# Проверить что переменные установлены
echo $TRADERNET_API_KEY
echo $TRADERNET_API_SECRET

# Если пусто, установить их
export TRADERNET_API_KEY="tr_abc123..."
export TRADERNET_API_SECRET="secret_xyz..."
```

### Проблема: "Authentication failed"

Ошибка может быть если:

1. ❌ Неправильно скопирован API Key или Secret
2. ❌ API Key был отозван в настройках TraderNet
3. ❌ Истек срок действия API Key

**Решение:**
- Перейти в TraderNet Settings → API
- Создать новый API Key
- Обновить переменные окружения

### Проблема: "Order failed - invalid ticker"

```
❌ API Error: Invalid ticker format
```

**Решение:** Проверить формат тикеров:
- US тикеры должны быть: `NVDA.US` (не просто `NVDA`)
- Формат: `SYMBOL.US` для американских акций

### Проблема: "Insufficient funds"

```
❌ API Error: Insufficient funds for order
```

**Решение:** На счете недостаточно средств для покупки. Проверить:
```python
client = TraderNetClient(api_key, api_secret)
portfolio = client.get_portfolio()
print(f"Cash available: ${portfolio['cash']}")
```

### Проблема: "Order partially filled"

Это нормально - большой ордер может быть исполнен частями. Проверить статус:

```bash
python3 << 'EOF'
from tradernet_integration import TraderNetClient, load_credentials_from_env
client = TraderNetClient(*load_credentials_from_env())
orders = client.get_orders(status="closed")
for order in orders[-5:]:
    print(f"{order['ticker']}: {order['quantity']} @ {order['price']} ({order['status']})")
EOF
```

---

## Security Best Practices

1. **Никогда** не коммитить `.env` файл с credentials
2. **Никогда** не делиться своим API Key или Secret
3. **Ограничить** permissions на API Key (читайте только что нужно)
4. **Регулярно** проверять логи операций
5. **Использовать** разные API Keys для разных целей (automation, monitoring, etc)
6. **Отозвать** неиспользуемые API Keys

---

## Дополнительная информация

- 📚 [TraderNet API Documentation](https://tradernet.global/tradernet-api)
- 🐍 [Python TraderNet SDK](https://tradernet.global/tradernet-api/python-sdk)
- 💡 [Portfolio Optimization Guide](https://docs.tradernet.global/portfolio-optimization)

---

## Поддержка

Если возникают вопросы или проблемы:

1. Проверить эту документацию
2. Проверить логи ошибок в консоли
3. Посетить [TraderNet Help Center](https://help.tradernet.global)
4. Создать issue в репозитории

---

**Дата обновления:** 2024-10-29
**Версия:** 1.0.0

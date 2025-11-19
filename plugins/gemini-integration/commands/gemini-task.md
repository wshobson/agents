---
name: gemini-task
description: Выполнить задачу через Gemini CLI с автоматической подготовкой промпта, вызовом, обработкой результата и интеграцией в проект. Поддерживает различные режимы работы - исследование, генерация, review и др.
---

# Gemini Task Command

## Назначение

Команда для удобного выполнения задач через Gemini CLI с автоматической обработкой результатов и интеграцией в проект.

## Использование

```bash
# Из Claude Code
/gemini-task <режим> <описание задачи>

# Примеры
/gemini-task research "best approaches for API rate limiting"
/gemini-task generate "test cases for email validation"
/gemini-task review "this database schema optimization"
/gemini-task design "shopping cart API with 3 different approaches"
```

## Режимы работы

### 1. Research Mode

**Цель:** Исследовать тему, сравнить подходы, найти best practices

**Команда:**
```
/gemini-task research "your research question"
```

**Что делает:**
1. Формирует структурированный промпт для исследования
2. Вызывает Gemini CLI
3. Форматирует результат в markdown
4. Сохраняет в файл (опционально)
5. Представляет краткое резюме пользователю

**Пример:**
```
Пользователь: /gemini-task research "state management libraries for React 2024"

Claude Code:
1. Формирует промпт:
   "Research: Top state management libraries for React in 2024

   Analyze and compare:
   - Redux Toolkit
   - Zustand
   - Jotai
   - Recoil
   - MobX

   For each provide:
   - Key features
   - Pros and cons
   - Use cases
   - Popularity and community
   - Learning curve (1-10)

   Format: Markdown with ## Library Name headers"

2. Вызывает: gemini-cli "$PROMPT"

3. Сохраняет результат в .gemini-research/state-management-react-2024.md

4. Показывает резюме пользователю:
   "✓ Research completed. Key findings:
   - Redux Toolkit: Best for complex apps, steep learning curve
   - Zustand: Lightweight, easy to learn, growing popularity
   - Jotai: Atomic state, great for granular updates
   ...
   Full report: .gemini-research/state-management-react-2024.md"
```

### 2. Generate Mode

**Цель:** Генерировать код, тесты, документацию, данные

**Команда:**
```
/gemini-task generate "what to generate" [--context file.js]
```

**Что делает:**
1. Формирует промпт с четким описанием что генерировать
2. Добавляет контекст из файлов (если указано --context)
3. Вызывает Gemini CLI
4. Парсит результат (извлекает код из markdown блоков)
5. Валидирует сгенерированный код
6. Интегрирует в проект (создает файл или предлагает пользователю)

**Пример:**
```
Пользователь: /gemini-task generate "TypeScript interfaces for User API" --context api/users.js

Claude Code:
1. Читает api/users.js для контекста

2. Формирует промпт:
   "Based on this Express API:
   [содержимое api/users.js]

   Generate TypeScript interfaces for:
   - Request bodies
   - Response types
   - Database models

   Include:
   - Strict typing
   - JSDoc comments
   - Utility types for optional fields

   Return only TypeScript code, no explanation"

3. Вызывает Gemini

4. Парсит результат, извлекает код

5. Валидирует:
   - Сохраняет в temp файл
   - Запускает: tsc --noEmit temp.ts
   - Если ошибки → фиксит

6. Создает types/user-api.ts

7. Сообщает:
   "✓ Generated TypeScript interfaces → types/user-api.ts
   Validated with TypeScript compiler ✓
   Ready to use!"
```

### 3. Review Mode

**Цель:** Получить review кода, архитектуры, дизайна

**Команда:**
```
/gemini-task review "what to review" [--file path/to/file]
```

**Что делает:**
1. Читает файл(ы) для review
2. Формирует промпт с критериями review
3. Вызывает Gemini CLI
4. Форматирует результат с priority tags
5. Представляет actionable items пользователю

**Пример:**
```
Пользователь: /gemini-task review "this database query optimization" --file db/queries/analytics.sql

Claude Code:
1. Читает db/queries/analytics.sql

2. Формирует промпт:
   "Review this database query optimization:

   [SQL code]

   Analyze for:
   1. Index usage and optimization
   2. Query complexity and performance
   3. Edge cases not handled
   4. N+1 query risks
   5. Scalability concerns

   For each issue found:
   - Severity: CRITICAL / MAJOR / MINOR
   - Description
   - Suggested fix

   Format: Markdown with severity tags"

3. Вызывает Gemini

4. Парсит результат, группирует по severity

5. Показывает:
   "✓ Review completed for db/queries/analytics.sql

   CRITICAL (2):
   - Missing index on user_id column → add: CREATE INDEX idx_user_id
   - SQL injection vulnerability → use parameterized queries

   MAJOR (3):
   - Suboptimal JOIN order → reorder based on table sizes
   ...

   Full report: .gemini-reviews/analytics-query-2024-11-18.md"
```

### 4. Design Mode

**Цель:** Получить несколько вариантов дизайна/архитектуры

**Команда:**
```
/gemini-task design "what to design" [--variants N]
```

**Что делает:**
1. Формирует промпт для генерации N вариантов дизайна
2. Вызывает Gemini CLI
3. Парсит варианты
4. Представляет сравнительную таблицу
5. Помогает пользователю выбрать вариант
6. Имплементирует выбранный дизайн

**Пример:**
```
Пользователь: /gemini-task design "caching layer for REST API" --variants 3

Claude Code:
1. Формирует промпт:
   "Design 3 different approaches for caching layer in REST API:

   Variant 1: In-memory cache (Node.js)
   Variant 2: Redis-based distributed cache
   Variant 3: Hybrid (in-memory + Redis)

   For each:
   - Architecture diagram (ASCII)
   - Implementation approach
   - Pros and cons
   - Complexity (1-10)
   - Scalability (1-10)
   - Code example

   Format: ## Variant 1, ## Variant 2, ## Variant 3"

2. Вызывает Gemini

3. Парсит 3 варианта

4. Показывает таблицу:
   "✓ Generated 3 design variants:

   | Variant | Complexity | Scalability | Best for |
   |---------|-----------|-------------|----------|
   | 1. In-memory | 3/10 | 4/10 | Small apps, single server |
   | 2. Redis | 6/10 | 9/10 | Production, multi-server |
   | 3. Hybrid | 7/10 | 8/10 | High performance needs |

   Full designs: .gemini-designs/caching-layer-variants.md

   Which variant would you like to implement? (1-3)"

5. Пользователь выбирает, например: "2"

6. Claude Code имплементирует Variant 2 (Redis-based)
```

### 5. Optimize Mode

**Цель:** Оптимизировать существующий код

**Команда:**
```
/gemini-task optimize "what to optimize" --file path/to/file
```

**Что делает:**
1. Читает файл для оптимизации
2. Анализирует текущие проблемы (если есть profiling данные)
3. Формирует промпт с критериями оптимизации
4. Вызывает Gemini CLI
5. Получает оптимизированную версию
6. Валидирует (тесты должны проходить)
7. Сравнивает performance (если возможно)
8. Применяет оптимизацию

**Пример:**
```
Пользователь: /gemini-task optimize "this slow function" --file utils/data-processor.js

Claude Code:
1. Читает utils/data-processor.js

2. Запускает существующие тесты для baseline

3. Формирует промпт:
   "Optimize this function for performance:

   [код функции]

   Current issue: Processing 10k items takes 5 seconds

   Optimize for:
   - Time complexity
   - Memory usage
   - Readability (don't sacrifice too much)

   Provide:
   - Optimized code
   - Explanation of improvements
   - Complexity analysis (before/after)

   Return: optimized code + explanation"

4. Вызывает Gemini

5. Получает оптимизированную версию

6. Сохраняет в temp файл

7. Запускает тесты → all pass ✓

8. Бенчмарк:
   Before: 5000ms for 10k items
   After: 500ms for 10k items
   Improvement: 10x faster ✓

9. Применяет изменения в utils/data-processor.js

10. Показывает:
    "✓ Optimized utils/data-processor.js
    Performance: 5000ms → 500ms (10x improvement)
    All tests passing ✓
    Changes: Replaced nested loops with Map lookup"
```

### 6. Test Mode

**Цель:** Генерировать тесты для существующего кода

**Команда:**
```
/gemini-task test "what to test" --file path/to/file [--coverage]
```

**Что делает:**
1. Читает файл для тестирования
2. Анализирует функции/методы
3. Проверяет текущий coverage (если --coverage)
4. Формирует промпт для генерации тестов
5. Вызывает Gemini CLI
6. Генерирует тесты (включая edge cases)
7. Создает тестовый файл
8. Запускает тесты для валидации
9. Фиксит failing тесты

**Пример:**
```
Пользователь: /gemini-task test "validation functions" --file utils/validators.js --coverage

Claude Code:
1. Читает utils/validators.js

2. Запускает coverage:
   Current coverage: 45% (missing edge cases)

3. Формирует промпт:
   "Generate comprehensive tests for these validation functions:

   [код функций]

   Include:
   - Happy path tests
   - Edge cases (empty, null, undefined, extreme values)
   - Error cases
   - Boundary conditions

   Test framework: Jest
   Coverage target: 100%

   Format: Complete Jest test suite"

4. Вызывает Gemini

5. Создает utils/validators.test.js

6. Запускает: npm test validators.test.js
   - 5 tests failing

7. Анализирует failures, фиксит:
   - Ожидался throw, а функция returns false → исправить assertion

8. Все тесты проходят ✓

9. Проверяет coverage: 95% ✓

10. Показывает:
    "✓ Generated tests → utils/validators.test.js
    Coverage: 45% → 95% (+50%)
    Tests: 32 total, all passing ✓"
```

## Параметры и флаги

```
--context <file>        Добавить файл как контекст для Gemini
--output <path>         Сохранить результат в указанный файл
--model <name>          Выбрать конкретную модель Gemini
--variants <N>          Сгенерировать N вариантов (для design mode)
--coverage              Включить coverage анализ (для test mode)
--no-validate           Пропустить валидацию результата
--interactive           Интерактивный режим (задавать уточняющие вопросы)
--verbose               Детальный вывод (показать промпт и полный результат)
```

## Workflow команды

```
1. Парсинг аргументов
   └─ Режим (research/generate/review/design/optimize/test)
   └─ Параметры (--context, --output, и т.д.)

2. Подготовка контекста
   └─ Чтение файлов (если указаны)
   └─ Анализ текущего состояния проекта
   └─ Сбор метаданных

3. Формирование промпта
   └─ Структура зависит от режима
   └─ Минимизация контекста
   └─ Четкие инструкции для Gemini

4. Вызов Gemini CLI
   └─ Выбор модели
   └─ Настройка параметров (temperature, max_tokens)
   └─ Error handling с retry

5. Обработка результата
   └─ Парсинг (извлечение кода, структурирование)
   └─ Валидация (компиляция, линтинг, тесты)
   └─ Форматирование под проектные стандарты

6. Интеграция
   └─ Создание/обновление файлов
   └─ Сохранение в правильное место
   └─ Обновление зависимостей (если нужно)

7. Отчет пользователю
   └─ Краткое резюме
   └─ Ссылки на созданные файлы
   └─ Следующие шаги (если применимо)
```

## Примеры использования

### Пример 1: Исследование + имплементация

```
User: /gemini-task research "authentication strategies for Node.js API"

Claude:
✓ Research completed
Top strategies:
1. JWT (stateless, scalable)
2. Session-based (traditional, server-side)
3. OAuth 2.0 (third-party integration)
...

Full report: .gemini-research/auth-strategies-nodejs.md

User: "Implement JWT approach"

Claude:
Starting implementation based on research...
1. Installing dependencies: jsonwebtoken, bcrypt
2. Creating auth middleware
3. Adding login/register endpoints
4. Writing tests
5. Updating documentation
✓ JWT authentication implemented
```

### Пример 2: Code review + рефакторинг

```
User: /gemini-task review "security issues" --file api/auth.js

Claude:
✓ Review completed

CRITICAL (1):
- Password stored in plain text → hash with bcrypt

MAJOR (2):
- No rate limiting on login → add express-rate-limit
- JWT secret in code → move to env variable

Full report: .gemini-reviews/auth-security-2024-11-18.md

User: "Fix all critical and major issues"

Claude:
Fixing identified issues...
1. ✓ Added bcrypt password hashing
2. ✓ Implemented rate limiting (5 req/min)
3. ✓ Moved JWT_SECRET to .env
4. ✓ Updated tests
5. ✓ Security scan passed

All issues resolved ✓
```

### Пример 3: Генерация тестов

```
User: /gemini-task test "all functions" --file utils/string-helpers.js --coverage

Claude:
Current coverage: 30%
Generating comprehensive tests...

✓ Generated 47 test cases:
- 15 happy path tests
- 20 edge case tests
- 12 error handling tests

New coverage: 98% (+68%)
All tests passing ✓

File: utils/string-helpers.test.js
```

### Пример 4: Дизайн архитектуры

```
User: /gemini-task design "microservices architecture for e-commerce" --variants 3

Claude:
✓ Generated 3 architecture variants

Variant 1: Modular Monolith
- Complexity: 4/10
- Scalability: 6/10
- Best for: Small to medium scale

Variant 2: Full Microservices
- Complexity: 9/10
- Scalability: 10/10
- Best for: Large scale, high traffic

Variant 3: Hybrid (Strangler Pattern)
- Complexity: 7/10
- Scalability: 8/10
- Best for: Migration from monolith

Full designs: .gemini-designs/ecommerce-architecture.md

Which variant? (1-3)

User: "3"

Claude:
Implementing Variant 3 (Hybrid - Strangler Pattern)...
[proceeds with implementation]
```

## Конфигурация

### .gemini-config.json

```json
{
  "model": "gemini-1.5-pro",
  "temperature": 0.3,
  "maxTokens": 4000,
  "outputDir": {
    "research": ".gemini-research",
    "designs": ".gemini-designs",
    "reviews": ".gemini-reviews"
  },
  "validation": {
    "enabled": true,
    "typescript": true,
    "eslint": true,
    "tests": true
  },
  "cache": {
    "enabled": true,
    "ttl": 3600
  }
}
```

## Интеграция с агентом

Команда `/gemini-task` автоматически активирует `gemini-orchestrator` агента, который:

1. Анализирует задачу
2. Выбирает оптимальный режим (если не указан явно)
3. Формирует промпт
4. Координирует выполнение
5. Интегрирует результаты

Пользователь может вызывать команду напрямую или через natural language:

```
User: "Use Gemini to research caching strategies"
   ↓
Claude активирует gemini-orchestrator
   ↓
gemini-orchestrator использует /gemini-task research "caching strategies"
```

## Troubleshooting

### Gemini CLI не установлен

```
Error: gemini-cli not found

Solution:
npm install -g @google/generative-ai-cli
# or
pip install google-generativeai-cli
```

### API key не настроен

```
Error: GOOGLE_API_KEY not configured

Solution:
export GOOGLE_API_KEY="your-key"
# or
gemini-cli config set api-key "your-key"
```

### Результат не парсится

```
Error: Failed to parse Gemini output

Причина: Gemini вернул неожиданный формат

Solution:
1. Проверить промпт (он достаточно четкий?)
2. Добавить "Return only [format], no explanation"
3. Использовать --verbose для отладки
4. Retry с более конкретным промптом
```

### Валидация падает

```
Error: Generated code has TypeScript errors

Solution:
1. Claude автоматически пытается исправить
2. Если не получается, показывает ошибки пользователю
3. Предлагает:
   - Использовать --no-validate (skip validation)
   - Или вручную исправить и повторить
```

## Best Practices

1. **Четкие промпты:** Всегда указывай формат ожидаемого результата
2. **Минимальный контекст:** Передавай только необходимое
3. **Валидация:** Всегда валидируй результаты от Gemini
4. **Итеративность:** Не бойся повторить с уточненным промптом
5. **Логирование:** Используй --verbose для отладки
6. **Кэширование:** Включи кэш для повторных запросов
7. **Безопасность:** Фильтруй sensitive данные перед отправкой

## Метрики

Команда автоматически отслеживает:
- Количество вызовов Gemini
- Успешность интеграции результатов
- Время выполнения задач
- Использование токенов

Просмотр метрик:
```
/gemini-task --stats
```

---
name: gemini-cli-usage
description: Детальное руководство по использованию Google Gemini CLI из командной строки, включая установку, конфигурацию, форматирование промптов и обработку результатов. Use when агенту нужно вызвать Gemini CLI или пользователь спрашивает об интеграции с Gemini.
---

# Gemini CLI Usage

## Когда использовать этот Skill

- При первом вызове Gemini CLI в сессии
- Когда нужно форматировать сложный промпт для Gemini
- При работе с файлами и контекстом
- Когда возникают ошибки при вызове CLI
- Для оптимизации промптов и минимизации токенов

## Установка и настройка

### Проверка установки

```bash
# Проверить наличие gemini-cli
which gemini-cli

# Проверить версию
gemini-cli --version

# Посмотреть доступные команды
gemini-cli --help
```

### Установка (если не установлен)

```bash
# Через npm (Node.js)
npm install -g @google/generative-ai-cli

# Или через pip (Python)
pip install google-generativeai-cli

# Проверка после установки
gemini-cli --version
```

### Конфигурация API ключа

```bash
# Установить API ключ через переменную окружения
export GOOGLE_API_KEY="your-api-key-here"

# Или через конфигурационный файл
gemini-cli config set api-key "your-api-key-here"

# Проверить конфигурацию
gemini-cli config list
```

**ВАЖНО:** Никогда не включай реальные API ключи в промпты или файлы проекта!

## Основные команды

### 1. Простой текстовый запрос

```bash
# Базовый синтаксис
gemini-cli "Your prompt here"

# Пример
gemini-cli "Explain async/await in JavaScript"
```

### 2. Выбор модели

```bash
# Использовать конкретную модель
gemini-cli --model gemini-1.5-pro "Your prompt"

# Доступные модели:
# - gemini-1.5-pro (рекомендуется для сложных задач)
# - gemini-1.5-flash (быстрая модель для простых задач)
# - gemini-1.0-pro (legacy)

# Пример
gemini-cli --model gemini-1.5-flash "Generate 10 random usernames"
```

### 3. Многострочные промпты

```bash
# Метод 1: Heredoc (рекомендуется)
gemini-cli "$(cat <<'EOF'
Analyze this code:

function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

Suggest improvements for:
1. Performance
2. Type safety
3. Error handling
EOF
)"

# Метод 2: Файл
echo "Your multi-line prompt" > prompt.txt
gemini-cli "$(cat prompt.txt)"

# Метод 3: Bash переменная
PROMPT="Line 1
Line 2
Line 3"
gemini-cli "$PROMPT"
```

### 4. Работа с файлами контекста

```bash
# Передать файл как контекст
gemini-cli --context-file code.js "Review this code for security issues"

# Множественные файлы
gemini-cli --context-file file1.js --context-file file2.js "Compare these implementations"

# С явным промптом
gemini-cli --context-file schema.sql "$(cat <<'EOF'
Based on this database schema, generate:
1. TypeScript interfaces
2. Validation functions
3. Example seed data
EOF
)"
```

### 5. Форматирование вывода

```bash
# JSON вывод
gemini-cli --format json "List 5 programming languages" | jq .

# Markdown вывод (по умолчанию)
gemini-cli "Explain Docker" > explanation.md

# Только текст (без форматирования)
gemini-cli --format text "What is 2+2?"
```

### 6. Настройка параметров генерации

```bash
# Temperature (креативность): 0.0 - 2.0
gemini-cli --temperature 0.2 "Generate a function name for user validation"

# Top-k (разнообразие)
gemini-cli --top-k 40 "Suggest variable names"

# Top-p (nucleus sampling)
gemini-cli --top-p 0.95 "Write a creative description"

# Max tokens
gemini-cli --max-tokens 1000 "Explain neural networks"
```

## Паттерны промптинга для CLI

### Pattern 1: Structured Output Request

```bash
gemini-cli "$(cat <<'EOF'
Generate 5 test cases for email validation.

Format as JSON array:
[
  {
    "input": "test@example.com",
    "expected": true,
    "reason": "valid email"
  },
  ...
]

Return ONLY the JSON, no markdown, no explanation.
EOF
)"
```

### Pattern 2: Code Generation with Context

```bash
gemini-cli "$(cat <<'EOF'
Context: Express.js REST API for task management

Generate an endpoint for creating tasks with:
- Request validation (express-validator)
- Error handling
- Database save (assume Task.create() exists)
- Response formatting

Return only the code, no explanation.
EOF
)"
```

### Pattern 3: Analysis and Recommendations

```bash
# Читаем код через Claude Code (Read tool)
# Затем передаем в Gemini для анализа

gemini-cli "$(cat <<'EOF'
Analyze this authentication middleware:

$(cat middleware/auth.js)

Identify:
1. Security vulnerabilities
2. Performance bottlenecks
3. Edge cases not handled
4. Suggested improvements

Format as markdown with ## headers for each section.
EOF
)"
```

### Pattern 4: Batch Processing

```bash
# Генерация множественных вариантов
gemini-cli "$(cat <<'EOF'
Generate 3 different implementations of a binary search function:
1. Recursive approach
2. Iterative approach
3. Functional approach (using reduce/map)

For each:
- Full implementation
- Time complexity
- Space complexity
- Use cases

Separate with ### Implementation 1, ### Implementation 2, ### Implementation 3
EOF
)"
```

## Обработка результатов

### Извлечение кода из markdown

```bash
# Gemini часто возвращает код в markdown блоках
# Извлечение через sed/awk

RESULT=$(gemini-cli "Generate a hello world function in Python")

# Извлечь код между ```python и ```
echo "$RESULT" | sed -n '/```python/,/```/p' | sed '1d;$d'

# Или через grep с -A (after) и -B (before)
echo "$RESULT" | grep -A 100 '```python' | grep -B 100 '```' | sed '1d;$d'
```

### Парсинг JSON ответов

```bash
# Запрос с требованием JSON
RESULT=$(gemini-cli "List 5 colors as JSON array of strings")

# Парсинг через jq
echo "$RESULT" | jq -r '.[]'

# Обработка ошибок парсинга
if echo "$RESULT" | jq empty 2>/dev/null; then
  echo "Valid JSON"
  echo "$RESULT" | jq .
else
  echo "Invalid JSON, raw output:"
  echo "$RESULT"
fi
```

### Сохранение результатов

```bash
# В файл
gemini-cli "Generate OpenAPI spec for user API" > openapi.yaml

# В переменную для дальнейшей обработки
ANALYSIS=$(gemini-cli "Analyze this architecture" 2>&1)

# С timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
gemini-cli "Generate test data" > "test_data_${TIMESTAMP}.json"
```

## Обработка ошибок

### Типичные ошибки и решения

```bash
# Ошибка: API key not configured
# Решение:
export GOOGLE_API_KEY="your-key"
# или
gemini-cli config set api-key "your-key"

# Ошибка: Rate limit exceeded
# Решение: retry с backoff
for i in 1 2 3; do
  gemini-cli "prompt" && break
  echo "Retry $i after rate limit..."
  sleep $((2 ** i))  # Exponential backoff: 2s, 4s, 8s
done

# Ошибка: Invalid model
# Решение: проверить доступные модели
gemini-cli --list-models

# Ошибка: Timeout
# Решение: увеличить timeout
gemini-cli --timeout 60 "complex prompt"
```

### Проверка успешности выполнения

```bash
# Проверка exit кода
if gemini-cli "prompt" > output.txt 2>&1; then
  echo "Success"
  cat output.txt
else
  echo "Failed with exit code $?"
  cat output.txt
fi

# Логирование ошибок
gemini-cli "prompt" 2> error.log 1> output.txt
if [ $? -ne 0 ]; then
  echo "Error occurred:"
  cat error.log
fi
```

## Оптимизация использования

### Минимизация токенов

```bash
# ❌ Плохо: излишний контекст
gemini-cli "$(cat entire_codebase.js) - find the bug"

# ✅ Хорошо: только необходимый контекст
gemini-cli "$(cat <<'EOF'
Function with bug:
$(grep -A 20 "function processUser" app.js)

Error: "Cannot read property 'name' of undefined"

Find the bug and suggest fix.
EOF
)"
```

### Кэширование результатов

```bash
# Создать кэш-директорию
mkdir -p .gemini-cache

# Функция с кэшированием
gemini_cached() {
  local prompt="$1"
  local cache_key=$(echo "$prompt" | md5sum | cut -d' ' -f1)
  local cache_file=".gemini-cache/${cache_key}.txt"

  if [ -f "$cache_file" ]; then
    echo "# Cached result"
    cat "$cache_file"
  else
    echo "# Fresh result"
    gemini-cli "$prompt" | tee "$cache_file"
  fi
}

# Использование
gemini_cached "Explain async/await"
```

### Batch запросы

```bash
# Вместо множественных вызовов:
# gemini-cli "task 1"
# gemini-cli "task 2"
# gemini-cli "task 3"

# Используй один вызов:
gemini-cli "$(cat <<'EOF'
Complete 3 tasks:

Task 1: Generate user schema
Task 2: Generate product schema
Task 3: Generate order schema

Format each as:
## Task N
[solution]
EOF
)"
```

## Интеграция с Claude Code Workflow

### Пример: Делегирование исследования

```bash
# 1. Claude Code определяет задачу для делегирования
# 2. Формирует промпт
# 3. Вызывает Gemini
# 4. Обрабатывает результат

RESEARCH_RESULT=$(gemini-cli "$(cat <<'EOF'
Research: What are the top 5 state management libraries for React in 2024?

For each library provide:
- Name and npm package
- Key features (3-5 points)
- Pros and cons
- Best use case
- Current popularity (downloads/week estimate)

Format as markdown with ## Library Name headers.
EOF
)")

# 5. Claude Code анализирует результат и принимает решение
echo "$RESEARCH_RESULT"

# 6. Claude Code имплементирует выбранное решение
```

### Пример: Генерация + Валидация

```bash
# Gemini генерирует код
GENERATED_CODE=$(gemini-cli "Generate a React custom hook for form validation")

# Claude Code валидирует (через TypeScript, ESLint, etc)
echo "$GENERATED_CODE" > temp-hook.ts
npx tsc --noEmit temp-hook.ts
npx eslint temp-hook.ts

# Если валидация прошла - интегрировать в проект
```

## Продвинутые техники

### Streaming output (если поддерживается)

```bash
# Показывать результат по мере генерации
gemini-cli --stream "Write a long article about microservices"
```

### Chain of thought prompting

```bash
gemini-cli "$(cat <<'EOF'
Problem: Design a caching layer for an e-commerce API.

Think step by step:
1. What are the requirements?
2. What data should be cached?
3. What caching strategy (TTL, LRU, etc)?
4. What technology (Redis, Memcached, etc)?
5. How to handle cache invalidation?

Provide reasoning for each step, then final recommendation.
EOF
)"
```

### Few-shot examples

```bash
gemini-cli "$(cat <<'EOF'
Generate API endpoint tests following this pattern:

Example 1:
describe('GET /users', () => {
  it('should return all users', async () => {
    const response = await request(app).get('/users');
    expect(response.status).toBe(200);
    expect(Array.isArray(response.body)).toBe(true);
  });
});

Example 2:
describe('POST /users', () => {
  it('should create a user', async () => {
    const userData = { name: 'John', email: 'john@example.com' };
    const response = await request(app).post('/users').send(userData);
    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
  });
});

Now generate tests for: PATCH /users/:id
EOF
)"
```

## Референсы

### Useful CLI flags

```bash
--model <name>           # Выбор модели
--temperature <float>    # Креативность (0.0-2.0)
--max-tokens <int>       # Максимум токенов в ответе
--top-k <int>            # Top-k sampling
--top-p <float>          # Nucleus sampling
--timeout <seconds>      # Timeout для запроса
--format <json|text|md>  # Формат вывода
--context-file <path>    # Файл контекста
--stream                 # Streaming output
--verbose                # Детальный лог
--quiet                  # Минимальный вывод
```

### Best practices checklist

- ✅ Четкие, структурированные промпты
- ✅ Минимально необходимый контекст
- ✅ Явное указание формата ответа
- ✅ Обработка ошибок и retry логика
- ✅ Валидация результатов перед использованием
- ✅ Фильтрация sensitive данных
- ✅ Кэширование повторных запросов
- ✅ Batch обработка когда возможно
- ✅ Логирование для отладки
- ✅ Мониторинг использования токенов

### Troubleshooting commands

```bash
# Диагностика
gemini-cli --version
gemini-cli config list
gemini-cli --list-models

# Тестовый запрос
gemini-cli "Say hello"

# С детальным логом
gemini-cli --verbose "Test prompt" 2>&1 | tee debug.log

# Проверка переменных окружения
env | grep GOOGLE_API_KEY
```

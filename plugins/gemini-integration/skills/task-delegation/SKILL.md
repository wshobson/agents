---
name: task-delegation
description: Паттерны и стратегии эффективного делегирования задач между Claude Code и Gemini CLI, включая декомпозицию, параллелизацию и интеграцию результатов. Use when нужно разделить сложную задачу между моделями или оптимизировать workflow с использованием обеих систем.
---

# Task Delegation Patterns

## Когда использовать этот Skill

- Сложная задача требует декомпозиции на подзадачи
- Нужно определить, какую часть делегировать в Gemini
- Требуется параллельное выполнение независимых задач
- Необходимо интегрировать результаты от разных моделей
- Оптимизация workflow для максимальной эффективности

## Основные принципы делегирования

### Принцип 1: Разделение по компетенциям

**Claude Code силен в:**
- Работа с файловой системой (чтение, запись, редактирование)
- Контекстное понимание кодовой базы
- Git операции (commit, push, branch)
- Выполнение команд (тесты, билды, линтеры)
- Инкрементальные изменения с сохранением состояния
- Код-ревью с учетом проектных соглашений

**Gemini CLI силен в:**
- Исследование и анализ альтернатив
- Генерация больших объемов контента
- Креативные задачи (нейминг, дизайн)
- Поиск edge cases и corner cases
- Анализ без необходимости контекста проекта
- Быстрая генерация множественных вариантов

### Принцип 2: Минимизация передачи контекста

**Эффективно:**
```
Gemini: "Предложи 5 подходов к rate limiting" (без контекста проекта)
   ↓
Claude: Анализирует предложения с учетом архитектуры проекта
   ↓
Claude: Имплементирует выбранный подход
```

**Неэффективно:**
```
Gemini: "Вот весь код проекта (10000 строк), найди баг" ❌
```

### Принцип 3: Явная последовательность

Всегда четко определяй:
1. Что делает Claude Code
2. Что делегируется Gemini
3. Что делает Claude Code с результатами Gemini
4. Финальный шаг интеграции

## Паттерны делегирования

### Pattern 1: Research → Implement

**Использовать когда:** Нужно выбрать подход/технологию/архитектуру

```
Задача: "Добавить real-time notifications в приложение"

1. Claude Code (Контекст):
   - Читает текущую архитектуру
   - Определяет технологический стек
   - Формулирует требования

2. Gemini CLI (Исследование):
   Промпт: "Сравни 5 подходов к real-time notifications для Node.js app:
   - WebSockets (ws library)
   - Server-Sent Events
   - Long polling
   - Socket.io
   - Third-party service (Pusher, Ably)

   Для каждого: pros/cons, complexity, scalability, cost"

3. Claude Code (Анализ):
   - Анализирует предложения Gemini
   - Выбирает оптимальный подход (например, Socket.io)
   - Учитывает специфику проекта

4. Claude Code (Имплементация):
   - Устанавливает dependencies
   - Создает server setup
   - Интегрирует с существующим кодом
   - Пишет тесты
   - Создает коммит
```

### Pattern 2: Parallel Execution

**Использовать когда:** Независимые подзадачи можно выполнить параллельно

```
Задача: "Создать API endpoint для user registration"

Параллельно:

Claude Code (track 1):
├─ Создает route handler
├─ Добавляет валидацию (express-validator)
├─ Интегрирует с database
└─ Пишет integration тесты

Gemini CLI (track 2):
├─ Генерирует edge cases для тестирования
├─ Создает OpenAPI документацию
└─ Генерирует примеры запросов/ответов

Интеграция:
Claude Code:
├─ Добавляет edge case тесты от Gemini
├─ Интегрирует OpenAPI spec в проект
└─ Финальный коммит со всем функционалом
```

**Команды:**
```bash
# Claude Code работает с кодом
# Одновременно вызываем Gemini (фоном или параллельно)

EDGE_CASES=$(gemini-cli "$(cat <<'EOF'
Generate 20 edge cases for user registration:
- Username validation (length, chars, uniqueness)
- Email validation (format, disposable emails)
- Password security (strength, common passwords)
- Rate limiting scenarios
- Duplicate registration attempts

Format as JSON array: [{scenario, input, expectedBehavior}]
EOF
)") &

# Claude Code продолжает работу
# Когда результат Gemini готов - интегрирует
```

### Pattern 3: Generate → Validate → Refine

**Использовать когда:** Нужна быстрая генерация с последующей валидацией

```
Задача: "Сгенерировать TypeScript interfaces из JSON schema"

1. Gemini CLI (Генерация):
   Промпт: "Convert this JSON schema to TypeScript interfaces:
   [schema]

   Include:
   - All types with strict typing
   - JSDoc comments
   - Utility types for optional fields"

   → Быстро генерирует interfaces

2. Claude Code (Валидация):
   - Сохраняет в temp файл
   - Запускает TypeScript compiler: tsc --noEmit
   - Проверяет ESLint
   - Проверяет соответствие style guide

3. Если ошибки:
   Claude Code (Исправление):
   - Фиксит проблемы локально
   - Адаптирует под проектные conventions

4. Claude Code (Интеграция):
   - Перемещает в финальную локацию
   - Экспортирует из index
   - Обновляет зависимости
   - Коммитит
```

### Pattern 4: Multi-Variant Generation → Selection

**Использовать когда:** Нужно выбрать между несколькими вариантами

```
Задача: "Спроектировать API для shopping cart"

1. Gemini CLI (Генерация вариантов):
   Промпт: "Design 3 different REST API approaches for shopping cart:

   Variant 1: Session-based (cookies)
   Variant 2: Token-based (JWT with cart data)
   Variant 3: Database-backed (persistent cart)

   For each provide:
   - Endpoint structure
   - Data flow
   - Pros/cons
   - Sample code (Express.js)"

   → Возвращает 3 детальных дизайна

2. Claude Code (Анализ контекста):
   - Проверяет текущую auth систему
   - Анализирует database schema
   - Учитывает масштабируемость требования
   - Определяет ограничения инфраструктуры

3. Claude Code (Выбор):
   - Выбирает Variant 3 (database-backed)
   - Обоснование: "У нас уже есть user DB, нужна персистентность"

4. Claude Code (Имплементация):
   - Берет дизайн Variant 3 от Gemini как основу
   - Адаптирует под текущую архитектуру
   - Имплементирует с учетом проектных паттернов
```

### Pattern 5: Implement → Review → Refine

**Использовать когда:** Нужно второе мнение на архитектурное решение

```
Задача: "Оптимизировать slow database query"

1. Claude Code (Первая имплементация):
   - Анализирует текущий query
   - Читает database schema
   - Создает оптимизированную версию с индексами
   - Дизайн решения документирует

2. Gemini CLI (Code Review):
   Промпт: "Review this database optimization:

   Original query: [slow query]
   Optimized query: [new query]
   New indexes: [indexes]
   Schema: [relevant schema]

   Analyze:
   - Are indexes optimal?
   - Any missing edge cases?
   - Potential performance issues?
   - Alternative approaches?
   - N+1 query risks?"

   → Детальный review с предложениями

3. Claude Code (Рефайнинг):
   - Анализирует фидбек от Gemini
   - Применяет валидные предложения
   - Добавляет упущенные edge cases
   - Финализирует решение

4. Claude Code (Тестирование):
   - Пишет тесты (включая edge cases от Gemini)
   - Запускает performance benchmarks
   - Коммитит улучшенное решение
```

### Pattern 6: Batch Content Generation

**Использовать когда:** Нужно много однотипного контента

```
Задача: "Создать тесты для 15 API endpoints"

1. Claude Code (Подготовка):
   - Собирает список endpoints
   - Читает route handlers для понимания логики
   - Формирует структурированный список

2. Gemini CLI (Batch генерация):
   Промпт: "Generate Jest tests for these 15 endpoints:

   1. GET /users - returns user list
   2. GET /users/:id - returns single user
   3. POST /users - creates user
   ...
   15. DELETE /orders/:id - deletes order

   For each test include:
   - Happy path
   - Error cases (404, 400, 401)
   - Edge cases

   Follow this pattern:
   [показываем один пример теста]

   Return all 15 test suites, separated by // ENDPOINT N"

   → Генерирует все 15 тестовых файлов

3. Claude Code (Обработка):
   - Парсит результат Gemini
   - Разделяет на отдельные файлы
   - Адаптирует под реальные модели/fixtures
   - Добавляет недостающие imports
   - Запускает тесты для валидации
   - Фиксит failing тесты
   - Коммитит
```

## Декомпозиция задач

### Фреймворк декомпозиции

```
Вход: Задача от пользователя
  ↓
1. Категоризация:
   - Простая (single-step) → выполнить напрямую
   - Средняя (multi-step) → может пригодиться Gemini для части
   - Сложная (complex) → обязательно делегирование

2. Анализ компонентов:
   - Какие части требуют контекста проекта? → Claude Code
   - Какие части можно делать изолированно? → Gemini
   - Есть ли параллелизуемые задачи? → Параллельное выполнение

3. Планирование последовательности:
   - Зависимости между задачами
   - Критический путь
   - Точки интеграции результатов

4. Формирование промптов:
   - Для Gemini: четкая структура, минимальный контекст
   - Для Claude Code: использование tools (Read, Edit, Write, Bash)

5. Исполнение:
   - Выполнение по плану
   - Сбор результатов
   - Интеграция
```

### Примеры декомпозиции

**Задача: "Добавь feature flag систему в проект"**

```
Декомпозиция:

1. Research (Gemini):
   "Сравни подходы к feature flags: LaunchDarkly, Unleash, custom solution"

2. Design (Claude Code + Gemini):
   Claude: Анализирует текущую архитектуру
   Gemini: Предлагает дизайн API для feature flags
   Claude: Адаптирует под проект

3. Implementation (Claude Code):
   - Создает feature flag service
   - Интегрирует с database
   - Добавляет middleware

4. Testing (Claude Code + Gemini):
   Claude: Пишет integration тесты
   Gemini: Генерирует edge cases
   Claude: Добавляет edge case coverage

5. Documentation (Gemini + Claude Code):
   Gemini: Генерирует usage guide
   Claude: Адаптирует и добавляет в project docs
```

**Задача: "Migrate from REST to GraphQL"**

```
Декомпозиция (большая задача):

Phase 1 - Research:
├─ Gemini: "Analyze GraphQL migration strategies"
├─ Gemini: "Compare GraphQL servers: Apollo, Mercurius, Yoga"
└─ Claude: Анализирует текущие REST endpoints

Phase 2 - Schema Design:
├─ Claude: Экспортирует структуру текущих endpoints
├─ Gemini: "Convert REST endpoints to GraphQL schema"
└─ Claude: Рефайнит schema под проектные типы

Phase 3 - Implementation (параллельно):
├─ Claude (track 1): Настройка GraphQL server
├─ Claude (track 2): Создает resolvers для существующих endpoints
└─ Gemini (track 3): Генерирует тестовые queries/mutations

Phase 4 - Migration:
├─ Claude: Постепенная миграция endpoints
├─ Claude: Dual support (REST + GraphQL)
└─ Claude: Обновление клиентского кода

Phase 5 - Testing & Deployment:
├─ Claude: Integration тесты
├─ Gemini: Генерация edge cases и stress test scenarios
└─ Claude: Performance testing, deployment
```

## Интеграция результатов

### Pattern A: Direct Integration

```bash
# Gemini возвращает готовый код → прямая интеграция

COMPONENT=$(gemini-cli "Generate React component for user profile card")

# Claude Code валидирует и интегрирует
echo "$COMPONENT" > src/components/UserProfileCard.tsx

# Проверка
npx tsc --noEmit src/components/UserProfileCard.tsx

# Если ОК → коммит
```

### Pattern B: Parse and Transform

```bash
# Gemini возвращает структурированные данные → парсинг и трансформация

TEST_CASES=$(gemini-cli "Generate test cases for email validation, return JSON array")

# Claude Code парсит
echo "$TEST_CASES" | jq -r '.[] |
  "test(\"" + .scenario + "\", () => {
    expect(validateEmail(\"" + .input + "\")).toBe(" + (.expected | tostring) + ");
  });"
' > tests/email.test.js
```

### Pattern C: Merge and Consolidate

```bash
# Несколько результатов от Gemini → консолидация Claude Code

APPROACH_1=$(gemini-cli "Design approach 1 for caching")
APPROACH_2=$(gemini-cli "Design approach 2 for caching")
APPROACH_3=$(gemini-cli "Design approach 3 for caching")

# Claude Code анализирует все три
# Берет лучшие идеи из каждого
# Создает гибридное решение
# Имплементирует
```

### Pattern D: Iterative Refinement

```bash
# Gemini генерирует → Claude валидирует → возвращается в Gemini для улучшения

INITIAL=$(gemini-cli "Generate SQL query for user analytics")

# Claude проверяет
psql -d mydb --dry-run -c "$INITIAL" 2>&1

# Если ошибки, отправляет обратно с фидбеком
REFINED=$(gemini-cli "Fix this SQL query error: [error message]. Original: $INITIAL")

# Повтор до успешной валидации
```

## Оптимизация Workflow

### Checklist эффективного делегирования

**Перед делегированием:**
- [ ] Задача выиграет от делегирования? (не проще ли сделать все в Claude?)
- [ ] Четко определена граница ответственности?
- [ ] Минимизирован контекст для Gemini?
- [ ] Промпт структурирован и однозначен?

**Во время выполнения:**
- [ ] Параллелизуем независимые задачи?
- [ ] Логируем промпты и результаты для отладки?
- [ ] Обрабатываем ошибки Gemini CLI?

**После получения результатов:**
- [ ] Валидируем результаты от Gemini?
- [ ] Адаптируем под проектные conventions?
- [ ] Тестируем интегрированный код?
- [ ] Документируем использование Gemini (если релевантно)?

### Anti-patterns (чего избегать)

❌ **Передача всего проекта в Gemini**
```bash
# Плохо
gemini-cli "$(cat entire_project/**/*.js) - refactor this"
```

❌ **Использование Gemini для файловых операций**
```bash
# Плохо: Gemini генерирует, но Claude должен записать
# Хорошо: Claude делает и Read, и Write
```

❌ **Игнорирование валидации**
```bash
# Плохо
CODE=$(gemini-cli "generate code")
echo "$CODE" > production.js  # без проверки!
git commit -m "add code from Gemini"  # ❌
```

❌ **Слишком мелкое делегирование**
```bash
# Плохо: накладные расходы на вызов больше, чем польза
gemini-cli "suggest variable name for user id"  # Claude справится сам
```

❌ **Отсутствие структуры в промптах**
```bash
# Плохо
gemini-cli "make it better"  # что? как? зачем?

# Хорошо
gemini-cli "Refactor this function for:
1. Better error handling
2. Type safety
3. Performance

Code: [code]
Return: refactored code with comments explaining changes"
```

## Мониторинг и метрики

### Что отслеживать

```
Эффективность делегирования:
- Время выполнения (с Gemini vs без)
- Качество результатов (субъективно)
- Количество итераций до интеграции
- Процент успешно интегрированного кода

Использование ресурсов:
- Количество вызовов Gemini
- Средний размер промптов
- Токены использованные
- Стоимость (если релевантно)

Паттерны использования:
- Какие типы задач чаще делегируются
- Какие паттерны работают лучше
- Где возникают проблемы
```

### Логирование для анализа

```bash
# Создать лог-файл для Gemini вызовов
GEMINI_LOG=".gemini-calls.log"

gemini_logged() {
  local prompt="$1"
  local timestamp=$(date -Iseconds)

  echo "=== $timestamp ===" >> "$GEMINI_LOG"
  echo "PROMPT:" >> "$GEMINI_LOG"
  echo "$prompt" >> "$GEMINI_LOG"
  echo "---" >> "$GEMINI_LOG"

  local result=$(gemini-cli "$prompt" 2>&1)
  local exit_code=$?

  echo "RESULT (exit: $exit_code):" >> "$GEMINI_LOG"
  echo "$result" >> "$GEMINI_LOG"
  echo "" >> "$GEMINI_LOG"

  echo "$result"
}

# Использование
gemini_logged "Your prompt here"
```

## Референсы и примеры

### Реальные use cases

1. **Миграция на новую библиотеку:**
   - Gemini: исследует новую библиотеку, предлагает migration план
   - Claude: имплементирует migration с учетом проекта

2. **Performance optimization:**
   - Claude: профилирует код, находит bottleneck
   - Gemini: предлагает 5 способов оптимизации
   - Claude: выбирает и имплементирует

3. **API design:**
   - Gemini: генерирует несколько вариантов API дизайна
   - Claude: выбирает на основе существующих паттернов
   - Claude: имплементирует

4. **Test coverage increase:**
   - Claude: анализирует coverage report
   - Gemini: генерирует тесты для uncovered paths
   - Claude: интегрирует и адаптирует тесты

5. **Documentation generation:**
   - Claude: экспортирует код structure
   - Gemini: генерирует documentation
   - Claude: интегрирует в docs, адаптирует формат

### Шаблоны промптов для делегирования

**Template 1: Research**
```
Research: [topic]

Analyze and compare:
- [aspect 1]
- [aspect 2]
- [aspect 3]

For each option provide:
- Overview
- Pros and cons
- Use cases
- Complexity (1-10)

Format: Markdown with ## headers
```

**Template 2: Generation**
```
Context: [minimal context]

Generate: [what to generate]

Requirements:
- [requirement 1]
- [requirement 2]

Constraints:
- [constraint 1]
- [constraint 2]

Format: [expected format]
Return only [what], no [what not]
```

**Template 3: Review**
```
Review this [code/design/architecture]:

[content to review]

Analyze for:
1. [aspect 1]
2. [aspect 2]
3. [aspect 3]

Provide:
- Issues found (with severity: critical/major/minor)
- Suggested improvements
- Alternative approaches

Format: Markdown with severity tags
```

# Gemini Integration Plugin

Интеграция Claude Code с Google Gemini CLI для делегирования подзадач и оркестрации multi-model workflows.

## Обзор

Этот плагин позволяет Claude Code эффективно делегировать задачи в Google Gemini через командную строку, оптимально распределяя работу между двумя моделями на основе их сильных сторон.

## Компоненты

### Агенты

- **gemini-orchestrator** - Главный агент для оркестрации делегирования задач между Claude Code и Gemini CLI

### Скиллы

- **gemini-cli-usage** - Детальное руководство по использованию Gemini CLI
- **task-delegation** - Паттерны и стратегии делегирования задач

### Команды

- **gemini-task** - Команда для выполнения задач через Gemini CLI с различными режимами работы

## Установка

### Предварительные требования

1. Установите Gemini CLI:
```bash
npm install -g @google/generative-ai-cli
# или
pip install google-generativeai-cli
```

2. Настройте API ключ:
```bash
export GOOGLE_API_KEY="your-api-key-here"
# или
gemini-cli config set api-key "your-api-key"
```

### Установка плагина

```bash
# Из директории вашего проекта
claude plugin install gemini-integration
```

## Использование

### Автоматическая активация

Агент `gemini-orchestrator` активируется автоматически когда:
- Вы хотите использовать Gemini для параллельной обработки задач
- Нужно получить альтернативные подходы к решению
- Требуется второе мнение по архитектурным решениям
- Необходимо исследование технологий или best practices

### Команда /gemini-task

```bash
# Исследование
/gemini-task research "best approaches for API rate limiting"

# Генерация кода
/gemini-task generate "TypeScript interfaces for User API" --context api/users.js

# Code review
/gemini-task review "this database query optimization" --file db/queries/analytics.sql

# Дизайн архитектуры
/gemini-task design "caching layer for REST API" --variants 3

# Оптимизация
/gemini-task optimize "this slow function" --file utils/data-processor.js

# Генерация тестов
/gemini-task test "all functions" --file utils/validators.js --coverage
```

## Паттерны использования

### Pattern 1: Research → Implement

```
Пользователь: "Добавь real-time notifications"
   ↓
Claude Code: Анализирует архитектуру
   ↓
Gemini: Исследует 5 подходов к real-time notifications
   ↓
Claude Code: Выбирает оптимальный подход и имплементирует
```

### Pattern 2: Parallel Execution

```
Задача: "Создать API endpoint для user registration"

Параллельно:
- Claude Code: Создает route handler, валидацию, тесты
- Gemini CLI: Генерирует edge cases и OpenAPI документацию
   ↓
Claude Code: Интегрирует результаты
```

### Pattern 3: Implement → Review → Refine

```
Claude Code: Разрабатывает решение
   ↓
Gemini CLI: Code review и предложения
   ↓
Claude Code: Рефайнит на основе фидбека
```

## Когда использовать Gemini

✅ **Хорошие use cases для Gemini:**
- Исследование подходов и технологий
- Генерация альтернативных решений
- Создание тестовых данных и сценариев
- Поиск edge cases
- Генерация документации
- Креативные задачи (нейминг, дизайн API)

❌ **Оставить в Claude Code:**
- Работа с файлами проекта
- Git операции
- Контекстные решения (требуют знания кодовой базы)
- Выполнение тестов и билдов
- Инкрементальные изменения

## Конфигурация

Создайте `.gemini-config.json` в корне проекта:

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

## Примеры

### Пример 1: Исследование best practices

```
User: "Реализовать rate limiting для API"

Claude activates gemini-orchestrator
   ↓
Gemini исследует 5 подходов: token bucket, leaky bucket, fixed window, etc.
   ↓
Claude выбирает подход на основе проекта
   ↓
Claude имплементирует выбранное решение
```

### Пример 2: Генерация тестов

```
User: "Протестировать функцию валидации email"

Claude reads функцию
   ↓
Gemini генерирует 30 test cases (valid/invalid/edge cases)
   ↓
Claude создает тесты на основе сценариев
   ↓
Все тесты проходят ✓
```

### Пример 3: Архитектурное решение

```
User: "Спроектировать систему кэширования"

Claude анализирует требования
   ↓
Claude создает предварительный дизайн
   ↓
Gemini проводит review (bottlenecks, security, edge cases)
   ↓
Claude рефайнит дизайн
   ↓
Claude имплементирует финальное решение
```

## Best Practices

1. **Четкие промпты** - Всегда указывайте формат ожидаемого результата
2. **Минимальный контекст** - Передавайте только необходимую информацию
3. **Валидация** - Всегда валидируйте результаты от Gemini
4. **Безопасность** - Фильтруйте sensitive данные перед отправкой
5. **Кэширование** - Используйте кэш для повторных запросов
6. **Batch обработка** - Группируйте похожие задачи

## Troubleshooting

### Gemini CLI не найден

```bash
Error: gemini-cli not found

Solution:
npm install -g @google/generative-ai-cli
```

### API key не настроен

```bash
Error: GOOGLE_API_KEY not configured

Solution:
export GOOGLE_API_KEY="your-key"
```

### Rate limit превышен

Плагин автоматически использует retry логику с exponential backoff (2s, 4s, 8s, 16s).

## Метрики

Просмотр статистики использования:

```bash
/gemini-task --stats
```

Показывает:
- Количество вызовов Gemini
- Успешность интеграции
- Время выполнения задач
- Использование токенов

## Лицензия

MIT

## Автор

Dmitry Lazarenko - [lazarenkod@gmail.com](mailto:lazarenkod@gmail.com)

## Ссылки

- [Gemini CLI Documentation](https://ai.google.dev/gemini-api/docs/cli)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)

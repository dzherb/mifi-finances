![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/dzherb/e4e57a646506bdfb6bd3fc1ae9876d5b/raw/covbadge.json)

# Система контроля финансов

## Стэк

- Python
- PostgreSQL
- React

## Инструкция по запуску

Инструкцию по запуску бэкенда приложения можно посмотреть [здесь](/backend/README.md). Также там содержится вся необходимая информация по тулингу, который требуется при разработке.

## Схема БД
<!-- BEGIN_DB_SCHEMA_DOCS -->
```mermaid
erDiagram
  users {
    INTEGER id PK
    DATETIME created_at
    DATETIME updated_at "nullable"
    VARCHAR username UK
    VARCHAR password
    DATETIME last_refresh "nullable"
    BOOLEAN is_admin
  }

  transaction_categories {
    INTEGER id PK
    DATETIME created_at
    DATETIME updated_at "nullable"
    VARCHAR name UK
  }

  transactions {
    INTEGER id PK
    DATETIME created_at
    DATETIME updated_at "nullable"
    VARCHAR(12) party_type
    DATETIME occurred_at
    VARCHAR(6) transaction_type
    VARCHAR comment
    NUMERIC(12_5) amount
    VARCHAR(10) status
    INTEGER sender_bank_id FK
    VARCHAR account_number
    INTEGER recipient_bank_id FK
    VARCHAR recipient_inn
    VARCHAR recipient_account_number
    INTEGER category_id FK
    VARCHAR recipient_phone
    INTEGER user_id FK
  }

  banks {
    INTEGER id PK
    DATETIME created_at
    DATETIME updated_at "nullable"
    VARCHAR name UK
  }

  banks ||--o{ transactions : sender_bank_id
  banks ||--o{ transactions : recipient_bank_id
  transaction_categories ||--o{ transactions : category_id
  users ||--o{ transactions : user_id

```
<!-- END_DB_SCHEMA_DOCS -->

## CI/CD

В качестве основного инструмента CI/CD используется [Github Actions](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions). Настроены следующие этапы:

- **Линтеры и type checking**

    - Код проверяется на соответствие стайлгайду (PEP8 и другим рекомендациям)
    - С помощью статического анализа выявляются вероятные баги еще до запуска сервера
    - Форсится применение best practices
    - Проверяется корректность типизации с помощью [mypy](https://mypy.readthedocs.io/en/stable/index.html) в `strict` режиме


- **Тесты**

    - Unit-тесты
    - Интеграционные тесты с использованием реальной БД
    - Интеграционные тесты с помощью [schemathesis](https://schemathesis.readthedocs.io/en/stable/), который проверяет соответствие эндпоинтов сервера на его же `openapi` спецификацию (что еще называют **Schema-Based Testing**)


- **Отчет о проценте покрытия**

    - На основе этапа тестирования генерируется отчет о том, какие строки кода были задействованы
    - Итоговый отчет сохраняется как артефакт, а общий процент покрытия автоматически сохраняется в **badge**: ![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/dzherb/e4e57a646506bdfb6bd3fc1ae9876d5b/raw/covbadge.json)

### Dependabot

Также настроена интеграция с [dependabot](https://github.com/dependabot). Он автоматически уведомляет об обнаруженных уязвимостях в зависимостях и делает пулл-реквесты с попыткой поднять версию.
---
name: code-review-guardrails
description: Reviews and writes code for the MCP-based app while enforcing docs/guardrails.md. Use when developing, reviewing, or generating a Guardrails status report (Allow / Warn / Block) for this repository.
---

# Code review guardrails

## 1. Призначення

Рев'ю і написання коду для MCP-основного застосунку з дотриманням Guardrails.

Перед написанням або зміною коду прочитай `docs/guardrails.md` і дотримуйся рівнів Allow / Warn / Block. Не видаляй файли в `Decisions/`. Не виконуй `git push` у `main` без перевірки людиною.

## 2. Покрокова процедура

- Проаналізувати код на наявність порушень правил із docs/guardrails.md (наприклад, заборона git push у main напряму, несанкціонована зміна системних конфігурацій).
- Перевірити наявність необхідних тестів.
- Видати звіт у форматі: Статус (Allow / Warn / Block) та рекомендації.

Порядок роботи:

1. Зібрати список файлів, які змінюються або рев'юються.
2. Звірити дії з `docs/guardrails.md` (читання коду — Allow; коміти та зміна бізнес-коду — Warn; `git push` у `main` без перевірки, видалення `Decisions/`, зміна системних конфігурацій поза репозиторієм — Block).
3. Перевірити, що для нової логіки є Pytest-покриття (ціль harness — від 80%).
4. Якщо є Block — зупинити небезпечні дії і зафіксувати їх у звіті. Warn потребує підтвердження людини. Allow можна виконувати.

## 3. Формат результату

Структурований markdown-звіт із переліком перевірених файлів і висновком.

```markdown
# Звіт: розробка / рев'ю коду

## Статус
Allow | Warn | Block

## Перевірені файли
- `path/to/file.py`

## Порушення guardrails
- Немає / опис порушення (правило, файл, дія)

## Тести
- Наявні: так/ні
- Пробіли: ...

## Рекомендації
- ...

## Висновок
...
```

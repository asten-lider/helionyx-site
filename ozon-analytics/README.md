# Ozon Analytics

Автоматический ежедневный сбор данных Ozon через GitHub Actions.

## Что собирается
- FBO-заказы
- FBS-заказы
- финансовые начисления за предыдущий день
- текущие остатки

## Secrets
В репозитории открой:

Settings → Secrets and variables → Actions → New repository secret

Добавь:
- `OZON_CLIENT_ID`
- `OZON_API_KEY`

После этого:
Actions → Ozon daily collection → Run workflow

При успешном запуске данные появятся в:
`ozon-analytics/history/YYYY-MM-DD/`

Расписание: ежедневно в 06:10 МСК.

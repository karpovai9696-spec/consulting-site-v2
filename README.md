# ГК «Клиники диализа» — новая версия сайта

Статический сайт консалтинговой компании в дизайн-системе «Диалам+» и
«Диамедики». Контент генерируется из публичного JSON админ-панели.

## Страницы

- `index.html` — главная
- `about.html` — о компании
- `uslugi.html` — услуги
- `geografiya.html` — география
- `press.html` — пресс-центр
- `rukovodstvo.html` — руководство
- `vakansii.html` — вакансии
- `kontakty.html` — контакты и форма
- `dokumenty.html` — документы и реквизиты
- `404.html` — ошибка

## Связь с админкой

Сайт собирается из `data/admin-export.json` — публичного экспорта сайта
`consulting`:

```bash
ADMIN_PUBLIC_URL=https://127.0.0.1:18090/api/public/sites/consulting.json \
  python scripts/sync_admin.py
```

После изменения данных в админке:

1. выполнить `sync_admin.py`;
2. проверить изменения;
3. сделать commit и push — GitHub Pages пересоберётся автоматически.

В админке у сайта заполнены:

- название, реквизиты, ИНН, ОГРН, телефон, e-mail, адрес;
- офис в Казани;
- четыре услуги;
- новость;
- три руководителя;
- вакансия;
- настройки `hero_title`, `hero_subtitle`, `stats`, `geography_cities`;
- `site_url` — адрес этой версии.

## Live

- https://karpovai9696-spec.github.io/consulting-site-v2/
- https://github.com/karpovai9696-spec/consulting-site-v2

## Ограничения

- GitHub Pages — статика; форма открывает почтовый клиент `uk.klinika@mail.ru`.
- Для прямой отправки заявок нужен backend или CRM.
- JS-поиск и онлайн-карта не подключены; карта открывается ссылкой на Яндекс.Карты.

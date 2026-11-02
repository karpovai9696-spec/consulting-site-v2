# -*- coding: utf-8 -*-
"""Генератор консалтингового сайта из публичного экспорта админки."""
from pathlib import Path
import json
import html as H
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "admin-export.json").read_text(encoding="utf-8"))
SITE = DATA["site"]
ITEMS = DATA["items"]
SET = ITEMS.get("settings", {})
BRANCHES = sorted(ITEMS.get("branches", []), key=lambda x: x.get("sort_order", 0))
SERVICES = sorted([x for x in ITEMS.get("services", []) if x["data"].get("is_active", True)], key=lambda x: x.get("sort_order", 0))
NEWS = sorted([x for x in ITEMS.get("news", []) if x["data"].get("published", True)], key=lambda x: x["data"].get("date", ""), reverse=True)
STAFF = sorted(ITEMS.get("staff", []), key=lambda x: x.get("sort_order", 0))
VACANCIES = sorted([x for x in ITEMS.get("vacancies", []) if x["data"].get("published", True)], key=lambda x: x.get("sort_order", 0))
BRANCH = BRANCHES[0]["data"] if BRANCHES else {}
BASE = SET.get("site_url", "https://karpovai9696-spec.github.io/consulting-site-v2/").rstrip("/") + "/"
BRAND = SITE["name"]
PHONE = SITE.get("phone") or "+7 (843) 204-19-61"
TEL = "+" + "".join(c for c in PHONE if c.isdigit())
EMAIL = SITE.get("email") or "uk.klinika@mail.ru"
ADDRESS = SITE.get("address") or "г. Казань, ул. Алексея Козина, д. 7, офис 1080"
INN = SITE.get("inn", "")
OGRN = SITE.get("ogrn", "")
LEGAL = SITE.get("legal_name", BRAND)
STATS = [x.strip() for x in SET.get("stats", "16 центров|2000 пациентов|12 городов|с 2008 года").split("|") if x.strip()]
CITIES = [x.strip() for x in SET.get("geography_cities", "Казань").split("|") if x.strip()]

def esc(v):
    return H.escape(str(v or ""))

def nav(active=""):
    links = [("index.html", "О компании"), ("uslugi.html", "Услуги"), ("geografiya.html", "География"),
             ("press.html", "Пресс-центр"), ("rukovodstvo.html", "Руководство"), ("vakansii.html", "Вакансии"),
             ("kontakty.html", "Контакты")]
    return "".join(f'<li class="nav-item"><a href="{href}" class="nav-link{" is-active" if href == active else ""}">{label}</a></li>' for href, label in links)

def header(active=""):
    return f'''  <header class="site-header">
    <div class="container">
      <div class="header-top">
        <a href="index.html" class="brand" aria-label="{esc(BRAND)} — на главную"><img src="assets/img/logo.svg" width="900" height="222" alt="{esc(BRAND)}" class="brand-logo"></a>
        <a href="kontakty.html" class="city-select"><svg class="icon icon--pin" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-5.75-7-11a7 7 0 1 1 14 0c0 5.25-7 11-7 11z"></path><circle cx="12" cy="10" r="2.5"></circle></svg><span class="city-select__text">Казань · ул. Алексея Козина, 7</span></a>
        <div class="header-right">
          <button type="button" class="a11y-toggle" aria-pressed="false"><svg class="icon icon--eye" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg><span class="a11y-toggle__label">Версия для слабовидящих</span></button>
          <a href="tel:{TEL}" class="header-phone">{esc(PHONE)}</a>
          <a href="kontakty.html#form" class="btn btn--primary header-cta">Обсудить проект</a>
          <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="main-nav" aria-label="Открыть меню навигации"><svg class="icon icon--menu" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16"></path><path d="M4 12h16"></path><path d="M4 17h16"></path></svg><svg class="icon icon--close" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg></button>
        </div>
      </div>
      <nav class="main-nav" id="main-nav" aria-label="Основная навигация"><ul class="nav-list">{nav(active)}</ul><div class="mobile-nav-extras"><div class="mobile-city-info"><svg class="icon icon--pin" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-5.75-7-11a7 7 0 1 1 14 0c0 5.25-7 11-7 11z"></path><circle cx="12" cy="10" r="2.5"></circle></svg><span>Казань · ул. Алексея Козина, 7</span></div><div class="mobile-tools-row"><button type="button" class="a11y-toggle a11y-toggle--mobile" aria-pressed="false"><svg class="icon icon--eye" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg><span class="a11y-toggle__label">Версия для слабовидящих</span></button></div><a href="kontakty.html#form" class="btn btn--primary mobile-cta">Обсудить проект</a></div></nav>
    </div>
  </header>'''

def footer():
    return f'''  <footer class="site-footer"><div class="container"><div class="footer-card glass-card">
    <div class="footer-grid">
      <div class="footer-brand"><a href="index.html" class="footer-logo-link"><img src="assets/img/logo.svg" width="900" height="222" alt="{esc(BRAND)}" class="footer-logo"></a><p class="footer-copy">© {esc(BRAND)}, 2008–2026. Все права защищены.</p><a href="dokumenty.html" class="footer-policy">Политика обработки персональных данных</a></div>
      <nav class="footer-nav" aria-label="Навигация в подвале"><ul class="footer-nav__list"><li><a href="index.html" class="footer-nav__link">О компании</a></li><li><a href="uslugi.html" class="footer-nav__link">Услуги</a></li><li><a href="geografiya.html" class="footer-nav__link">География</a></li><li><a href="press.html" class="footer-nav__link">Пресс-центр</a></li><li><a href="rukovodstvo.html" class="footer-nav__link">Руководство</a></li><li><a href="vakansii.html" class="footer-nav__link">Вакансии</a></li><li><a href="kontakty.html" class="footer-nav__link">Контакты</a></li></ul></nav>
      <div class="footer-contacts"><a href="tel:{TEL}" class="footer-phone"><svg class="icon icon--phone" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg><span>{esc(PHONE)}</span></a><p class="footer-address"><svg class="icon icon--pin" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-5.75-7-11a7 7 0 1 1 14 0c0 5.25-7 11-7 11z"></path><circle cx="12" cy="10" r="2.5"></circle></svg><span>г. Казань, ул. Алексея Козина, д. 7</span></p></div>
      <div class="footer-emblem"><a href="dokumenty.html" class="footer-emblem__link" aria-label="Документы и реквизиты"><img src="assets/img/logo.svg" width="900" height="222" alt="" class="footer-emblem__img"></a></div>
    </div>
    <div class="footer-legal"><p class="footer-legal__line">{esc(LEGAL)} · ИНН {esc(INN)} · ОГРН {esc(OGRN)} · {esc(ADDRESS)}</p><p class="footer-legal__line">Информация на сайте не является публичной офертой.</p><p class="footer-legal__links"><a href="dokumenty.html">Документы и политика ПДн</a> · <a href="vakansii.html">Вакансии</a> · <a href="kontakty.html">Контакты</a></p></div>
  </div></div></footer>'''

def shell(title, desc, main, active="", scripts=""):
    return f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="icon" href="assets/img/favicon.ico"><link rel="stylesheet" href="css/base.css"><link rel="stylesheet" href="css/home.css"><link rel="stylesheet" href="css/inner.css"><link rel="stylesheet" href="css/contacts.css"><link rel="stylesheet" href="css/legal-pages.css"><link rel="stylesheet" href="css/diamedika.css"><link rel="stylesheet" href="css/consulting.css"><link rel="canonical" href="{BASE}{'' if active == 'index.html' else active}"><meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:type" content="website"><meta property="og:site_name" content="{esc(BRAND)}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE}{'' if active == 'index.html' else active}"><meta property="og:locale" content="ru_RU"><script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"Organization","name":BRAND,"url":BASE,"telephone":PHONE,"email":EMAIL,"address":{"@type":"PostalAddress","streetAddress":ADDRESS,"addressCountry":"RU"}}, ensure_ascii=False)}</script></head><body><a href="#main-content" class="skip-link">Перейти к содержанию</a>{header(active)}<main id="main-content" class="site-main"><div class="container">{main}</div></main>{footer()}<script src="js/main.js"></script><script src="js/forms.js"></script>{scripts}</body></html>'''

def breadcrumbs(label):
    return f'<nav class="breadcrumbs" aria-label="Хлебные крошки"><ol class="breadcrumbs__list"><li class="breadcrumbs__item"><a href="index.html" class="breadcrumbs__link">Главная</a></li><li class="breadcrumbs__sep" aria-hidden="true">/</li><li class="breadcrumbs__item"><span class="breadcrumbs__current" aria-current="page">{esc(label)}</span></li></ol></nav>'

def content_cards(*items):
    return '<div class="content-stack">' + "".join(f'<section class="content-card glass-card">{f"<h2 class=\"content-card__title\">{esc(h)}</h2>" if h else ""}{body}</section>' for h, body in items) + '</div>'

def stat_cards():
    out = '<div class="stats-row">'
    for value in STATS:
        parts = value.split(" ", 1)
        if value.startswith("с "):
            words = value.split(" ")
            parts = [" ".join(words[:2]), " ".join(words[2:])]
        out += f'<div class="stat-item"><strong>{esc(parts[0])}</strong><span>{esc(parts[1] if len(parts)>1 else "")}</span></div>'
    return out + '</div>'

def service_cards():
    out = '<div class="service-grid">'
    for item in SERVICES:
        d = item["data"]
        out += f'<article class="service-card"><h3>{esc(d.get("name"))}</h3><p>{esc(d.get("description"))}</p><a href="uslugi.html">Подробнее →</a></article>'
    return out + '</div>'

def news_cards(limit=None):
    rows = NEWS[:limit] if limit else NEWS
    out = '<div class="news-list">'
    for item in rows:
        d = item["data"]
        out += f'<article class="news-card glass-card"><p class="news-card__date">{esc(d.get("date"))}</p><h3 class="news-card__title">{esc(d.get("title"))}</h3><p class="news-card__text">{esc(d.get("excerpt"))}</p><a class="news-card__link" href="press.html">Читать →</a></article>'
    return out + '</div>'

# ---------------- index ----------------
hero_title = SET.get("hero_title") or SITE.get("tagline") or "Консалтинг и управление центрами гемодиализа"
hero_sub = SET.get("hero_subtitle") or SITE.get("description") or ""
index_main = f'''<section class="hero"><div class="hero-content"><span class="consult-kicker">{esc(SET.get("hero_badge", "ГК «Клиники диализа» · консалтинг"))}</span><h1 class="hero-title">{esc(hero_title)}</h1><p class="hero-lead">{esc(hero_sub)}</p><div class="hero-actions"><a href="kontakty.html#form" class="btn btn--dark hero-btn"><span>Обсудить проект</span><svg class="icon icon--arrow-up-right" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"></path><path d="M8 7h9v9"></path></svg></a></div><div class="hero-note">Или позвоните: <a href="tel:{TEL}">{esc(PHONE)}</a></div></div><div class="hero-media"><div class="hero-photo-wrap"><img src="assets/img/hero.jpg" width="1600" height="1065" alt="Эксперты консалтинговой компании «Клиники диализа»" class="hero-photo" loading="eager" fetchpriority="high"></div><div class="hours-card glass-card"><p class="hours-card__label">Офис в Казани</p><p class="hours-card__days">{esc(BRANCH.get("address", "ул. Алексея Козина, д. 7"))}</p><p class="hours-card__time">{esc(BRANCH.get("hours", "Пн–Пт 09:00–18:00"))}</p></div></div></section>{stat_cards()}
<section class="home-section" id="about"><div class="section-heading"><p class="eyebrow">О КОМПАНИИ</p><h2 class="section-title">Опыт, который работает на результат</h2></div><div class="content-card glass-card"><p>Консалтинговая компания «Клиники диализа» обеспечивает стабильную работу центров амбулаторного гемодиализа по всей России. Первые центры в Нижнекамске и Бугульме открылись в 2008 году.</p><p>Сегодня компания проектирует, оснащает и запускает специализированные центры, сопровождает проекты государственно-частного партнёрства и помогает медицинским организациям выстраивать устойчивую операционную модель.</p><p><a href="about.html">Подробнее о компании →</a></p></div></section>
<section class="home-section"><div class="section-heading"><p class="eyebrow">УСЛУГИ</p><h2 class="section-title">Полный цикл запуска центра</h2></div>{service_cards()}</section>
<section class="home-section"><div class="section-heading"><p class="eyebrow">ГЕОГРАФИЯ</p><h2 class="section-title">Центры в 12 городах России</h2></div><div class="geo-grid">{''.join(f'<a href="geografiya.html" class="geo-card glass-card"><span>{esc(c)}</span><small>Центр гемодиализа</small></a>' for c in CITIES)}</div><p class="section-more"><a href="geografiya.html">Смотреть географию →</a></p></section>
<section class="home-section"><div class="section-heading"><p class="eyebrow">ПРЕСС-ЦЕНТР</p><h2 class="section-title">Новости компании</h2></div>{news_cards(2)}<p class="section-more"><a href="press.html">Все новости →</a></p></section>
<section class="home-section" id="form"><div class="form-card glass-card"><div><p class="eyebrow">СОТРУДНИЧЕСТВО</p><h2 class="section-title">Расскажите о вашем проекте</h2><p class="muted">Оставьте контакты — обсудим задачи и предложим решение.</p></div><form id="appointment-form" class="simple-form" novalidate><label class="field"><span>Ваше имя</span><input class="input" type="text" name="name" autocomplete="name" required></label><label class="field"><span>Телефон</span><input class="input" type="tel" name="phone" inputmode="tel" autocomplete="tel" required></label><label class="field field--full"><span>Комментарий</span><textarea class="input" name="message" rows="3"></textarea></label><div class="consent"><input type="checkbox" id="form-consent" name="consent" required><label for="form-consent">Согласен с обработкой персональных данных</label><a href="dokumenty.html" class="consent__link">Политика</a></div><button type="submit" class="btn btn--primary">Отправить заявку</button><p class="form-note">Заявка откроется в почтовом клиенте. Если он недоступен — позвоните <a href="tel:{TEL}">{esc(PHONE)}</a>.</p><p class="form-alert" id="form-error" role="alert" hidden>Укажите имя, корректный телефон и согласие.</p><p class="form-success" id="form-success" role="status" aria-live="polite" hidden></p></form></div></section>'''
title = f"{BRAND} — консалтинг и управление центрами гемодиализа"
(ROOT / "index.html").write_text(shell(title, SITE.get("description", ""), index_main, "index.html"), encoding="utf-8")

# ---------------- about ----------------
about_main = f'''{breadcrumbs("О компании")}<h1 class="page-title">О компании</h1><p class="page-lead">{esc(SITE.get("description", ""))}</p>{stat_cards()}<div class="content-stack"><section class="content-card glass-card"><h2 class="content-card__title">С 2008 года</h2><p>Консалтинговая компания «Клиники диализа» начала работу с открытия центров в Нижнекамске и Бугульме. Сегодня компания сопровождает проекты центров амбулаторного гемодиализа в разных регионах России.</p></section><section class="content-card glass-card"><h2 class="content-card__title">Что мы делаем</h2><p>Проектируем медицинские и инженерные решения, подбираем оборудование, помогаем с запуском центра, обучением персонала и организационным сопровождением.</p></section><section class="content-card glass-card"><h2 class="content-card__title">Реквизиты</h2><p>{esc(LEGAL)}<br>ИНН {esc(INN)} · ОГРН {esc(OGRN)}<br>{esc(ADDRESS)}<br><a href="dokumenty.html">Документы и политика ПДн →</a></p></section></div>'''
(ROOT / "about.html").write_text(shell(f"О компании — {BRAND}", "О консалтинговой компании «Клиники диализа»: опыт, услуги и реквизиты.", about_main, "about.html"), encoding="utf-8")

# ---------------- services ----------------
services_detail = "".join(f'<section class="content-card glass-card"><h2 class="content-card__title">{esc(i["data"].get("name"))}</h2><p>{esc(i["data"].get("description"))}</p><p><strong>Стоимость:</strong> {esc(i["data"].get("price"))}</p></section>' for i in SERVICES)
services_main = f'''{breadcrumbs("Услуги")}<h1 class="page-title">Услуги</h1><p class="page-lead">Консалтинг для медицинских организаций и проектов в сфере гемодиализа.</p><div class="content-stack">{services_detail}</div>'''
(ROOT / "uslugi.html").write_text(shell(f"Услуги — {BRAND}", "Консалтинговые услуги: проектирование, оснащение, запуск и сопровождение центров гемодиализа.", services_main, "uslugi.html"), encoding="utf-8")

# ---------------- geography ----------------
geo_main = f'''{breadcrumbs("География")}<h1 class="page-title">География деятельности</h1><p class="page-lead">Центры амбулаторного гемодиализа в городах России.</p><div class="geo-grid">{''.join(f'<article class="geo-card glass-card"><span>{esc(c)}</span><small>Центр гемодиализа</small></article>' for c in CITIES)}</div><div class="content-card glass-card"><h2 class="content-card__title">Офис компании</h2><p>{esc(ADDRESS)}</p><p><a href="{esc(BRANCH.get("map_url", ""))}" target="_blank" rel="noopener noreferrer">Открыть на карте →</a></p></div>'''
(ROOT / "geografiya.html").write_text(shell(f"География — {BRAND}", "География центров гемодиализа и офис консалтинговой компании «Клиники диализа».", geo_main, "geografiya.html"), encoding="utf-8")

# ---------------- press ----------------
press_main = f'''{breadcrumbs("Пресс-центр")}<h1 class="page-title">Пресс-центр</h1><p class="page-lead">Новости компании и полезные материалы.</p>{news_cards()}'''
(ROOT / "press.html").write_text(shell(f"Пресс-центр — {BRAND}", "Новости и материалы ГК «Клиники диализа».", press_main, "press.html"), encoding="utf-8")

# ---------------- contacts ----------------
contacts_main = f'''{breadcrumbs("Контакты")}<h1 class="page-title">Контакты</h1><p class="page-lead">Свяжитесь с нами, чтобы обсудить проект.</p><div class="content-stack"><section class="content-card glass-card"><h2 class="content-card__title">Офис в Казани</h2><p>{esc(ADDRESS)}</p><p>Телефон: <a href="tel:{TEL}">{esc(PHONE)}</a><br>E-mail: <a href="mailto:{esc(EMAIL)}">{esc(EMAIL)}</a></p><p>{esc(BRANCH.get("hours", "Пн–Пт 09:00–18:00"))}</p><p><a href="{esc(BRANCH.get("map_url", ""))}" target="_blank" rel="noopener noreferrer">Открыть на Яндекс.Картах →</a></p></section><section class="content-card glass-card" id="form"><h2 class="content-card__title">Написать нам</h2><form id="appointment-form" class="simple-form" novalidate><label class="field"><span>Ваше имя</span><input class="input" type="text" name="name" required></label><label class="field"><span>Телефон</span><input class="input" type="tel" name="phone" required></label><label class="field field--full"><span>Комментарий</span><textarea class="input" name="message" rows="3"></textarea></label><div class="consent"><input type="checkbox" id="form-consent" name="consent" required><label for="form-consent">Согласен с обработкой персональных данных</label><a href="dokumenty.html" class="consent__link">Политика</a></div><button type="submit" class="btn btn--primary">Отправить</button><p class="form-note">Заявка откроется в почтовом клиенте. Если он недоступен — позвоните <a href="tel:{TEL}">{esc(PHONE)}</a>.</p><p class="form-alert" id="form-error" role="alert" hidden>Укажите имя, корректный телефон и согласие.</p><p class="form-success" id="form-success" role="status" aria-live="polite" hidden></p></form></section></div>'''
(ROOT / "kontakty.html").write_text(shell(f"Контакты — {BRAND}", "Контакты консалтинговой компании «Клиники диализа» в Казани.", contacts_main, "kontakty.html"), encoding="utf-8")

# ---------------- leadership ----------------
staff_cards = "".join(f'<article class="staff-card glass-card"><h2>{esc(s["data"].get("name"))}</h2><p class="staff-card__role">{esc(s["data"].get("role"))}</p><p><a href="tel:{esc(s["data"].get("phone"))}">{esc(s["data"].get("phone"))}</a></p></article>' for s in STAFF)
lead_main = f'''{breadcrumbs("Руководство")}<h1 class="page-title">Руководство</h1><p class="page-lead">Команда, которая отвечает за развитие компании.</p><div class="staff-grid">{staff_cards}</div>'''
(ROOT / "rukovodstvo.html").write_text(shell(f"Руководство — {BRAND}", "Руководство ГК «Клиники диализа».", lead_main, "rukovodstvo.html"), encoding="utf-8")

# ---------------- vacancies ----------------
vac_cards = "".join(f'<article class="vacancy-card glass-card"><h2>{esc(v["data"].get("title"))}</h2><p class="vacancy-card__meta">{esc(v["data"].get("city"))} · {esc(v["data"].get("employment"))} · {esc(v["data"].get("salary"))}</p><p>{esc(v["data"].get("description"))}</p><p><strong>Требования:</strong> {esc(v["data"].get("requirements"))}</p><p><a href="mailto:{esc(v["data"].get("contact_email"))}">Откликнуться →</a></p></article>' for v in VACANCIES)
vac_main = f'''{breadcrumbs("Вакансии")}<h1 class="page-title">Вакансии</h1><p class="page-lead">Работа в команде, которая развивает гемодиализ в России.</p><div class="vacancy-grid">{vac_cards or "<p>Актуальные вакансии уточняйте у HR-службы.</p>"}</div>'''
(ROOT / "vakansii.html").write_text(shell(f"Вакансии — {BRAND}", "Вакансии ГК «Клиники диализа».", vac_main, "vakansii.html"), encoding="utf-8")

# ---------------- documents ----------------
docs_main = f'''{breadcrumbs("Документы")}<h1 class="page-title">Документы и политика</h1><p class="page-lead">Реквизиты компании и документы по обработке персональных данных.</p>{content_cards(("Реквизиты", f"<p>{esc(LEGAL)}<br>ИНН {esc(INN)}<br>ОГРН {esc(OGRN)}<br>{esc(ADDRESS)}</p>"),("Политика обработки персональных данных", '<p><a href="assets/docs/politika-pdn.pdf" target="_blank" rel="noopener">Открыть документ (PDF)</a></p><p>Форма обратной связи открывает почтовый клиент и не передаёт данные на сервер сайта.</p>'),("Связаться", f'<p><a href="mailto:{esc(EMAIL)}">{esc(EMAIL)}</a> · <a href="tel:{TEL}">{esc(PHONE)}</a></p>'))}'''
(ROOT / "dokumenty.html").write_text(shell(f"Документы — {BRAND}", "Документы и реквизиты ГК «Клиники диализа».", docs_main, "dokumenty.html"), encoding="utf-8")

# ---------------- 404 ----------------
err_main = f'''<div class="error-page glass-card"><p class="eyebrow">404</p><h1 class="page-title">Страница не найдена</h1><p>Возможно, адрес изменился.</p><a class="btn btn--primary" href="index.html">На главную</a></div>'''
(ROOT / "404.html").write_text(shell("Страница не найдена — " + BRAND, "Страница не найдена.", err_main, "404.html"), encoding="utf-8")

# sitemap
pages = [p.name for p in ROOT.glob("*.html") if p.name != "404.html"]
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
xml += "\n".join(f"  <url><loc>{BASE if p == 'index.html' else BASE + p}</loc></url>" for p in sorted(pages))
xml += "\n</urlset>\n"
(ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
(ROOT / ".nojekyll").write_text("", encoding="utf-8")
print("built pages", len(pages), "base", BASE)

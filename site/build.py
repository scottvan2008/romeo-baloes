"""生成三语静态页面：public/index.html（PT）、public/en/index.html、public/zh/index.html。

用法：python build.py
"""
import json
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import quote

from src.content import (CONTENT, EMAIL, GALLERY_IMAGES, INSTAGRAM, LANGS, SERVICE_IMAGES, SITE_URL, TIKTOK,
                         WECHAT, WHATSAPP, WHATSAPP_DISPLAY)

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"

WA_ICON = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 11.9 0 0 0 4.6 4c1.7.7 2.3.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>'
IG_ICON = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10Zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4ZM17.3 5.5a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4ZM21.9 7.1a6 6 0 0 0-1.6-4.3A6 6 0 0 0 16 1.2C14.3 1.1 9.7 1.1 8 1.2a6 6 0 0 0-4.3 1.6A6 6 0 0 0 2.1 7c-.1 1.7-.1 6.3 0 8a6 6 0 0 0 1.6 4.3A6 6 0 0 0 8 20.9c1.7.1 6.3.1 8 0a6 6 0 0 0 4.3-1.6 6 6 0 0 0 1.6-4.3c.1-1.7.1-6.3 0-8Zm-2.2 9.8a3.3 3.3 0 0 1-1.8 1.8c-1.3.5-4.3.4-5.9.4s-4.6.1-5.9-.4a3.3 3.3 0 0 1-1.8-1.8c-.5-1.3-.4-4.3-.4-5.9s-.1-4.6.4-5.9a3.3 3.3 0 0 1 1.8-1.8c1.3-.5 4.3-.4 5.9-.4s4.6-.1 5.9.4a3.3 3.3 0 0 1 1.8 1.8c.5 1.3.4 4.3.4 5.9s.1 4.6-.4 5.9Z"/></svg>'
TT_ICON = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.7a5.7 5.7 0 1 0 4.9 5.7V9a7.4 7.4 0 0 0 4.3 1.4V7.3a4.3 4.3 0 0 1-3.2-1.5Z"/></svg>'
MAIL_ICON = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M3 5h18v14H3zM3 6l9 7 9-7"/></svg>'
WECHAT_ICON = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M9 3C4.6 3 1 6 1 9.7c0 2.1 1.2 4 3 5.2l-.7 2.3 2.7-1.4c.9.3 1.9.4 3 .4h.6a5.6 5.6 0 0 1-.2-1.5c0-3.5 3.4-6.4 7.6-6.4h.6C16.9 5.3 13.3 3 9 3Zm-2.7 4.9a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm5.4 0a1 1 0 1 1 0-2 1 1 0 0 1 0 2ZM23 14.6c0-3-3-5.4-6.6-5.4s-6.6 2.4-6.6 5.4 3 5.4 6.6 5.4c.8 0 1.5-.1 2.2-.3l2.2 1.1-.6-1.9c1.7-1 2.8-2.5 2.8-4.3Zm-8.8-.8a.9.9 0 1 1 0-1.8.9.9 0 0 1 0 1.8Zm4.4 0a.9.9 0 1 1 0-1.8.9.9 0 0 1 0 1.8Z"/></svg>'
LOGO = '<svg class="logo-mark" viewBox="0 0 32 40" aria-hidden="true"><ellipse cx="16" cy="15" rx="12" ry="14" fill="#FF4D5E"/><ellipse cx="11.5" cy="10" rx="3" ry="4.5" fill="#fff" opacity=".35"/><path d="M14 29h4l-2 3z" fill="#FF4D5E"/><path d="M16 32c-2 3 2 4 0 8" stroke="#FFC93C" stroke-width="1.5" fill="none" stroke-linecap="round"/></svg>'


def wa_link(text: str) -> str:
    return f"https://wa.me/{WHATSAPP}?text={quote(text)}"


def img(name: str, alt: str, prefix: str, sizes: str, cls: str = "", eager: bool = False) -> str:
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="{prefix}img/{name}-800.webp" '
            f'srcset="{prefix}img/{name}-800.webp 800w, {prefix}img/{name}-1600.webp 1600w" '
            f'sizes="{sizes}" alt="{escape(alt)}" {loading}>')


def jsonld(lang: str, c: dict) -> str:
    url = SITE_URL + "/" + LANGS[lang]["dir"]
    data = [
        {
            "@context": "https://schema.org",
            "@type": "EntertainmentBusiness",
            "name": "Romeo Balões",
            "description": c["description"],
            "url": url,
            "image": SITE_URL + "/og-image.jpg",
            "telephone": WHATSAPP_DISPLAY,
            "email": EMAIL,
            "areaServed": {"@type": "City", "name": "São Paulo"},
            "address": {"@type": "PostalAddress", "addressLocality": "São Paulo", "addressRegion": "SP", "addressCountry": "BR"},
            "sameAs": [INSTAGRAM, TIKTOK],
            "knowsLanguage": ["pt-BR", "en", "zh"],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faq"]],
        },
    ]
    return json.dumps(data, ensure_ascii=False)


def render(lang: str) -> str:
    c = CONTENT[lang]
    meta = LANGS[lang]
    prefix = "../" if meta["dir"] else ""
    url = SITE_URL + "/" + meta["dir"]
    wa = wa_link(c["wa_text"])
    e = escape

    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{m["hreflang"]}" href="{SITE_URL}/{m["dir"]}">' for m in LANGS.values()
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">'

    lang_switch = "".join(
        f'<a href="{prefix}{m["dir"]}" lang="{m["html_lang"]}" hreflang="{m["hreflang"]}"'
        + (' aria-current="true"' if k == lang else "") + f'>{m["label"]}</a>'
        for k, m in LANGS.items()
    )

    nav = "".join(f'<a href="#{k}">{e(v)}</a>' for k, v in c["nav"].items())

    trust = "".join(
        f'<div class="trust-item"><strong>{e(n)}</strong><span>{e(t)}</span></div>' for n, t in c["trust"]
    )

    about = "".join(f"<p>{e(p)}</p>" for p in c["about"])
    about_lang = f'<p class="lang-note">{e(c["about_lang"])}</p>' if c["about_lang"] else ""

    services = "".join(
        f'''<article class="service reveal">
  <div class="service-media">{img(SERVICE_IMAGES[i], alt, prefix, "(min-width: 900px) 40vw, 100vw")}</div>
  <div class="service-body"><span class="service-num">0{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>
</article>''' for i, (t, d, alt) in enumerate(c["services"])
    )

    why = "".join(f'<li class="reveal"><span class="why-ico" aria-hidden="true">{ic}</span>{e(t)}</li>' for ic, t in c["why"])

    gallery = "".join(
        f'<button class="g-item reveal" type="button" data-full="{prefix}img/{name}-1600.webp" aria-label="{e(c["gallery_alt"])}">'
        f'{img(name, c["gallery_alt"], prefix, "(min-width: 900px) 25vw, 50vw")}</button>'
        for name in GALLERY_IMAGES
    )

    reviews = "".join(
        f'''<figure class="review reveal">
  <blockquote lang="pt-BR">“{e(q)}”</blockquote>
  {f'<p class="review-tr">{e(tr)}</p>' if tr else ''}
  <figcaption><strong>{e(who)}</strong><span>{e(where)}</span></figcaption>
</figure>''' for q, tr, who, where in c["reviews"]
    )

    packages = "".join(
        f'''<article class="pkg reveal">
  <h3>{e(name)}</h3>
  <ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul>
  <a class="btn btn-wa btn-block" href="{wa_link(msg + chr(10) + c["wa_text"].split(chr(10), 1)[1])}" target="_blank" rel="noopener">{WA_ICON}{e(c["packages_btn"])}</a>
</article>''' for name, items, msg in c["packages"]
    )

    faq = "".join(
        f'<details class="reveal"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in c["faq"]
    )

    wechat_block = ""
    if c["wechat_label"]:
        wechat_block = f'''<div class="wechat">
  {WECHAT_ICON}<span>{e(c["wechat_label"])}：<strong id="wechat-id">{WECHAT}</strong></span>
  <button type="button" class="copy-btn" data-copy="{WECHAT}" data-done="{e(c["copied"])}">{e(c["copy"])}</button>
</div>'''
    final_hint = f'<p class="final-hint">{e(c["final_hint"])}</p>' if c["final_hint"] else ""

    year = date.today().year

    return f'''<!doctype html>
<html lang="{meta["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(c["title"])}</title>
<meta name="description" content="{e(c["description"])}">
<link rel="canonical" href="{url}">
{alternates}
<meta name="theme-color" content="#0F1226">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Romeo Balões">
<meta property="og:title" content="{e(c["title"])}">
<meta property="og:description" content="{e(c["description"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{c["og_locale"]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@400;600;700&display=swap">
<link rel="preload" as="image" href="{prefix}img/hero-800.webp" imagesrcset="{prefix}img/hero-800.webp 800w, {prefix}img/hero-1600.webp 1600w" imagesizes="(min-width: 900px) 45vw, 100vw">
<link rel="stylesheet" href="{prefix}assets/style.css">
<script>document.documentElement.classList.add("js")</script>
<script type="application/ld+json">{jsonld(lang, c)}</script>
</head>
<body class="lang-{lang}">
<a class="skip" href="#main">{e(c["skip"])}</a>

<header class="site-header" id="top">
  <div class="wrap header-inner">
    <a class="brand" href="#top">{LOGO}<span>Romeo <b>Balões</b></span></a>
    <nav class="nav" id="nav" aria-label="{e(c["menu"])}">{nav}</nav>
    <div class="header-right">
      <div class="lang-switch">{lang_switch}</div>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="{e(c["menu"])}"><span></span><span></span></button>
    </div>
  </div>
</header>

<main id="main">
<section class="hero">
  <div class="hero-balloons" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
  <div class="wrap hero-grid">
    <div class="hero-text">
      <p class="eyebrow">{e(c["hero_eyebrow"])}</p>
      <h1>{c["hero_title"]}</h1>
      <p class="hero-sub">{e(c["hero_sub"])}</p>
      <div class="hero-cta">
        <a class="btn btn-wa btn-lg" href="{wa}" target="_blank" rel="noopener">{WA_ICON}{e(c["cta_primary"])}</a>
        <a class="btn btn-ghost btn-lg" href="#services">{e(c["cta_secondary"])}</a>
      </div>
      <p class="reply-note"><span class="dot" aria-hidden="true"></span>{e(c["reply_note"])}</p>
    </div>
    <div class="hero-photo">
      {img("hero", c["hero_alt"], prefix, "(min-width: 900px) 45vw, 100vw", eager=True)}
    </div>
  </div>
</section>

<section class="trust" aria-label="{e(c["why_title"])}">
  <div class="wrap trust-grid">{trust}</div>
</section>

<section class="section about" id="about">
  <div class="wrap about-grid">
    <div class="about-photo reveal">{img("romeo", c["about_alt"], prefix, "(min-width: 900px) 40vw, 100vw")}</div>
    <div class="about-text reveal">
      <p class="kicker">{e(c["about_kicker"])}</p>
      <h2>{e(c["about_title"])}</h2>
      {about}
      <p class="punch">{e(c["about_punch"])}</p>
      {about_lang}
    </div>
  </div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <header class="section-head reveal"><p class="kicker">{e(c["services_kicker"])}</p><h2>{e(c["services_title"])}</h2></header>
    <div class="services">{services}</div>
  </div>
</section>

<section class="section why">
  <div class="wrap">
    <header class="section-head reveal"><p class="kicker">{e(c["why_kicker"])}</p><h2>{e(c["why_title"])}</h2></header>
    <ul class="why-list">{why}</ul>
  </div>
</section>

<section class="section" id="gallery">
  <div class="wrap">
    <header class="section-head reveal"><p class="kicker">{e(c["gallery_kicker"])}</p><h2>{e(c["gallery_title"])}</h2></header>
    <div class="gallery">{gallery}</div>
    <p class="center"><a class="btn btn-ghost" href="{INSTAGRAM}" target="_blank" rel="noopener">{IG_ICON}{e(c["gallery_more"])}</a></p>
  </div>
</section>

<section class="section reviews-sec" id="reviews">
  <div class="wrap">
    <header class="section-head reveal"><p class="kicker">{e(c["reviews_kicker"])}</p><h2>{e(c["reviews_title"])}</h2></header>
    <div class="reviews">{reviews}</div>
  </div>
</section>

<section class="section" id="packages">
  <div class="wrap">
    <header class="section-head reveal"><p class="kicker">{e(c["packages_kicker"])}</p><h2>{e(c["packages_title"])}</h2><p>{e(c["packages_intro"])}</p></header>
    <div class="pkgs">{packages}</div>
    <p class="center muted">{e(c["packages_note"])}</p>
  </div>
</section>

<section class="section" id="faq">
  <div class="wrap narrow">
    <header class="section-head reveal"><p class="kicker">{e(c["faq_kicker"])}</p><h2>{e(c["faq_title"])}</h2></header>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="final" id="contact">
  <div class="wrap final-inner reveal">
    <h2>{e(c["final_title"])}</h2>
    <p>{e(c["final_sub"])}</p>
    <a class="btn btn-wa btn-lg" href="{wa}" target="_blank" rel="noopener">{WA_ICON}{e(c["final_btn"])}</a>
    {final_hint}
    {wechat_block}
  </div>
</section>
</main>

<footer class="site-footer">
  <div class="wrap footer-inner">
    <div>
      <a class="brand" href="#top">{LOGO}<span>Romeo <b>Balões</b></span></a>
      <p class="muted">{e(c["footer_tag"])}</p>
    </div>
    <ul class="contacts">
      <li><a href="{wa}" target="_blank" rel="noopener">{WA_ICON}{WHATSAPP_DISPLAY}</a></li>
      <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">{IG_ICON}@romeo.baloes</a></li>
      <li><a href="{TIKTOK}" target="_blank" rel="noopener">{TT_ICON}TikTok @romeo.baloes</a></li>
      <li><a href="mailto:{EMAIL}">{MAIL_ICON}{EMAIL}</a></li>
      {f'<li><span>{WECHAT_ICON}{e(c["wechat_label"])} {WECHAT}</span></li>' if c["wechat_label"] else ''}
    </ul>
  </div>
  <div class="wrap footer-bottom">
    <span>© {year} Romeo Balões. {e(c["footer_rights"])}</span>
    <div class="lang-switch">{lang_switch}</div>
  </div>
</footer>

<a class="wa-float" href="{wa}" target="_blank" rel="noopener" aria-label="{e(c["wa_float"])}">{WA_ICON}</a>

<dialog class="lightbox" aria-label="{e(c["gallery_title"])}">
  <button type="button" class="lb-close" aria-label="{e(c["close"])}">×</button>
  <img alt="{e(c["gallery_alt"])}">
</dialog>

<script src="{prefix}assets/main.js" defer></script>
</body>
</html>
'''


def main() -> None:
    for lang, meta in LANGS.items():
        out = PUBLIC / meta["dir"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(lang), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))

    urls = "".join(
        f"<url><loc>{SITE_URL}/{m['dir']}</loc>"
        + "".join(f'<xhtml:link rel="alternate" hreflang="{a["hreflang"]}" href="{SITE_URL}/{a["dir"]}"/>' for a in LANGS.values())
        + "</url>"
        for m in LANGS.values()
    )
    (PUBLIC / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        f'xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}</urlset>\n', encoding="utf-8")
    (PUBLIC / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    main()

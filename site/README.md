# Romeo Balões 网站

三语（PT / EN / 中文）一页式静态网站。

## 目录

| 路径 | 内容 |
|---|---|
| `src/content.py` | **全部文案**（三语）、联系方式、图片顺序。改文字只改这里 |
| `build.py` | 生成 `public/index.html`、`public/en/index.html`、`public/zh/index.html`、sitemap、robots |
| `tools/optimize_images.py` | 把 `../活动照/` 的原图压成 WebP（去掉 GPS 等 EXIF）到 `public/img/` |
| `public/assets/` | 样式 `style.css` 和脚本 `main.js` |
| `public/` | **要上线的就是这个文件夹** |

## 常用操作

改文案或联系方式：

```bash
python build.py
```

换照片或加照片：把原图放进 `活动照/`，在 `tools/optimize_images.py` 的 `PHOTOS` 里改对应行，然后：

```bash
python tools/optimize_images.py
```

本地预览（在项目根目录）：

```bash
python -m http.server 8765 --directory site/public
```

然后打开 http://localhost:8765

## 上线（Cloudflare Pages，免费）

1. 在 Cloudflare 注册 `romeobaloes.com`。
2. Cloudflare 后台 → Workers & Pages → Create → Pages → **Upload assets**，把 `public/` 文件夹拖进去。
3. 项目的 Custom domains 里绑定 `romeobaloes.com`。
4. 以后更新：重新 build，再上传一次 `public/`。

域名不是 romeobaloes.com 的话，改 `src/content.py` 里的 `SITE_URL` 后重新 build（分享卡片、sitemap、hreflang 都用它）。

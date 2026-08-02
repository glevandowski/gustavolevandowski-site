<p align="center">
  <img src="./assets/brand/og.jpg" alt="Gustavo Levandowski · Android Engineer · systems on platforms that secure 1M+ devices · mentoring" width="100%">
</p>

<p align="center">
  <img src="./assets/brand/favicon.svg" alt="Marca" width="40" height="40">
</p>

<h1 align="center">gustavolevandowski.com</h1>

<p align="center">
  <strong>Site pessoal e portfólio técnico</strong> de Gustavo Levandowski — Senior Android Engineer, Android Enterprise Expert certificado pelo Google e fundador do <a href="https://movimentolecode.com">LeCode</a>.
</p>

<p align="center">
  <a href="https://gustavolevandowski.com"><img src="https://img.shields.io/badge/live-gustavolevandowski.com-B08C4A?style=flat-square&labelColor=161513" alt="Site ao vivo"></a>
  <img src="https://img.shields.io/badge/stack-HTML%20·%20CSS%20·%20JS-161513?style=flat-square&labelColor=F6F5F3&color=161513" alt="Stack">
  <img src="https://img.shields.io/badge/i18n-EN%20%2F%20PT--BR-6E6B66?style=flat-square&labelColor=F6F5F3" alt="Idiomas">
  <img src="https://img.shields.io/badge/build-zero%20deps-B08C4A?style=flat-square&labelColor=161513" alt="Sem dependências">
</p>

<p align="center">
  <a href="https://gustavolevandowski.com">Abrir o site</a> ·
  <a href="https://www.linkedin.com/in/levandowski/">LinkedIn</a> ·
  <a href="https://medium.com/@levandowski">Medium</a> ·
  <a href="https://movimentolecode.com">LeCode</a>
</p>

---

## Sobre

Página única, estática e sem build step, pensada como **referência técnica** em Android em escala e em carreira em programação. O conteúdo cobre sistemas em plataformas que protegem **mais de 1 milhão de dispositivos corporativos**, cases de engenharia (MDM, WebRTC, browser seguro, Android Enterprise Recommended), mentoria e FAQ orientado a SEO/AEO.

O design segue uma identidade editorial minimalista — fundo papel (`#F6F5F3`), tipografia Instrument Sans + IBM Plex Mono e o detalhe da **rosa dos ventos** como marca visual.

| | |
| --- | --- |
| **1M+** | Dispositivos corporativos gerenciados por sistemas construídos |
| **9+** | Anos de engenharia Android (código desde 2013) |
| **7** | Certificações Google Android Enterprise (até Expert) |
| **20K+** | Usuários no Local Chat, produto cofundado e lançado |

---

## O que o site entrega

### Experiência

- **Hero** com rosa dos ventos animada e CTAs para conversa e cases
- **Métricas** com contadores animados ao entrar na viewport
- **Quatro cases** com diagramas SVG interativos (replay no clique):
  1. **MDM** — gestão completa de dispositivos sobre AOSP
  2. **Remote Cast** — controle remoto em tempo real com WebRTC
  3. **Secure Browser** — navegador corporativo em camadas
  4. **Android Enterprise Recommended** — ~58 features para o selo global
- **Capacidades**, **sobre**, **recomendações** e faixa cinematográfica
- **FAQ** amplo (carreira, Android Enterprise, entrevistas técnicas)
- **Contato** com e-mail e WhatsApp

### Interação

| Recurso | Comportamento |
| --- | --- |
| **Compass HUD** | Indicador flutuante da seção atual; clique avança para a próxima |
| **EN / PT** | Alternância de idioma no cliente (preview); produção prevê rotas `/en` e `/pt` |
| **Reveal** | Entrada suave dos blocos via `IntersectionObserver` |
| **Diagramas** | Traçado animado na primeira visibilidade; clique redesenha |
| **Botões magnéticos** | Micro-movimento no hover (ponteiro fino) |
| **`prefers-reduced-motion`** | Animações reduzidas quando o SO pede |

### SEO e descoberta

- Meta tags Open Graph e Twitter Card (`assets/brand/og.jpg` 1200×630)
- JSON-LD: `WebSite`, `ProfilePage`, `Person` e `FAQPage`
- Rotas canônicas `/en/` e `/pt/` com `hreflang` (root redireciona para `/en/`)
- HTML enxuto (~50 KB por idioma); CSS, JS, fotos e diagramas em `/assets` com cache HTTP
- `robots.txt` com Allow explícito para bots de IA (GPTBot, ChatGPT-User, ClaudeBot, …)
- `sitemap.xml`, `llms.txt`, IndexNow e checklist em `DISCOVERY.md`
- Web app manifest e favicon SVG + PNG
- Locales `en_US` e `pt_BR`

---

## Estrutura do repositório

```text
gustavolevandowski-site/
├── src/index.html          # Fonte bilíngue (editar aqui)
├── en/index.html           # Build EN — página indexável
├── pt/index.html           # Build PT-BR — página indexável
├── assets/
│   ├── css/main.css        # Design system + layout
│   ├── js/main.js          # Interações (HUD, reveals, diagramas, i18n routes)
│   ├── img/                # Fotos (ex-base64)
│   ├── diagrams/           # SVGs dos cases
│   └── brand/              # favicon, og.jpg, og-card.html
├── _redirects              # / → /en/, legacy brand paths, llms
├── _headers                # Cache de HTML vs assets
├── netlify.toml            # Build: i18n + IndexNow
├── .github/workflows/      # CI: build + IndexNow pós-deploy
├── site.webmanifest
├── robots.txt
├── sitemap.xml
├── llms.txt
├── DISCOVERY.md
├── requirements.txt
├── scripts/                # build_i18n.py, submit_indexnow.py
└── README.md
```

Depois de editar `src/index.html`, a pipeline gera `/en` e `/pt` no Netlify (e no GitHub Actions). Localmente:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_i18n.py
```

Faça commit de `en/`, `pt/` e `sitemap.xml` se quiser pré-visualizar no Git sem build; o deploy sempre reconstrói. Assets em `/assets` são cacheados via `_headers`.

---

## Como rodar localmente

Gere as páginas de idioma e sirva a pasta do projeto:

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_i18n.py
python3 -m http.server 8080
```

Abra [http://localhost:8080/en/](http://localhost:8080/en/) (a raiz redireciona para `/en/` no Netlify).

> Abrir `src/index.html` por `file://` não carrega `/assets` nem os diagramas; use um servidor local.

---

## Regenerar o card Open Graph

O `assets/brand/og.jpg` é exportado a partir de `assets/brand/og-card.html` (canvas fixo 1200×630).

1. Abra `assets/brand/og-card.html` no navegador (idealmente em 1200×630 ou com zoom 100%).
2. Capture a viewport (DevTools → device metrics, ou ferramenta de screenshot full-page limitada ao body).
3. Exporte como JPEG de qualidade alta e substitua `assets/brand/og.jpg`.
4. As meta tags apontam para:

```text
https://gustavolevandowski.com/assets/brand/og.jpg
```

Paths legados `/og.jpg`, `/favicon.svg` e `/favicon.png` redirecionam para `assets/brand/`.

---

## Design system (tokens)

| Token | Valor | Uso |
| --- | --- | --- |
| Surface | `#F6F5F3` | Fundo papel |
| Ink | `#161513` | Texto principal |
| Ink muted | `#6E6B66` / `#A3A099` | Secundário |
| Gold | `#B08C4A` | Destaque e marca |
| Hairline | `#E8E6E2` | Bordas |
| Display | Instrument Sans | Títulos e corpo |
| Mono | IBM Plex Mono | Labels, nav, métricas |

A rosa dos ventos (compass rose) aparece no hero, no HUD, no favicon e no card OG — é o fio visual do projeto.

---

## Seções da página

```text
Nav (fixa) + toggle EN/PT
│
├── Hero
├── Proof (métricas)
├── Work (4 cases + diagramas)
├── Capabilities
├── About
├── Endorsements
├── Field (faixa visual)
├── FAQ
├── Contact
└── Footer
```

O HUD da bússola acompanha a seção sob o centro da viewport e permite pular para a próxima com um clique (ou Enter/Espaço).

---

## Deploy

Qualquer host de arquivos estáticos serve o projeto:

- [GitHub Pages](https://pages.github.com/)
- [Cloudflare Pages](https://pages.cloudflare.com/)
- [Netlify](https://www.netlify.com/)
- [Vercel](https://vercel.com/)
- Bucket S3 / qualquer CDN

Publique a raiz do repositório. Em produção, `/` redireciona para `/en/`; as páginas indexáveis são `/en/` e `/pt/` com `hreflang`. A fonte bilíngue fica em `src/index.html` e é buildada na pipeline.

---

## Contato

| Canal | Link |
| --- | --- |
| Site | [gustavolevandowski.com](https://gustavolevandowski.com) |
| E-mail | [contato@gustavolevandowski.com](mailto:contato@gustavolevandowski.com) |
| LinkedIn | [linkedin.com/in/levandowski](https://www.linkedin.com/in/levandowski/) |
| Medium | [medium.com/@levandowski](https://medium.com/@levandowski) |
| LeCode | [movimentolecode.com](https://movimentolecode.com) |
| Instagram | [@lecode.oficial](https://www.instagram.com/lecode.oficial/) |

---

<p align="center">
  <img src="./assets/brand/favicon.svg" alt="" width="28" height="28"><br>
  <sub>EST 2013 · ANDROID 2017 · SC / BR · Remote, worldwide</sub>
</p>

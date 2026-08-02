# Descoberta em buscadores e LLMs

Checklist para o site pessoal (`gustavolevandowski.com`) ficar fácil de indexar no Google, Bing e ferramentas como ChatGPT.

## Já no repositório

- Rotas canônicas: `/en/` e `/pt/` (geradas por `scripts/build_i18n.py`)
- Root `/` redireciona para `/en/` (`_redirects`)
- `robots.txt` libera crawlers gerais e bots de IA (GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, PerplexityBot, …)
- `sitemap.xml` com hreflang EN/PT
- `llms.txt` + `/.well-known/llms.txt`
- IndexNow key na raiz + `scripts/submit_indexnow.py` (Bing e parceiros)

## Depois do deploy

### 1. Bing Webmaster (importante para ChatGPT)

1. Abra [Bing Webmaster Tools](https://www.bing.com/webmasters)
2. Adicione `https://gustavolevandowski.com`
3. Em **Sitemaps**, envie: `https://gustavolevandowski.com/sitemap.xml`
4. Em **URL Inspection** / **Submit URL**, envie também `/en/` e `/pt/`

### 2. Google Search Console

1. Abra [Google Search Console](https://search.google.com/search-console)
2. Adicione a propriedade do domínio ou da URL
3. Em **Sitemaps**, envie: `https://gustavolevandowski.com/sitemap.xml`
4. Peça indexação de `/en/` e `/pt/`

### 3. IndexNow (automático via script)

Com o site já no ar (incluindo o arquivo `{key}.txt` na raiz):

```bash
.venv/bin/python scripts/submit_indexnow.py
```

### 4. Backlinks manuais (LinkedIn, Medium, LeCode)

Publique o site pessoal como link canônico nestes perfis:

| Canal | Ação |
| --- | --- |
| LinkedIn | Website / Featured → `https://gustavolevandowski.com/en/` (ou `/pt/`) |
| Medium | About / links da bio → mesmo URL |
| LeCode (`movimentolecode.com`) | Link “Fundador” / “Sobre o mentor” → site pessoal |
| Empresa | Já aponta para o site pessoal em `levandowskistudio.com` |

## Regenerar páginas de idioma

Após editar o `index.html` bilíngue na raiz:

```bash
python3 -m venv .venv && .venv/bin/pip install beautifulsoup4
.venv/bin/python scripts/build_i18n.py
```

Faça commit de `en/`, `pt/` e `sitemap.xml` junto com a fonte.

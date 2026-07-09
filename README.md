# Claude Dev Plugin — Plugin de Sistemas Complexos

Plugin para o [Claude Code](https://claude.ai/code) com 8 especialistas autônomos que cobrem todo o ciclo de construção de sistemas complexos — da arquitetura ao deploy.

## Instalação

```bash
# Via Claude Code
/install-skill https://github.com/sidneydiaraujo/claude-dev-plugin
```

Ou copie as pastas de `skills/` para `~/.claude/skills/`.

---

## Skills incluídas

### `dev-product-builder` — Engenheiro Sênior Autônomo
O maestro do plugin. Age como sócio técnico que toma todas as decisões de desenvolvimento sozinho: escolhe stack, escreve e edita arquivos, instala dependências, roda testes, faz commit/push e aciona deploy — sem pedir aprovação para ações rotineiras.

**Aciona quando:** "cria", "constrói", "implementa", "faz um", "continua o projeto", "adiciona funcionalidade", "corrige bug", "faz o deploy"

---

### `system-architect` — Arquiteto de Sistemas
Projeta a estrutura geral do sistema com base no contexto real do projeto. Entrega diagramas Mermaid (C4, sequência, componentes), ADRs de decisão e comparativo de alternativas. Para apenas em mudanças arquiteturais irreversíveis.

**Aciona quando:** arquitetura, microserviços, monolito, CQRS, DDD, event-driven, "como estruturar esse sistema"

---

### `api-designer` — Designer de APIs
Define contratos REST, GraphQL e gRPC seguindo os padrões do projeto existente. Entrega especificação OpenAPI 3.0 completa com exemplos de request/response, status codes e tratamento de erros. Auto-corrige CORS aberto e endpoints sem autenticação.

**Aciona quando:** endpoint, REST, GraphQL, OpenAPI, Swagger, "como modelar essa rota"

---

### `db-expert` — Especialista em Banco de Dados
Modela schemas, escolhe o banco certo para o problema e otimiza queries. Entrega SQL pronto com índices, constraints e migrations. Avisa antes de operações destrutivas e auto-corrige padrões de SQL injection.

**Aciona quando:** banco de dados, schema, modelagem, SQL, MongoDB, PostgreSQL, Redis, "qual banco usar"

---

### `ux-ui-designer` — Designer UX/UI
Cria interfaces com linguagem visual autoral quando não há design system, ou adapta ao Tailwind, shadcn/ui, Material UI, Ant Design, etc. quando existente. Entrega código funcional (JSX/TSX ou HTML/CSS) com responsividade, estados e acessibilidade embutidos.

**Aciona quando:** UI, UX, tela, layout, componente, wireframe, "cria uma interface de", design system

---

### `devops-engineer` — Engenheiro DevOps
Containeriza aplicações com Docker (multi-stage, non-root, sem secrets hardcoded), configura pipelines CI/CD (GitHub Actions, GitLab CI, Azure DevOps) e infraestrutura como código. Para antes de deploys em produção e operações com custo.

**Aciona quando:** Docker, CI/CD, pipeline, deploy, Dockerfile, Kubernetes, Terraform, "como automatizar"

---

### `security-reviewer` — Revisor de Segurança
Analisa a superfície de ataque usando o OWASP Top 10. Corrige imediatamente SQL injection, XSS, credentials hardcoded, CORS aberto e endpoints sem auth — e informa o que foi corrigido. Demais achados vão no relatório estruturado com severidade e código corrigido.

**Aciona quando:** segurança, vulnerabilidade, OWASP, JWT, OAuth, "isso é seguro?", "como proteger"

---

### `tech-writer` — Escritor Técnico
Lê a documentação existente antes de criar qualquer coisa. Produz ADRs, READMEs, specs de feature, runbooks e diagramas Mermaid. Documenta o *porquê* das decisões, não o *o quê* que o código já diz.

**Aciona quando:** documentação, ADR, README, diagrama, "escreve uma spec", "documenta essa decisão"

---

## Regras operacionais compartilhadas

Todas as skills do plugin seguem as mesmas regras:

| Regra | Comportamento |
|---|---|
| **Idioma** | Sempre em português do Brasil |
| **Contexto primeiro** | Lê arquivos existentes do projeto antes de propor qualquer coisa |
| **Autonomia** | Age sem pedir confirmação para ações rotineiras da sua área |
| **Protocolo de risco** | Para e avisa apenas em ações irreversíveis, produção, custos ou quebra de contrato |
| **Auto-correção** | Corrige e informa issues críticos de segurança em vez de apenas reportar |
| **Entregável completo** | Código/artefato funcional e pronto — nunca sugestão incompleta |

### Sinais de alerta padronizados

```
⚠️ [Descrição simples do risco e impacto]. [Pergunta ou confirmação de como proceder]
```

---

## Fluxo de trabalho sugerido

```
system-architect → api-designer + db-expert → dev-product-builder + ux-ui-designer → security-reviewer → devops-engineer → tech-writer
```

Cada skill é acionada pelo contexto — não é necessário invocar manualmente.

---

## Stack suportado

Node.js · TypeScript · Python · FastAPI · Django · Java · Spring Boot · .NET · C#  
React · Next.js · Vue · Tailwind CSS · shadcn/ui · Material UI  
PostgreSQL · MongoDB · Redis · MySQL · SQLite · Prisma  
Docker · GitHub Actions · GitLab CI · Azure DevOps · Terraform  
AWS · Azure · GCP · Vercel · Railway · Fly.io

---

## Autor

Sidney de Araujo Silva — [@sidneydiaraujo](https://github.com/sidneydiaraujo)

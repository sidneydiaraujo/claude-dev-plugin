# time-dev: time de desenvolvimento para o Claude Code

Time de desenvolvimento para o [Claude Code](https://claude.com/claude-code), em português do Brasil: **10 skills especialistas** que cobrem o ciclo de um sistema, da ideia ao deploy, e **2 agents revisores** que dão uma segunda opinião sem o viés de quem escreveu o código.

## Instalar

### Como plugin (recomendado)

Dentro do Claude Code:

```
/plugin marketplace add sidneydiaraujo/claude-dev-plugin
/plugin install time-dev@sidneydiaraujo
```

Para atualizar depois: `/plugin marketplace update sidneydiaraujo`.

### Cópia manual

```bash
git clone https://github.com/sidneydiaraujo/claude-dev-plugin.git
cp -r claude-dev-plugin/skills/* ~/.claude/skills/
cp claude-dev-plugin/agents/*.md ~/.claude/agents/
```

No Windows (PowerShell):

```powershell
git clone https://github.com/sidneydiaraujo/claude-dev-plugin.git
Copy-Item -Recurse claude-dev-plugin\skills\* $HOME\.claude\skills\
Copy-Item claude-dev-plugin\agents\*.md $HOME\.claude\agents\
```

## Skills

| Skill | Para quê |
|---|---|
| `dev-product-builder` | Sócio técnico: constrói, testa, commita e faz deploy, pedindo aprovação só em risco crítico |
| `system-architect` | Arquitetura e trade-offs, com diagramas Mermaid e ADRs |
| `api-designer` | Contratos REST, GraphQL e gRPC |
| `db-expert` | Modelagem, queries, migrações e conciliação de números |
| `ux-ui-designer` | Telas fiéis à referência, com prova em screenshot |
| `qa-engineer` | Estratégia e escrita de testes, incluindo testes-ouro de regressão |
| `devops-engineer` | Docker, CI/CD e infraestrutura como código |
| `security-reviewer` | Segurança enquanto o código é escrito |
| `tech-writer` | ADR, README, diagramas e especificações |
| `dev-prompt-engineer` | Transforma um pedido solto em prompt técnico completo |

Todas seguem dois protocolos comuns em `skills/_shared/`:

- **Comunicação e risco:** quando agir sozinho e quando parar e perguntar.
- **Métricas:** todo número derivado de dado (Jira, banco, API) vem com o rastro do cálculo e um teste que prova a regra.

## Agents

Rodam em contexto isolado e **só leem e relatam**, sem editar nada:

| Agent | Para quê |
|---|---|
| `security-reviewer` | Revisão de segurança independente antes de deploy ou após mexer em autenticação |
| `test-coverage-auditor` | Mapa do que está sem teste e qual o risco real disso |

## Templates

| Pasta/arquivo | Para quê |
|---|---|
| `templates/eslint/` | 3 regras ESLint testadas: teto de 350 linhas, sem `console` direto e tela sem acesso direto ao banco. Inclui configs e `verify.mjs`. Cópia revisada do [vibe-coding-toolkit](https://github.com/soumatheusgomes/vibe-coding-toolkit) (MIT). |
| `templates/check_max_lines.py` | O mesmo teto de linhas para C#, Python, HTML/SCSS e SQL, com linha de base. |

O `dev-product-builder` usa esses templates pelo guia `skills/dev-product-builder/references/qualidade-e-refatoracao.md`.

## Personalize sem editar as skills

As skills são genéricas. O seu contexto fica em arquivos opcionais, em `~/.claude/skills/_local/` (ou na pasta de configuração que você usa):

| Arquivo | O que colocar |
|---|---|
| `como-o-usuario-pede.md` | Como você costuma pedir: quando "valide" é só análise, como separa vários pedidos numa mensagem |
| `ux-ui-designer.md` | Seu dicionário visual ("moderno", "discreto"...), design system e preferências |
| `protocolo-metricas.md` | Regras de métricas dos seus projetos |
| `<nome-da-skill>.md` | Qualquer complemento para uma skill específica |

O contexto de cada projeto fica no `CLAUDE.md` e no `docs/` do próprio projeto. As skills leem esses arquivos primeiro.

## Licença

[MIT](LICENSE).

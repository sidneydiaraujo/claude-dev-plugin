# Protocolo compartilhado — Comunicação e Risco

Bloco comum a todas as skills do conjunto `dev-product-builder` (system-architect,
api-designer, db-expert, ux-ui-designer, qa-engineer, devops-engineer,
security-reviewer, tech-writer). Cada skill referencia este arquivo em vez de
repetir o texto — mudar uma regra aqui vale para todas, sem precisar editar
9 arquivos. Cada skill mantém, no seu próprio SKILL.md, só os casos de risco
*específicos* da sua área (esses não são genéricos e não pertencem aqui).

## Caminhos

`$CLAUDE_CONFIG_DIR` nestes arquivos = pasta de configuração ativa do Claude
Code. Se a variável de ambiente não estiver definida, é `~/.claude`. Nunca
leia `_local/` de outra pasta de configuração que não a ativa: cada conta tem
o seu, e eles não se misturam.

## Leitura obrigatória complementar

- `$CLAUDE_CONFIG_DIR/skills/_local/como-o-usuario-pede.md` (opcional, se existir): como
  interpretar os pedidos do usuário (quando é só análise × implementar, mensagens com vários
  itens, hipótese × instrução). Vale para **todas** as skills.
- `protocolo-metricas.md`: obrigatório sempre
  que a tarefa calcular, exibir, explicar ou validar um número derivado de
  dado de origem (Jira, banco, API), ou mapear um campo dessa origem.

## Contexto do projeto e overlays locais

Estas skills são genéricas e servem a vários projetos sem relação entre si.
Contexto de um projeto específico (marca, telas, regras de negócio, caminhos)
**não** mora aqui:

1. Leia primeiro o `CLAUDE.md` e a pasta `docs/` do projeto em que você está
   trabalhando. É lá que mora o contexto daquele projeto.
2. Se existir `$CLAUDE_CONFIG_DIR/skills/_local/<nome-da-skill>.md`, leia também. São
   complementos desta máquina, fora do repositório das skills.
3. **Não misture projetos:** referência visual, regra ou dado de um projeto
   nunca é aplicado em outro sem o usuário pedir. Na dúvida sobre qual
   projeto é o atual, olhe o diretório de trabalho.
4. Ao melhorar uma skill, mantenha o texto genérico. Se a melhoria só vale
   para um projeto, ela vai para o `docs/` daquele projeto ou para o overlay
   em `_local/`, não para o SKILL.md.

## Comunicação

- Fale sempre em **português do Brasil**, inclusive nas mensagens curtas
  entre uma ferramenta e outra.
- Antes de uma tarefa maior, diga o plano em 1-2 linhas antes de executar.
- Updates curtos durante o trabalho, no gerúndio: "Analisando X..." / "Escrevendo Y...".
- Entregue artefatos prontos para uso (código, SQL, YAML, spec) — nunca
  esqueletos com `// TODO` ou pseudocódigo.
- Nunca explique o que é óbvio; justifique só decisões não-triviais.
- Ao terminar, confirme o que foi entregue em 2-3 linhas.
- Faça UMA pergunta de esclarecimento apenas se for genuinamente bloqueante
  — decida e siga em qualquer outro caso.

## Consciência de custo (uso via API paga por token)

Antes de disparar um **Agent** dedicado (contexto isolado — `security-reviewer`,
`test-coverage-auditor`, ou qualquer outro futuro) ou um **Workflow** com
múltiplos agentes, diga em uma frase o que vai rodar e por quê, para o usuário
acompanhar o gasto — sobretudo se o saldo de créditos estiver baixo (pergunte
ou releia o contexto da conversa se não souber). Isso não se aplica ao trabalho
normal dentro da própria skill (que já faz parte da conversa em andamento).

## Auto-correção de problemas críticos de segurança

Independente da área da skill, se você encontrar durante o trabalho um destes
problemas, corrija antes de continuar e informe — não é opcional para nenhuma
skill:

- SQL/NoSQL/command injection (input sem parametrização/sanitização)
- Credenciais, tokens ou chaves hardcoded no código ou versionadas
- Endpoints sem autenticação que claramente deveriam ter
- CORS aberto (`*`) em API com dados sensíveis
- Tokens ou dados sensíveis sendo logados

Formato da mensagem:

> ⚠️ Encontrei um risco de segurança: **[problema, em uma frase]**. Corrigi antes de continuar.

## Quando parar e sinalizar (genérico)

Além dos casos específicos que cada skill já lista no seu próprio arquivo,
pare sempre antes de:

- Qualquer perda de dados irreversível
- Deploy em produção
- Push direto em `main`/`master` sem PR
- Ações que geram custo em serviços pagos de terceiros

Linguagem simples, foco no impacto prático, sem jargão — o usuário decide, você não assume.

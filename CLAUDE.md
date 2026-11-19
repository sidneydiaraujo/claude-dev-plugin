# claude-dev-plugin (plugin `time-dev`)

Repositório **público** com a versão aberta das skills e agents de desenvolvimento.

## Regra principal

**Não edite as skills aqui.** A fonte é um repositório privado; este é gerado por
script, que tira o que é pessoal (nomes, caminhos de máquina, preferências
individuais). Mudança feita direto aqui some na próxima geração.

Exceções que se editam aqui: `README.md`, `LICENSE`, `CLAUDE.md` e `.claude-plugin/`.

## Publicar uma versão nova

1. Gere a versão pública a partir da fonte (script `publicar-plugin.py` da fonte).
2. Revise o diff: nada de nomes de pessoas, empresas, clientes ou caminhos locais.
3. Suba a `version` em `.claude-plugin/plugin.json`, commit e push.

## Regras de conteúdo

- Tudo em português do Brasil.
- Contexto pessoal ou de projeto não entra: ele mora em overlays
  `$CLAUDE_CONFIG_DIR/skills/_local/` de quem usa.

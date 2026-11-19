# Qualidade contínua: régua, refatoração por tamanho e queima de avisos

Leia este guia quando o pedido for "instala a régua/lint/quality gate", "quebra
os arquivos grandes", "zera os avisos", ao iniciar um projeto novo, ou quando
for editar um arquivo acima de 350 linhas. Fora disso, não precisa.

Ferramentas prontas (pasta `templates/` do repositório deste plugin):
- `eslint/` — 3 regras ESLint já testadas (`quality/max-lines`,
  `quality/no-direct-console`, `quality/no-direct-data-access`) + configs de
  exemplo + `verify.mjs`. Cópia revisada do vibe-coding-toolkit (MIT), commit
  `13add21`. **Copie byte a byte, nunca reescreva** — regra escrita na hora
  erra em silêncio.
- `check_max_lines.py` — o mesmo teto para o que o ESLint não cobre (C#,
  Python, `.html`/`.scss` do Angular, SQL), com linha de base.

## Princípios (valem nos três modos)

1. **Verdade por comando.** Toda contagem (avisos, arquivos acima do teto,
   testes) vem de um comando rodado agora. Nunca de memória, mensagem anterior
   ou soma mental. Saída cortada por wrapper → rode a invocação direta.
2. **Medir antes de mudar.** Regra com zero violação nasce como erro; regra
   com violação nasce como aviso, com a contagem anotada ao lado (linha de
   base). A migração termina quando a contagem chega a zero e a regra volta a
   erro. Gate que nasce vermelho em código antigo vira ruído e é desligado.
3. **Nunca subir o teto para passar.** Infrator conhecido vai para o `ignore`
   da regra ou para `.max-lines-baseline`. Teto padrão: 350 linhas.
4. **Afrouxar uma regra é mudança de configuração**, nunca "código mais
   limpo". Diga isso explicitamente no relatório e no commit.
5. **Decisão cara ou arriscada → opções e espera.** Diferente do prompt
   original, não assuma uma opção por padrão: mostre os números, as opções e
   a recomendação, e espere o usuário naquela área. O resto segue.
6. **Critério de sucesso é comando + saída esperada**, e o checklist final
   só é marcado rodando de novo.
7. **Zero mudança de comportamento.** Correção que não é mecânica (extrair,
   renomear, mover) sai do lote e vira item separado para revisão.

## Modo 1 — Instalar a régua (só mede, não corrige nada)

Antes: leia o projeto e relate gerenciador de pacotes, versão do linter,
linguagem, raiz do código, camada de apresentação, módulo de dados e
adaptador de log. Descubra os comandos de lint/teste/typecheck/build no
`package.json`, `*.csproj`/`*.sln` ou `pyproject.toml`.

### JavaScript / TypeScript (Node, Next.js, React)
1. Exige ESLint 9+ (usa `defineConfig`/`globalIgnores`). ESLint 8 → pare e avise.
2. Copie `eslint-rules/*.cjs`, `eslint.config.mjs.example` → `eslint.config.mjs`,
   `eslint.typed.config.mjs.example` (só TS), `verify.mjs`.
3. `npm i -D eslint@^9 @eslint/js@^9` (+ `typescript-eslint` em TS). **Fixe
   `@eslint/js` no mesmo major do eslint**, senão dá ERESOLVE.
4. Adapte a config ao projeto real: globs, `max: 350`, `modules`/`bindings`/
   `layers` do acesso a dados (sem módulo de dados → remova a regra), bloco de
   `console` liberado só no adaptador de log, `globalIgnores` do build.
5. Duas armadilhas silenciosas: bloco que desliga regra tem que vir **depois**
   do que liga; `except` em zona de `no-restricted-paths` é relativo a `from`.
6. Scripts: `lint`, `lint:fix`, `lint:types` (o tipado fica fora do pre-commit,
   é lento).
7. `node verify.mjs` → três linhas `: ok`. Só então confie em qualquer contagem.
   Depois apague o `verify.mjs` ou ligue-o ao script de teste.

### Angular
1. `ng add @angular-eslint/schematics` (versão com o mesmo major do Angular;
   se não existir, pare e avise). Ele cria a config flat e o alvo `ng lint`.
2. Acrescente o plugin `quality` do `templates/eslint` nos arquivos `.ts`.
   Remova `no-direct-data-access` (Angular busca dados por serviço/HttpClient).
   `no-direct-console`: libere só no serviço de log, se houver.
3. Templates e estilos: `python check_max_lines.py --ext .html .scss`.
4. Testes Karma sem watch: `ng test --watch=false --browsers=ChromeHeadless`.

### C# / .NET
1. Em `Directory.Build.props`: `<AnalysisLevel>latest-recommended</AnalysisLevel>`
   e `<EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>`.
2. Meça: `dotnet build --no-incremental` e conte os avisos por id (CAxxxx,
   IDExxxx). **Não ligue `TreatWarningsAsErrors` global em código existente.**
   Ids com zero ocorrência vão para `<WarningsAsErrors>`; os demais ficam
   como aviso com a contagem anotada num comentário do props.
3. Estilo: `dotnet format --verify-no-changes`.
4. Teto: `python check_max_lines.py --ext .cs`.

### Python
1. `ruff`: `ruff check --statistics` para medir; `ruff format --check`.
   `T201` (proíbe `print`) é o equivalente ao `no-direct-console`.
2. Ruff não tem nível "aviso": regras com zero violação entram em `select`;
   as com violação ficam fora, com a contagem num comentário do `pyproject.toml`.
3. Teto: `python check_max_lines.py --ext .py`. Tipos: `mypy`/`pyright` se já houver.

### Relatório do Modo 1
Regras instaladas e puladas (e por quê), contagem por regra, quais nasceram
como aviso com linha de base, arquivos acima do teto do maior para o menor, e
os comandos exatos para rodar. **Pare aqui.** Corrigir é outro trabalho.

## Modo 2 — Quebrar arquivos grandes

1. **Verdade:** rode o lint/`check_max_lines.py` agora e liste os infratores
   com contagem real, do maior para o menor.
2. **Lote de 3**, os maiores. Para cada um, antes de editar: responsabilidade
   em uma frase, costuras encontradas e onde vai cortar, exports públicos.
3. **Corte por responsabilidade, nunca por número de linha.** Costuras, nesta
   ordem: regra de negócio misturada em tela/rota → serviço de domínio; bloco
   de UI repetido → subcomponente; acesso a dados → repositório/adaptador;
   aglomerado de helpers de um conceito → módulo utilitário daquele domínio.
   Sem costura natural → diga "sem costura natural", não mexa, siga. Arquivo
   `utils/helpers/misc/common` com as sobras é fracasso.
4. **Preserve a interface:** os exports/assinaturas públicos continuam iguais.
   TS: o arquivo original reexporta. Python: o módulo original (ou
   `__init__.py`) reexporta. C#: classes e métodos públicos mantidos;
   registre os novos serviços na DI. `partial class` **não** é divisão — só
   esconde o tamanho.
5. **Código de cálculo/métrica** (ex.: o utilitário que calcula durações): antes de mexer,
   testes-ouro com `qa-engineer` e grep de todos os consumidores, seguindo o
   protocolo de métricas. Sem teste, não quebra.
6. **Um arquivo por vez:** dividir → typecheck (`tsc --noEmit`/`ng build`/
   `dotnet build`/`mypy`) → testes → lint + teto (o arquivo saiu da lista e
   nada novo apareceu) → commit nomeando o arquivo e a costura. Falhou? Corrige
   antes de seguir. Push só no fim do lote.
7. Armadilhas: a função extraída pode estourar o teto do arquivo novo; a
   extração pode mudar o tipo inferido de retorno (aparece como erro de tipo).
   Ambas se resolvem no mesmo commit.
8. **Pare após 3** e relate: divididos e costura usada, não divididos e por
   quê, contagem final rodada de novo, efeitos colaterais em outras regras.
   Tire da linha de base os arquivos que passaram a caber.

## Modo 3 — Zerar avisos restantes

0. **Verdade:** lint agora, total por regra e por arquivo.
1. **Portão de decisão:** ache a parte mais cara/arriscada (uma regra
   concentrada em poucos arquivos difíceis), com números reais. Opções:
   (A) corrigir tudo; (B) corrigir a maioria e registrar o resto como dívida
   visível (comentário + item no backlog), nunca supressão silenciosa;
   (C) mudar o escopo da regra — ⚠️ mudança de config, dito assim. Recomende
   uma e **espere o usuário nessa área**; o restante segue.
2. **Critérios em comando:** `lint` com 0 avisos (ou o número combinado),
   typecheck limpo, testes verdes, build ok, zero mudança de comportamento.
3. **Execução:** em sessão, por grupos de arquivos. Ondas paralelas com vários
   agentes só com aprovação, avisando o custo antes (protocolo comum).
4. **Armadilhas** (cache de lint que não invalida, arquivo já no limite do
   teto, extração que alarga o tipo, fixture compartilhada): se usar agente,
   copie a lista **literalmente** no briefing — ele não vê esta conversa.
5. **Revisão:** área de auth/dinheiro/dados sensíveis → agent
   `security-reviewer`; lógica alterada sem teste → agent `test-coverage-auditor`.
6. **Checklist final, marcado só rodando de novo:** lint, typecheck, testes,
   build; lista de cada `eslint-disable`/`noqa`/`#pragma` adicionado com
   justificativa (ou vazia); lista de correções não mecânicas separadas (ou vazia).

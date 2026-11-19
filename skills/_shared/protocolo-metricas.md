# Protocolo de métricas e cálculos derivados

Vale para qualquer skill ou agente que calcule, exiba ou explique um número
derivado de dado de origem (Jira, banco, API externa, planilha): durações,
dias úteis, contagens, totais, datas de início/fim, percentuais. Existe porque
número errado dado com confiança é pior que "não sei". As causas típicas:
- regra reescrita sem checar a anterior;
- a mesma fórmula copiada em vários lugares;
- número dado sem rastro;
- campo ou filtro da origem presumido pelo nome.

> Contexto local: se existir `$CLAUDE_CONFIG_DIR/skills/_local/protocolo-metricas.md`,
> leia também. Ele traz regras de projetos específicos desta máquina, que não
> ficam neste repositório.

## 1. Antes de mexer: ler a regra vigente

Procure no projeto o registro de decisões de métricas (ex.:
`docs/METRICAS-DECISOES.md`) e a documentação de cálculo. Se não existir e a
métrica for importante, proponha criar. Depois, reescreva a regra em 3 linhas:

```
Métrica: <nome> (<contexto>)
Começa: <evento exato> · Termina: <evento exato>
Exclui: <o que não conta> · Unidade: <dias corridos, dias úteis, horas…>
```

## 2. Checar conflito

Se o pedido novo contradiz uma decisão registrada, **não implemente em
silêncio**. Mostre as duas falas com data e pergunte qual vale e em qual
contexto. Uma pergunta, com recomendação.

## 3. Todo número com rastro

Ao validar ou explicar um valor, mostre sempre:

```
<item> · <métrica>
Eventos de origem: <data/hora e evento, um por linha>
Regra aplicada: <início, fim, como conta o primeiro e o último dia>
Descontos: <o que saiu e por quê>
Conta: <aritmética explícita>
Sistema mostra: <valor> ✓  (ou: mostra <outro> ✗ → causa: …)
```

Nunca diga "está correto" ou dê um número sem essa conta. Se o dado não
estiver acessível, diga "não consegui verificar porque …".

## 4. Vínculo com a origem

- Cite o identificador exato do campo (ex.: `customfield_XXXXX` no Jira, a
  coluna no banco) e confirme num registro real antes de usar. Não presuma
  pelo nome.
- Ao contar itens, mostre a **consulta exata** usada (JQL, SQL, filtro). Se o
  número diferir do número de referência do usuário, concilie item a item e
  diga a diferença de filtro.
- Eventos automáticos (segundos após a criação) não são trabalho humano.

## 5. Um motor só

A regra mora num único lugar (normalmente o backend). Telas, e-mails,
relatórios e rotinas **consomem o valor pronto**, sem recalcular. Ao mudar
uma regra:
- `grep` pela métrica em todo o projeto e liste todos os lugares que calculam;
- se houver cópia, mude o motor e faça as cópias usarem o motor, ou avise
  explicitamente quais ficaram divergentes.

## 6. Exemplo do usuário vira teste-ouro, antes da correção

Todo caso concreto (item + datas + número esperado) vira teste com o nome do
item e o valor dito, e **o teste tem que falhar antes da correção**. Chame a
skill `qa-engineer` para isso quando a regra for nova.

## 7. Depois de mudar: tabela de números que mudaram

Recalcule 3 a 5 itens reais (o citado e outros do mesmo tipo), antes e
depois, e entregue:

| Item | Métrica | Antes | Depois | Por quê |
|---|---|---|---|---|

Número que mudou sem explicação é regressão. Rode a suíte inteira de testes,
não só o teste novo.

## 8. Registrar

No mesmo commit: nova linha no registro de decisões (data + fala do usuário
+ contexto) e ajuste na documentação da métrica.

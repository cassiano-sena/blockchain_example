# Enunciado do trabalho

Execute o seguinte teste e faça o que é pedido.

## Cenário de teste

Dado 2 computadores participando da rede.

Realize as seguintes operações em sequência
1. Computador 1: minera 2 blocos em sequência
2. Computador 1: transfere 10 moedas para Computador 2

Agora, realize as seguintes operações em paralelo (deve ser solicitado ao mesmo tempo, ou quase ao mesmo tempo, para ambos computadores)
3. Computador 1: minera 1 bloco
4. Computador 2: minera 1 bloco

Por fim, realize o seguinte
5. Computador 1: verifica estado da blockchain
6. Computador 2: verifica estado da blockchain

## Verificação dos resultados:

O computador que finalizar a mineração primeiro deverá ver algo assim:
Index: 0, Hash: 0...,          Tx: 0
Index: 1, Hash: 000024f3c0..., Tx: 1
Index: 2, Hash: 000087593f..., Tx: 1
Index: 3, Hash: 0000b110ba..., Tx: 2

O computador que finalizar a mineração por último verá dois blocos com o mesmo índice (Index 3), mostrando uma inconsistência.
Index: 0, Hash: 0...,          Tx: 0
Index: 1, Hash: 000024f3c0..., Tx: 1
Index: 2, Hash: 000087593f..., Tx: 1
Index: 3, Hash: 0000b110ba..., Tx: 2
Index: 3, Hash: 0000f190c7..., Tx: 2

## Análise

Esses resultados nos mostram que houve uma inconsistência na blockchain pois os indexes deveriam ser sequênciais e únicos.

## Tarefa

Identifique a causa do erro e como é chamado esse tipo de problema. Em seguida, pesquise por soluções adotadas para este tipo de problema em moedas digitais e selecione um método e faça uma implementação para corrigir esse problema.

Monte um relatório contendo:

1. A verificação inicial com estado inconsistente pelos computadores 1 e 2
2. Apresente o raciocínio para a causa do erro
3. Apresente os métodos mais utilizados para resolver tal problema
4. Selecione um método e faça sua implementação para corrigir o erro e manter a consistência da blockchain.
4. Apresente os novos resultados

Ao final, faça público o seu código no github e grave uma apresentação explicando as alterações realizadas.

## Critério de avaliação

1. Justificativa para causa do erro
2. Método selecionado para correção do erro
3. Corretude da solução
4. Qualidade do relatório, código e apresentação.


## Pontos extras:

Para aqueles que estiverem interessados em ganhar ponto extra, segue algumas outras sugestões de melhorias:

1. Possibilitar que 1 novo par descubra os pares atuais participantes da rede a partir de um único par (easy)
2. Verificar se alguém tentando fazer uma transação possui saldo para tal (hard)
3. Garantir que alguém tentando fazer uma transação não esteja utilizando uma moeda já gasta (medium)
4. Possibilitar múltiplas conexões de clientes paralelas na thread do servidor (easy)

Caso você descubra outras vulnerabilidades e pontos de melhoria, apresente-ás. Você ganhará ponto extra por isso. 
# Importação, cores e validação

## Acesso rápido

Use a barra FreeCAD Bridge ou os comandos equivalentes em Extensões. STEP inicia conversão; JSON importa uma conversão existente. Os dois atalhos ficam indisponíveis enquanto houver conversão em andamento. Veja [barra de ferramentas](BARRA_DE_FERRAMENTAS.md).

Para conferir instalação sem converter STEP, abra [o exemplo sintético](../examples/tetraedro_vermelho.json) pelo ícone JSON. O teste de exemplo não comprova a validade de arquivos CAD externos.

## Preparar no FreeCAD

1. Confira que cada peça a importar resulta em pelo menos um sólido.
2. Atribua nomes claros aos objetos e selecione o conjunto pretendido.
3. Exporte STEP com nomes e cores conforme os recursos da versão do CAD.
4. Reabra o STEP e confira contagem, posições e cores.

A extensão lê STEP, não `.FCStd`. Metadados que não foram exportados ficam fora de seu alcance. Objetos extras ou ocultos dependem do que foi gravado no arquivo.

## Importar

No contexto desejado do SketchUp, execute **Extensões → FreeCAD Bridge → Importar STEP automaticamente**. Selecione `.step` ou `.stp`, desvio linear e modo. A conversão roda em processo separado; a criação das faces no SketchUp ocorre depois e ainda pode levar tempo.

Mantenha o mesmo modelo e contexto de edição durante a conversão. Se mudarem, a inserção é interrompida. Há uma conversão por vez e limite de dez minutos.

## Qualidade

O desvio linear está em milímetros. Padrão `0,05 mm`; intervalo aceito de `0,001` a `5 mm`. Valores menores normalmente aumentam faces e custo, sem relação linear garantida. Comece pelo padrão e refine apenas quando necessário. Menor desvio não garante reparar topologia.

## Modos

**Estrito:** exige CAD válido e malha fechada no conversor; o SketchUp também verifica cada componente final. Uma falha final desfaz toda a operação.

**Visualização:** permite os melhores resultados disponíveis e registra avisos. `[VERIFICAR]` identifica falha no componente final ou nos indicadores de origem. A aparência correta não comprova fechamento.

## Relatório

| Campo | Interpretação |
| --- | --- |
| Índice STEP | Posição enumerada nesta execução; não é um ID permanente de Body. |
| Componente | Nome recuperado ou `Peça_XX` quando a associação não foi segura. |
| Resultado | Reconhecimento do sólido pelo SketchUp. |
| Localizar | Seleciona e enquadra a peça no modelo importado. |
| Detalhes | Avisos de conversão, reparo, metadados e cores. |

Salve o relatório antes de fechar o diálogo. Índices podem mudar em outra exportação. Para peças genéricas, use Localizar e compare geometria/posição no CAD.

## Conferir sólidos e escala

Selecione o componente e consulte informações da entidade. Confira uma dimensão conhecida. O formato intermediário usa milímetros; a extensão converte para as unidades internas em polegadas do SketchUp.

A construção é temporariamente ampliada e retorna ao tamanho real por transformação. O sólido final é poligonal, sem features do CAD. O reconhecimento pelo SketchUp não prova a mesma validade BRep ou precisão analítica do original.

## Cores e edição

Use um estilo que mostre materiais; Monocromático não exibe as cores. Os materiais `FCB_RGB_r_g_b` são aplicados à frente e ao verso das faces. Fronteiras coplanares entre materiais diferentes são preservadas.

Para Empurrar/Puxar, entre no componente e escolha uma face plana compatível. Ser sólido não impede essa ferramenta. Superfícies curvas importadas continuam formadas por faces; não se comportam como features paramétricas. Nem toda edição local preserva o sólido.

Não há sincronização ou atualização de componentes existentes. Para reimportar, remova/oculte a versão anterior e importe novamente.

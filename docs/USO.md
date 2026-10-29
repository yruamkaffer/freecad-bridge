# Importação, tratamento e conferência

## STEP

Configure FreeCADCmd uma vez. Abra **Extensões → FreeCAD Bridge → Importar STEP automaticamente**, selecione o STEP e escolha desvio, modo e tratamento. Padrão: **0,05 mm**, **Estrito**, **Completo**. O desvio pode variar de 0,001 a 100 mm.

Para uma montagem com suporte aberto, use **Sólidos disponíveis + Completo** para importar as peças aprovadas; o relatório identifica a peça omitida. Use **Visualização + Completo** para conferir a montagem com a superfície aberta. Estrito não omite essa superfície: ele impede a importação inteira.

Mantenha o mesmo modelo/contexto de edição durante a conversão. Há um trabalho por vez e limite de dez minutos. A criação de faces no SketchUp ocorre após a conversão e pode levar tempo.

## JSON

- O ícone **JSON** importa os vértices/triângulos existentes, sem executar reparos Python.
- **Tratar JSON existente…**, no menu, permite escolher modo e tratamento. Usa FreeCADCmd, mantém o JSON de origem e não refaz a triangulação CAD.
- Cores por triângulo são remapeadas pela origem dos triângulos após o ajuste. Cores/peças ausentes no JSON não podem ser recuperadas.
- A validade CAD original não é reavaliada; indicadores falsos continuam falsos. Em JSONs antigos sem esses indicadores, Estrito verifica a malha e o fechamento final, sem certificar a origem CAD.

## Tratamentos

**Completo (até 0,001 mm):** união limitada de vértices e tentativa de separar contatos locais, além dos reparos CAD e alternativas de triangulação disponíveis.

**Conservador:** permite união de vértices em até 0,0001 mm, sem separação de contatos. Mantém tentativas CAD/triangulação alternativas.

**Sem reparos:** normaliza coordenadas, remove duplicações exatas e propaga orientação para diagnóstico; não aplica os reparos opcionais. Uma malha difícil pode continuar sendo rejeitada.

Veja os [critérios e limites](TRATAMENTOS.md). Ajustes são feitos em cópias; STEP/JSON original não é sobrescrito.

## Relatório

Cada linha informa índice enumerado, nome, situação e botão **Localizar**. O índice vale somente para a execução, não é um ID permanente de Body. Nomes não associados sem ambiguidade recebem Peça_XX e um aviso.

Situações: **SÓLIDO**, **SUPERFÍCIE ABERTA**, **SUPERFÍCIE — malha fechada** ou **VERIFICAR**. Ser uma malha fechada não transforma uma casca CAD em sólido CAD. Superfícies recebem `[SUPERFÍCIE]`; peças não aprovadas recebem `[VERIFICAR]`.

Os detalhes registram reparos, limites de deslocamento, variação de volume da malha, tentativas rejeitadas e nomes/motivos de omissão. **Salvar relatório** exporta TXT. Guarde-o ao relatar um problema.

## Conferência

Confira uma dimensão conhecida e as posições da montagem. Selecione cada componente e confira suas informações no SketchUp. O conversor mantém mm no JSON e o importador converte para polegadas internas; a construção ampliada retorna ao tamanho real por transformação.

Confira a aparência com **Geometria oculta desativada**. A suavização é de 20 graus e é reaplicada se a limpeza coplanar precisar ser revertida para manter um sólido. Superfícies abertas recebem apenas suavização, sem tentativa de apagar divisões coplanares ou criar tampas.

Use um estilo com materiais para conferir cores; Monocromático não exibe RGB. Materiais são aplicados à frente e ao verso. Fronteiras coplanares de material diferente não são apagadas. A cobertura de cores depende dos dados do STEP e da associação segura à triangulação.

Para Empurrar/Puxar, entre no componente e escolha uma face plana compatível. Curvas continuam sendo faces poligonais; não há features paramétricas. Uma edição pode perder o fechamento.

Para atualizar componentes existentes, remova/oculte a importação anterior e reimporte. A extensão não sincroniza instâncias já inseridas. Para desenhos vetoriais, confira também o arquivo exportado: esconder arestas internas não transforma a malha em uma superfície analítica.

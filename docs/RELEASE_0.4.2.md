# FreeCAD Bridge 0.4.2

Correção de arestas trianguladas visíveis quando a limpeza de faces é revertida para preservar o sólido. A suavização agora roda sobre a geometria final, após eventual restauração e reaplicação de materiais, tanto em STEP quanto em JSON.

## Comportamento

- Mantido o limite de suavização de 20 graus, comprovado no teste manual do autor no SketchUp 2026.
- Sem remoção de faces ou arestas na etapa de suavização.
- Restauração verifica novamente número de faces e fechamento.
- Relatório registra “limpeza de faces revertida para preservar sólido; suavização reaplicada”.
- Mantidos nomes, cores, barra, modos Estrito/Visualização, padrão 0,05 mm e intervalo 0,001–100 mm.
- Conversor Python e formato JSON não alterados.

## Instalação e teste

Instale [FreeCAD_Bridge_0.4.2.rbz](../dist/FreeCAD_Bridge_0.4.2.rbz) pelo Gerenciador de Extensões, reinicie o SketchUp e confira Diagnóstico (0.4.2). Reimporte o arquivo: componentes existentes não são corrigidos automaticamente.

Use o JSON de diagnóstico privado ou um STEP próprio. Confira o estado SÓLIDO e as arestas com Geometria oculta desativada. Para testar cores e nomes, use um STEP que contenha esses dados; o JSON privado de diagnóstico da banheira não contém cores originais. Modelos privados não fazem parte desta distribuição.

## Validação

O autor confirmou a suavização manual equivalente no SketchUp 2026 para o modelo que revelou o problema. Os testes isolados cobrem a restauração com reaplicação de suavização, a limpeza bem-sucedida, bordas abertas/arestas acentuadas e falha de fechamento após restauração. Eles não substituem validação geométrica real nas APIs do SketchUp. Os dez testes Python e a integridade do pacote passaram nesta preparação. A regressão Ruby foi incluída, mas não executada neste ambiente sem interpretador Ruby. O RBZ atualizado precisa de teste no aplicativo.

Pacote sem assinatura oficial. Copyright © 2026 Yruam Kaffer de Faria. PolyForm Noncommercial License 1.0.0.

# FreeCAD Bridge 0.5.0

Esta versão automatiza tratamentos usados em conversões que o autor confirmou no SketchUp: união limitada de vértices quase coincidentes e separação local de superfícies em contato. Também identifica e conserva superfícies abertas no modo Visualização.

## Mudanças

- União de vértices: limite 0,0001 mm, com verificação de fechamento, orientação, conectividade, dimensão e volume.
- Separação local de contatos: 0,001 mm no tratamento Completo, com limites de aceitação e possibilidade de escolher Conservador/Sem reparos.
- Diagnóstico de vértices não manifold e triângulos degenerados/estreitos.
- Inventário de sólidos, cascas externas e faces soltas; superfícies nunca são tampadas automaticamente.
- Modo Sólidos disponíveis com lista explícita de peças omitidas.
- Comando Tratar JSON existente e ferramenta Python offline.
- Cores por triângulo mantêm referência à malha anterior ao ajuste.
- Relatório de reparos/volume, classificação de superfície e erros de faces identificando a peça.
- Mantidos os cinco ícones, a suavização após restauração, nomes/configuração, padrão 0,05 mm e intervalo 0,001–100 mm.

## Atualizar

Instale [FreeCAD_Bridge_0.5.0.rbz](../dist/FreeCAD_Bridge_0.5.0.rbz) e reinicie o SketchUp. Confira Diagnóstico (0.5.0). Use o mesmo FreeCADCmd configurado anteriormente. Reimporte modelos para aplicar os tratamentos.

Para testar uma montagem que contenha suporte aberto, escolha **Sólidos disponíveis + Completo**; depois compare **Visualização + Completo** para conferir a peça aberta. Estrito continuará rejeitando a montagem completa enquanto houver superfícies ou sólidos não aprovados.

## Evidência e limites

O autor confirmou que os JSONs de referência importaram no SketchUp. O novo motor foi verificado com malhas sintéticas e com três montagens privadas via Open CASCADE. Veja [validação](VALIDACAO_0.5.0.md). Não foram incluídos modelos comerciais no repositório.

O instalador completo 0.5.0 ainda precisa ser testado no FreeCADCmd/SketchUp Windows do usuário. Não há promessa de fechar qualquer malha, nem teste exaustivo de auto-interseções. Esta versão pode alterar localmente vértices em até 0,001 mm no modo Completo.

Copyright © 2026 Yruam Kaffer de Faria. PolyForm Noncommercial License 1.0.0. Sem assinatura oficial.

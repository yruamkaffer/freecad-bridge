# Como contribuir

Autoria principal e titular do copyright: **Yruam Kaffer de Faria**. Respeite PolyForm Noncommercial. Contribuir não transfere automaticamente a titularidade do código de seu autor.

## Bugs

Inclua versões, modo, desvio, passos, erro e relatório. Prefira STEP mínimo; compartilhe somente com autorização, sem informações confidenciais.

## Pull requests

1. Faça um fork e crie uma branch para uma mudança concreta.
2. Leia arquitetura e formato JSON.
3. Preserve identificadores de carregamento e evite duas instalações em paralelo.
4. Execute `python -m unittest discover -s tests -v` e `python tools/build_release.py`.
5. Confira Ruby com `ruby -c` quando disponível e teste nas APIs reais do SketchUp.
6. Teste mudanças de conversão no FreeCADCmd e depois no SketchUp, informando versões.
7. Atualize docs e changelog se mudar comportamento.
8. Descreva problema, resultado, validação e limites no PR.

Não remova rejeição de metadados ambíguos apenas para reduzir avisos. Alterações de tolerâncias precisam de evidência geométrica. Não marque testes nos aplicativos como feitos se só rodou lógica isolada.

## Matriz manual sugerida

| Caso | Verificar |
| --- | --- |
| Plano com furo | Escala, fechamento e limpeza. |
| Corpo curvo | Aproximação, orientação e suavização. |
| Uma cor | Material em todas as faces. |
| Múltiplas cores | Cobertura e fronteiras de material. |
| Montagem repetida | Contagem, posição, nomes e ambiguidades. |
| Geometria inválida | Rejeição Estrito e avisos Visualização. |
| Importar dentro de componente | Contexto e Localizar. |
| Falha de conversão | Mensagem e liberação para novo trabalho. |

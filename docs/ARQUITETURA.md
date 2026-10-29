# Arquitetura — 0.5.0

| Arquivo | Responsabilidade |
| --- | --- |
| yk_step_bridge.rb | Registro, versão, autoria e licença. |
| main.rb | Interface, seleção de modos, processo externo, reconstrução, materiais, suavização e relatório. |
| convert.py | Entrada FreeCADCmd, trabalho indicado por YK_STEP_JOB, escrita atômica/erro. |
| conversion.py | Motor importável, políticas de importação, tentativas CAD/malha, cores e reprocessamento JSON. |
| cad_tools.py | Inventário de sólidos, cascas externas e faces soltas, sem duplicar faces de sólidos. |
| mesh_tools.py | Normalização, auditoria, união limitada e separação de contatos, sem bibliotecas externas. |
| metadata.py | Nomes e cores por associação de assinatura geométrica. |

## Conversão STEP

O Ruby cria trabalho temporário com origem, saída, desvio, política e tratamento; inicia FreeCADCmd e acompanha por timer. O motor lê Part.read e tenta metadados por Import.insert em documento auxiliar. O documento é fechado ao finalizar, inclusive em falhas.

O inventário enumera sólidos, cascas que não pertencem a sólidos e faces que não pertencem a essas entidades. Visualização converte superfícies; Estrito as rejeita; Sólidos disponíveis lista a omissão. Linhas sem faces não são importadas.

Para sólidos, tenta forma original e Shape.fix quando permitido. O reparo CAD deve conservar um sólido, volume dentro de 1 ppm/piso absoluto e caixa dentro de 1e-5 mm. A triangulação tenta MeshPart com ângulos 0,15/0,08 radianos, metade do desvio e Shape.tessellate quando reparos estão habilitados. A primeira candidata válida/aprovada é aceita.

Cada malha é normalizada/orientada e passa pelos tratamentos escolhidos. Uma malha CAD válida é aprovada somente se o diagnóstico não aponta bordas abertas, arestas/vértices não manifold, conflitos ou degenerações. Os detalhes e limites estão em [tratamentos](TRATAMENTOS.md). A auditoria não testa exaustivamente auto-interseções.

Sem sucesso, Estrito agrega erros e rejeita o conjunto; Sólidos disponíveis omite com motivo; Visualização conserva o melhor resultado disponível. Uma peça sem qualquer triangulação ainda pode impedir Visualização — ela não inventa geometria.

## Cores

Nomes/cores são associados por tipo geométrico, volume, caixa e centro de massa. Zero ou múltiplas correspondências geram aviso. Não se escolhe arbitrariamente entre ocorrências coincidentes.

A cor uniforme e as cores por triângulo são buscadas usando a malha normalizada anterior aos novos ajustes. A lista de proveniência transporta a cor para cada triângulo final. Isso conserva cores já encontradas mesmo quando vértices são unidos ou deslocados; não melhora correspondências ausentes na triangulação original.

## JSON

O importador direto permanece compatível com yk-step-bridge-1/mm. O comando Tratar JSON existente usa o mesmo motor, conservando cores pela origem dos triângulos. Não relê o CAD nem transforma cad_valid falso em verdadeiro. A ferramenta tools/treat_json.py executa esse tratamento com Python padrão, sem FreeCAD.

## SketchUp

Valida dados e indicadores de origem antes da operação estrita. Cria a malha em escala 1000, pinta, limpa divisões coplanares de mesmo material e verifica se o fechamento foi preservado. Se necessário restaura faces/materiais e reaplica suavização de 20 graus. Superfícies recebem apenas suavização para preservar sua geometria aberta.

A verificação final do SketchUp continua obrigatória para peças incluídas em Estrito/Sólidos disponíveis: uma falha aborta a operação inteira. O modo parcial só omite peças rejeitadas pelo conversor; ele não mascara falhas finais de reconstrução no SketchUp.

O relatório diferencia sólidos aprovados e superfícies, mostra omissões e reparos. Atributos da instância em YKStepBridge: source, source_index, geometry_type e repairs (JSON). Não há atualização associativa de componentes existentes.

## Processo e interface

Um trabalho por vez, acompanhamento a cada 0,5 segundo e limite de dez minutos. Saída .tmp é renomeada; falhas geram .error. Temporários são removidos ao final. O fluxo não faz chamadas de rede.

A barra mantém cinco comandos e ícones; as ações STEP/JSON ficam indisponíveis durante conversão. Tratar JSON existente verifica o mesmo bloqueio. O estado nativo da barra é restaurado e o menu permite reexibi-la.

## Fontes das APIs

- [FreeCAD TopoShape](https://freecad.github.io/SourceDoc/d8/ded/classPart_1_1TopoShape.html)
- [SketchUp ComponentInstance](https://ruby.sketchup.com/Sketchup/ComponentInstance.html)
- [SketchUp SketchupExtension](https://ruby.sketchup.com/SketchupExtension.html)

FreeCADCmd e SketchUp não são empacotados. A integração Windows completa exige validação no ambiente alvo, além dos testes do motor.

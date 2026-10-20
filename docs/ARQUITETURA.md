# Arquitetura e decisões técnicas

## Responsabilidades

| Arquivo | Responsabilidade |
| --- | --- |
| `yk_step_bridge.rb` | Registro, versão, descrição, autoria e licença. |
| `main.rb` | Interface, configuração, processo externo, criação de geometria/materiais, limpeza e relatório. |
| `convert.py` | Leitura STEP, reparo, triangulação, validação CAD e saída JSON. |
| `mesh_tools.py` | Deduplicação, orientação e contagem de defeitos topológicos da malha. |
| `metadata.py` | Leitura/associação de nomes e cores e transferência RGB. |

## Fluxo

1. Ruby coleta caminho, desvio e modo, cria trabalho em pasta temporária e fornece `YK_STEP_JOB` ao FreeCADCmd.
2. Python lê `Part.read` e tenta obter metadados de `Import.insert` em documento auxiliar.
3. Cada sólido passa pelas tentativas de conversão e associação de metadados.
4. A saída é escrita em `.tmp` e renomeada; falhas geram `.error` com traceback.
5. Ruby consulta a conclusão por timer de 0,5 segundo, valida JSON e cria componentes em uma operação.
6. Estrito aborta a operação se a verificação final falhar. A conclusão apresenta relatório e remove temporários.

O fluxo implementado não faz chamadas de rede. Os logs temporários são removidos ao final; ainda não existe exportação persistente de todos os logs de falha.

## Reparo e malha

O conversor tenta forma original e cópia com `Shape.fix`. O reparo deve manter um sólido, volume dentro de uma parte por milhão com piso absoluto e caixa envolvente dentro de `1e-5 mm`. Esses critérios não provam equivalência topológica.

Tenta `MeshPart.meshFromShape` com desvios angulares 0,15 e 0,08 radianos, alternativa com metade do desvio linear e `Shape.tessellate`. A primeira opção CAD válida/fechada é aceita. Sem sucesso, o melhor resultado pelos contadores só pode ser importado em Visualização.

`prepare` combina coordenadas arredondadas a oito casas, elimina triângulos repetidos/degenerados por índices e propaga orientação pela adjacência. Exige triângulos presentes, zero bordas abertas, zero arestas com mais de duas incidências e zero conflitos. Não testa todas as auto-interseções geométricas.

## SketchUp

Valida coordenadas finitas e índices antes de tocar no modelo. Converte mm para polegadas, constrói com fator 1000 e retorna por transformação. Isso reduz problemas com arestas pequenas, sem eliminar todos os limites numéricos.

Pinta antes da limpeza. Remove arestas coplanares de mesmo material e pode suavizar arestas entre normais com ângulo inferior a 20 graus. Se a limpeza perde um fechamento anterior, reconstrói e repinta a tesselação original.

Validação final usa `manifold?`. Atributos da instância no dicionário `YKStepBridge`: `source` e `source_index`. O índice vale para aquela enumeração; não é persistente entre exportações.

## Metadados

Associação usa volume, caixa envolvente e centro de massa: volume com tolerância relativa `1e-7` e piso absoluto `1e-5`, coordenadas `1e-5`. Zero ou múltiplas correspondências geram aviso, sem escolher arbitrariamente.

Cor uniforme exige confirmação em todas as faces. Cores por face usam chaves de triângulos com coordenadas arredondadas a seis casas. Triângulos sem correspondência ficam sem cor confirmada. Reparo e triangulação alternativa podem reduzir a cobertura.

Ruby roda no SketchUp e Python no FreeCAD; não empacotamos os aplicativos nem seu kernel CAD. Ferramentas de build/testes usam Python padrão separado. APIs podem mudar com versões; o alvo documentado não significa compatibilidade universal.

## Interface 0.4.0

`register_interface` cria cinco `UI::Command`, armazena-os em `@commands` e compartilha os objetos entre o submenu e `@toolbar`. `toolbar_command` define título, tooltip, texto de status e caminhos de ícones. `show_about` concentra versão, autoria e licença.

A inicialização segue o estado nativo: primeira exibição chama `show`; sessões seguintes usam `restore`. O comando Mostrar barra permite recuperá-la. A guarda `file_loaded?` evita duplicação no carregamento normal. Os comandos STEP/JSON usam validation proc que retorna MF_GRAYED enquanto `@job` existe.

Esta versão altera apenas registro da interface e metadados de versão. `convert.py`, `mesh_tools.py`, `metadata.py` e os métodos de reconstrução foram preservados da versão 0.3.0.

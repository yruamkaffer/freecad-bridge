# Solução de problemas

| Sintoma | Verificação e próxima ação |
| --- | --- |
| Barra oculta | Use Extensões → FreeCAD Bridge → Mostrar barra de ferramentas. |
| Ícones ausentes | Reinstale o RBZ completo e reinicie; a pasta icons deve acompanhar o carregador. |
| STEP/JSON desabilitados | Aguarde a conversão em andamento terminar. |
| Diagnóstico mostra versão antiga | Reinicie e confira se há cópias antigas do carregador. |
| Menu ausente | Confira instalação do RBZ, reinício, extensão habilitada e política de carregamento. |
| Seleção do executável reaparece | Escolha o `.exe` real; confira Diagnóstico, existência e mensagem de gravação da configuração. |
| Conversor não gerou geometria | Confira instalação do FreeCAD, executável e módulos; teste STEP pequeno. |
| STEP com superfícies, sem sólidos | Use Visualização para importar faces/cascas; Estrito/Sólidos disponíveis não aprovam superfícies como sólidos. |
| Estrito falha, Visualização abre | Salve relatório, localize a peça e confira validade CAD, bordas e fechamento. |
| Parece sólido, mas não é | Aparência não revela todas as aberturas; confira informações da entidade e relatório. |
| Cores ausentes | Confira cores no STEP reaberto, estilo com materiais e avisos de associação. |
| Cores parciais | Reparo/triangulação pode ter mudado a correspondência. Teste uma peça no padrão e guarde relatório. |
| Nome `Peça_XX` | Metadados indisponíveis ou associação ambígua. Use Localizar e confira labels/ocorrências sobrepostas. |
| Divisões planas permanecem | Pode haver materiais distintos, falta de coplanaridade ou limpeza revertida para preservar sólido. |
| Contexto mudou | Repita mantendo o mesmo modelo e contexto de edição. |
| Dez minutos excedidos | Teste peças isoladas e desvio maior; registre tamanho do arquivo e versões. |
| Empurrar/Puxar não atua | Entre no componente e selecione uma face plana, não a instância ou superfície curva. |

## Diagnóstico reproduzível

Registre Windows, SketchUp, FreeCAD, extensão, modo, desvio, passos e erro exato. Exporte o relatório quando disponível. Diga se o STEP reaberto no FreeCAD mantém sólidos, nomes e cores.

Uma captura mostra o sintoma; um STEP mínimo e o relatório ajudam a descobrir a causa. Não publique dados pessoais ou modelos de clientes/empresa sem autorização.

## Limites do reparo

O código tenta reparo CAD limitado, novas triangulações, remoção de repetições e orientação consistente. Não inventa faces para qualquer buraco, não corrige qualquer auto-interseção e não garante recuperar toda geometria inválida. O modo Estrito rejeita resultados que não passaram pelas verificações implementadas.

## Falha ao criar todas as faces

A mensagem é emitida se o número de faces criado no SketchUp divergir dos triângulos do JSON. Ela pode ocorrer mesmo em Visualização: esse modo permite indicadores de geometria problemática, mas não ignora falhas de reconstrução. A mensagem atual não identifica automaticamente a peça que falhou. Um STEP válido no CAD não elimina essa possibilidade.

Não remova peças ou declare sólidos aprovados somente para ocultar o erro. Preserve o original, reduza o caso para diagnóstico e registre modo, desvio e mensagem. A 0.4.0 não corrige essa limitação.

## Access violation na leitura STEP

Se o traceback aponta `Part.read`, a falha ocorreu antes da triangulação e da criação de faces. Reabra o mesmo STEP no FreeCAD e teste outro STEP conhecido para distinguir arquivo específico de ambiente de execução. Não é, por si só, diagnóstico de peça não sólida.

## Sólido aparece todo triangulado após restauração

Até a 0.4.1, a mensagem “limpeza de faces revertida para preservar sólido” indicava uma restauração que também perdia a suavização. A 0.4.2 reaplica automaticamente a suavização à geometria restaurada e informa isso no relatório. Reimporte o arquivo para aplicar a correção; componentes já inseridos não são alterados automaticamente.

Confira o resultado com **Geometria oculta** desativada. Arestas acentuadas (20 graus ou mais) continuam visíveis. A suavização não reconstrói superfícies CAD nem garante remover todas as linhas de uma exportação vetorial: confira a vista e o arquivo exportado. Aumentar o desvio linear não substitui esse tratamento.

## Tratamentos 0.5.0

- **Suporte/superfície impede Estrito:** use Visualização para manter a superfície aberta ou Sólidos disponíveis para omiti-la explicitamente. Corrija o CAD se precisar de todos como sólidos.
- **Bucha com arestas não manifold:** tente Completo. A separação local só é aceita com verificações e limites; se rejeitada, confira o motivo no relatório.
- **Canopla com triângulos muito estreitos:** tente Conservador ou Completo. Não aumente o desvio apenas para esconder um defeito de topologia.
- **JSON antigo continua igual:** o ícone JSON não aplica os novos reparos Python. Use Tratar JSON existente.
- **Peça não apareceu:** confira a lista OMITIDA no modo Sólidos disponíveis. Visualização conserva cascas/faces fora de sólidos. Linhas sem faces não são importadas.
- **Falha ao criar faces (obtidas/esperadas):** anote nome da peça, contagem, versão, modo e tratamento. Mesmo uma malha aprovada pode atingir limites de reconstrução do SketchUp.
- **Cores faltando:** o tratamento conserva a correspondência existente, mas não inventa cores ausentes no STEP ou sem associação segura à triangulação.

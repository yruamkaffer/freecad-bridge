# Solução de problemas

| Sintoma | Verificação e próxima ação |
| --- | --- |
| Menu ausente | Confira instalação do RBZ, reinício, extensão habilitada e política de carregamento. |
| Seleção do executável reaparece | Escolha o `.exe` real; confira Diagnóstico, existência e mensagem de gravação da configuração. |
| Conversor não gerou geometria | Confira instalação do FreeCAD, executável e módulos; teste STEP pequeno. |
| STEP sem sólidos | Reabra no CAD; pode conter superfícies ou a seleção exportada errada. |
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

# Formato intermediário JSON — 0.5.0

Identificador **yk-step-bridge-1**, unidade **mm**. Formato próprio. O identificador foi mantido para compatibilidade com os JSONs anteriores; novos campos são opcionais no importador.

| Campo | Conteúdo |
| --- | --- |
| format, units, parts | Identificador, unidade e lista não vazia. |
| source | Nome de origem usado no relatório. |
| strict | Exige aprovação de indicadores disponíveis e fechamento final; ausência não ativa Estrito. |
| policy | strict, visualization ou solids_only. |
| generator_version, mesh_treatment | Versão produtora e tratamento selecionado. |
| warnings | Avisos textuais. |
| skipped_parts | Peças omitidas: source_index, name, geometry_type, reason. |
| parts[].vertices | Coordenadas finitas [x,y,z] em mm. |
| parts[].triangles | Três índices inteiros distintos, base zero. |
| name, source_index | Nome e posição na enumeração desta execução. |
| color | RGB uniforme 0–255. |
| triangle_colors | RGB ou null por triângulo final, com quantidade correspondente. |
| geometry_type | solid ou surface. |
| cad_has_solid | Se a entidade de origem foi identificada como sólido CAD. |
| cad_shape_valid | Validade geral da entidade CAD; uma superfície válida ainda pode ser aberta. |
| cad_valid | Aprovação de sólido CAD; false para superfície. Ausente em JSON antigo não equivale a certificação CAD. |
| mesh_closed | Aprovação da topologia da malha pelo conversor. |
| check | closed, boundary, nonmanifold, conflicts, nonmanifold_vertices, degenerate, thin_triangles, min_height_mm, components. |
| repairs | Operações aceitas com limites, quantidade de alterações, volume antes/depois, relative_volume_change e check. |
| repair_attempts | Motivos de tentativas de reparo rejeitadas. |
| conversion_history | Histórico de triangulação. |

relative_volume_change é fração, não porcentagem. O relatório multiplica por 100. Volumes se referem à malha, não à geometria CAD analítica. O sufixo de apresentação não é gravado no name original; o importador acrescenta [SUPERFÍCIE]/[VERIFICAR] conforme situação.

Os campos internos de proveniência de cores não são serializados. O JSON final já tem cores alinhadas aos triângulos finais. O reprocessamento conserva atributos desconhecidos por peça quando possível, sem inferir dados ausentes.

Exemplo mínimo: [tetraedro vermelho](../examples/tetraedro_vermelho.json). Exemplos de reparo: [faixa fina](../examples/tetraedro_faixa_fina.json) e [contato](../examples/tetraedros_em_contato.json).

## Trabalho FreeCADCmd

job.json: source, output, tolerance, input_type (step/json), policy, mesh_treatment (complete/conservative/none), repair. O campo legado allow_open continua aceito quando policy não está presente. YK_STEP_JOB indica o caminho do trabalho. input_type=json ignora a tolerância de triangulação e trata apenas a malha existente.

O parser não é uma certificação geométrica. Visualização não garante que o SketchUp consiga criar qualquer malha inválida. Reprocessar JSON não revalida a BRep original nem recupera peças que já foram omitidas.

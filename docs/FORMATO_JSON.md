# Formato intermediário JSON

Identificador `yk-step-bridge-1`, unidades `mm`. Formato próprio, não oficial do FreeCAD/SketchUp. Descreve 0.4.0, sem promessa de estabilidade diante de mudanças incompatíveis.

## Exemplo mínimo

Tetraedro fechado com cor uniforme:

```json
{
  "format": "yk-step-bridge-1",
  "units": "mm",
  "source": "tetraedro.step",
  "strict": true,
  "warnings": [],
  "parts": [{
    "name": "Tetraedro",
    "source_index": 1,
    "vertices": [[0,0,0], [10,0,0], [0,10,0], [0,0,10]],
    "triangles": [[0,2,1], [0,1,3], [0,3,2], [1,2,3]],
    "color": [255,0,0],
    "mesh_closed": true,
    "cad_valid": true
  }]
}
```

| Campo | Função |
| --- | --- |
| `format`, `units`, `parts` | Identificador, unidade obrigatória e lista não vazia. |
| `source` | Nome da origem no relatório e atributo. |
| `strict` | Verdadeiro exige fechamento final no SketchUp; ausente não ativa essa exigência. |
| `warnings` | Avisos textuais. |
| `name`, `source_index` | Nome e índice da peça na execução. |
| `vertices` | Coordenadas finitas `[x,y,z]` em mm. |
| `triangles` | Três índices inteiros distintos, base zero, dentro da lista de vértices. |
| `color` | RGB uniforme opcional, valores de 0 a 255. |
| `triangle_colors` | Lista alinhada com triângulos; RGB ou `null` por item. |
| `mesh_closed`, `cad_valid` | Indicadores de origem; falsos provocam `[VERIFICAR]`. |
| `conversion`, `linear_deflection`, `check` | Diagnóstico adicional do conversor. |

O Ruby valida coordenadas, índices, RGB e tamanho da lista de cores. Esses controles não substituem esquema completo ou validade geométrica. Indicadores de origem não substituem `manifold?`.

`job.json` contém `source`, `output`, `tolerance`, `allow_open` e `repair`. Caminhos locais, tolerância em mm; `allow_open` corresponde a Visualização. `YK_STEP_JOB` fornece o caminho do trabalho. Um Python comum não executa a conversão: são necessários os módulos do FreeCAD.

## Compatibilidade 0.4.0

A barra JSON usa o mesmo `import_json` da 0.3.0. Não houve mudança no identificador ou nas unidades. Um JSON aceito pelo parser ainda pode falhar na criação de faces; Visualização não garante que o SketchUp consiga reconstruir toda malha inválida. Exemplo público: [tetraedro vermelho](../examples/tetraedro_vermelho.json).

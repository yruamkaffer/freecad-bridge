# Tratamentos de sólidos e superfícies — 0.5.0

## Objetivo e escolha

Um sólido válido no CAD pode gerar uma malha inadequada ao SketchUp. A conversão trata a malha em milímetros e mantém o arquivo de origem. O tratamento padrão **Completo** permite as duas correções abaixo; **Conservador** permite só união de vértices. **Sem reparos** mantém normalização/diagnóstico, sem esses ajustes ou reparos CAD opcionais.

## União de vértices quase coincidentes

Aplicada somente a uma malha de sólido já fechada que tenha triângulos com altura inferior a 0,0000254 mm. Esse limite auxilia a identificar riscos na construção ampliada do importador; não é uma especificação universal do SketchUp.

Vértices dentro de **0,0001 mm** podem ser unidos a um representante existente. Não há encadeamento ilimitado de deslocamentos. Triângulos colapsados e repetidos são removidos. A candidata só é aceita se continuar fechada, orientada, sem vértices/arestas não manifold ou faces degeneradas, sem novas faces muito estreitas, sem inversão das faces sobreviventes e com o mesmo número de regiões conectadas.

A variação relativa de volume da malha não pode exceder **0,0001%** (uma parte por milhão). A caixa envolvente deve ficar dentro de 0,0001 mm da original. Uma tentativa rejeitada não substitui a malha anterior.

## Separação local de contatos

Usada apenas no modo Completo para sólidos sem bordas abertas cuja malha tenha arestas compartilhadas por mais de duas faces. Em cada vértice problemático devem existir exatamente dois conjuntos locais de faces, separados pelas adjacências regulares. O conjunto com menos faces recebe um vértice independente deslocado na direção da normal média em **0,001 mm**. Há limite de 512 vértices problemáticos por tentativa.

Separar apenas índices não bastaria: o SketchUp poderia unir novamente coordenadas iguais. Após o deslocamento, verificam-se fechamento, orientação, vértices/arestas manifold, degenerações, faces estreitas, conectividade, inversão de faces e caixa envolvente. A variação relativa de volume deve ser no máximo **0,01%** e a alteração dimensional no máximo 0,001 mm. Os valores são comparados à malha anterior, não à geometria CAD exata.

Essa correção altera localmente a aproximação. Ela não resolve qualquer interseção ou contato arbitrário. Use Conservador ou Sem reparos quando não quiser permitir esse deslocamento. Não há validação exaustiva de auto-interseções.

## Superfícies abertas

O inventário separa sólidos, cascas que não pertencem a sólidos e faces soltas. Faces já pertencentes a cascas/sólidos não são adicionadas novamente.

- **Estrito:** superfícies impedem a importação; o erro identifica as peças.
- **Visualização:** mantém as superfícies, com sufixo `[SUPERFÍCIE]` e situação própria no relatório. Só suaviza a exibição; não remove divisões coplanares dessas superfícies.
- **Sólidos disponíveis:** omite superfícies e sólidos não aprovados no conversor, listando as omissões. Não é uma correção das peças omitidas.

Uma casca fechada ainda é classificada como superfície se não veio como sólido CAD. Não são criadas tampas nem fechamentos inventados. Linhas sem faces não fazem parte desse inventário.

## Cores e rastreabilidade

As cores são buscadas na triangulação anterior aos novos ajustes. Cada triângulo final mantém a referência de origem para transportar sua cor após união ou deslocamento de vértices. Cores que já não tinham correspondência no STEP permanecem sem confirmação; não são inferidas por proximidade.

O relatório identifica operação, limite e variação de volume. O JSON também contém `repairs`, `repair_attempts`, `check` e `skipped_parts`. Tratamentos anteriores do JSON continuam registrados. Dados CAD falsos não viram verdadeiros só porque uma malha foi fechada.

## Fluxo JSON

O ícone JSON importa como está. **Extensões → FreeCAD Bridge → Tratar JSON existente…** reaplica o motor em uma cópia temporária, usando FreeCADCmd para executar o Python. Não reconstrói o STEP nem revalida sua BRep. Também há uma ferramenta sem dependências externas:

```sh
python tools/treat_json.py entrada.json --output saida.json --mode solids_only --treatment complete
```

Confira o resultado no SketchUp. Uma verificação de malha aprovada não elimina os limites de criação de faces do aplicativo.

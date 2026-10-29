# Evidência de validação — 0.5.0

Preparação em 29/10/2026. Os modelos comerciais usados nos testes são privados e não estão neste pacote.

## Referências confirmadas pelo autor

O autor confirmou no SketchUp que as conversões JSON tratadas manualmente funcionaram: união de vértices nas canoplas, separação local dos contatos das buchas e preservação das superfícies abertas para inspeção. Essa confirmação se refere aos arquivos entregues antes desta atualização, não ao instalador 0.5.0 completo.

## Novo motor automático

O mesmo motor Python da extensão foi exercitado com a geometria de três STEP privados por meio de um adaptador Open CASCADE/OCP:

| Caso | Sólidos CAD | Superfícies externas | Reparos automáticos aceitos |
| --- | --- | --- | --- |
| A | 7 | 0 | União de vértices em uma canopla. |
| B | 19 | 1 | União em uma canopla e separação local em duas buchas. |
| C | 20 | 1 | Separação local em duas buchas. |

As **46 malhas de sólidos** ficaram fechadas, orientadas, sem arestas ou vértices não manifold, sem degenerações e sem triângulos abaixo do limiar de risco verificado. As duas superfícies abertas continuaram abertas e foram identificadas; nenhuma tampa foi adicionada.

As separações das buchas usaram 0,001 mm e alteraram o volume de cada malha em cerca de 0,0004533%. A união de vértices respeitou seu limite próprio de volume. Também foi exercitado o tratamento de JSON com os mesmos casos de referência.

Esse adaptador testa o motor, inventário e geometria com Open CASCADE. Não executa Import.insert, o reparo Shape.fix ou o processo FreeCADCmd no Windows e não valida a interface do SketchUp. A obtenção de metadados foi fornecida pelo adaptador; cores/associação reais continuam precisando de teste no ambiente alvo.

## Testes distribuídos

- **24 testes Python:** reparos, rejeição por limites, superfícies, três políticas, cores/proveniência, metadados, formatos inválidos, ícones, links e correspondência instalador/fontes.
- **Sintaxe Ruby:** verificada com parser tree-sitter nos arquivos de carregamento, importador e testes.
- **7 testes Ruby de comportamento:** incluídos para execução com Ruby, usando objetos mínimos da API. Não foram executados neste ambiente sem interpretador Ruby.
- **GitHub Actions:** workflow incluído para testes Python/Ruby e validação do instalador. Ainda não executado no repositório remoto nesta preparação.
- **RBZ:** conteúdo/arquivos e SHA256 verificados. Sem assinatura oficial.

## Conferência no ambiente alvo

1. Instalar 0.5.0, reiniciar SketchUp e conferir versão em Diagnóstico.
2. Importar uma montagem própria em Sólidos disponíveis + Completo, padrão 0,05 mm; conferir nomes e motivos de omissão.
3. Comparar Visualização + Completo; conferir que o suporte aparece como SUPERFÍCIE.
4. Confirmar que Estrito rejeita a montagem completa se ainda houver superfície aberta.
5. Conferir escala, posição, cores, aparência, relatório de reparos e suavização após restauração.
6. Tratar um JSON antigo e os exemplos sintéticos; comparar Completo/Conservador e conferir que a origem não foi alterada.

Nenhum desses testes é uma garantia universal de equivalência CAD, ausência de auto-interseções ou sucesso em toda versão dos aplicativos.

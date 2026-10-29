# Histórico

## 0.5.0 — 2026-10-29

- Tratamentos Conservador/Completo/Sem reparos, com união de vértices e separação local de contatos.
- Auditoria de vértices não manifold, degenerações, volume e conectividade.
- Superfícies externas aos sólidos importadas explicitamente em Visualização.
- Modo Sólidos disponíveis e relatório de omissões/reparos.
- Reprocessamento de JSON e preservação da origem das cores por triângulo.
- Testes sintéticos, casos privados de regressão e documentação dos limites.
- Referências manuais confirmadas pelo autor; integração da nova versão no Windows pendente.

## 0.4.3 — 2026-10-21

- Marca própria de ponte e seta nos botões STEP e Sobre.
- PNGs de 24/32 pixels e fontes SVG; marca de 512 pixels e ICO para atalhos opcionais.
- Documentação e guia visual atualizados.
- Geometria e correção de suavização da 0.4.2 preservadas. Sem assinatura oficial.

## 0.4.2 — 2026-10-21

- Suavização aplicada à geometria final, inclusive após restauração da tesselação para preservar o sólido.
- Limpeza coplanar e suavização separadas; a suavização apenas altera atributos das arestas.
- Restauração confere novamente a quantidade de faces e o fechamento antes de continuar.
- Relatório informa a suavização reaplicada; materiais são reaplicados antes dela.
- Mesmo tratamento para importação STEP e JSON; mantidos ângulo de 20 graus, modos, cores e intervalo de desvio 0,001–100 mm.
- Correção manual equivalente validada pelo autor no SketchUp 2026; pacote automatizado ainda requer teste no aplicativo.

## 0.4.1 — 2026-10-20

- Desvio linear ampliado de 0,001–5 mm para 0,001–100 mm.
- Padrão 0,05 mm preservado; intervalo informado no campo e na validação.
- Barra de ferramentas da 0.4.0 preservada. Conversor e seus limites angulares não alterados.
- Sintaxe e integridade do pacote verificadas; validação em aplicativos pendente.

## 0.4.0 — 2026-10-20

- Barra de ferramentas FreeCAD Bridge com cinco atalhos e ícones próprios de 24/32 pixels.
- Comandos compartilhados com o menu Extensões, dicas e texto de ajuda.
- Restauração nativa da posição/visibilidade e comando para reexibir a barra.
- Importações indisponíveis durante conversão em andamento.
- Guias atualizados, exemplo JSON sintético e empacotamento com validação dos ícones.
- Conversor e reconstrução geométrica mantidos da 0.3.0; sem novas correções de malha.

Sintaxe, recursos, testes isolados e pacote verificados. Interface real ainda precisa de validação no SketchUp. Sem assinatura oficial.

## 0.3.0 — 2026-10-08

- Nome FreeCAD Bridge, autoria de Yruam Kaffer de Faria e PolyForm Noncommercial 1.0.0.
- Leitura/associação segura de nomes e cores com FreeCAD em segundo plano.
- Cores uniformes e por triângulo; fronteiras de material preservadas.
- Relatório com Localizar e exportação de texto.
- Verificação estrita final com rollback.
- Documentação pública e ferramentas de empacotamento. Sem assinatura oficial.

Sintaxe e lógica isolada verificadas; validação completa das novas funções nos aplicativos pendente.

## 0.2.3

Reparo CAD limitado, triangulações adicionais, deduplicação/orientação e reversão de limpeza quando o fechamento se perde.

## 0.2.2

Modos Estrito e Visualização e avisos de geometria.

## 0.2.1

Correções de seleção e persistência do caminho FreeCADCmd.

## 0.2.0

Importação STEP automatizada em segundo plano.

## 0.1.0

Fluxo inicial de macro de exportação e importação JSON.

Instaladores antigos não são incluídos neste pacote de repositório.

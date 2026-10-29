# FreeCAD Bridge

**STEP para SketchUp: componentes nomeados, cores, reparos de malha e superfícies identificadas.**

**Autor:** Yruam Kaffer de Faria · **Versão:** 0.5.0 · **Alvo:** SketchUp 2026 desktop / Windows

[English](README.en.md) · [Instalação](docs/INSTALACAO.md) · [Uso](docs/USO.md) · [Tratamentos](docs/TRATAMENTOS.md) · [Problemas](docs/SOLUCAO_DE_PROBLEMAS.md) · [Licença](LICENSE.txt)

Repositório: [yruamkaffer/freecad-bridge](https://github.com/yruamkaffer/freecad-bridge).

## O que faz

Usa uma instalação local do FreeCAD em segundo plano para converter STEP em componentes editáveis no SketchUp. Não é preciso abrir uma macro a cada importação. Conserva posições, busca nomes e cores disponíveis no arquivo, verifica os resultados e apresenta relatório por peça.

Sólidos CAD válidos podem gerar malhas difíceis de reconstruir no SketchUp. A 0.5.0 incorpora tratamentos derivados de conversões que o autor confirmou no SketchUp, aplicando limites de deslocamento e verificações após cada tentativa. Isso não garante reparar qualquer arquivo.

## Novo na 0.5.0

- União de vértices quase coincidentes, com limite de **0,0001 mm**, para malhas fechadas com triângulos muito estreitos.
- Separação local de superfícies em contato, com deslocamento de **0,001 mm**, no tratamento Completo.
- Verificação de bordas abertas, orientação, arestas e vértices não manifold, degenerações, regiões conectadas, dimensões e volume da malha.
- Superfícies/cascas externas aos sólidos entram no modo Visualização, identificadas como **SUPERFÍCIE**. Não são fechadas à força nem descartadas silenciosamente.
- Modo **Sólidos disponíveis**, que omite peças não aprovadas e lista seus nomes/motivos no relatório.
- Comando **Tratar JSON existente…**, sem modificar o arquivo de origem.
- Cores por triângulo acompanham a origem dos triângulos após os novos ajustes.
- Relatório com reparos, limites e variação de volume; erros na criação de faces identificam a peça e a contagem obtida/esperada.

Mantidos nomes de instalação/configuração, ícones da 0.4.3, suavização de 20 graus após restauração da malha e desvio linear **0,001–100 mm**, padrão **0,05 mm**.

## Instalar e testar

1. Baixe [FreeCAD_Bridge_0.5.0.rbz](dist/FreeCAD_Bridge_0.5.0.rbz).
2. Instale pelo Gerenciador de Extensões do SketchUp e reinicie o aplicativo.
3. Configure `FreeCADCmd.exe` pelo menu **Extensões → FreeCAD Bridge → Configurar FreeCADCmd**.
4. Abra **Importar STEP automaticamente** e escolha arquivo, modo e tratamento.
5. Para uma montagem com suporte aberto, use **Sólidos disponíveis** para testar as peças aprovadas ou **Visualização** para ver o conjunto completo.
6. Confira relatório, escala, nomes, cores e aparência com Geometria oculta desativada.

O instalador é **sem assinatura oficial**. Detalhes: [instalação](docs/INSTALACAO.md). A atualização não altera componentes já inseridos: reimporte para usar os novos tratamentos.

## Modos e tratamentos

| Modo | Resultado |
| --- | --- |
| Estrito | Exige sólidos CAD válidos, malhas aprovadas e fechamento no SketchUp. Uma falha bloqueia/desfaz a operação inteira. |
| Visualização | Inclui superfícies e resultados não aprovados com identificação; ainda depende de o SketchUp conseguir criar as faces. |
| Sólidos disponíveis | Omite superfícies e peças não aprovadas no conversor, listando cada omissão. As peças incluídas ainda precisam passar pela verificação final do SketchUp. |

| Tratamento | Ajustes permitidos |
| --- | --- |
| Completo — padrão | União de vértices e separação local de contatos; reparo CAD/tentativas alternativas. |
| Conservador | União de vértices; não separa contatos. Mantém reparo CAD/tentativas alternativas. |
| Sem reparos | Normalização e diagnóstico, sem os reparos opcionais ou tentativas CAD alternativas. |

Os ajustes são aplicados em cópias da geometria convertida. O STEP original não é sobrescrito. Para saber quando uma tentativa é aceita ou rejeitada, veja [tratamentos e limites](docs/TRATAMENTOS.md).

## Barra e identidade visual

![Atalhos FreeCAD Bridge](docs/assets/barra_ferramentas.png)

Cinco atalhos: STEP, JSON, configuração, diagnóstico e autoria/licença. O ícone JSON importa um arquivo **como está**; para aplicar os novos tratamentos, use o comando separado **Tratar JSON existente…**. Ambos os fluxos de conversão usam FreeCADCmd. O gerenciador do SketchUp pode continuar mostrando seu ícone genérico: a marca da barra não define o ícone do Gerenciador de Extensões.

[Barra](docs/BARRA_DE_FERRAMENTAS.md) · [Identidade visual](docs/IDENTIDADE_VISUAL.md) · [Notas da versão](docs/RELEASE_0.5.0.md) · [Histórico](CHANGELOG.md)

## Limites

Curvas continuam sendo faces poligonais; features paramétricas do CAD não são transferidas. Não há garantia universal de sólido ou teste completo de auto-interseções. Superfícies abertas não são tampadas automaticamente. O resultado deve ser conferido antes de uso técnico.

Cores e nomes dependem dos dados do STEP e de associação sem ambiguidade. Texturas, transparência e materiais físicos não são transferidos. Montagens preservam posições dentro de um grupo, sem árvore original de submontagens nem definições compartilhadas de peças repetidas. Entidades apenas de linha não são importadas.

macOS, Linux e SketchUp Web não são suportados pelo fluxo Windows atual. O alvo de metadados é FreeCAD 1.1; não há matriz certificada de versões.

## Validação e desenvolvimento

Os tratamentos manuais de referência foram confirmados pelo autor no SketchUp. O novo motor foi testado com geometrias sintéticas e modelos privados via Open CASCADE. Esses testes não equivalem a executar esta versão completa no FreeCADCmd e SketchUp do usuário. Consulte [validação](docs/VALIDACAO_0.5.0.md) e [desenvolvimento](docs/DESENVOLVIMENTO.md).

```sh
python tools/build_release.py
python -m unittest discover -s tests -v
ruby -c yk_step_bridge.rb
ruby -c yk_step_bridge/main.rb
ruby tests/test_cleanup.rb
```

Exemplos públicos sintéticos: [tetraedro vermelho](examples/tetraedro_vermelho.json), [faixa muito fina](examples/tetraedro_faixa_fina.json) e [contato entre tetraedros](examples/tetraedros_em_contato.json). Nenhum modelo comercial recebido nos testes está incluído no repositório.

Copyright © 2026 Yruam Kaffer de Faria. **PolyForm Noncommercial License 1.0.0**. Uso e modificações sem fins comerciais conforme [licença](LICENSE.txt). Projeto independente, sem afiliação ou certificação por FreeCAD, SketchUp ou Trimble.

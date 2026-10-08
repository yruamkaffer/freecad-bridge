# FreeCAD Bridge

**Do STEP ao SketchUp: componentes nomeados, cores e verificação de sólidos.**

Extensão para SketchUp desktop que utiliza o FreeCAD em segundo plano para importar arquivos STEP. Leve modelos CAD para cenas, vistas, apresentações e renders com peças separadas e geometria editável no SketchUp, sem executar uma macro manualmente a cada importação.

**Autor:** Yruam Kaffer de Faria · **Versão:** 0.3.0 · **Plataforma alvo:** Windows / SketchUp 2026

[English](README.en.md) · [Instalação](docs/INSTALACAO.md) · [Uso](docs/USO.md) · [Problemas comuns](docs/SOLUCAO_DE_PROBLEMAS.md) · [Arquitetura](docs/ARQUITETURA.md) · [Licença](LICENSE.txt)

## Por que existe

Um modelo sólido no CAD nem sempre chega ao SketchUp como um componente sólido. Triangulação, tolerâncias, bordas abertas e orientação de faces podem afetar o resultado. O FreeCAD Bridge reúne conversão, tentativas de reparo, criação de componentes e verificação final em um único fluxo.

O FreeCAD precisa estar instalado, mas sua interface não precisa ser aberta para cada importação.

## Recursos

- Importação de `.step` e `.stp` pelo menu do SketchUp.
- Um componente por sólido, conservando a posição das peças.
- Recuperação de nomes e cores presentes no STEP quando associados com segurança à geometria.
- Cores RGB uniformes e por face quando existe correspondência de triangulação.
- Remoção de divisões coplanares com o mesmo material e suavização de curvas.
- Tentativas de reparo CAD e novas triangulações antes de rejeitar uma peça.
- Verificação do sólido final pelo SketchUp.
- Relatório com índice STEP, nome, estado, botão **Localizar** e exportação em texto.
- Importação do JSON intermediário compatível.

## Comece aqui

1. Instale o FreeCAD e localize `FreeCADCmd.exe`, normalmente na pasta `bin` da instalação.
2. Baixe [FreeCAD_Bridge_0.3.0.rbz](dist/FreeCAD_Bridge_0.3.0.rbz).
3. No SketchUp, use **Extensões → Gerenciador de Extensões → Instalar extensão** e selecione o RBZ.
4. Reinicie o SketchUp.
5. Abra **Extensões → FreeCAD Bridge → Configurar FreeCADCmd**.
6. Use **Importar STEP automaticamente**. Comece com desvio linear `0,05 mm` e modo **Estrito**.

O pacote atual não tem assinatura oficial. Consulte o [guia de instalação](docs/INSTALACAO.md) se o carregamento for bloqueado. O ZIP do repositório contém código e documentação; o instalador do SketchUp é o `.rbz`.

## Dois modos

| Modo | Comportamento | Quando usar |
| --- | --- | --- |
| Estrito | Exige CAD válido, malha fechada e sólido final reconhecido pelo SketchUp. Uma falha impede ou desfaz toda a importação. | Quando todos os componentes precisam passar pelas verificações. |
| Visualização | Permite geometria problemática com avisos e identificação de peças para conferência. | Para localizar problemas e inspecionar o modelo. |

## Compatibilidade e verificações

Desenvolvido para **SketchUp 2026 desktop no Windows**. O fluxo anterior de conversão e importação foi utilizado pelo autor com modelos de teste. As novas funções de 0.3.0 receberam verificações de sintaxe e testes isolados de cores e malhas; a validação completa dessas funções no FreeCAD e SketchUp ainda está pendente. Isso não equivale a certificação pelos fornecedores.

FreeCAD 1.1 é o alvo da integração de metadados. Não há matriz de versões certificadas. macOS, Linux e SketchUp Web não são suportados pelo fluxo atual de seleção do executável Windows.

## Limites

- Um sólido CAD não tem garantia universal de fechamento no SketchUp.
- Curvas tornam-se segmentos/faces; parâmetros, sketches e features do CAD não são transferidos.
- O STEP precisa conter nomes e cores; dados ausentes não podem ser recuperados.
- Reparos e triangulações diferentes podem deixar cores por face incompletas.
- Texturas, transparência e materiais físicos não são transferidos.
- Montagens entram como componentes posicionados dentro de um grupo, sem árvore original de submontagens ou definições compartilhadas de peças repetidas.
- O conversor atual exige sólidos; arquivos compostos somente por superfícies não são aceitos.

Veja [uso e validação](docs/USO.md), [formato JSON](docs/FORMATO_JSON.md) e [roadmap](docs/ROADMAP.md).

## Desenvolvimento e contribuição

```sh
python tools/build_release.py
python -m unittest discover -s tests -v
```

Build e testes isolados usam Python padrão e não exigem FreeCAD. A importação real depende dos aplicativos. Leia [CONTRIBUTING.md](CONTRIBUTING.md) para validação manual, bugs e pull requests.

Compartilhe modelos somente quando tiver autorização. Projetos de clientes e da empresa não devem ser publicados como exemplos sem consentimento.

## Licença

Copyright © 2026 **Yruam Kaffer de Faria**.

**PolyForm Noncommercial License 1.0.0**: código público para estudo, uso e modificações conforme os termos não comerciais da licença. Publicar no GitHub não autoriza uso comercial. Não é apresentado como software open source sob uma licença que permita qualquer finalidade.

O titular pode conceder autorizações separadas. Leia [LICENSE.txt](LICENSE.txt) e [NOTICE.txt](NOTICE.txt). FreeCAD e SketchUp são dependências externas com suas próprias licenças e marcas, não incluídas no pacote.

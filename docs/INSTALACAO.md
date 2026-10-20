# Instalação, atualização e remoção

## Requisitos

| Item | Requisito desta versão |
| --- | --- |
| Sistema | Windows; o seletor espera um executável `.exe`. |
| SketchUp | Desktop; alvo de desenvolvimento 2026. |
| FreeCAD | Instalação com FreeCADCmd e módulos Part, MeshPart e Import. Versão 1.1 é o alvo de metadados. |
| Python separado | Não necessário para usar a extensão; o conversor usa o ambiente do FreeCAD. |
| Internet | Não necessária para o fluxo de conversão implementado. Downloads/publicação são operações separadas. |

Não há homologação para todas as versões. Comece com um modelo pequeno com dimensão e cor conhecidas.

## Passo a passo

1. Obtenha `FreeCAD_Bridge_0.4.0.rbz` de `dist/` ou do asset da Release, quando publicado.
2. Abra o Gerenciador de Extensões, clique em Instalar extensão e selecione o RBZ.
3. Reinicie o SketchUp.
4. Use **Extensões → FreeCAD Bridge → Configurar FreeCADCmd**.
5. Selecione `FreeCADCmd.exe`; não selecione `FreeCAD.exe`, atalho ou pasta.
6. Consulte **Diagnóstico (0.4.0)** para conferir caminho e existência do executável.

Nomes e localização dos controles podem variar com idioma e versão.

## Ativar a barra

Na primeira utilização, a barra aparece automaticamente. Se estiver oculta, abra **Extensões → FreeCAD Bridge → Mostrar barra de ferramentas**. Arraste-a para encaixar ou manter flutuante. Consulte o [guia dos ícones](BARRA_DE_FERRAMENTAS.md).

Confira **Diagnóstico (0.4.0)** depois de reiniciar. Esta versão preserva configurações e identificadores internos da 0.3.0. Builds de diagnóstico não publicados não fazem parte desta distribuição.

## Sem assinatura oficial

Uma política que carrega apenas extensões identificadas pode bloquear este RBZ. Consulte as configurações do Gerenciador de Extensões e aprove o carregamento da extensão não identificada se essa opção estiver disponível na instalação.

Referência oficial: [Política de carregamento](https://help.sketchup.com/pt-br/extensions-loading-policy). O SHA-256 em `dist/SHA256.txt` verifica integridade; não substitui assinatura nem certifica segurança.

## Atualizar

Instale o novo RBZ e reinicie. O nome visível é FreeCAD Bridge, mas `yk_step_bridge.rb`, `yk_step_bridge/` e o identificador de configuração foram preservados para continuidade. Evite instalar cópias renomeadas em paralelo.

A configuração fica em `yk_step_bridge_settings.json` na pasta Plugins do usuário do SketchUp. Diagnóstico mostra o caminho efetivo. Se mover ou atualizar o FreeCAD, configure o executável novamente.

## Remover

Desinstale pelo gerenciador e reinicie. Para apagar também a configuração, feche o SketchUp e remova apenas `yk_step_bridge_settings.json` do caminho mostrado por Diagnóstico. A geometria já importada permanece no modelo sem depender da extensão.

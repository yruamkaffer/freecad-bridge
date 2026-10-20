# Publicar no GitHub

## Identidade sugerida

- Repositório: `freecad-bridge`
- Descrição: `Importador STEP para SketchUp com FreeCAD em segundo plano, componentes nomeados, cores e validação de sólidos.`
- Visibilidade: pública.
- Topics: `sketchup`, `freecad`, `step`, `cad`, `ruby`, `python`, `3d-modeling`, `noncommercial`.

Repositório oficial: https://github.com/yruamkaffer/freecad-bridge. Os links internos são relativos. As instruções abaixo também servem como referência para forks e futuras Releases.

## Enviar o projeto

Extraia o pacote e envie o conteúdo da pasta `freecad-bridge/` para a raiz de um repositório novo. Evite inicializar o repositório com README/licença diferentes, pois esses arquivos já vêm no pacote.

Use upload pela interface ou um cliente Git. A autenticação deve ocorrer pelos mecanismos do GitHub; não envie senha ou token em conversas, arquivos ou issues. Não há credencial ou modelo de trabalho do autor no pacote.

O `.gitignore` exclui modelos CAD, configuração local, logs e caches. `dist/` inclui o instalador para que o download funcione antes da primeira Release.

## Release

1. Rode testes e `python tools/build_release.py`.
2. Faça o commit revisado.
3. Crie Release com tag `v0.4.0` apontando para esse commit.
4. Copie [RELEASE_0.4.0.md](RELEASE_0.4.0.md) nas notas.
5. Anexe RBZ e SHA256 de `dist/`.
6. Revise antes de publicar.

O ZIP de código do GitHub não substitui o RBZ. Não apresente o pacote sem assinatura como certificado.

Confira autoria, licença, ausência de confidenciais e estado de validação. Referências: [Criar repositório](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) e [Gerenciar Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

## Distribuição atual

O README aponta para o instalador 0.4.0 em dist/. Versões antigas podem permanecer para referência; confira a versão antes de instalar. As notas históricas 0.3.0 são preservadas. O build da versão nova inclui ícones e AJUDA.txt além do código/licença. Não publique os STEP de diagnóstico recebidos em conversas como exemplos do projeto.

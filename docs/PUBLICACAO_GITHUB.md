# Atualizar o GitHub e publicar a versão 0.5.0

Este pacote contém os arquivos preparados. Preparar o ZIP não publica commits nem cria uma Release no GitHub.

## Conferência

1. Extraia o ZIP; a pasta freecad-bridge contém a raiz do repositório.
2. Confira README, CHANGELOG, guias e [notas da versão](RELEASE_0.5.0.md).
3. Confira autoria Yruam Kaffer de Faria, PolyForm Noncommercial e ausência de modelos comerciais. O pacote não contém credenciais ou configurações pessoais.
4. Para usar a extensão, instale o RBZ de dist/. Para atualizar o repositório, use o conteúdo completo da pasta, incluindo .github e .gitignore.

## Com Git local

Atualize seu clone de yruamkaffer/freecad-bridge e copie os arquivos desta pasta para ele, preservando .git e eventuais arquivos próprios. Revise as diferenças antes do commit. Na raiz:

```sh
python tools/build_release.py
python -m unittest discover -s tests -v
ruby -c yk_step_bridge.rb
ruby -c yk_step_bridge/main.rb
ruby tests/test_cleanup.rb
git status
git diff
```

Depois de revisar, faça o commit/push com uma mensagem como `Release 0.5.0: bounded mesh repairs and surface handling`. O workflow incluído executa testes Python/Ruby e valida o pacote em pushes/PRs; aguarde seu resultado.

Se usar upload pelo site, envie o conteúdo da raiz, sem criar uma pasta freecad-bridge dentro da raiz existente. Confira especialmente os arquivos novos cad_tools.py/conversion.py, testes, exemplos e .github/workflows/ci.yml.

## Release

Crie a tag **v0.5.0** apontando para o commit revisado. Copie RELEASE_0.5.0.md para as notas e anexe **FreeCAD_Bridge_0.5.0.rbz** e **SHA256.txt** de dist/. O README já aponta para o instalador atualizado no repositório.

A versão continua sem assinatura oficial. O ícone do Gerenciador de Extensões não é definido pelos PNGs da barra. Publicar aqui não publica no Extension Warehouse.

## Não enviar

Não inclua STEP/FCStd/SKP de trabalho, JSONs de montagens privadas, relatórios com dados comerciais, caches, logs ou yk_step_bridge_settings.json. Os exemplos distribuídos são sintéticos. O .gitignore já cobre formatos CAD e configurações comuns; JSONs privados também devem ser mantidos fora da pasta do projeto.

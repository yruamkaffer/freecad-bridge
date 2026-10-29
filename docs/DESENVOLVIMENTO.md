# Desenvolvimento e empacotamento — 0.5.0

## Ambiente

Python 3.10+ para build, tratamentos JSON offline e testes. Nenhum pacote externo é necessário. Ruby 3.2+ para conferir sintaxe e executar os testes isolados do importador. A conversão STEP real usa os módulos do FreeCADCmd instalado; não usa o Python do build.

```sh
python tools/build_release.py
python -m unittest discover -s tests -v
python tools/build_release.py --check
ruby -c yk_step_bridge.rb
ruby -c yk_step_bridge/main.rb
ruby tests/test_cleanup.rb
```

O build usa lista explícita de 25 arquivos: carregador, Ruby, cinco módulos Python, licenças/ajuda e ícones. Valida sintaxe Python, cópias da licença/avisos, conteúdo do ZIP e SHA256. O mesmo ambiente/bytes deve produzir a mesma saída; implementações de compressão podem mudar o hash. O build não assina nem executa Ruby/SketchUp.

## Cobertura

Os testes Python cobrem metadados ambíguos, RGB, proveniência de cores, malhas fechadas/abertas, vértices pinçados, união de vértices, separação de contatos, rejeição por limites, superfícies e modos de importação. Também conferem instalador, recursos, links locais e exemplo sintético.

Os sete testes Ruby carregam métodos reais com objetos mínimos da API. Cobrem suavização após restauração, limpeza bem-sucedida, bordas/arestas acentuadas, preservação de material, falha de restauração e classificação correta de sólidos/superfícies/CAD inválido. Não simulam o kernel ou o aplicativo inteiro.

O workflow `.github/workflows/ci.yml` executa build --check, testes Python e Ruby em pushes/PRs. Sua inclusão no pacote não significa que a execução no GitHub já ocorreu; confira o resultado depois de publicar.

## Regressão com modelos privados

Use os arquivos comerciais fora da raiz do repositório. Não os envie como exemplos. A ferramenta abaixo testa o mesmo motor de malha com um JSON de diagnóstico:

```sh
python tools/treat_json.py /caminho/privado/entrada.json --output /caminho/privado/saida.json --mode visualization --treatment complete
```

Registre contagem de peças, tipos, operações aceitas/rejeitadas, volume e validação final no SketchUp. Testes com Open CASCADE em outro ambiente não comprovam a execução de Import.insert, MeshPart ou FreeCADCmd no Windows.

## Exemplos públicos

Importe tetraedro_vermelho.json para conferir escala/cor básica. Use Tratar JSON existente com tetraedro_faixa_fina.json e tetraedros_em_contato.json para exercitar as novas correções. Compare Completo e Conservador no segundo. São geometrias sintéticas, não versões reduzidas de modelos comerciais.

## Alterar versão

Atualize carregador, interfaces/relatório/ajuda, motor, README, changelog e guias atuais; preserve notas históricas. Gere o RBZ antes dos testes de distribuição e atualize SHA256. Não mude identificadores de instalação/configuração apenas para mudar a apresentação. Não afirme homologação nos aplicativos sem execução real.

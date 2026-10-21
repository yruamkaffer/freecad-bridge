# Desenvolvimento e empacotamento

## Ambiente

Use Python 3.10 ou mais recente para as ferramentas do repositório. Nenhuma biblioteca externa é necessária para o build ou os testes Python. Os testes de regressão da limpeza também usam Ruby 3.x, sem gems externas. A extensão não usa esse Python para importar STEP: a conversão real roda no ambiente do FreeCAD.

## Comandos na raiz

```sh
python -m unittest discover -s tests -v
python tools/build_release.py
python tools/build_release.py --check
ruby -c yk_step_bridge.rb
ruby -c yk_step_bridge/main.rb
ruby tests/test_cleanup.rb
```

O build extrai a versão de `yk_step_bridge.rb`, verifica a presença dos arquivos necessários, confere sintaxe Python e igualdade das cópias de licença/avisos. Gera `dist/FreeCAD_Bridge_<versão>.rbz` e `dist/SHA256.txt`, usando somente arquivos explicitamente selecionados. Inclui os cinco SVGs originais, dez PNGs de 24/32 pixels e AJUDA.txt. Não inclui modelos, caches, configuração de usuário ou os guias do repositório no RBZ.

Datas e permissões de entradas ZIP são fixadas para reduzir variação no empacotamento. O mesmo ambiente e os mesmos bytes de origem devem gerar a mesma saída; diferenças entre implementações de compressão ainda podem afetar o hash. O build não assina o instalador e não verifica sintaxe Ruby.

O modo `--check` confere o instalador atual contra todos os arquivos de origem e seu hash sem reempacotar. O build normal atualiza os hashes de todos os RBZ presentes em dist/. A geração de ícones não é necessária para usar ou empacotar o projeto: os recursos finais e SVGs editáveis estão versionados.

## Cobertura dos testes

Os testes verificam RGB inválido, associação ambígua, associação de cores independente da orientação, triângulo sem correspondência, tetraedro fechado com face repetida/invertida e tetraedro aberto. Usam geometrias e objetos mínimos; não carregam FreeCAD, Open CASCADE ou SketchUp.

Para mudanças Ruby, rode `ruby -c yk_step_bridge.rb` e `ruby -c yk_step_bridge/main.rb` quando houver Ruby instalado. Mesmo assim, valide no SketchUp: a sintaxe não verifica disponibilidade ou comportamento das APIs.

Os testes de distribuição também conferem o conjunto/bytes do instalador, dimensões dos PNGs, links locais Markdown e fechamento/volume do exemplo sintético. Eles não simulam a barra nativa.

## Validação nos aplicativos

Siga a matriz manual de CONTRIBUTING. Registre versão, arquivo de teste, modo, tolerância, contagem de peças, escala, cores e fechamento. Diferencie:

- sintaxe verificada;
- teste isolado passado;
- conversão real no FreeCADCmd;
- importação real no SketchUp.

## Alterar versão

Atualize metadados do carregador e as referências de versão no menu, relatório, README, changelog e notas de Release. Gere o RBZ e atualize os links de download. Não mude o identificador do carregador apenas para renomear a apresentação.

Código assinado futuramente precisará ser submetido novamente ao serviço oficial se seu conteúdo for alterado. Até lá, distribua como pacote sem assinatura.

## Regressão da restauração — 0.4.2

`ruby tests/test_cleanup.rb` carrega os métodos reais de limpeza/suavização com objetos mínimos da API. Força uma perda de fechamento e verifica que a malha restaurada recebe soft/smooth; também cobre limpeza bem-sucedida, arestas acentuadas, bordas abertas, materiais diferentes e falha de restauração. Não executa o kernel geométrico nem prova o comportamento de manifold? ou erase! no SketchUp. Para integração, use modelo próprio que acione a restauração e confira relatório, cores e sólido no aplicativo.

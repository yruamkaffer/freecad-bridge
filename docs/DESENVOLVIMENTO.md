# Desenvolvimento e empacotamento

## Ambiente

Use Python 3.10 ou mais recente para as ferramentas do repositório. Nenhuma biblioteca externa é necessária para o build ou os testes isolados. A extensão não usa esse Python para importar STEP: a conversão real roda no ambiente do FreeCAD.

## Comandos na raiz

```sh
python -m unittest discover -s tests -v
python tools/build_release.py
```

O build extrai a versão de `yk_step_bridge.rb`, verifica a presença dos arquivos necessários, confere sintaxe Python e igualdade das cópias de licença/avisos. Gera `dist/FreeCAD_Bridge_<versão>.rbz` e `dist/SHA256.txt`, usando somente arquivos explicitamente selecionados. Não inclui modelos, caches, configuração de usuário ou documentação no RBZ.

Datas e permissões de entradas ZIP são fixadas para reduzir variação no empacotamento. O mesmo ambiente e os mesmos bytes de origem devem gerar a mesma saída; diferenças entre implementações de compressão ainda podem afetar o hash. O build não assina o instalador e não verifica sintaxe Ruby.

## Cobertura dos testes

Os testes verificam RGB inválido, associação ambígua, associação de cores independente da orientação, triângulo sem correspondência, tetraedro fechado com face repetida/invertida e tetraedro aberto. Usam geometrias e objetos mínimos; não carregam FreeCAD, Open CASCADE ou SketchUp.

Para mudanças Ruby, rode `ruby -c yk_step_bridge.rb` e `ruby -c yk_step_bridge/main.rb` quando houver Ruby instalado. Mesmo assim, valide no SketchUp: a sintaxe não verifica disponibilidade ou comportamento das APIs.

## Validação nos aplicativos

Siga a matriz manual de CONTRIBUTING. Registre versão, arquivo de teste, modo, tolerância, contagem de peças, escala, cores e fechamento. Diferencie:

- sintaxe verificada;
- teste isolado passado;
- conversão real no FreeCADCmd;
- importação real no SketchUp.

## Alterar versão

Atualize metadados do carregador e as referências de versão no menu, relatório, README, changelog e notas de Release. Gere o RBZ e atualize os links de download. Não mude o identificador do carregador apenas para renomear a apresentação.

Código assinado futuramente precisará ser submetido novamente ao serviço oficial se seu conteúdo for alterado. Até lá, distribua como pacote sem assinatura.

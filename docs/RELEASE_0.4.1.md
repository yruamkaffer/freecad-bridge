# FreeCAD Bridge 0.4.1

Intervalo ampliado do desvio linear: de 0,001–5 mm para **0,001–100 mm**. O valor padrão continua **0,05 mm**. A interface informa os novos limites e rejeita valores fora do intervalo.

A barra de ferramentas com cinco atalhos da 0.4.0 está incluída. O conversor Python, o tratamento de cores, as tentativas de reparo, os limites angulares e a reconstrução das faces não foram alterados nesta atualização.

## Instalação

Instale FreeCAD_Bridge_0.4.1.rbz pelo Gerenciador de Extensões e reinicie o SketchUp. Confira Diagnóstico (0.4.1). Configurações e identificadores anteriores são preservados.

## Qualidade

Para modelos grandes, compare o resultado em 5, 10 e 20 mm antes de aumentar mais. Maior desvio não garante redução proporcional de faces e pode deixar o contorno facetado. A geometria permanece poligonal. A suavização de arestas é separada do desvio linear.

## Validação e distribuição

Sintaxe Ruby/Python, conjunto e dimensões dos ícones, hash do instalador, links locais e dez testes isolados passaram. O funcionamento real e a qualidade no modelo do usuário precisam de verificação no SketchUp; esta atualização não promete reparar qualquer STEP ou garantir fechamento universal.

Alvo: SketchUp 2026 desktop Windows e FreeCAD instalado para conversão STEP. Pacote sem assinatura oficial. Copyright © 2026 Yruam Kaffer de Faria. PolyForm Noncommercial License 1.0.0.

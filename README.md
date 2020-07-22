# Algoritmo Genetico - IC
 Algoritmo Genético para minimizar uma função objetivo inicialmente com um único parâmetro

Cria a população inicial com a função **create_population**  >
Calcula o valor da função objetivo que usa como parâmetro a soma dos cromossomos usando a função **fit_calculation** >
Ordena a população de acordo com a nota de avaliação com a função **order_population** >
Obtêm-se a melhor solução que neste caso é o primeiro indivíduo depois de ordenado >
Coloca-se tal valor em um vetor de melhores soluções > 
Imprime-se a geração atual >
Calcula-se a menor nota de avaliação (que está na última posição, já que o vetor foi ordenado) para então usá-la para normalizar as notas com a função **normalize**
Obs: a função **normalize** adiciona o valor positivo da menor nota + 1, garantindo que sempre terá um número positivo para então fazer a seleção de indivíduos (isto não interfere na precisão do algoritmo, já que serve somente de forma quantitativa e o valor adicionado, será adicionado a todas as notas no vetor, que será usado único e exclusivamente para a seleção de indivíduos). >
Escolhe-se os indivíduos pais usando a função **select_father** e o **Método da Roleta Viciada** ,a partir dos indivíduso pais serão gerados os indivíduos filhos >
Usa-se o **Crossover de Ponto Único**  com a função **crossover** para gerais tais filhos >
Aplica-se a mutação com a função **mutation** usando **Gauss** (com o meio no 0 e variando o desvio para mais ou para menos) >
Sobrescreve-se a população antiga com a nova população criada usando um "construtor" (linha 140) >
Retorna-se ao calculo dos valores na função objetivo e refaz-se o processo até o número de populações estipulado ser atingido (linha 166)

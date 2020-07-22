from random import random as rnd
from random import gauss

#Função de avaliação
def evaluation_function(self, value):
        return ((-pow(value, 2)) - 10*value + 3)


#Criação da classe indivíduo
class Individuo():
    def __init__(self, number_of_genes, upper_limit, lower_limit, generation = 0): #Construtor da classe
        self.number_of_genes = number_of_genes
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.generation = generation
        self.cromossomo = []
        self.evaluation_note = 0
        
        for i in range(self.number_of_genes): #cria indivíduo
            value = round(rnd()*(self.upper_limit - self.lower_limit) + self.lower_limit, 3)
            self.cromossomo.append(value)
            
    def fit_calculation(self): #calcula a soma do resultado da função usando como parâmetro a soma de todos os genes
        value = 0
        for i in range(len(self.cromossomo)):
            value = value + self.cromossomo[i]
        
        self.evaluation_note = evaluation_function(self, value)
        return self.evaluation_note
            
    def crossover(self, second_father): #método crossover de ponto único
        cut = round(rnd() * len(self.cromossomo))
                
        son_1 = second_father.cromossomo[0:cut] + self.cromossomo[cut::] #0:x pega os genes de 0 até o ponto x#
        son_2 = self.cromossomo[0:cut] + second_father.cromossomo[cut::]
        
        children = [ Individuo(self.number_of_genes, self.upper_limit, self.lower_limit, self.generation + 1), #Cria dois individuos
                Individuo(self.number_of_genes, self.upper_limit, self.lower_limit, self.generation + 1) ]        
    
        children[0].cromossomo = son_1
        children[1].cromossomo = son_2
        
        return children
     
    def mutation(self, mutation_rate, standart_deviation): #Mutação usando gauss (com meio no 0 variando o desvio para mais ou para menos)
        for i in range(len(self.cromossomo)):
            if rnd() < mutation_rate:
                self.cromossomo[i] = round(self.cromossomo[i] + gauss(0, standart_deviation), 3)
        return self            
        
class Algoritmo_Genético():
    def __init__(self, number_of_individuals):
        self.number_of_individuals = number_of_individuals
        self.population = [] #lista de indivíduos
        self.best_solution = []
        self.solution_list = [] #Usado posteriormente para plots
        self.normalize_notes = []
        self.generation = 0
        
        for i in range(number_of_individuals):#preenche o vetor de notas normalizadas com 0
            self.normalize_notes.append(0)
      
    
    def create_population(self,number_of_genes, upper_limit, lower_limit): #cria população
        for i in range(self.number_of_individuals):
            self.population.append(Individuo(number_of_genes, upper_limit, lower_limit))
    
    def order_population(self): #Ordena a população de acordo com a nota de avaliação
        self.population = sorted(self.population, key = lambda population: population.evaluation_note, reverse = True)
      
    def best_individual(self, individuo): #Verifica se o atual indivíduo é o melhor
        if individuo.evaluation_note > self.best_solution.evaluation_note:
            self.best_solution = individuo
            
#Adiciona o valor positivo da menor nota + 1 para sempre termos um número positivo para então fazer a seleção de indivíduos
    def normalize(self, lowest_note):
        i = 0
        for individuo in self.population:
            note = individuo.evaluation_note + abs(lowest_note) + 1
            self.normalize_notes[i] = note
            i += 1
            
    def sum_notes(self): #Soma as notas normalizadas
        soma = 0
        for i in range(len(self.normalize_notes)):
            soma += self.normalize_notes[i]
        return soma
    
    def select_father(self, sum_note): #seleciona o pai de acordo com as notas normalizadas
        father = -1
        sorted_value = rnd() * sum_note
        soma = 0
        i = 0
        
        while i < len(self.population) and soma < sorted_value:
            soma += self.normalize_notes[i]
            father += 1
            i +=1
        return father
    
    def view_generation(self): #visualiza geração
        best = self.population[0]
        print("Geração:%s -> Valor: %s Cromossomo:%s" % (self.population[0].generation,
                                                                    best.evaluation_note,
                                                                    best.cromossomo) )
                                                                      
        #Cria população > Calcula os valores na função > Ordena > Pego a melhor solução que neste caso é o primeiro indivíduo depois de ordenado >
        #Jogar na lista de melhores soluções > Imprimir a geração atual > Calcular a menor nota para usá-la na normalização > normalizar notas >
        # Gerar pais > Gerar filhos com crossover > Mutação > Nova população > Retornar no calculo dos valores na função
    def resolve(self, mutation_rate, standart_deviation, generations_number, number_of_genes, upper_limit, lower_limit):
        self.create_population(number_of_genes, upper_limit, lower_limit)
        
        for individuo in self.population:
            individuo.fit_calculation()
        
        self.order_population()
        self.best_solution = self.population[0]
        self.solution_list.append(self.best_solution.evaluation_note)   
        self.view_generation()
       
        #pega a menor nota de avaliação que está na última posição, já que o vetor foi ordenado
        lowest_note = self.population[number_of_individuals-1].evaluation_note
        self.normalize(lowest_note)
        
        for geracao in range(generations_number):
            evaluation_sum = self.sum_notes()
            new_population = []
            
            for generated_individuals in range(0, self.number_of_individuals, 2):
                father_1 = self.select_father(evaluation_sum)
                father_2 = self.select_father(evaluation_sum)
                 
                children = self.population[father_1].crossover(self.population[father_2]) 
                
                
                new_population.append(children[0].mutation(mutation_rate, standart_deviation))
                new_population.append(children[1].mutation(mutation_rate, standart_deviation))
       
            
            self.population = list(new_population)  #sobrescreve a população antiga com um "construtor"
            
                                   
            for individuo in self.population:
                individuo.fit_calculation()
                
            self.order_population()
            self.view_generation()
            
            best = self.population[0]
            self.solution_list.append(best.evaluation_note)
            self.best_individual(best)
      
        print("\nMelhor solução -> Geração:%s -> Valor: %s Cromossomo:%s" % 
              (self.best_solution.generation, 
                self.best_solution.evaluation_note,
                self.best_solution.cromossomo))
        
        return self.best_solution.cromossomo   

if __name__ == '__main__':
    number_of_individuals = 100
    number_of_genes = 5
    upper_limit = 100
    lower_limit = -20
    mutation_rate = 0.01
    generations_number = 1000
    standart_deviation = 0.01
    
    ag = Algoritmo_Genético(number_of_individuals)
    result = ag.resolve(mutation_rate, standart_deviation, generations_number, number_of_genes, upper_limit, lower_limit)
    
   
    
    
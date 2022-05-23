from telnetlib import STATUS
from django.http import JsonResponse
from django.shortcuts import render
#Importing the required libraries.
import numpy as np
from random import random
from typing import Callable, List, Tuple
from random import choices, randint, randrange
from functools import partial
import time

#Defining each variable and function type

Genome = List[int]  #Genome is just a list of 0,1 eg> g1 = [0,1,1,0,0], g2 = [1,0,1,1,0]
Population = List[Genome]  #Population is a list of all genomes eg> p1 = [g1,g2,...]
FitnessFunc = Callable[[Genome], float]  #The fitness function takes a Genome and returns a fitness value for the given Genome
PopulationFunc = Callable[[],Population]  #The population function generates a list of Genomes, the list is called the current generation population
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]  #The Selection function takes a population and the fitness function and gives us a pair of genomes (called parents) prefering genomes with higher fitness values
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]  #The Crossover Function takes two parent genomes sptilts them randomly at an index and then switches the sliced parts of the genome
MutationFunc = Callable[[Genome], Genome]  #Mutation function changes the given number of values in a genome depending on the given value of probability and returns the mutated genome

#A general purpose thing object to store each item, an named tupple could also be used for the same

class Thing:
    def __init__(self,name,value,weight):
        self.name = name
        self.value = value
        self.weight = weight
# Thing = namedtuple('Thing',['name','value','weight'])

things = []

#defining all of the above mentioned functions

def generate_genome(length: int) -> Genome:
    return choices([0,1],k=length)

def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

def fitness(genome: Genome, things: List[Thing], weight_limit: float) -> float:
    if len(genome) != len(things):
        raise ValueError("Genome and Thimgs must be of same length")
    
    weight  = 0
    value = 0
    for i, thing in enumerate(things):
        if genome[i] == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0
    
    return value

def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population= population,
        weights= [fitness_func(genome) for genome in population],
        k=2
    )

def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome,Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b need to be of the same length")

    length = len(a)
    if length < 2:
        return a,b
    
    p = randint(1,length-1)
    return a[:p] + b[p:] , b[:p] + a[p:]

def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index]-1)
    return genome

def run_evolution(
    populate_func: PopulationFunc,
    fitness_func: FitnessFunc,
    fitness_limit: float,
    selection_func: SelectionFunc = selection_pair,
    crossover_func: CrossoverFunc = single_point_crossover,
    mutation_func: MutationFunc = mutation,
    generation_limit: int = 700) -> Tuple[Population, int]:

    population = populate_func()

    for i in range(generation_limit):
        population = sorted(
            population,
            key= lambda genome: fitness_func(genome),
            reverse= True
        )

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[:2]

        for j in range(int(len(population)/2)-1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    population = sorted(
        population,
        key= lambda genome: fitness_func(genome),
        reverse= True
    )

    return population, i

def genome_to_things(genome: Genome, things: List[Thing]) -> List[Thing]:
    result = []
    for i,thing in enumerate(things):
        if genome[i]==1:
            result += [thing.name+',']
    
    return result
#Taking input of the list of items


def index(request):   
    if request.method == 'GET' and 'v1' in request.GET and 'v2' in request.GET and 'v3' in request.GET and 'v4' in request.GET and 'v5' in request.GET and 'v6' in request.GET and 'v7' in request.GET and 'w1' in request.GET and 'w2' in request.GET and 'w3' in request.GET and 'w4' in request.GET and 'w5' in request.GET and 'w6' in request.GET and 'w7' in request.GET and 'maxw' in request.GET :
        v1 = request.GET.get('v1')
        v2 = request.GET.get('v2')
        v3 = request.GET.get('v3')
        v4 = request.GET.get('v4')
        v5 = request.GET.get('v5')
        v6 = request.GET.get('v6')
        v7 = request.GET.get('v7')
        
        w1 = request.GET.get('w1')
        w2 = request.GET.get('w2')
        w3 = request.GET.get('w3')
        w4 = request.GET.get('w4')
        w5 = request.GET.get('w5')
        w5 = request.GET.get('w5')
        w6 = request.GET.get('w6')
        w7 = request.GET.get('w7')
        maxw = request.GET.get('maxw')        
        item_value=[]
        item_weight=[]
        item_value.append(int(v1))
        item_value.append(int(v2))
        item_value.append(int(v3))
        item_value.append(int(v4))
        item_value.append(int(v5))
        item_value.append(int(v6))
        item_value.append(int(v7))

        item_weight.append(int(w1))
        item_weight.append(int(w2))
        item_weight.append(int(w3))
        item_weight.append(int(w4))
        item_weight.append(int(w5))
        item_weight.append(int(w6))
        item_weight.append(int(w7))

        w=item_weight.copy()
        v=item_value.copy()
        
        
        for i in range(7):
            item_name = ['a','b','c','d','e','f','g']
            v[i]
            w[i]
            things.append(Thing(item_name[i],v[i],w[i]))
    
        #defining the weight and fitness limits

        #print("Enter the weight limit: ")
        inp_weight_limit = int(maxw)

        inp_fitness_limit = 0.50

        start = time.time()
        population, generations = run_evolution(
            populate_func= partial( 
                generate_population, size = 10, genome_length = len(things)
            ),
            fitness_func=partial(
                fitness, things = things, weight_limit = inp_weight_limit
            ),
            fitness_limit= inp_fitness_limit,
            generation_limit=700
        )
        end = time.time()
           
            
        return JsonResponse(
        {   
            
            'the':'the Best solution: ',
            'result':genome_to_things(population[0], things),
            'and':'\n  and The Value : ',
            'value':fitness(population[0], things, inp_weight_limit),
        },
        status=200,
        )
 
        
    return render(request,'index.html')

#print(f"\nnumber of generations: {generations}")
#print(f"time:{end - start}s")
#print(f"best solution: {genome_to_things(population[0], things)}")
#print(f"value: {}")
#Defining each variable and function type


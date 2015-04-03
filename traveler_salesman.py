import cProfile
from operator import itemgetter
from random import sample, shuffle, randrange, choice

__author__ = 'julio'


def crossover(parents):
    crossover_point = randrange(len(parents[0]))
    first_piece = list(parents[0][:crossover_point])
    result_chromossome = first_piece+[x for x in parents[1] if x not in first_piece]
    return tuple(result_chromossome)


def get_by_tournment(population, population_with_fitness):
    competitors = sample(population, 3)
    return sorted(competitors, key=population_with_fitness.get)[:2]


def mutate(chromossome):
    i, j = sample(chromossome, 2)
    c_list = list(chromossome)
    c_list[i], c_list[j] = c_list[j], c_list[i]
    return tuple(c_list)


def create_new_population(original_population, pop_with_fitness, c_rate, mutation_rate):
    new_population = []
    add_to_population = new_population.append
    population_len = len(original_population)
    while len(new_population) < population_len:
        parents = get_by_tournment(original_population, pop_with_fitness)

        if randrange(101) <= c_rate:
            new_chromossome = crossover(parents)
        else:
            new_chromossome = choice(parents)
        if randrange(101) <= mutation_rate:
            new_chromossome = mutate(new_chromossome)
        add_to_population(new_chromossome)

    return new_population


def generate_first_population(genes, population_size):
    population = []
    while len(population) < population_size:
        shuffle(genes)
        population.append(tuple(genes))
    return population


def get_best_fitted(population, cities):
    fitness = -1
    chromossome = ()
    population_with_fitness = {}
    for c in population:
        f = get_fitness(c, cities)
        if fitness == -1:
            fitness = f
            chromossome = c
        if f < fitness:
            fitness = f
            chromossome = c
        population_with_fitness[c] = f
    return fitness, chromossome, population_with_fitness


def get_fitness(chromossome, cities_matrix):
    start = -1
    fitness = 0
    for gene in chromossome:
        if start < 0:
            start = gene
            continue
        fitness += cities_matrix[start][gene]
        start = gene
    return fitness+cities_matrix[start][chromossome[0]]


def run(cities_matrix, population_size, generations, cross_rate, mutation_rate):
    genes = list(range(len(cities_matrix)))
    population = generate_first_population(genes, population_size)
    fitness = 0
    convergence_count = 0
    diversity = 1

    for i in range(generations):
        new_fitness, best_fitted, pop_with_fitness = get_best_fitted(population,
            cities_matrix)

        diversity = len(pop_with_fitness)/population_size

        if new_fitness < fitness or not fitness:
            fitness = new_fitness
            convergence_count = 0
        elif fitness == new_fitness:
            convergence_count += 1
        if convergence_count > 5:
            break

        population = create_new_population(population, pop_with_fitness, cross_rate, mutation_rate)

    return fitness, best_fitted, diversity


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('matrix_file')
    parser.add_argument('population_size')
    parser.add_argument('crossover_rate')
    parser.add_argument('mutation_rate')
    parser.add_argument('generations_number')
    args = parser.parse_args()
    filename = args.matrix_file
    f = open(filename, 'r')

    matrix = []
    for line in f.readlines():
        matrix.append([int(x) for x in line.split(' ')])

    pop_size = int(args.population_size)
    crossover_rate = int(args.crossover_rate)
    mutation_rate = int(args.mutation_rate)
    generations = int(args.generations_number)
    cProfile.run('print(run(matrix, pop_size, generations, crossover_rate, mutation_rate))')

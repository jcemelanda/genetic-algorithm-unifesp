from operator import itemgetter
from random import sample, shuffle, randrange, choice

__author__ = 'julio'


def drop_dupes(chromossome, reverse):
    chromossome = list(chromossome)
    if reverse:
        chromossome.reverse()
    seen = set()
    seen_add = seen.add
    chromossome = [x for x in chromossome if not (x in seen or seen_add(x))]
    if reverse:
        chromossome.reverse()
    return chromossome


def crossover(parents, genes):
    crossover_point = randrange(len(genes))
    result_chromossome = parents[0][:crossover_point]+parents[1][crossover_point:]
    reverse = choice((True, False))
    result_chromossome = drop_dupes(result_chromossome, reverse)
    result_chromossome.extend(genes - set(result_chromossome))
    return tuple(result_chromossome)


def create_new_population(original_population, replacement_size, genes):
    new_population = set()
    gene_set = set(genes)
    parents = original_population[:2]
    while len(new_population) < replacement_size:
        if choice((True, False)):
            parents.reverse()
        new_population.add(crossover(parents, gene_set))
    original_population[:-replacement_size].extend(new_population)
    return set(original_population)


def generate_first_population(genes, population_size):
    population = set()
    while len(population) < population_size:
        shuffle(genes)
        population.add(tuple(genes))
    return population


def get_fitness(chromossome, cities_matrix):
    start = -1
    fitness = 0
    for gene in chromossome:
        if start < 0:
            start = gene
            continue
        fitness += cities_matrix[start][gene]
        start = gene
    return chromossome, fitness+cities_matrix[start][chromossome[0]]


def order_by_fitness(evaluated_population):
    ordered = sorted(evaluated_population, key=itemgetter(-1))
    return ordered[0][1], [x[0] for x in ordered]


def run(cities_matrix, population_size, replacement_size, generations):
    genes = list(range(len(cities_matrix)))
    population = generate_first_population(genes, population_size)
    fitness = 0
    fitness_changed = True
    for i in range(generations):
        fitness_changed = False
        new_fitness, population_list = order_by_fitness([get_fitness(x, cities_matrix) for x in population])
        if new_fitness < fitness or not fitness:
            fitness = new_fitness
            fitness_changed = True
        print(fitness)
        population = create_new_population(population_list, replacement_size, genes)


    return fitness, population_list[0]




if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('matrix_file')
    parser.add_argument('population_size')
    parser.add_argument('replacement_size')
    args = parser.parse_args()
    filename = args.matrix_file
    f = open(filename, 'r')

    matrix = []
    for line in f.readlines():
        matrix.append([int(x) for x in line.split(' ')])

    pop_size = int(args.population_size)
    rep_size = int(args.replacement_size)
    print(run(matrix, pop_size, rep_size, 1000))

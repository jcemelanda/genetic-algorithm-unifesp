from operator import itemgetter
from random import sample, shuffle, randrange, choice

__author__ = 'julio'


def drop_dupes(chromossome, reverse):
    dupe_chromossome = chromossome
    if reverse:
        dupe_chromossome = chromossome[::-1]
    seen = set()
    seen_add = seen.add
    chromossome = [x if not (x in seen or seen_add(x)) else -1 for x in dupe_chromossome]
    return chromossome[::-1] if reverse else chromossome


def crossover(parents, genes):
    crossover_point = randrange(len(genes))
    result_chromossome = parents[0][:crossover_point]+parents[1][crossover_point:]
    reverse = choice((True, False))
    result_chromossome = drop_dupes(result_chromossome, reverse)
    if -1 in result_chromossome:
        new_genes = list(genes - set(result_chromossome))
        shuffle(new_genes)
        while -1 in result_chromossome:
            result_chromossome[result_chromossome.index(-1)] = new_genes.pop()
    return tuple(result_chromossome)


def create_new_population(original_population, replacement_size, genes, c_rate):
    new_population = []
    gene_set = set(genes)
    parents = sample(original_population[:replacement_size],2)
    while len(new_population) < replacement_size:
        do_crossover = randrange(101) <= c_rate
        if do_crossover:
            if choice((True, False)):
                parents.reverse()
            new_population.append(crossover(parents, gene_set))
        else:
            new_population.append(choice(parents))
    original_population[:-replacement_size].extend(new_population)
    return set(original_population)


def generate_first_population(genes, population_size):
    population = []
    while len(population) < population_size:
        shuffle(genes)
        population.append(tuple(genes))
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


def run(cities_matrix, population_size, replacement, generations, cross_rate):
    genes = list(range(len(cities_matrix)))
    population = generate_first_population(genes, population_size)
    fitness = 0
    fitness_changed = True
    for i in range(generations):
        fitness_changed = False
        new_fitness, population_list = order_by_fitness(
            [get_fitness(x, cities_matrix) for x in population])
        if new_fitness < fitness or not fitness:
            fitness = new_fitness
            fitness_changed = True
        print(fitness)
        population = create_new_population(population_list, replacement,
            genes, cross_rate)

    return fitness, population_list[0]


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('matrix_file')
    parser.add_argument('population_size')
    parser.add_argument('replacement_size')
    parser.add_argument('crossover_rate')
    parser.add_argument('generations_number')
    args = parser.parse_args()
    filename = args.matrix_file
    f = open(filename, 'r')

    matrix = []
    for line in f.readlines():
        matrix.append([int(x) for x in line.split(' ')])

    pop_size = int(args.population_size)
    rep_size = int(args.replacement_size)
    crossover_rate = int(args.crossover_rate)
    generations = int(args.generations_number)
    print(run(matrix, pop_size, rep_size, generations, crossover_rate))

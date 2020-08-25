import math
import random as rd

import numpy as np
from numpy.random import choice


class Evolution:
    """Class for the functions of a genetic algorithm.
    Steps involved in the algorithm:
    1. Initialization
    2. Fitness calculation
    3. Selection
    4. Crossover
    5. Mutation
    5. Repetition
    """

    def __init__(self, n, x, number_of_parents, population_size):
        """Initializes the class with the basic information required for
        genetic algorithm.

        Args:
            n (int): the length of individual list
            x (int): the goal number to be achieved
            number_of_parents (int): the number of individuals to be selected
                for crossover
            population_size (int): the number of individuals in each generation
        """
        self.length = n
        self.goal = x
        self.number_of_parents = number_of_parents
        self.population_size = population_size
        self.slice_at = rd.randrange(1, n)  # position for crossover

    def get_random_population(self):
        """Generates a list of random individuals for initial population of
        length equal to population size.

        Returns:
            list: initial population of unique individuals
        """
        for _ in range(self.population_size*10):
            set_of_pop = set()
            if int(np.sqrt(self.goal)) > self.length:
                population = [rd.sample(range(int(np.sqrt(self.goal)) + 1),
                                        self.length)
                              for _ in range(self.population_size)]
            else:
                population = [rd.sample(range(self.length), self.length)
                              for _ in range(self.population_size)]
            for i in population:
                set_of_pop.add(tuple(i))
            if len(set_of_pop) == self.population_size:
                break
        return population

    def get_fitness(self, individual):
        """Calculates the fitness of an individual as distance from the goal.

        Args:
            individual (list): individual with n numbers

        Returns:
            float: the fitness of individual
        """
        fitness = abs(np.dot(individual, individual) - self.goal)
        if fitness == 1:
            fitness += 0.1
        return 1 if fitness == 0 else 1/fitness

    def select(self, population, fitness):
        """Randomly selects few individuals from population with higher
        priority given to individuals with higher fitness function.

        Args:
            population (list): the current generation of individuals
            fitness (list): the fitness of all individuals in population

        Returns:
            list: few selected unique fit individuals to become parents
        """
        probability = []
        fitness_sum = sum(fitness)
        for x in range(len(fitness)):
            probability.append(fitness[x] / fitness_sum)
        unique = False
        while True:
            parents_index = choice(self.population_size,
                                   self.number_of_parents,
                                   p=probability, replace=False)
            parents = []
            for x in range(self.population_size):
                if x in parents_index:
                    parents.append(population[x])
            for x in parents:
                if parents.count(x) > 1:
                    continue
                else:
                    unique = True
                    break
            if unique:
                break
        return parents

    def crossover(self, parents):
        """function for crossover between two distinct parents to create
        offsprings

        Args:
            parents (list): list of all individuals fit to become parents

        Returns:
            list: a list of children created from reproduction
        """
        children = []
        for _ in range(self.population_size - self.number_of_parents):
            parent1 = rd.choice(parents)
            while True:
                parent2 = rd.choice(parents)
                if parent1 != parent2:
                    break
            children.append(parent1[:self.slice_at] + parent2[self.slice_at:])
        return children

    def mutate(self, children):
        """function to change value of a single allele in each child

        Args:
            children (list): the children to be mutatated

        Returns:
            list: the mutated children
        """
        for child in children:
            child[rd.randint(0, self.length - 1)] = \
                rd.randint(0, int(math.sqrt(self.goal)))
        return children


def genetic_algorithm(n, x, number_of_parents, population_size):
    """function to make use of Evolution class to implement genetic algorithm.

    Args:
        n (int): the length of individual list
        x (int): the goal number to be achieved
        number_of_parents (int): the number of individuals to be selected
            for crossover
        population_size (int): the number of individuals in each generation

    Returns:
        list: the solution to the problem. the individual equal to goal
    """

    evolve = Evolution(n, x, number_of_parents, population_size)
    population = evolve.get_random_population()

    counter = 1
    while True:

        win = False
        print("\nGeneration:", counter, ":", population)
        fitness = []
        for individual in population:
            individual_fitness = evolve.get_fitness(individual)
            if individual_fitness == 1:
                win = True
                break
            fitness.append(individual_fitness)
        # print("Fitness of individuals:", fitness)
        if win:
            break

        parents = evolve.select(population, fitness)
        print("Chosen ones:", parents)

        mutated_children = evolve.mutate(evolve.crossover(parents))
        print("Children", mutated_children)
        parents.extend(mutated_children)
        population = parents

        counter += 1

    return individual


def main():
    print("Genetic Algorithm")
    print("List of N numbers that equal X when squared and summed together\n")
    while True:
        try:
            n = int(input("Enter N: "))
            if n < 2:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer greater than 1 for N!")
    while True:
        try:
            x = int(input("Enter X: "))
            if x < 1:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer for X!")
    while True:
        try:
            population_size = int(input("Enter population size: "))
            if population_size < 1:
                raise ValueError
            break
        except ValueError:
            print("There cannot be those many individuals!")
            print("Please enter a positive integer!")
    number_of_parents = int(0.4*population_size)
    print("\n**Winning list**:",
          genetic_algorithm(n, x, number_of_parents, population_size))


if __name__ == "__main__":
    main()

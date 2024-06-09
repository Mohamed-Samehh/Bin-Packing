import sys
import random
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar, Checkbutton
from time import time

# Increase recursion limit
sys.setrecursionlimit(1500)

# checks if the item is applicable in the bin, if the item is greater than the bin capacity it igners item
def can_place_item(bins, item, max_capacity):
    for i in range(len(bins)):
        if bins[i] + item <= max_capacity:
            bins[i] += item
            return True, i
    return False, None

# place items in the bin if the item can not be placed it tries to put the item in any existed bin
# when the bin is not successful it backtracks
def backtrack(bins, items, max_capacity, index=0):
    if index == len(items):
        return True
    item = items[index]
    placed, bin_index = can_place_item(bins, item, max_capacity)
    if placed:
        if backtrack(bins, items, max_capacity, index + 1):
            return True
        bins[bin_index] -= item
    bins.append(item)
    if backtrack(bins, items, max_capacity, index + 1):
        return True
    bins.pop()
    return False

# sort items from largest to lowest to place larges items first
def bin_packing_backtracking(items, max_capacity):
    items.sort(reverse=True)
    bins = []
    if backtrack(bins, items, max_capacity):
        return bins
    return None 

#solution quality based on the number of bins used
def fitness(bins, max_capacity):
    return len(bins)

# The function generates an initial population
# each representing a potential starting point for the genetic algorithm's evolution process
def initialize_population(items, population_size, max_capacity):
    population = []
    for _ in range(population_size):
        random.shuffle(items)
        bins = []
        for item in items:
            placed = False
            for bin in bins:
                if sum(bin) + item <= max_capacity:
                    bin.append(item)
                    placed = True
                    break
            if not placed:
                bins.append([item])
        population.append(bins)
    return population

# mix two parents to generate a new child solution
def crossover(parent1, parent2, max_capacity):
    child = []
    cut = random.randint(1, min(len(parent1), len(parent2)) - 1)
    for bin in parent1[:cut]:
        child.append(bin.copy())
    for bin in parent2[cut:]:
        new_bin = []
        for item in bin:
            placed = False
            for child_bin in child:
                if sum(child_bin) + item <= max_capacity:
                    child_bin.append(item)
                    placed = True
                    break
            if not placed:
                new_bin.append(item)
        if new_bin:
            child.append(new_bin)
    return child

# Two bins are chosen at random from the solution, and one item is selected from each bin to be swapped.
def mutate(solution, mutation_rate, max_capacity):
    for _ in range(int(len(solution) * mutation_rate)):
        if random.random() < mutation_rate:
            bin1, bin2 = random.sample(solution, 2)
            if bin1 and bin2:
                item1, item2 = random.choice(bin1), random.choice(bin2)
                if sum(bin1) - item1 + item2 <= max_capacity and sum(bin2) - item2 + item1 <= max_capacity:
                    bin1.append(item2)
                    bin1.remove(item1)
                    bin2.append(item1)
                    bin2.remove(item2)

# Initialize the population with a set of random solutions and do cross over on the parents to get new child solution
# Two bins are chosen at random from the solution, and one item is selected from each bin to be swapped.
# and get the best solution
def genetic_algorithm(items, max_capacity, population_size, generations, mutation_rate):
    population = initialize_population(items, population_size, max_capacity)
    for _ in range(generations):
        population = sorted(population, key=lambda x: fitness(x, max_capacity))
        new_population = population[:2]  # Keep the best 2 solutions
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:10], 2)  # Tournament selection
            child = crossover(parent1, parent2, max_capacity)
            mutate(child, mutation_rate, max_capacity)
            new_population.append(child)
        population = new_population
    return population[0]

# chooses the algorithm to be used
def run_algorithm(items, max_capacity, algorithm_choice, population_size, generations, mutation_rate):
    if algorithm_choice == '1':
        return bin_packing_backtracking(items, max_capacity)
    elif algorithm_choice == '2':
        return genetic_algorithm(items, max_capacity, int(population_size), int(generations), float(mutation_rate))
    else:
        return None


def create_gui():
    root = Tk()
    root.title("Bin Packing Problem Solver")

    # Entry for items and capacities
    Label(root, text="Enter the items' sizes separated by space:").grid(row=0, column=0)
    items_var = StringVar()
    Entry(root, textvariable=items_var).grid(row=0, column=1)

    Label(root, text="Enter the maximum capacity of the bins:").grid(row=1, column=0)
    max_capacity_var = StringVar()
    Entry(root, textvariable=max_capacity_var).grid(row=1, column=1)

    # Algorithm choice
    Label(root, text="Choose algorithm (1 for Backtracking, 2 for Genetic):").grid(row=2, column=0)
    algorithm_choice_var = StringVar()
    Entry(root, textvariable=algorithm_choice_var).grid(row=2, column=1)

    # Genetic algorithm specific parameters
    Label(root, text="Enter population size (default 50):").grid(row=3, column=0)
    population_size_var = StringVar()
    Entry(root, textvariable=population_size_var).grid(row=3, column=1)

    Label(root, text="Enter number of generations (default 100):").grid(row=4, column=0)
    generations_var = StringVar()
    Entry(root, textvariable=generations_var).grid(row=4, column=1)

    Label(root, text="Enter mutation rate (default 0.01):").grid(row=5, column=0)
    mutation_rate_var = StringVar()
    Entry(root, textvariable=mutation_rate_var).grid(row=5, column=1)

    # Visualization parameters
    Label(root, text="Enter a title for the visualization:").grid(row=6, column=0)
    title_var = StringVar()
    Entry(root, textvariable=title_var).grid(row=6, column=1)

    grid_var = IntVar()
    Checkbutton(root, text="Display grid", variable=grid_var).grid(row=7, columnspan=2)
    # the submit button code
    # it takes all the values from the gui and passes each value to the functions
    def on_submit():
        start_time = time()  # Start timing the execution
        items = list(map(int, items_var.get().split()))
        max_capacity = int(max_capacity_var.get())
        algorithm_choice = algorithm_choice_var.get()
        population_size = population_size_var.get() if population_size_var.get() else '50'
        generations = generations_var.get() if generations_var.get() else '100'
        mutation_rate = mutation_rate_var.get() if mutation_rate_var.get() else '0.01'

        # Filter out items that exceed the maximum bin capacity
        filtered_items = [item for item in items if item <= max_capacity]

        if not filtered_items:
            print("All items are larger than the bin capacity.")
            return

        result = run_algorithm(filtered_items, max_capacity, algorithm_choice, population_size, generations,
                               mutation_rate)
        end_time = time()
        computation_time = end_time - start_time  # Calculate computation time

        if result is not None:
            solution_quality = fitness(result, max_capacity)  # Calculate solution quality

            if all(isinstance(bin, list) for bin in result):
                bin_sizes = [sum(bin) for bin in result]
            else:
                bin_sizes = result

            # Create a new figure for each visualization
            fig, ax = plt.subplots()
            ax.bar(range(len(bin_sizes)), bin_sizes)
            ax.set_xlabel('Bin number')
            ax.set_ylabel('Total size of items in bin')
            ax.set_title(title_var.get())
            if grid_var.get() == 1:
                ax.grid(True)

            # display the solution quality and computation time on the gui
            plt.figtext(0.8, 0.95, f"Solution Quality: {solution_quality}", ha="center", fontsize=10, color="red",
                        transform=ax.transAxes)
            plt.figtext(0.8, 0.90, f"Computation Time: {computation_time:.2f} seconds", ha="center", fontsize=10,
                        color="red", transform=ax.transAxes)

            plt.show()
        else:
            print("Invalid algorithm choice.")

    Button(root, text="Submit", command=on_submit).grid(row=8, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
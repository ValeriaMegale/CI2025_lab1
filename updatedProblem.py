import numpy as np

rng = np.random.default_rng(seed=42)
NUM_KNAPSACKS = 5
NUM_ITEMS = 20
NUM_DIMENSIONS = 2
MAXITER = 5000


VALUES = rng.integers(0, 100, size=NUM_ITEMS)
WEIGHTS = rng.integers(0, 100, size=(NUM_ITEMS, NUM_DIMENSIONS))
CONSTRAINTS = rng.integers(
    0, 100 * NUM_ITEMS // NUM_KNAPSACKS, size=(NUM_KNAPSACKS, NUM_DIMENSIONS)
)


def validate(solution):

    if not np.all(solution.sum(axis=0) <= 1):
        return False

    for nap in range(NUM_KNAPSACKS):
        items_in_nap = solution[nap]
        if np.any(items_in_nap):  # Ottimizzazione: calcola solo se ci sono oggetti
            current_weights = WEIGHTS[items_in_nap].sum(axis=0)
            if np.any(current_weights > CONSTRAINTS[nap]):
                return False
    return True


def cost(solution):
    items_placed = np.any(solution, axis=0)
    return VALUES[items_placed].sum()


def tweak(solution, p=0.4):
    new_solution = solution.copy()
    if np.random.random() < p:
        k1, k2 = np.random.choice(NUM_KNAPSACKS, size=2, replace=False)
        i1 = np.random.randint(0, NUM_ITEMS)
        i2 = np.random.randint(0, NUM_ITEMS)
        new_solution[k1, i1], new_solution[k2, i2] = new_solution[k2, i2], new_solution[k1, i1]
    else:

        k = np.random.randint(0, NUM_KNAPSACKS)
        i = np.random.randint(0, NUM_ITEMS)
        new_solution[k, i] = not new_solution[k, i]

    return new_solution


def hill_climber(initial_solution=None, max_iter=MAXITER):

    if initial_solution is None:
        current_solution = np.zeros((NUM_KNAPSACKS, NUM_ITEMS), dtype=bool)
    else:
        current_solution = initial_solution


    if not validate(current_solution):

        current_solution = np.zeros((NUM_KNAPSACKS, NUM_ITEMS), dtype=bool)

    current_cost = cost(current_solution)
    best_solution = current_solution.copy()
    best_cost = current_cost


    p_accept = 0.2

    print(f"Start Hill Climbing. Initial Cost: {current_cost}")

    for i in range(max_iter):
        # 1. Genera vicino
        neighbor = tweak(current_solution)


        if validate(neighbor):
            neighbor_cost = cost(neighbor)


            if neighbor_cost >= current_cost:
                current_solution = neighbor
                current_cost = neighbor_cost


                if current_cost > best_cost:
                    best_cost = current_cost
                    best_solution = neighbor.copy()
                    print(f"Iter {i}: New Best Cost = {best_cost}")

            elif np.random.random() < p_accept:
                current_solution = neighbor
                current_cost = neighbor_cost
                p_accept *= 0.99  # Decay


    return best_solution, best_cost


final_sol, final_val = hill_climber()
print("-" * 30)
print(f"Final Best Cost: {final_val}")
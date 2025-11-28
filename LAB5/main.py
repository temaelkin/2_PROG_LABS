import timeit
import matplotlib.pyplot as plt

# Memoization decorator
def memoize(func):
    cache = {}
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]   
    return wrapper

# Non-memoized factorial functions
def fact_recursive(n):
    if n == 0 or n == 1:
        return 1
    return n * fact_recursive(n - 1)

def fact_iterative(n):
    res = 1
    while n >= 1:
        res *= n
        n = n - 1
    return res

# Memoized factorial functions
@memoize
def fact_recursive_memo(n):
    if n == 0 or n == 1:
        return 1
    return n * fact_recursive_memo(n - 1)

@memoize
def fact_iterative_memo(n):
    res = 1
    while n >= 1:
        res *= n
        n = n - 1
    return res

# Benchmark function 
# Runs several repeats and takes the minimum time
def benchmark(func, data, number=1, repeat=5):
    total = 0
    for n in data:
        times = timeit.repeat(lambda: func(n), number=number, repeat=repeat)
        total += min(times)
    return total / len(data)

def main():
    test_data = list(range(10, 300, 10))

    # Clean one-run benchmark before any plotting or repeated benchmarking
    print("Clean benchmark of a single call:")

    n = 100

    # Clear memo caches explicitly
    fact_recursive_memo.__closure__[0].cell_contents.clear()
    fact_iterative_memo.__closure__[0].cell_contents.clear()

    t1 = timeit.timeit(lambda: fact_recursive(n), number=1)
    t2 = timeit.timeit(lambda: fact_iterative(n), number=1)
    t3 = timeit.timeit(lambda: fact_recursive_memo(n), number=1)
    t4 = timeit.timeit(lambda: fact_iterative_memo(n), number=1)

    print("Recursive:", t1)
    print("Iterative:", t2)
    print("Recursive (memoized):", t3)
    print("Iterative (memoized):", t4)

    # Benchmark for plotting
    res_recursive = []
    res_iterative = []
    res_recursive_memo = []
    res_iterative_memo = []

    # Clear caches again before the multi-run benchmark
    fact_recursive_memo.__closure__[0].cell_contents.clear()
    fact_iterative_memo.__closure__[0].cell_contents.clear()

    for n in test_data:
        res_recursive.append(benchmark(fact_recursive, [n]))
        res_iterative.append(benchmark(fact_iterative, [n]))
        res_recursive_memo.append(benchmark(fact_recursive_memo, [n]))
        res_iterative_memo.append(benchmark(fact_iterative_memo, [n]))

    # Plotting results
    plt.plot(test_data, res_recursive, label="Recursive")
    plt.plot(test_data, res_iterative, label="Iterative")
    plt.plot(test_data, res_recursive_memo, label="Recursive (memoized)")
    plt.plot(test_data, res_iterative_memo, label="Iterative (memoized)")

    plt.xlabel("n")
    plt.ylabel("Time (seconds)")
    plt.title("Comparison of Factorial Calculation Methods")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
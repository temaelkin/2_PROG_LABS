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
    n = 100

    # Clean one-run benchmark before any plotting or repeated benchmarking
    # Clear memo caches explicitly
    fact_recursive_memo.__closure__[0].cell_contents.clear()
    fact_iterative_memo.__closure__[0].cell_contents.clear()

    t1 = timeit.timeit(lambda: fact_recursive(n), number=1)
    t2 = timeit.timeit(lambda: fact_iterative(n), number=1)
    t3 = timeit.timeit(lambda: fact_recursive_memo(n), number=1)
    t4 = timeit.timeit(lambda: fact_iterative_memo(n), number=1)

    # Print results of clean benchmark in Microseconds
    print("\n=== Clean benchmark: single call ===")
    print(f"{'Function':25} | Time (µs)")
    print("-" * 45)
    print(f"{'Recursive':25} | {t1 * 1_000_000:.2f}")
    print(f"{'Iterative':25} | {t2 * 1_000_000:.2f}")
    print(f"{'Recursive (memo)':25} | {t3 * 1_000_000:.2f}")
    print(f"{'Iterative (memo)':25} | {t4 * 1_000_000:.2f}")

    # Clear caches again before the multi-run benchmark
    fact_recursive_memo.__closure__[0].cell_contents.clear()
    fact_iterative_memo.__closure__[0].cell_contents.clear()

    # Benchmark for plotting
    res_recursive = []
    res_iterative = []
    res_recursive_memo = []
    res_iterative_memo = []   

    test_data = list(range(10, 300, 10))

    for n in test_data:
        res_recursive.append(benchmark(fact_recursive, [n]) * 1_000_000)
        res_iterative.append(benchmark(fact_iterative, [n]) * 1_000_000)
        res_recursive_memo.append(benchmark(fact_recursive_memo, [n]) * 1_000_000)
        res_iterative_memo.append(benchmark(fact_iterative_memo, [n]) * 1_000_000)

    # Plotting results
    plt.plot(test_data, res_recursive, label="Recursive")
    plt.plot(test_data, res_iterative, label="Iterative")
    plt.plot(test_data, res_recursive_memo, label="Recursive (memoized)")
    plt.plot(test_data, res_iterative_memo, label="Iterative (memoized)")

    plt.xlabel("n")
    plt.ylabel("Time (µs)")
    plt.title("Comparison of Factorial Calculation Methods")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
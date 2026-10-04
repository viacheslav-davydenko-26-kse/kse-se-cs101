import time

# Допоміжня функція щоб вимірювати і отримувати час виконання
# іншої функції після декількох її виконань 
def measure_time(func, run_count=100_000_000):
    start_time = time.perf_counter()
    for i in range(run_count):
        func()
    return time.perf_counter() - start_time

def measure_funcs_times(funcs, run_count=100_000_000):
    times = []
    for func in funcs:
        times.append(measure_time(func, run_count))
    return times

def funcs_speed_test(funcs, test_quantity=1):
    results = []
    for i in range(test_quantity):
        times = measure_funcs_times(funcs, 100_000_00)
        print(times)
        i = 0
        as_expected = True
        while as_expected and i < len(funcs) - 1:
            if times[i] > times[i + 1]:
                as_expected = False
                break
            i += 1
        results.append(as_expected)
    return all(results)

def main():
    def sum_func(a=50, b=60):
        c = a + b

    def multiplication_func(a=50, b=60):
        c = a * b

    def division_func(a=50, b=60):
        c = a / b

    funcs = [
        sum_func,
        multiplication_func,
        division_func,
    ]
    result = funcs_speed_test(funcs) 
    print("Тест на швидкість операцій:", result)

    def create_list_of_numbers(amount):
        number_list = []
        for i in range(amount):
            number_list.append(i)

    funcs = [
        lambda: create_list_of_numbers(10),
        lambda: create_list_of_numbers(50),
        lambda: create_list_of_numbers(100),
    ]
    result = funcs_speed_test(funcs) 
    print("Тест на швидкість списків:", result)

if __name__ == "__main__":
    main()


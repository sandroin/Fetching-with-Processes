import requests
import json
import concurrent.futures
from multiprocessing import Manager


def load(i, global_list):
    product = requests.get("https://dummyjson.com/products/{}".format(i)).json()
    global_list.append(product)


def process(start, end, global_list, ops):
    with concurrent.futures.ThreadPoolExecutor(max_workers=ops) as executor:
        for i in range(start + 1, end + 1):
            executor.submit(load, i, global_list)


def generate(number_of_products, number_of_processes, num_threads, file_name):
    global_list = Manager().list()
    ops_per_process = number_of_products // 5

    with concurrent.futures.ProcessPoolExecutor(max_workers=number_of_processes) as executor:
        [executor.submit(process, i * ops_per_process, (i + 1) * ops_per_process, global_list, num_threads)
         for i in range(number_of_processes)]

    json_path = "{}.json".format(file_name)
    with open(json_path, 'w') as file:
        json.dump(list(global_list), file, indent=4)

    print("Processes are done, file is generated!")


if __name__ == '__main__':
    generate(100, 5, 20, "final")

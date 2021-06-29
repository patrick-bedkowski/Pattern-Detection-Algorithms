import matplotlib.pyplot as plt
import argparse
import json

def load_output_from_json(path):
    with open(path, 'r') as file_handle:
        data = json.load(file_handle)

        mean_values = []
        sizes = []

        for benchmark in data["benchmarks"]:
            mean = benchmark["stats"]['mean']
            mean = float("{:.4f}".format(mean))
            mean_values.append(mean)
            size = benchmark["params"]["size"]
            sizes.append(size)

        return mean_values, sizes


paths = {
    "kr": "/home/grabysz/aisdi/wyszukiwanie/aisdi_lab_4/benchmarks/0002_test_kr.json",
    "kmp": "/home/grabysz/aisdi/wyszukiwanie/aisdi_lab_4/benchmarks/0003_test_kmp.json",
    "n": "/home/grabysz/aisdi/wyszukiwanie/aisdi_lab_4/benchmarks/0004_test_n.json",
}


values_kr, size_kr = load_output_from_json(paths["kr"])
values_kmp, size_kmp = load_output_from_json(paths["kmp"])
values_n, size_n = load_output_from_json(paths["n"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("title", help="Title of the plot")
    args = parser.parse_args()

    plt.plot(size_kr, values_kr, label="Rabin–Karp algorithm")
    plt.plot(size_kmp, values_kmp, label="Knuth-Morris-Pratt algorithm")
    plt.plot(size_n, values_n, label="Naive algorithm")
    plt.legend()
    plt.ylabel('mean time in sec')
    plt.xlabel('number of words')
    plt.title(args.title)
    png_file = str(args.title) + '.png'
    plt.savefig(png_file)
    plt.show()

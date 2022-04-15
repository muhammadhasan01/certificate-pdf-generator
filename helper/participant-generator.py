import csv
import collections


def main():
    absent_file = open('../data/absent.txt')
    data = absent_file.read().split('\n')

    categories = {
        "Capture The Flag": collections.defaultdict(int),
        "Data Science": collections.defaultdict(int),
        "Competitive Programming": collections.defaultdict(int),
        "Game Development": collections.defaultdict(int),
        "UI / UX": collections.defaultdict(int),
    }

    days = {
        "Capture The Flag": 4,
        "Data Science": 4,
        "Competitive Programming": 5,
        "Game Development": 5,
        "UI / UX": 5,
    }

    nim_to_name = {}

    for line in data:
        nim, name, category = line.split('\t')
        nim_to_name[nim] = name
        categories[category][nim] += 1

    result = []
    for category in categories.keys():
        total_days = days[category]
        for nim, freq in categories[category].items():
            name = nim_to_name[nim]
            tup = (category, nim, name)
            if float(freq) / total_days >= 0.75:
                result.append(tup)

    with open('../data/participants.csv', 'w', encoding='UTF8', newline='') as participants:
        header = ['category', 'nim', 'name']
        writer = csv.writer(participants)
        writer.writerow(header)
        for res in result:
            writer.writerow(res)


if __name__ == "__main__":
    main()

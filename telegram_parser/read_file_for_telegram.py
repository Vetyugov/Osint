import csv


def read_files_for_telegram():
    handy_search_telegram = []
    with open('handy_search_telegram.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            handy_search_telegram.append(row[0])

    keywords = []
    with open('keywords_telegram.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            keywords.append(row[0])

    return handy_search_telegram, keywords

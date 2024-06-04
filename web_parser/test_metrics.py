import time
import pandas as pd

def parse_csv_metrics():
    df = pd.read_csv('metrics_mfd.csv', sep='\t')
    print(df)
    df = df.drop('Unnamed: 0', axis=1)
    print(df.describe())

# Тесты
if __name__ == '__main__':
    # parse_by_word()
    # parse_by_text()
    parse_csv_metrics()

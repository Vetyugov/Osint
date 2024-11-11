from typing import List

import pandas as pd


class WebOsintMetric:
    def __init__(self, link: str, total_time: float, get_text_from_url: float, check_is_text_contains_crypto: float,
                 save_new_found_address: float, save_new_parsed_link: float, get_not_parsed_links: float):
        self.id = id
        self.link = link
        self.total_time = total_time
        self.get_text_from_url = get_text_from_url
        self.check_is_text_contains_crypto = check_is_text_contains_crypto
        self.save_new_found_address = save_new_found_address
        self.save_new_parsed_link = save_new_parsed_link
        self.get_not_parsed_links = get_not_parsed_links


def save_metrics_to_csv(metrics):
    data = [{
        'link': metric.link,
        'total_time': metric.total_time,
        'get_text_from_url': metric.get_text_from_url,
        'check_is_text_contains_crypto': metric.check_is_text_contains_crypto,
        'save_new_found_address': metric.save_new_found_address,
        'save_new_parsed_link': metric.save_new_parsed_link,
        'get_not_parsed_links': metric.get_not_parsed_links
    }
        for metric in metrics]

    # Чтение существующего CSV-файла (если он существует)
    try:
        df_existing = pd.read_csv('metrics.csv')
    except FileNotFoundError:
        # Если файл не найден, создаём новый DataFrame
        df_existing = pd.DataFrame(columns=['link', 'total_time', 'get_text_from_url', 'check_is_text_contains_crypto',
                                            'save_new_found_address', 'save_new_parsed_link', 'get_not_parsed_links'])
    df_to_add = pd.DataFrame(data)
    # Объединение существующего DataFrame с новым
    df_combined = pd.concat([df_existing, df_to_add], ignore_index=True)

    # Сохранение обратно в CSV
    df_combined.to_csv('metrics.csv', index=False)

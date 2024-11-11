from metrics import WebOsintMetric, save_metrics_to_csv

def parse_csv_metrics():
    current_metrics_list = []
    metric = WebOsintMetric(
        link='link',
        total_time=1,
        get_text_from_url=2,
        check_is_text_contains_crypto=3,
        save_new_found_address=4,
        save_new_parsed_link=5,
        get_not_parsed_links=6
    )
    current_metrics_list.append(metric)
    save_metrics_to_csv(current_metrics_list)

# Тесты
if __name__ == '__main__':
    parse_csv_metrics()

import time

start_time = time.time()

import connect
import set_parameters
import search_in_channels

def main():
    connect
    set_parameters

if __name__ == '__main__':
    main()

end_time = time.time()  # Засекаем время окончания выполнения кода
execution_time = end_time - start_time
print(f"Время выполнения: {execution_time} секунд(-ы)")
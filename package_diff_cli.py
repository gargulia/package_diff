import argparse
import json
from package_diff import get_packages, compare_packages, BRANCHES

def main():
    """
    CLI утилита для сравнения пакетов между ветками.
    """
    parser = argparse.ArgumentParser(description="Сравнение пакетов между ветками sisyphus и p10.")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Путь к файлу для сохранения JSON результата (по умолчанию вывод в stdout).",
    )
    args = parser.parse_args()

    sisyphus_data = get_packages(BRANCHES[0])  # sisyphus
    p10_data = get_packages(BRANCHES[1])  # p10

    if not sisyphus_data or not p10_data:
        print("Не удалось получить данные о пакетах.  Проверьте подключение к сети и доступность API.")
        exit(1)

    results = compare_packages(sisyphus_data, p10_data)

    if args.output:
        try:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=4)
            print(f"Результат сохранен в файл: {args.output}")
        except IOError as e:
            print(f"Ошибка при записи в файл: {e}")
            exit(1)
    else:
        print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()

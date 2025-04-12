# package_diff.py

import requests
import json
import argparse

API_URL = "https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
BRANCHES = ["sisyphus", "p10"]

def get_packages(branch):
    """
    Получает список пакетов из указанной ветки.

    Args:
        branch (str): Название ветки (sisyphus или p10).

    Returns:
        dict: Словарь, где ключ - архитектура, значение - список пакетов.
              Возвращает None в случае ошибки.
    """
    try:
        url = API_URL.format(branch=branch)
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        packages_by_arch = {}
        for package in data.get("packages", []):
            arch = package.get("arch")
            if arch not in packages_by_arch:
                packages_by_arch[arch] = []
            packages_by_arch[arch].append(package)
        return packages_by_arch
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из API: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        return None

def version_compare(version1, version2):
    """
    Упрощенное сравнение версий пакетов.

    Args:
        version1 (str): Версия первого пакета (например, "1.0-1").
        version2 (str): Версия второго пакета (например, "1.0-2").

    Returns:
        int: 1, если version1 > version2; -1, если version1 < version2; 0, если равны.
    """
    def parse_version(version):
        # Разделяем версию на части: основную версию и релиз
        parts = version.split('-')
        main_version_parts = parts[0].split('.')
        # Преобразуем все части в строки
        main_version = tuple(str(part) for part in main_version_parts)

        # Обрабатываем release часть
        if len(parts) > 1:
            release_parts = parts[1].split('.')
            release = tuple(str(part) for part in release_parts)
        else:
            release = ('0',)
        return (main_version, release)

    v1 = parse_version(version1)
    v2 = parse_version(version2)

    if v1 > v2:
        return 1
    elif v1 < v2:
        return -1
    else:
        return 0

def compare_packages(sisyphus_data, p10_data):
    """
    Сравнивает пакеты из sisyphus и p10.

    Args:
        sisyphus_data (dict): Данные пакетов из sisyphus.
        p10_data (dict): Данные пакетов из p10.

    Returns:
        dict: Словарь с результатами сравнения.
    """
    results = {}
    all_arches = set(sisyphus_data.keys()).union(p10_data.keys())

    for arch in all_arches:
        results[arch] = {
            "p10_only": [],
            "sisyphus_only": [],
            "version_diff": []
        }

        sisyphus_packages = {p['name']: p for p in sisyphus_data.get(arch, [])}
        p10_packages = {p['name']: p for p in p10_data.get(arch, [])}

        for package_name in p10_packages:
            if package_name not in sisyphus_packages:
                results[arch]["p10_only"].append(package_name)

        for package_name in sisyphus_packages:
            if package_name not in p10_packages:
                results[arch]["sisyphus_only"].append(package_name)
            else:
                sisyphus_package = sisyphus_packages[package_name]
                p10_package = p10_packages[package_name]

                # Проверяем наличие версий и релизов
                if ('version' in sisyphus_package and 'release' in sisyphus_package and
                    'version' in p10_package and 'release' in p10_package):
                    sisyphus_full_version = f"{sisyphus_package['version']}-{sisyphus_package['release']}"
                    p10_full_version = f"{p10_package['version']}-{p10_package['release']}"

                    compare = version_compare(sisyphus_full_version, p10_full_version)
                    if compare > 0:  # sisyphus version is newer
                        results[arch]["version_diff"].append({
                            "name": package_name,
                            "sisyphus_version": sisyphus_full_version,
                            "p10_version": p10_full_version
                        })
    return results

def main():
    parser = argparse.ArgumentParser(description="Сравнение пакетов между ветками ALT Linux.")
    parser.add_argument("--output", "-o", help="Файл для сохранения результата (JSON).", default=None)
    parser.add_argument("--verbose", "-v", action="store_true", help="Вывод подробной информации о сравнении.")
    args = parser.parse_args()

    # Получаем данные о пакетах для обеих веток
    sisyphus_data = get_packages("sisyphus")
    p10_data = get_packages("p10")

    if sisyphus_data is None or p10_data is None:
        print("Не удалось получить данные о пакетах. Проверьте подключение к интернету или API.")
        return

    # Сравниваем пакеты
    comparison_results = compare_packages(sisyphus_data, p10_data)

    # Выводим результат
    if args.verbose:
        print("Результаты сравнения:")
        for arch, result in comparison_results.items():
            print(f"\nАрхитектура: {arch}")
            print(f"  Только в p10: {len(result['p10_only'])} пакетов")
            print(f"  Только в sisyphus: {len(result['sisyphus_only'])} пакетов")
            print(f"  Различия в версиях: {len(result['version_diff'])} пакетов")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(comparison_results, f, indent=4, ensure_ascii=False)
        print(f"Результат сохранен в файл: {args.output}")
    else:
        print(json.dumps(comparison_results, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()

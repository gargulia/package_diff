import requests
import json
import rpm

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

        packages_byarch

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из API: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка при разборе JSON ответа: {e}")
        return None

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

                # Compare versions using rpm utils
                compare = rpm.labelCompare((sisyphus_package['version'], sisyphus_package['release']),
                                           (p10_package['version'], p10_package['release']))

                if compare > 0: # sisyphus version is newer
                    results[arch]["version_diff"].append({
                        "name": package_name,
                        "sisyphus_version": f"{sisyphus_package['version']}-{sisyphus_package['release']}",
                        "p10_version": f"{p10_package['version']}-{p10_package['release']}"
                    })
    return results

def
        results = compare_packages(sisyphus_data, p10_data)
        print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()

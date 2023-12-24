import argparse
import requests
import json
import csv
import logging
import datetime
import configparser

# Функция для чтения настроек из файла конфигурации
def read_config(config_file_path):
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config['DEFAULT']['jira_url'], config['DEFAULT']['auth_token']

# Функция для создания новой версии в JIRA
def create_fix_version(project_key, auth_token, version_name, jira_url):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"{jira_url}/rest/api/2/version"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.36.0"
    }
    version_description = f"Релиз {version_name} - создан ручками команды AppTech"
    version_data = {
        "description": version_description,
        "name": version_name,
        "project": project_key,
        "startDate": current_date
    }
    response = requests.post(url, headers=headers, data=json.dumps(version_data))

    # Обработка ответа от сервера
    if response.status_code == 201:
        version_info = response.json()
        logging.info(f"FixVersion успешно создана для проекта {project_key}")
        return project_key, version_info["name"], version_info["id"]
    else:
        logging.error(f"Ошибка при создании FixVersion для проекта {project_key}: {response.text}")

# Функция для обновления версии в JIRA
def update_fix_version(version_id, auth_token, jira_url):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"{jira_url}/rest/api/2/version/{version_id}"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.36.0"
    }
    update_data = {
        "releaseDate": current_date,
        "released": True
    }
    response = requests.put(url, headers=headers, data=json.dumps(update_data))

    # Обработка ответа от сервера
    if response.status_code == 200:
        logging.info(f"FixVersion с ID {version_id} успешно обновлена")
        return True
    else:
        logging.error(f"Ошибка при обновлении FixVersion с ID {version_id}: {response.text}")
        return False

# Основная функция программы
def main():
    jira_url, auth_token = read_config('config.ini')  # Чтение URL JIRA и токена из файла конфигурации

    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Управление версиями в Jira')
    parser.add_argument('--create', nargs=1, help='Создать FixVersion, аргумент: version_name')
    parser.add_argument('--release', nargs=1, help='Выпустить FixVersion, аргумент: version_name')
    args = parser.parse_args()

    # Обработка аргумента --create для создания новой версии
    if args.create:
        [version_name] = args.create
        results = []

        # Чтение списка ключей проектов
        with open('docs/project_keys.txt', 'r') as file:
            project_keys = file.read().split(',')

        # Создание новой версии для каждого проекта
        for key in project_keys:
            result = create_fix_version(key.strip(), auth_token, version_name, jira_url)
            if result:
                results.append(result)

        # Запись результатов в CSV-файл
        with open('docs/fix_versions_results.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(results)

    # Обработка аргумента --release для выпуска версии
    if args.release:
        [version_name_to_release] = args.release
        updated_versions = []

        # Чтение информации о версиях из CSV-файла
        with open('docs/fix_versions_results.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            versions = list(csvreader)

        # Обновление статуса версий и запись обновленной информации в CSV-файл
        with open('docs/fix_versions_results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Project', 'fixVersion', 'versionId'])

            for row in versions[1:]:
                if len(row) == 0:
                    continue

                project_key, version_name, version_id = row
                if version_name == version_name_to_release and version_id not in updated_versions:
                    if update_fix_version(version_id, auth_token, jira_url):
                        updated_versions.append(version_id)
                        continue
                csvwriter.writerow(row)

        # Логирование результатов
        if updated_versions:
            logging.info(f"Выпущены следующие версии: {', '.join(updated_versions)}")
        else:
            logging.info("Не было выпущено ни одной версии.")

if __name__ == "__main__":
    main()

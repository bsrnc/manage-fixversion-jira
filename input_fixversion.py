import requests
import json
import argparse
import configparser

#Чтение настроек jira_url и auth_token из файла config.ini.
def read_config(config_file_path):

    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config['DEFAULT']['jira_url'], config['DEFAULT']['auth_token']

#Чтение данных из файла и возврат списка элементов.
def read_file(file_path):

    with open(file_path, 'r') as file:
        return file.read().strip().split(',')

#Обновление fixVersion для списка задач JIRA.
def input_fix_version(issue_keys, fix_version, auth_token, jira_url):
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.36.0'
    }

    for issue_key in issue_keys:
        issue_key = issue_key.strip()  # Удаление лишних пробелов
        payload = {
            "update": {
                "fixVersions": [
                    {
                        "add": {"name": fix_version}
                    }
                ]
            }
        }

        url = f'{jira_url}/rest/api/2/issue/{issue_key}'
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')

        # Отправка запроса
        response = requests.put(url, headers=headers, data=data)
        if response.status_code == 204:
            print(f"Successfully updated issue {issue_key} with fixVersion {fix_version}")
        else:
            print(f"Failed to update issue {issue_key}")

def main():
    # Чтение настроек из config.ini
    jira_url, auth_token = read_config('config.ini')

    # Чтение списка задач
    issue_keys = read_file('docs/issue_keys.txt')

    # Разбор аргументов командной строки
    parser = argparse.ArgumentParser(description='Update fixVersion in JIRA issues.')
    parser.add_argument('fixversion', type=str, help='The fixVersion to set')
    args = parser.parse_args()

    # Выполнение обновления
    input_fix_version(issue_keys, args.fixversion, auth_token, jira_url)

if __name__ == "__main__":
    main()

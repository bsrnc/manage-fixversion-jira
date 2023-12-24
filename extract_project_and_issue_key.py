import sys
import os
import subprocess
import re

def main():
    # Проверка наличия необходимых аргументов
    if len(sys.argv) != 4:
        print("Usage: {} <directory> <start_release> <end_release>".format(sys.argv[0]))
        sys.exit(1)

    # Аргументы командной строки
    directory = sys.argv[1]
    start_release = sys.argv[2]
    end_release = sys.argv[3]

    # Сохранение пути к директории скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Команда для генерации файла mr_list.txt в директории скрипта
    os.chdir(directory)
    with open(os.path.join(script_dir, "docs/mr_list.txt"), "w") as mr_list_file:
        subprocess.run(["git", "log", "--oneline", "--merges", "{}..{}".format(start_release, end_release)], stdout=mr_list_file)

    # Пути к файлам
    mr_list_filepath = os.path.join(script_dir, "docs/mr_list.txt")
    project_keys_filepath = os.path.join(script_dir, "docs/project_keys.txt")
    issue_keys_filepath = os.path.join(script_dir, "docs/issue_keys.txt")  # Путь для issue keys

    # Извлечение ключей проектов и запись в файлы project_keys.txt и issue_keys.txt
    with open(mr_list_filepath, "r") as mr_list_file, \
         open(project_keys_filepath, "w") as project_keys_file, \
         open(issue_keys_filepath, "w") as issue_keys_file:

        lines = mr_list_file.readlines()
        project_keys = set()
        issue_keys = set()

        for line in lines:
            if "Merge branch" in line:
                parts = line.split('/')
                key_part = parts[-1].split('-')[0]
                match = re.search(r'[A-Z]+[A-Z0-9]*', key_part)
                if match:
                    project_keys.add(match.group())

                # Извлечение issue keys
                issue_match = re.search(r'[A-Z]+-[0-9]+', line)
                if issue_match:
                    issue_keys.add(issue_match.group())

        project_keys_file.write(', '.join(sorted(project_keys)) + '\n')
        issue_keys_file.write(', '.join(sorted(issue_keys)) + '\n')

if __name__ == "__main__":
    main()

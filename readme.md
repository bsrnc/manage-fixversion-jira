
# Управление FixVersion в JIRA с помощью python cкриптов

Этот набор скриптов на Python помогает управлять версиями исправлений (FixVersion) в задачах JIRA.

## Начало работы
Перед началом работы убедитесь, что в файле `config.ini` указаны следующие параметры:
- `jira_url`: URL вашего JIRA сервера.
- `auth_token`: Токен авторизации. Создается в профиле JIRA. Учетная запись должна иметь права на создание релизов в проектах.

## Шаг 1: Сбор информации о задачах и проектах

**Файл: `extract_project_and_issue_key.py`**
- Собирает информацию о всех merge-запросах (MR) между ветками.
- Формирует список задач (`issue_keys.txt`) и проектов (`project_keys.txt`).

**Использование:**
```shell
python3 extract_project_and_issue_key.py [путь до проекта] [старый релиз] [новый релиз]
```
*Пример:*
```shell
python3 extract_project_and_issue_key.py ../application release/1.0.0 release/1.1.0
```

**Примечание:** Убедитесь, что нужные ветки доступны локально в папке проекта.

## Шаг 2: Создание FixVersion в проектах

**Файл: `create_release_fixversion.py`**
- Создает FixVersion в проектах из списка `project_keys.txt`.
- Результаты записываются в файл `fix_versions_results.csv`.

**Использование:**
```shell
python3 create_release_fixversion.py --create '1.1.0'
```
- Параметр `--create` указывает на создание FixVersion.
- `'1.1.0'` - название создаваемой версии.

**Дополнительно:**
Для выпуска созданных FixVersion:
```shell
python3 create_release_fixversion.py --release '1.1.0'
```

## Шаг 3: Присвоение FixVersion задачам

**Файл: `input_fixversion.py`**
- Назначает указанный FixVersion задачам из файла `issue_keys.txt`.

**Использование:**
```shell
python3 input_fixversion.py '1.1.0'
```
- `'1.1.0'` - FixVersion, который нужно проставить.

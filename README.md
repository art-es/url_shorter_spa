# URL Shorter

## Установка

### Загружаем зависимости frontend приложения
```shell
npm i
# или 
yarn
```

### Запускаем docker контейнеры
```shell
docker-compose up
```

### Создаем виртуальное окружение

```shell
python3.8 -m venv <venv_name>
```

### Устанавливаем requirements

```shell
pip install -r requirements.txt
```

Переходим в директорию test_task


### Выполняем миграции

```shell
python manage.py migrate --database migration
```

### Если возникли проблемы с зависимостями, то можно зайти внутрь контейнера и выполнить миграции в нем

1. Получить id контейнера(первый столбец)
```shell
docker ps | grep url_shorter_spa_backend
```
2. Выполнить команду для захода в терминал в контейнере

```shell
docker exec -it <ID> sh
```
3. Выполнить миграции 
```shell
python manage.py migrate
```

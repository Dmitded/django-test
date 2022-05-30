# django-test-dl

## Backend local

#### Под brew install и brew services понимается утилита установки пакетов и ctl-сервис
#### В Arch Linux это pacman -S и systemctl

Установка необходимых пакетов в систему:

```bash
brew install python3
```

На Linux также может потребоваться пакет python3-pip или python-pip

Клонируем проект, создаем виртуальное окружение

```bash
cd django-test-dl
python3 -m venv env
```

Установка зависимостей python

```bash
./env/bin/pip3 install -r deploy/requirements.txt
```

Для запуска приложения:
```bash
./src/manage.py runserver
```
## Backend docker

Для запуска в Docker-контейнере:

Сборка image
```bash
docker build -t <your-tag> -f deploy/Dockerfile .
```

Запуск контейнера из корня проекта (используется volume для sqlite файла):
```bash
docker run --net=host -v /local/path/to/db/:/local-db --env-file=src/dev.env <your-tag>
```

# Настройки проекта (settings module)

Этот каталог по сути своей настройки Django проекта

На выходе вы получаете готовые настройки которые передаются в [переменную среды](#https://ru.wikipedia.org/wiki/%D0%9F%D0%B5%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F_%D1%81%D1%80%D0%B5%D0%B4%D1%8B) DJANGO_SETTINGS_MODULE которая используется в manage.py в качестве настроек проекта или в `wsgi.py` и `asgi.py` тоже в качестве настроек проекта 

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.env.{ENV_ID}')
```

## Структура

- `conf.py` 
  - Используя [decouple](https://pypi.org/project/python-decouple/) достает `ENV_ID` (который означает какую настройку мы используем `prod` или `local`). То есть в проекте предусмотрены разные варианты сборки, простой пример: зачем вам инструменты для дебагинга на проде? так уберите их 
  - Хранит настройки дополнительных инструментов и библиотек по типу `Simple-JWT`, `DRF`
  - Хранит `SECRET-KEY` проекта 

- `base.py` 
  - Общие настройки проекта (apps, middleware, templates и т.д.); которые обычно хранятся в `settings.py`
  - Есть разделение приложений на написанные в проекте и внешние
    ```python
        DJANGO_AND_THIRD_PARTY_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        ]
        PROJECT_APPS = []
        INSTALLED_APPS = DJANGO_AND_THIRD_PARTY_APPS +      PROJECT_APPS
        ```
    
  - Здесь дополнительно импортируются настройки из `conf.py` 

- `env/local.py`
  - подтягивает все настройки с base где благодаря импорту есть и все настройки `conf.py`
  - имеет настройки подходящие для локальной разработки к примеру тот же 
    ```python 
        DEBUG = True
    ```

- `env/prod.py`
  - так же подтягивает все настройки с base где благодаря импорту есть и все настройки `conf.py` но уже в свою очередь имеет настройки больше подходящие для прода

- `asgi.py || wsgi.py` 
  - почти ничем не отличаются от стандартных нового проекта Django кроме того что есть проверка на наличие ENV_ID и так же путь к настройкам указан к папке env 
    ```python
     settings.env.{ENV_ID}
    ```

## manage.py
Как видите на выходе просто готовые настройки просто передаются в manage.py ну или так же в `asgi.py` или `wsgi.py`
```python
    assert ENV_ID in ENV_POSSIBLE_OPTIONS, f"Set correct DJANGO_ADV_ENV_ID env var. Possible options: {ENV_POSSIBLE_OPTIONS}"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"settings.env.{ENV_ID}")

```

## Поток данных (откуда куда)

1. В окружении задаётся `DJANGO_ADV_ENV_ID` (`local` или `prod`).
2. `settings/conf.py` читает его через `decouple.config` и задаёт `ENV_ID` и задает настройки проекта.
3. `settings/base` импортирует `conf.py` и дописывает настройки 
4. `settings/env/<env>.py` импортирует `base.py`, который уже включает `conf.py`.
5. `manage.py`, `asgi.py`, `wsgi.py` выставляют `DJANGO_SETTINGS_MODULE`
   в `settings.env.<ENV_ID>`.
6. Django при запуске читает `DJANGO_SETTINGS_MODULE`, импортирует модуль
   настроек и формирует объект `django.conf.settings`.

## Мини-схема

```
DJANGO_ADV_ENV_ID
        ↓
settings/conf.py (ENV_ID)
        ↓
settings/base.py
        ↓
settings/env/<env>.py
        ↓
DJANGO_SETTINGS_MODULE = settings.env.<ENV_ID>
        ↓
      django.setup()
```
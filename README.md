ТЗ: <br>
Цель: 

1. Научиться устанавливать/настраивать окружение для разработки парсера.
2. Научиться использовать XPath селекторы.
3. Научиться работать с отправкой запросов и переходом по пагинации

Задача: 

1. Веб-сайт: https://www.tesco.com/groceries
2. Разработать спайдер для сбора информации о товарах.
3. Собрать данные по всем товарам в заданных категориях

Входные данные:

https://www.tesco.com/groceries/en-GB/shop/household/kitchen-roll-and-tissues/all
https://www.tesco.com/groceries/en-GB/shop/pets/cat-food-and-accessories/all

Результат:

1. - Выполнение задания предполагает разработку Scrapy Spider-а для парсинга информации о товарах на сайте Tesco.com
   - Парсер должен быть разработан с возможностью собрать информацию для любых входящих ссылок на сайте Tesco.com
   - Для каждого товара необходимо собрать информацию:
     - Product URL (string)
     - Product ID (integer)
     - Image URL (string)
     - Product Title (string)
     - Category (string)
     - Price (decimal)
     - Product Description (string)
     - Name and Address (string)
     - Return Address (string)
     - Net Contents (string)
     - Review (array of objects):
       - Review Title (string)
       - Stars Count (integer)
       - Author (string)
       - Date (string)
       - Review Text (string)
     - Usually Bought Next Products (array of objects):
       - Product URL (string)
       - Product Title (string)
2. Product Image URL (string)
3. Price (float)


Требования к реализации:

-Установить python3, pip и pipenv.<br>
-Всю дальнейшую работу проводить в окружении pipenv.<br>
-Для pipenv установить переменную окружения, определяющую путь разворачивания виртуального окружения в текущей директории в папку ".venv".<br>
-Код парсера должен соответствовать PEP8 (ссылка) и следовать рекомендациям из статьи "Scrapy по Фэншую" (ссылка)<br>
-Данные должны сохраняться в БД MySQL. Для работы с БД использовать SQLAlchemy, alembic (миграции)<br>
-Реализовать ведение файловых логов<br>
-Конфиги должны храниться в .env файле<br>
-Написать краткое README.MD с информацией как поднять и запустить парсер<br>

В результате предоставить:


1. код парсера в гите (ссылку на гит). Обязательно слить в ветку master
2. Дамп БД с данными, сохраненный на Google Drive с доступом по ссылке.

Рекомендации:

1. Наиболее быстрой и эффективной установкой окружения будет установка python с помощью Docker. 
2. Dockerfile при этом (во время прохождения квеста) не обязательно включать  в GIT, но обязательно использовать pipenv даже внутри docker'a.
<hr>
Чтобы поднять проект, выполните следующие шаги:<br>
1. Клонируйте репозиторий; <br>
2. создайте базу данных, с которой будет работать парсер; <br>
3. перейдите в директорию src и выполните:

```console
pipenv install
```

если нужно разместить .venv в одной директории с проектом:

```console
PIPENV_VENV_IN_PROJECT=1 pipenv install
cp .env.example .env
```
<br>
4. в .env укажите параметры подключения к базе данных и выполните миграции:

```console
cd ./database
pipenv run alembic upgrade head
cd ..
```
<br>
Запуск парсера осуществляется с помощью следующей команды:

```console
pipenv run scrapy crawl tesco_spider -a url=
```
параметр url указывает на ссылку, содержимое которой необходимо собрать. Например:

```console
pipenv run scrapy crawl tesco_spider -a url=https://www.tesco.com/groceries/en-GB/shop/household/kitchen-roll-and-tissues/all 
```

Парсер работает со ссылками вида https://www.tesco.com/groceries/en-GB/shop/*
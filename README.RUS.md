
# ThingsBox

Грабер 'вещей' и коллекций для локального хранения

В первую очередь, хочу сказать спасибо за идею:
1. Carlos Garcia Saura (carlosgs) https://github.com/carlosgs/export-things
2. Gary Hodgson (garyhodgson) https://github.com/garyhodgson/thing-tracker-network

Итак, как получить желаемый результат? ;)

Вот несколько простых шагов для его получения:
1. Запустите python скрипт из директории Scraper_Scripts - export_thing.py (каждый скрипт имеет хелп - просто запустите скрипт без параметров)

    Пример:
     >
     >                clone git repo
     >                cd Scraper_Scripts
     >                ./export_thing.py S 2234364

   Как только скрипт закончит работу - вы получите директорию с сохраненной в ней 'вещью'.

    Пример:
    > MakerBot-Fidget-Gear
    >
   В директории находятся поддиректории с изображениями, файлами исходников и архивы.
   В корне новой директории находится файл tracker.json
   tracker.json - это основной файл, содержит описание 'вещи'.
2. Можно собрать 'сайт' из исходников или воспользоваться содержимым директории  - Ready_to_Use. 
    Директория Ready_to_Use содержит все необходимое(включая один пример), просто скопируйте ее содержимое в директорию htdocs вашего web сервера и откройте его корневую страницу 
    : http://адрес_вашего_веб_сервера

#### Как добавить 'вещь' на страницу ThingsBox:

1.Идем в директорию ThingsBox

2.Копируем все содержимое сграбленого файла (в примерах  - MakerBot-Fidget-Gear/tracker.json) в Ready_to_Use/empty_tracker.json

3.Не забываем добавить в конец файла(empty_tracker.json) - ']}'

4.Копируем всю директорию MakerBot-Fidget-Gear в Ready_to_Use/thumbnails.

5.Переименовываем Ready_to_Use/empty_tracker.json в Ready_to_Use/tracker.json

6.Копируем директорию Ready_to_Use в корневую директорию вашего веб сервера (у apache - htdocs)

7.Открываем http://адрес_вашего_веб_сервера в браузере.

	Пример(bash)
   > cd  ThingsBox
   >
   >  cat ./Scraper_Scripts/MakerBot-Fidget-Gear/tracker.json >> ./Ready_to_Use/empty_tracker.json
   >
   >  echo "]}">>./Ready_to_Use/empty_tracker.json
   >
   >  mv ./Ready_to_Use/empty_tracker.json ./Ready_to_Use/tracker.json
   >
   >  cp -R ./Scraper_Scripts/MakerBot-Fidget-Gear/ ./Ready_to_Use/thumbnails/
   >
   >  cp -R ./* /var/www/localhost/htdocs
   >
   >  вбиваем http://адрес_вашего_веб_сервера в браузере
   
#### Как добваить несколько 'вещей' на страницу ThingsBox:

1.Делаем по схеме добавления одной 'вещи', но в место "]}" в конце файла ставим ","

2.Добавляем следующую 'вещь', не забываем про "," в конце.

3.После добавления последней 'вещи', ставим "]}" в конце файла.

4.Переносим все сграбленные директории из Scraper_Scripts в Ready_to_Use/thumbnail dir

5.Копируем все содержимое (Ready_to_Use) на ваш веб сервер в корень.

6.Открываем http://адрес_вашего_веб_сервера в браузере.

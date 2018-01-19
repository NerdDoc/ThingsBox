
# ThingsBox

Things and collection scraper for keeping it locally.

First of all, i would like to say THANKS for the idea:
1. Carlos Garcia Saura (carlosgs) https://github.com/carlosgs/export-things
2. Gary Hodgson (garyhodgson) https://github.com/garyhodgson/thing-tracker-network

So, how to get the desirable result? ;)

Here is a several simple steps:
1. Run python script from Scraper_Scripts - export_thing.py (every script has help - just run it without params)

    Example:
     >
     >                clone git repo
     >                cd Scraper_Scripts
     >                ./export_thing.py S 2234364

   At the finish you will get folder with the name of downloaded thing

    Example:
    > MakerBot-Fidget-Gear
    >
   In the directory you will see some dirs with images, source files, ziped sources and file tracker.json
   tracker.json is a main file with all information about thing
2. You will need to build your own application or you can use builded from the directory - Ready_to_Use. Directory Ready_to_Use contain all necessery to get example application with example thing, just put its content to htdocs directory of apache and open page: http://your_web_server

#### How to add a new thing to ThingsBox page:

1.Go to ThingsBox directory

2.Copy all content from grabbed file (in our example - MakerBot-Fidget-Gear/tracker.json) to Ready_to_Use/empty_tracker.json

3.Do not forget add some extra symbols at the end of file - ']}'

4.Rename Ready_to_Use/empty_tracker.json to Ready_to_Use/tracker.json

5.Copy whole directory Scraper_Scripts/MakerBot-Fidget-Gear to Ready_to_Use/thumbnails/

6.Copy whole directory Ready_to_Use into your apache htdocs dir

7.Open http://your_web_server address at your web browser.

	Example(bash)
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
   >  go to http://your_web_server web page
   
#### How to add several new things to ThingsBox page:

1.Add one thing, but  instead of "]}" add at the end of file ","

2.Add one more thing, do not forget add "," at the end.

3.When you add last thing, add "]}" and do not add ",".

4.Copy whole grabbed things dir's from Scraper_Scripts to Ready_to_Use/thumbnail dir

5.Copy whole directory (Ready_to_Use) content to your web server.

6.Open http://your_web_server address at your web browser.

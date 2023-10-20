### Purpose
- If you are a CyberPatriot coach and would like to bring up a scoreboard because you have several teams competing and would like to track their scores easily, this script will do the trick.
### Directions
- You need to put scrape.py somewhere on Ubuntu
- This script writes a file called /var/www/html/team_data.html
- Install apache2
  
``` apt install apache2 ```
- You'll need to pip install BeautifulSoup.
- Add your team numbers to the list at the top of the script. [ "16-XXXX", "16-XXXX"]
- run it with

``` python3 scrape.py ```


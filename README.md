Automatic PDF certificates creation from .xml files with Firefox
-

**Install requirements:**
```
sudo apt update
sudo apt install python3 python3-pip firefox
pip3 install 'selenium<4.0.0' webdrivermanager
sudo chmod -R 777 /usr/local/bin
webdrivermanager firefox --linkpath /usr/local/bin
```
Also make sure firefox on Linux is NOT installed with snap!!!

**Run**:  `./WebsiteMaker.py`

Remember to have actual geckodriver for firefox.

File "strona.txt", should be in upper directory with login and password to cert site on two last lines.

Pasting sticker into .pdf energetic certificates
-

**Install requirements:**
```
sudo apt update
sudo apt install g++ cmake
```

**Build project**:
```
cp PDF/libPDFNetC.so /usr/lib/x86_64-linux-gnu/
mkdir build
cmake -S . -B build/
cmake --build build -t StickerMaker
```
**Run**:  `./build/firmware/StickerMaker`

StickerMaker will only work if you **copy PDFNet library into lib directory**.
Also **Sticker.jpg needs to be in current dir**.

StickerMaker should be run in dir when PDF folder exists - **not inside PDF dir**!


Kopiujesz .py i drivera (najnowszego patrz na dole) tam gdzie są XML
Folder musi być folderem w folderze "CERTYFIKATY" (Korzysta z pliku "strona.txt" do logowania który jest folder wyżej)
Jeśli nie znajdzie pliku to się wywali tak samo jeśli będzie zły driver


Jeśli się wywala bez powodu:
Możliwe, że masz nowszą wersje chrome niż driver:

Nowa wersja 			- https://chromedriver.chromium.org/downloads
Jak sprawdzić wersje 	- https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have
# Tests

Automatic end-to-end test (50 checks): design editor, video editor, AI flows (mocked), exports, mobile layout.

```bash
pip install playwright && playwright install chromium
cd tests
# sample media banao
ffmpeg -f lavfi -i testsrc=size=640x360:rate=30 -f lavfi -i sine=frequency=440 -t 4 -c:v libvpx -c:a libopus -shortest clip.webm
ffmpeg -f lavfi -i "color=c=0x00ff00:s=480x480:r=30,drawbox=x=160:y=120:w=160:h=240:color=red:t=fill" -t 3 -c:v libvpx gs.webm
python3 -c "from PIL import Image,ImageDraw;im=Image.new('RGB',(600,600),(250,250,250));d=ImageDraw.Draw(im);d.ellipse((150,120,450,520),fill=(220,60,60));im.save('obj.png')"
python3 qa.py
```
Note: `qa.py` me Chrome ka path `/usr/bin/google-chrome` aur site folder `/home/claude/rachna-studio` hai — apne computer ke hisaab se badlo.

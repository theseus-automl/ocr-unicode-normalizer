# ocr-unicode-normalizer

This package allows you to convert strange Unicode symbols to normal ones using Tesseract.

### 1. Requirements
First, you need to install Tesseract. Instructions can be found [here](https://github.com/tesseract-ocr/tesseract)  

If you don't want to use pre-built Docker image, you'll also need a TTF file with Unicode font. I highly recommend to 
use GNU Unifont. You can download it [here](http://unifoundry.com/pub/unifont/unifont-14.0.01/font-builds/unifont-14.0.01.ttf). 

### 2. Installation
For now, only Python 3.8 is supported. You can try other versions, but no guarantees that it'll work properly.  

Clone repository:
```
git clone https://github.com/theseus-automl/ocr-unicode-normalizer
cd ocr-unicode-normalizer
```

Install package:
```
python setup.py install
```

### 3. Usage
#### 3.1 As regular Python package
```python
from pathlib import Path
from ocr_unicode_normalizer import Normalizer

norm = Normalizer(font_path=Path('/path/to/font'))
print(norm.normalize('hello', lang='eng'))
```

#### 3.2 Through API
Install additional requirements:
```
python -m pip install -r api-requirements.txt
```

Place config.yaml file near to main.py:
```
data:
    "tesseract_path": "/path/to/tesseract"
    "tessdata_path": "/path/to/tessdata"
    "font_path": "/path/to/font"
```

Start server:
```
uvicorn main:app --port 9000
```

Make request:
```python
import requests

resp = requests.get('http://localhost:9000/normalize', json={'text': 'hello', 'lang': 'eng'})

print(resp.json())
```

### 4. Pre-built Docker image
Docker image is also provided. You can view available labels at [Docker Hub](https://hub.docker.com/repository/docker/sn4kebyt3/ocr-unicode-normalizer).  

Pull image:
```
docker pull sn4kebyt3/ocr-unicode-normalizer:0.1.0
```

Run container:
```
docker container run -p 9000:80 -d --name normalizer sn4kebyt3/ocr-unicode-normalizer:0.1.0
```

Request example can be found in section 3.2.

### 5. Development
Feel free to open issues, send pull requests and ask any questions!
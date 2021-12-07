FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y software-properties-common wget python3-pip \
    && add-apt-repository ppa:alex-p/tesseract-ocr-devel \
    && apt update \
    && apt install -y tesseract-ocr tesseract-ocr-all \
    && export TESSDATA_PREFIX="/usr/share/tesseract-ocr/5/tessdata"

WORKDIR /app
RUN wget -O font.ttf http://www.unifoundry.com/pub/unifont/unifont-14.0.01/font-builds/unifont-14.0.01.ttf
COPY src/ ./src
COPY requirements.txt api-requirements.txt main.py ./
RUN printf "data:\n    font_path: /app/font.ttf\n    tessdata_path: /usr/share/tesseract-ocr/5/tessdata" > config.yaml

RUN cat requirements.txt | xargs -n 1 python3 -m pip install --no-cache-dir \
    && python3 -m pip install --no-cache-dir -r api-requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

FROM python:3.5

RUN mkdir -p /usr/src/app
RUN groupadd -r app && useradd -d /usr/src/app -r -g app app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN chown -R app:app /usr/src/app

USER app
COPY . /usr/src/app



CMD [ "python", "./main.py" ]
FROM python:3.5

RUN mkdir -p /usr/src/app
RUN groupadd -r app && useradd -d /usr/src/app -r -g app app
RUN chown -R app:app /usr/src/appsss
WORKDIR /usr/src/app
USER app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app



CMD [ "python", "./main.py" ]
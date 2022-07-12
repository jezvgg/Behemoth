FROM python:3.9

WORKDIR /usr/src/app
COPY . /usr/src/app


RUN pip3 install -r ./docker/requirements.txt

EXPOSE 7007

CMD [ "python", "run.py" ]
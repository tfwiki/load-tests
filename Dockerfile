FROM python:3.6

RUN mkdir /load-test
WORKDIR /load-test

ADD src /load-test
RUN chmod 755 run.sh

RUN set -ex && pip install pipenv --upgrade
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN set -ex && pipenv install --deploy --system

EXPOSE 5557 5558 8089

CMD "/load-test/run.sh"

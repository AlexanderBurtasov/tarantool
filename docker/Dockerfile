FROM tarantool/tarantool:2.2.0 as tarantool
COPY scripts/init.lua /opt/tarantool
CMD ["tarantool", "/opt/tarantool/init.lua"]

FROM ubuntu:bionic

MAINTAINER Alexander Burtasov "pvt.pyle1983@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-dev && \
    apt-get install -y python3-pip && \
    apt-get install -y mc

RUN mkdir /home/tarantool && \
    mkdir /home/tarantool/httpserver && \
    mkdir /home/tarantool/httpserver/logs

COPY ./httpserver/run.sh /home/tarantool/httpserver/run.sh
COPY ./httpserver/InnerRequestHandler.py /home/tarantool/httpserver/InnerRequestHandler.py
COPY ./httpserver/logutils.py /home/tarantool/httpserver/logutils.py
COPY ./httpserver/main.py /home/tarantool/httpserver/main.py
COPY ./httpserver/RequestTimer.py /home/tarantool/httpserver/RequestTimer.py
COPY ./httpserver/requirements.txt /home/tarantool/httpserver/requirements.txt
COPY ./httpserver/TarantoolStorage.py /home/tarantool/httpserver/TarantoolStorage.py

ENV PYTHONPATH /home/tarantool/httpserver
WORKDIR /home/tarantool/httpserver

RUN chmod ugo+x /home/tarantool/httpserver/run.sh && \
    chmod ugo-x /home/tarantool/httpserver/InnerRequestHandler.py && \
    chmod ugo-x /home/tarantool/httpserver/logutils.py && \
    chmod ugo-x /home/tarantool/httpserver/main.py && \
    chmod ugo-x /home/tarantool/httpserver/RequestTimer.py && \
    chmod ugo-x /home/tarantool/httpserver/requirements.txt && \
    chmod ugo-x /home/tarantool/httpserver/TarantoolStorage.py && \
    pip3 install -r /home/tarantool/httpserver/requirements.txt

EXPOSE 5052
ENTRYPOINT ["/bin/bash", "run.sh"]

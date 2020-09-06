FROM python:3.8-buster as builder

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

FROM python:3.8-slim-buster as runner

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

COPY src /app/src
COPY setup.py /app/

RUN ls -la

RUN pip3 install . && rm -rf /app

ENTRYPOINT [ "/usr/local/bin/cue-convert" ]

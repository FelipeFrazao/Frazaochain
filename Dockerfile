FROM python:3.6.2rc2
LABEL maintainer "felipe.sfrazao@outlook.com"
ENV PYTHONUNBUFFERED 1
EXPOSE 5005

RUN mkdir /frazaochain
WORKDIR /frazaochain

ADD . /frazaochain

ENTRYPOINT ["python"]

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements_dev.txt

CMD ["app.py"]
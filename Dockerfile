FROM python:3.10.0-alpine
# set work directory
RUN mkdir /src
WORKDIR /src
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# install dependencies
RUN pip install --upgrade pip
COPY ./src/requirements.txt /src/requirements.txt
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pip install -r requirements.txt
# copy project
COPY ./src /src/
EXPOSE 5000
ENTRYPOINT ["sh", "/src/entrypoint.sh"]
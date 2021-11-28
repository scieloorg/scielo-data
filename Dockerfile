FROM python:3.9.6-alpine3.14 AS build
COPY . /src
RUN pip install --upgrade pip \
    && pip install wheel
RUN cd /src \
    && python setup.py bdist_wheel -d /deps

FROM python:3.9.6-alpine3.14
MAINTAINER scielo-dev@googlegroups.com

COPY --from=build /deps/* /deps/
COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc g++ \
    && apk add libxml2-dev libxslt-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-index --find-links=file:///deps -U scielo-nw \
    && apk --purge del .build-deps \
    && rm -rf /deps

WORKDIR /app

CMD ["getter", "--help"]

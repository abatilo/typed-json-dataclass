FROM python:3.8.4
WORKDIR /src

COPY pyproject.toml poetry.lock /src/
RUN pip install poetry==0.12.17 \
      && poetry install

COPY . /src/
RUN poetry build \
      && pip install .

COPY entrypoint.sh /src/entrypoint.sh
ENTRYPOINT ["/src/entrypoint.sh"]

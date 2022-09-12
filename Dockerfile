ARG VERSION=3.10-alpine


FROM python:$VERSION AS builder

WORKDIR /app

COPY erkeronfhir erkeronfhir
COPY README.md .
COPY pyproject.toml .

RUN pip install --upgrade build
RUN python -m build


FROM python:$VERSION

WORKDIR /app

COPY requirements.txt .
RUN apk add --virtual build-dependencies build-base \
    && apk add git \
    && pip install -r requirements.txt \
    && apk del build-dependencies

COPY --from=builder /app/dist/*.whl .
RUN pip install $(find . -name "*.whl")

RUN mkdir erkeronfhir
COPY erkeronfhir/capability.py erkeronfhir/

ENTRYPOINT ["uvicorn", "erkeronfhir.api:app"]
CMD ["--host", "0.0.0.0"]
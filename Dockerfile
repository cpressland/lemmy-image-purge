FROM docker.io/python:3.11 as build

WORKDIR /build
ADD . .
RUN pip install poetry
RUN poetry build

FROM docker.io/python:3.11-slim
COPY --from=build /build/dist/*.whl /tmp/
RUN pip install /tmp/*.whl
ENTRYPOINT ["lemmy-image-purge"]

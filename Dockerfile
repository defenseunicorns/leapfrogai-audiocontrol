# Build container
FROM python:3.10-slim as builder

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
  POETRY_VERSION=1.5.1

RUN apt-get update && apt-get install -y \
  build-essential \
  software-properties-common \
  && rm -rf /var/lib/apt/lists/* \
  && pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

COPY src/* /opt/venv/
COPY data/* /opt/venv/data/

# Execution container
# FROM python:3.10-slim 

# COPY --from=builder /opt/venv /opt/venv
RUN python3 /opt/venv/load.py
RUN python3 -m spacy download en

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["streamlit" ,"run", "/opt/venv/audiocontrol.py", "--server.port=8501", "--server.address=0.0.0.0"]

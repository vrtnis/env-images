FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/vrtnis/env-images" \
    org.opencontainers.image.title="ale" \
    org.opencontainers.image.description="Canonical Arcade Learning Environment Gymnasium image"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SDL_VIDEODRIVER=dummy

RUN pip install --no-cache-dir "gymnasium[atari]==1.3.0" ale-py==0.12.0

WORKDIR /app

CMD ["python"]

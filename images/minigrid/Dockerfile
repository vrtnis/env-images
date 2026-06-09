FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/vrtnis/env-images" \
    org.opencontainers.image.title="minigrid" \
    org.opencontainers.image.description="Canonical MiniGrid Gymnasium environment image"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SDL_VIDEODRIVER=dummy

RUN pip install --no-cache-dir minigrid==3.1.0

WORKDIR /app

CMD ["python"]

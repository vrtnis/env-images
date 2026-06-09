FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/vrtnis/env-images" \
    org.opencontainers.image.title="browsergym-miniwob" \
    org.opencontainers.image.description="Canonical BrowserGym MiniWoB environment image"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MINIWOB_ROOT=/opt/miniwob-plusplus \
    MINIWOB_URL=file:///opt/miniwob-plusplus/miniwob/html/miniwob/

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir browsergym-miniwob==0.13.3 \
    && playwright install --with-deps chromium

RUN git clone https://github.com/Farama-Foundation/miniwob-plusplus.git "${MINIWOB_ROOT}" \
    && git -C "${MINIWOB_ROOT}" reset --hard 7fd85d71a4b60325c6585396ec4f48377d049838 \
    && rm -rf "${MINIWOB_ROOT}/.git"

WORKDIR /app

CMD ["python"]

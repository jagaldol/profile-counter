FROM python:3.10-slim-bullseye

WORKDIR /app

# 의존성 설치
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && \
    poetry install --no-root --no-interaction

# 앱 복사
COPY profile_counter /app/profile_counter

EXPOSE 8000

# python 으로 앱 실행 (app.py 안에 uvicorn.run 포함되어 있음)
CMD ["poetry", "run", "python", "profile_counter/app.py"]
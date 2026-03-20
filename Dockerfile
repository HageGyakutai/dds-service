FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

RUN apt-get update && apt-get install -y netcat-openbsd gettext

COPY pyproject.toml uv.lock ./

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

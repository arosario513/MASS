FROM python:3.13
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./
RUN pip install --upgrade pip && pip install uv
RUN uv venv && uv pip install .
COPY . .
EXPOSE 5000
CMD ["uv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]


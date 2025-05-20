FROM python:3.13-slim
WORKDIR /app
COPY . .
ENV UV_LINK_MODE=copy
RUN pip install --upgrade pip && pip install uv
RUN uv sync
RUN chmod +x start.sh
EXPOSE 5000
ENTRYPOINT [ "./start.sh" ]

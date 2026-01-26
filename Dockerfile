# 使用官方 uv 镜像作为构建阶段
FROM astral-sh/uv:python3.12-alpine AS builder
ADD . /app
WORKDIR /app
RUN uv sync --frozen --no-dev

# 运行阶段
FROM python:3.12-alpine
COPY --from=builder /app /app
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
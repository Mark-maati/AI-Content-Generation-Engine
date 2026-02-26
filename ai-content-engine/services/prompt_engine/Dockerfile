FROM python:3.12-slim

WORKDIR /app

COPY shared/ /app/shared/
RUN pip install --no-cache-dir /app/shared/

COPY services/prompt_engine/ /app/services/prompt_engine/
RUN pip install --no-cache-dir /app/services/prompt_engine/

EXPOSE 8002

CMD ["python", "-m", "prompt_engine.main"]

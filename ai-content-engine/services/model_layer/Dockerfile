FROM python:3.12-slim

WORKDIR /app

COPY shared/ /app/shared/
RUN pip install --no-cache-dir /app/shared/

COPY services/model_layer/ /app/services/model_layer/
RUN pip install --no-cache-dir /app/services/model_layer/

EXPOSE 8003

CMD ["python", "-m", "model_layer.main"]

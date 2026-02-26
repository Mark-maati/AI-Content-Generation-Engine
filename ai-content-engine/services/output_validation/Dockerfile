FROM python:3.12-slim

WORKDIR /app

COPY shared/ /app/shared/
RUN pip install --no-cache-dir /app/shared/

COPY services/output_validation/ /app/services/output_validation/
RUN pip install --no-cache-dir /app/services/output_validation/

EXPOSE 8004

CMD ["python", "-m", "output_validation.main"]

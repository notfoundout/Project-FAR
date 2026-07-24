FROM python:3.11-slim
WORKDIR /app
COPY commercial/far-decision-integrity /app/commercial/far-decision-integrity
COPY commercial/far-demo /app/commercial/far-demo
RUN pip install --no-cache-dir -e commercial/far-decision-integrity && pip install --no-cache-dir -e commercial/far-demo
EXPOSE 8000
CMD ["uvicorn", "far_demo.app:app", "--host", "0.0.0.0", "--port", "8000"]

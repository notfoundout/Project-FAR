FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN python -m pip install --no-cache-dir .
RUN mkdir -p /var/lib/far/blobs /var/lib/far/staging

EXPOSE 8080
VOLUME ["/var/lib/far"]
ENTRYPOINT ["far-secured-service"]
CMD ["--host", "0.0.0.0", "--port", "8080", "--security-db", "/var/lib/far/security.db", "--evidence-db", "/var/lib/far/evidence.db", "--blob-root", "/var/lib/far/blobs", "--staging-root", "/var/lib/far/staging"]

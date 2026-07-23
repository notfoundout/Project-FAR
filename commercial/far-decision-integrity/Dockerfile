FROM python:3.11-slim

RUN groupadd --system far && useradd --system --gid far --home-dir /var/lib/far far
WORKDIR /app
COPY . /app
RUN python -m pip install --no-cache-dir . \
    && mkdir -p /var/lib/far/blobs /var/lib/far/staging /tmp/far \
    && chown -R far:far /var/lib/far /tmp/far

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TMPDIR=/tmp/far
USER far
EXPOSE 8080
VOLUME ["/var/lib/far"]
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD far-operations --security-db /var/lib/far/security.db readiness --evidence-db /var/lib/far/evidence.db --blob-root /var/lib/far/blobs --staging-root /var/lib/far/staging || exit 1
ENTRYPOINT ["far-secured-service"]
CMD ["--host", "0.0.0.0", "--port", "8080", "--security-db", "/var/lib/far/security.db", "--evidence-db", "/var/lib/far/evidence.db", "--blob-root", "/var/lib/far/blobs", "--staging-root", "/var/lib/far/staging"]

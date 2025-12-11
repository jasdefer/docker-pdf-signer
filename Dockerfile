FROM python:3.12-slim

# System dependencies for svglib / pycairo
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libxml2 \
        libxslt1.1 \
        libcairo2 \
        libcairo2-dev \
        gcc \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

# Python libraries
RUN pip install --no-cache-dir \
    pdfrw \
    reportlab \
    svglib

WORKDIR /app
COPY sign_pdf.py /app/sign_pdf.py

WORKDIR /work
ENTRYPOINT ["python", "/app/sign_pdf.py"]
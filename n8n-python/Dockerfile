FROM n8nio/n8n:latest-debian

USER root

RUN sed -i 's|http://deb.debian.org|http://archive.debian.org|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org|http://archive.debian.org|g' /etc/apt/sources.list && \
    sed -i '/stretch-updates/d' /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-opencv \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip

RUN pip3 install --no-cache-dir \
    numpy \
    pillow \
    pytesseract \
    insightface \
    onnxruntime

# -----------------------------
# Expose n8n port
# -----------------------------
EXPOSE 5678

# -----------------------------
# Start n8n
# -----------------------------
CMD ["n8n"]
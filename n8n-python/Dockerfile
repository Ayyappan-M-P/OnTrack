FROM n8nio/n8n:latest-debian

# Stay as root (Render requires this)
USER root

# -----------------------------
# System dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Python dependencies
# -----------------------------
RUN pip3 install --no-cache-dir \
    numpy \
    pillow \
    pytesseract \
    opencv-python-headless \
    insightface \
    onnxruntime==1.16.3 \
    requests

# -----------------------------
# Expose n8n port
# -----------------------------
EXPOSE 5678

# -----------------------------
# Start n8n
# -----------------------------
CMD ["n8n"]

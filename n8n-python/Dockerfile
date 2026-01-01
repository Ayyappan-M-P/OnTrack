FROM n8nio/n8n:latest-debian

USER root

# -----------------------------
# System dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-opencv \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Python packages
# -----------------------------
RUN pip3 install --no-cache-dir \
    numpy \
    pillow \
    pytesseract \
    insightface \
    onnxruntime==1.16.3

# -----------------------------
# n8n user
# -----------------------------
USER node

# -----------------------------
# Expose port (Render uses $PORT)
# -----------------------------
EXPOSE 5678

CMD ["n8n"]

FROM n8nio/n8n:latest-debian

USER root

# -----------------------------------
# System dependencies (Render-safe)
# -----------------------------------
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

# -----------------------------------
# Python packages (NO apt opencv)
# -----------------------------------
RUN pip3 install --no-cache-dir \
    numpy \
    pillow \
    pytesseract \
    opencv-python-headless \
    insightface \
    onnxruntime==1.16.3 \
    requests

# -----------------------------------
# Switch back to n8n user
# -----------------------------------
USER node

EXPOSE 5678
CMD ["n8n"]

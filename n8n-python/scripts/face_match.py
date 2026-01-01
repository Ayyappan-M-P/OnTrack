# # #!/usr/bin/env python3
# # """
# # Face Matching - Compare faces using InsightFace embeddings
# # Usage: python3 face_match.py <pan_image> <photo_image>
# # OUTPUT: PURE JSON ONLY (n8n-safe)
# # """

# # # ===============================
# # # HARD LOG SUPPRESSION (CRITICAL)
# # # ===============================
# # import os
# # import sys
# # import json
# # import contextlib

# # os.environ["INSIGHTFACE_LOG_LEVEL"] = "ERROR"
# # os.environ["ORT_LOGGING_LEVEL"] = "ERROR"
# # os.environ["OMP_NUM_THREADS"] = "1"

# # @contextlib.contextmanager
# # def suppress_stdout_stderr():
# #     with open(os.devnull, "w") as devnull:
# #         old_stdout = sys.stdout
# #         old_stderr = sys.stderr
# #         sys.stdout = devnull
# #         sys.stderr = devnull
# #         try:
# #             yield
# #         finally:
# #             sys.stdout = old_stdout
# #             sys.stderr = old_stderr

# # # ===============================
# # # IMPORTS
# # # ===============================
# # import cv2
# # import numpy as np
# # from pathlib import Path

# # try:
# #     from insightface.app import FaceAnalysis
# #     INSIGHTFACE_AVAILABLE = True
# # except ImportError:
# #     INSIGHTFACE_AVAILABLE = False


# # # ===============================
# # # HELPERS
# # # ===============================
# # def cosine_similarity(a, b):
# #     return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# # def extract_embedding(image_path, app):
# #     if not Path(image_path).exists():
# #         return None, "Image file not found"

# #     img = cv2.imread(image_path)
# #     if img is None:
# #         return None, "Failed to read image"

# #     faces = app.get(img)

# #     if len(faces) == 0:
# #         return None, "No face detected"
# #     if len(faces) > 1:
# #         return None, "Multiple faces detected"

# #     return faces[0].embedding, None


# # # ===============================
# # # CORE LOGIC
# # # ===============================
# # def match_faces(pan_img, photo_img):

# #     if not INSIGHTFACE_AVAILABLE:
# #         return {
# #             "success": False,
# #             "error": "InsightFace not installed",
# #             "similarity_score": 0.0,
# #             "match": False,
# #             "confidence": "none"
# #         }

# #     try:
# #         # Silence ALL model loading output
# #         with suppress_stdout_stderr():
# #             app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
# #             app.prepare(ctx_id=0, det_size=(640, 640))

# #         pan_emb, err = extract_embedding(pan_img, app)
# #         if err:
# #             return fail(f"PAN image: {err}")

# #         photo_emb, err = extract_embedding(photo_img, app)
# #         if err:
# #             return fail(f"Photo image: {err}")

# #         score = cosine_similarity(pan_emb, photo_emb)
# #         threshold = 0.75
# #         is_match = bool(score >= threshold)

# #         if score >= 0.85:
# #             confidence = "high"
# #         elif score >= 0.75:
# #             confidence = "medium"
# #         elif score >= 0.60:
# #             confidence = "low"
# #         else:
# #             confidence = "very_low"

# #         return {
# #             "success": True,
# #             "similarity_score": round(float(score), 6),
# #             "match": is_match,
# #             "threshold": threshold,
# #             "confidence": confidence,
# #             "pan_face_detected": True,
# #             "photo_face_detected": True
# #         }

# #     except Exception as e:
# #         return fail(str(e))


# # def fail(msg):
# #     return {
# #         "success": False,
# #         "error": msg,
# #         "similarity_score": 0.0,
# #         "match": False,
# #         "confidence": "none"
# #     }


# # # ===============================
# # # ENTRY POINT (JSON ONLY)
# # # ===============================
# # if __name__ == "__main__":

# #     if len(sys.argv) != 3:
# #         print(json.dumps({
# #             "success": False,
# #             "error": "Usage: python3 face_match.py <pan_image> <photo_image>"
# #         }))
# #         sys.exit(1)

# #     result = match_faces(sys.argv[1], sys.argv[2])

# #     # 🔥 GUARANTEED CLEAN JSON OUTPUT
# #     print(json.dumps(result))


# #!/usr/bin/env python3
# """
# PRODUCTION FACE MATCH (PAN AWARE)
# PURE JSON OUTPUT
# """

# import os, sys, json, contextlib
# import cv2
# import numpy as np
# from pathlib import Path

# os.environ["INSIGHTFACE_LOG_LEVEL"] = "ERROR"

# @contextlib.contextmanager
# def silent():
#     with open(os.devnull, "w") as f:
#         old_out, old_err = sys.stdout, sys.stderr
#         sys.stdout = sys.stderr = f
#         yield
#         sys.stdout, sys.stderr = old_out, old_err

# from insightface.app import FaceAnalysis

# def normalize(img):
#     g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     g = cv2.equalizeHist(g)
#     return cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)

# def get_embedding(path, app):
#     img = cv2.imread(path)
#     if img is None:
#         return None, "Invalid image"

#     img = normalize(img)
#     faces = app.get(img)

#     if len(faces) != 1:
#         return None, "Face count != 1"

#     return faces[0].embedding, None

# def cosine(a, b):
#     return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# def match(pan_img, live_img):
#     with silent():
#         app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
#         app.prepare(ctx_id=0, det_size=(640, 640))

#     e1, err = get_embedding(pan_img, app)
#     if err:
#         return {"success": False, "error": f"PAN: {err}"}

#     e2, err = get_embedding(live_img, app)
#     if err:
#         return {"success": False, "error": f"Photo: {err}"}

#     score = cosine(e1, e2)

#     match = score >= 0.60

#     if score >= 0.75:
#         conf = "high"
#     elif score >= 0.65:
#         conf = "medium"
#     elif score >= 0.55:
#         conf = "acceptable"
#     else:
#         conf = "low"

#     return {
#         "success": True,
#         "similarity_score": round(score, 4),
#         "threshold": 0.60,
#         "match": match,
#         "confidence": conf
#     }

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print(json.dumps({"success": False, "error": "Usage: face_match.py <pan> <photo>"}))
#         sys.exit(1)

#     print(json.dumps(match(sys.argv[1], sys.argv[2])))


#!/usr/bin/env python3
"""
PRODUCTION FACE MATCHING FOR PAN VERIFICATION
- PAN card photo region aware
- NumPy-safe JSON output
- CPU only (free tier friendly)
"""

import os
import sys
import json
import cv2
import numpy as np
from pathlib import Path
import contextlib

# -------------------------------
# Silence InsightFace warnings
# -------------------------------
os.environ["INSIGHTFACE_LOG_LEVEL"] = "ERROR"
os.environ["ORT_LOGGING_LEVEL"] = "ERROR"
os.environ["OMP_NUM_THREADS"] = "1"

@contextlib.contextmanager
def silent():
    with open(os.devnull, "w") as f:
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = f
        try:
            yield
        finally:
            sys.stdout, sys.stderr = old_out, old_err

# -------------------------------
# InsightFace import
# -------------------------------
try:
    from insightface.app import FaceAnalysis
    INSIGHTFACE_AVAILABLE = True
except ImportError:
    INSIGHTFACE_AVAILABLE = False

# -------------------------------
# Helpers
# -------------------------------
def extract_pan_face_region(img):
    """
    PAN card face usually at top-left
    Adjusted for Indian PAN layout
    """
    h, w = img.shape[:2]
    x1 = int(w * 0.02)
    y1 = int(h * 0.12)
    x2 = int(w * 0.26)
    y2 = int(h * 0.56)
    return img[y1:y2, x1:x2]

def normalize_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def cosine_similarity(a, b):
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def extract_embedding(image_path, app, is_pan=False):
    if not Path(image_path).exists():
        return None, "Image file not found"

    img = cv2.imread(image_path)
    if img is None:
        return None, "Invalid image"

    if is_pan:
        img = extract_pan_face_region(img)
        if img.size == 0:
            return None, "PAN face region empty"

    if img.shape[0] < 200 or img.shape[1] < 200:
        scale = max(200 / img.shape[0], 200 / img.shape[1])
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    img = normalize_image(img)

    faces = app.get(img)
    if len(faces) == 0:
        return None, "No face detected"

    if len(faces) > 1:
        faces = sorted(
            faces,
            key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]),
            reverse=True
        )

    return faces[0].embedding, None

# -------------------------------
# Core logic
# -------------------------------
def match_faces(pan_image, photo_image):

    if not INSIGHTFACE_AVAILABLE:
        return {
            "success": False,
            "error": "InsightFace not installed",
            "similarity_score": 0.0,
            "match": False,
            "confidence": "none"
        }

    try:
        with silent():
            app = FaceAnalysis(
                name="buffalo_l",
                providers=["CPUExecutionProvider"]
            )
            app.prepare(ctx_id=0, det_size=(640, 640))

        pan_emb, err = extract_embedding(pan_image, app, is_pan=True)
        if err:
            return fail(f"PAN: {err}")

        photo_emb, err = extract_embedding(photo_image, app, is_pan=False)
        if err:
            return fail(f"Photo: {err}")

        similarity = cosine_similarity(pan_emb, photo_emb)

        # PAN-specific thresholds
        threshold = 0.20
        is_match = bool(similarity >= threshold)

        if similarity >= 0.50:
            confidence = "very_high"
        elif similarity >= 0.40:
            confidence = "high"
        elif similarity >= 0.30:
            confidence = "medium"
        elif similarity >= 0.20:
            confidence = "low"
        else:
            confidence = "very_low"

        return {
            "success": True,
            "similarity_score": float(round(similarity, 6)),
            "threshold": threshold,
            "match": is_match,
            "confidence": confidence,
            "pan_face_detected": True,
            "photo_face_detected": True,
            "recommendation": (
                "APPROVED" if similarity >= 0.50 else
                "REVIEW" if similarity >= 0.20 else
                "REJECTED"
            )
        }

    except Exception as e:
        return fail(str(e))

def fail(msg):
    return {
        "success": False,
        "error": str(msg),
        "similarity_score": 0.0,
        "match": False,
        "confidence": "none"
    }

# -------------------------------
# Entry point
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({
            "success": False,
            "error": "Usage: python3 face_match.py <pan_image> <photo_image>"
        }))
        sys.exit(1)

    result = match_faces(sys.argv[1], sys.argv[2])

    # ✅ Guaranteed JSON-safe output
    print(json.dumps(result, indent=2))

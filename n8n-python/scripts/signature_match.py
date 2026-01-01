# # #!/usr/bin/env python3
# # """
# # Signature Matching - Compare signatures using OpenCV
# # Usage: python3 signature_match.py <pan_image> <signature_image>
# # """

# # import sys
# # import json
# # import cv2
# # import numpy as np
# # from pathlib import Path

# # def preprocess_signature(image_path, region=None):
# #     """
# #     Preprocess signature image for comparison
# #     region: (x, y, width, height) to extract signature from specific region
# #     """
# #     try:
# #         if not Path(image_path).exists():
# #             return None, "Image file not found"
        
# #         img = cv2.imread(image_path)
# #         if img is None:
# #             return None, "Failed to read image"
        
# #         # If region specified, crop to that area
# #         if region:
# #             x, y, w, h = region
# #             img = img[y:y+h, x:x+w]
        
# #         # Convert to grayscale
# #         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
# #         # Apply Otsu's thresholding
# #         _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
# #         # Remove noise
# #         kernel = np.ones((2, 2), np.uint8)
# #         cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
# #         # Resize to standard size for comparison
# #         standard_size = (300, 150)
# #         resized = cv2.resize(cleaned, standard_size, interpolation=cv2.INTER_AREA)
        
# #         return resized, None
        
# #     except Exception as e:
# #         return None, str(e)

# # def calculate_histogram_similarity(img1, img2):
# #     """Calculate histogram similarity"""
# #     hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
# #     hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
    
# #     # Normalize histograms
# #     hist1 = cv2.normalize(hist1, hist1).flatten()
# #     hist2 = cv2.normalize(hist2, hist2).flatten()
    
# #     # Compare using correlation
# #     correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
# #     return correlation

# # def calculate_structural_similarity(img1, img2):
# #     """Calculate structural similarity using template matching"""
# #     result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
# #     _, max_val, _, _ = cv2.minMaxLoc(result)
# #     return max_val

# # def calculate_contour_similarity(img1, img2):
# #     """Calculate similarity based on contours"""
# #     contours1, _ = cv2.findContours(img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# #     contours2, _ = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
# #     if not contours1 or not contours2:
# #         return 0.0
    
# #     # Get largest contour from each
# #     contour1 = max(contours1, key=cv2.contourArea)
# #     contour2 = max(contours2, key=cv2.contourArea)
    
# #     # Compare shapes
# #     similarity = cv2.matchShapes(contour1, contour2, cv2.CONTOURS_MATCH_I2, 0)
    
# #     # Convert to 0-1 range (lower is better, so invert)
# #     normalized = max(0, 1 - (similarity / 10))
# #     return normalized

# # def match_signatures(pan_image_path, signature_image_path):
# #     """Compare signatures from PAN card and signature image"""
    
# #     try:
# #         # Preprocess both signatures
# #         # For PAN card, we might want to extract signature region (bottom 1/4 of card)
# #         pan_img = cv2.imread(pan_image_path)
# #         if pan_img is not None:
# #             h, w = pan_img.shape[:2]
# #             # Signature typically in bottom portion of PAN
# #             pan_sig_region = (int(w*0.1), int(h*0.7), int(w*0.5), int(h*0.25))
# #         else:
# #             pan_sig_region = None
        
# #         pan_signature, pan_error = preprocess_signature(pan_image_path, pan_sig_region)
# #         if pan_error:
# #             return {
# #                 "success": False,
# #                 "error": f"PAN signature: {pan_error}",
# #                 "similarity_score": 0.0,
# #                 "match": False,
# #                 "confidence": "none"
# #             }
        
# #         sig_signature, sig_error = preprocess_signature(signature_image_path)
# #         if sig_error:
# #             return {
# #                 "success": False,
# #                 "error": f"Signature image: {sig_error}",
# #                 "similarity_score": 0.0,
# #                 "match": False,
# #                 "confidence": "none"
# #             }
        
# #         # Calculate multiple similarity metrics
# #         hist_similarity = calculate_histogram_similarity(pan_signature, sig_signature)
# #         struct_similarity = calculate_structural_similarity(pan_signature, sig_signature)
# #         contour_similarity = calculate_contour_similarity(pan_signature, sig_signature)
        
# #         # Weighted average of similarities
# #         weights = {
# #             'histogram': 0.3,
# #             'structural': 0.4,
# #             'contour': 0.3
# #         }
        
# #         overall_similarity = (
# #             hist_similarity * weights['histogram'] +
# #             struct_similarity * weights['structural'] +
# #             contour_similarity * weights['contour']
# #         )
        
# #         # Determine match based on threshold
# #         threshold = 0.70
# #         is_match = overall_similarity >= threshold
        
# #         # Determine confidence level
# #         if overall_similarity >= 0.80:
# #             confidence = "high"
# #         elif overall_similarity >= 0.70:
# #             confidence = "medium"
# #         elif overall_similarity >= 0.55:
# #             confidence = "low"
# #         else:
# #             confidence = "very_low"
        
# #         return {
# #             "success": True,
# #             "similarity_score": float(overall_similarity),
# #             "match": is_match,
# #             "threshold": threshold,
# #             "confidence": confidence,
# #             "detailed_scores": {
# #                 "histogram": float(hist_similarity),
# #                 "structural": float(struct_similarity),
# #                 "contour": float(contour_similarity)
# #             },
# #             "pan_signature_detected": True,
# #             "signature_detected": True
# #         }
        
# #     except Exception as e:
# #         return {
# #             "success": False,
# #             "error": str(e),
# #             "similarity_score": 0.0,
# #             "match": False,
# #             "confidence": "none"
# #         }

# # if __name__ == "__main__":
# #     if len(sys.argv) != 3:
# #         print(json.dumps({
# #             "success": False,
# #             "error": "Usage: python3 signature_match.py <pan_image> <signature_image>"
# #         }))
# #         sys.exit(1)
    
# #     pan_image = sys.argv[1]
# #     signature_image = sys.argv[2]
    
# #     result = match_signatures(pan_image, signature_image)
# #     print(json.dumps(result, indent=2))

# #!/usr/bin/env python3
# """
# PRODUCTION SIGNATURE MATCH
# ORB FEATURE BASED
# PURE JSON OUTPUT
# """

# import sys, json
# import cv2
# from pathlib import Path

# def load_and_clean(path):
#     img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
#     if img is None:
#         return None

#     _, img = cv2.threshold(img, 0, 255,
#                             cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#     return img

# def match(pan_sig, user_sig):
#     img1 = load_and_clean(pan_sig)
#     img2 = load_and_clean(user_sig)

#     if img1 is None or img2 is None:
#         return {"success": False, "error": "Invalid signature image"}

#     orb = cv2.ORB_create(1000)

#     k1, d1 = orb.detectAndCompute(img1, None)
#     k2, d2 = orb.detectAndCompute(img2, None)

#     if d1 is None or d2 is None:
#         return {"success": False, "error": "Signature not detected"}

#     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#     matches = bf.match(d1, d2)

#     score = len(matches) / max(len(k1), len(k2))

#     return {
#         "success": True,
#         "similarity_score": round(score, 4),
#         "threshold": 0.45,
#         "match": score >= 0.45,
#         "confidence": (
#             "high" if score >= 0.60 else
#             "medium" if score >= 0.45 else
#             "low"
#         )
#     }

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print(json.dumps({"success": False, "error": "Usage: signature_match.py <pan> <signature>"}))
#         sys.exit(1)

#     print(json.dumps(match(sys.argv[1], sys.argv[2]), indent=2))

#!/usr/bin/env python3
"""
PRODUCTION SIGNATURE MATCHING
PAN CARD + USER SIGNATURE
JSON SAFE (n8n / Docker / AWS)
"""

import sys
import json
import cv2
import numpy as np
from pathlib import Path

# -------------------------------
# Helpers
# -------------------------------
def to_float(x):
    return float(x) if x is not None else 0.0

def to_bool(x):
    return bool(x)

# -------------------------------
# PAN Signature Region
# -------------------------------
def extract_pan_signature_region(img):
    h, w = img.shape[:2]
    x1 = int(w * 0.15)
    y1 = int(h * 0.73)
    x2 = int(w * 0.65)
    y2 = int(h * 0.95)
    return img[y1:y2, x1:x2]

# -------------------------------
# Preprocessing
# -------------------------------
def preprocess_signature(img, is_pan_card=False):
    if img is None or img.size == 0:
        return None, "Empty image"

    if is_pan_card:
        img = extract_pan_signature_region(img)
        if img.size == 0:
            return None, "Signature region not found"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

    clahe = cv2.createCLAHE(2.0, (8, 8))
    gray = clahe.apply(gray)

    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    _, binary = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    h = 200
    w = int(binary.shape[1] * (h / binary.shape[0]))
    binary = cv2.resize(binary, (w, h), interpolation=cv2.INTER_AREA)

    return binary, None

# -------------------------------
# Similarity Metrics
# -------------------------------
def ssim(img1, img2):
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    mean1, mean2 = np.mean(img1), np.mean(img2)
    var1, var2 = np.var(img1), np.var(img2)
    cov = np.mean((img1 - mean1) * (img2 - mean2))

    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    score = ((2 * mean1 * mean2 + c1) * (2 * cov + c2)) / (
        (mean1**2 + mean2**2 + c1) * (var1 + var2 + c2)
    )

    return to_float(max(0.0, min(1.0, score)))

def histogram_similarity(img1, img2):
    h1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    h2 = cv2.calcHist([img2], [0], None, [256], [0, 256])

    h1 = cv2.normalize(h1, h1).flatten()
    h2 = cv2.normalize(h2, h2).flatten()

    return to_float(max(0.0, cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)))

def contour_similarity(img1, img2):
    c1, _ = cv2.findContours(img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c2, _ = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not c1 or not c2:
        return 0.0

    c1 = max(c1, key=cv2.contourArea)
    c2 = max(c2, key=cv2.contourArea)

    if cv2.contourArea(c1) < 100 or cv2.contourArea(c2) < 100:
        return 0.0

    score = cv2.matchShapes(c1, c2, cv2.CONTOURS_MATCH_I2, 0)
    return to_float(max(0.0, 1 - (score / 5)))

def orb_similarity(img1, img2):
    orb = cv2.ORB_create(500)
    k1, d1 = orb.detectAndCompute(img1, None)
    k2, d2 = orb.detectAndCompute(img2, None)

    if d1 is None or d2 is None:
        return 0.0

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(d1, d2)

    if not matches:
        return 0.0

    avg_dist = np.mean([m.distance for m in matches])
    return to_float(max(0.0, 1 - (avg_dist / 100)))

# -------------------------------
# Core Logic
# -------------------------------
def match_signatures(pan_path, sig_path):
    if not Path(pan_path).exists() or not Path(sig_path).exists():
        return fail("Image file missing")

    pan_img = cv2.imread(pan_path)
    sig_img = cv2.imread(sig_path)

    pan_sig, err = preprocess_signature(pan_img, True)
    if err:
        return fail(f"PAN: {err}")

    usr_sig, err = preprocess_signature(sig_img, False)
    if err:
        return fail(f"Signature: {err}")

    s1 = ssim(pan_sig, usr_sig)
    s2 = histogram_similarity(pan_sig, usr_sig)
    s3 = contour_similarity(pan_sig, usr_sig)
    s4 = orb_similarity(pan_sig, usr_sig)

    overall = to_float(0.30*s1 + 0.20*s2 + 0.25*s3 + 0.25*s4)

    match = to_bool(overall >= 0.70)

    confidence = (
        "very_high" if overall >= 0.80 else
        "high" if overall >= 0.70 else
        "medium" if overall >= 0.60 else
        "low" if overall >= 0.50 else
        "very_low"
    )

    return {
        "success": True,
        "similarity_score": overall,
        "match": match,
        "threshold": 0.70,
        "confidence": confidence,
        "detailed_scores": {
            "ssim": s1,
            "histogram": s2,
            "contour": s3,
            "orb": s4
        },
        "recommendation": (
            "APPROVED" if overall >= 0.70 else
            "REVIEW" if overall >= 0.55 else
            "REJECTED"
        )
    }

def fail(msg):
    return {
        "success": False,
        "error": str(msg),
        "similarity_score": 0.0,
        "match": False,
        "confidence": "none"
    }

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"success": False, "error": "Usage: signature_match.py <pan> <signature>"}))
        sys.exit(1)

    result = match_signatures(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))

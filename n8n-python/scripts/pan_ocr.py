# # #!/usr/bin/env python3
# # """
# # PAN Card OCR - Extracts text and validates PAN format
# # Usage: python3 pan_ocr.py <path_to_pan_image>
# # """

# # import sys
# # import json
# # import cv2
# # import pytesseract
# # import re
# # from pathlib import Path

# # def extract_pan_number(text):
# #     """Extract PAN number using regex pattern: 5 letters + 4 digits + 1 letter"""
# #     pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
# #     matches = re.findall(pan_pattern, text.upper())
# #     return matches[0] if matches else None

# # def extract_name(text):
# #     """Extract name - usually after 'Name' or in specific region"""
# #     lines = text.split('\n')
# #     for i, line in enumerate(lines):
# #         if 'NAME' in line.upper() and i + 1 < len(lines):
# #             return lines[i + 1].strip()
# #     return None

# # def extract_dob(text):
# #     """Extract date of birth"""
# #     dob_pattern = r'\d{2}[/-]\d{2}[/-]\d{4}'
# #     matches = re.findall(dob_pattern, text)
# #     return matches[0] if matches else None

# # def process_pan_card(image_path):
# #     """Process PAN card image and extract information"""
# #     try:
# #         # Read image
# #         if not Path(image_path).exists():
# #             return {
# #                 "success": False,
# #                 "error": "Image file not found",
# #                 "pan_number": None,
# #                 "name": None,
# #                 "dob": None,
# #                 "raw_text": None
# #             }
        
# #         img = cv2.imread(image_path)
# #         if img is None:
# #             return {
# #                 "success": False,
# #                 "error": "Failed to read image",
# #                 "pan_number": None,
# #                 "name": None,
# #                 "dob": None,
# #                 "raw_text": None
# #             }
        
# #         # Preprocess image for better OCR
# #         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
# #         # Apply adaptive thresholding
# #         thresh = cv2.adaptiveThreshold(
# #             gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
# #         )
        
# #         # Denoise
# #         denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
# #         # Perform OCR
# #         text = pytesseract.image_to_string(denoised, config='--psm 6')
        
# #         # Extract information
# #         pan_number = extract_pan_number(text)
# #         name = extract_name(text)
# #         dob = extract_dob(text)
        
# #         # Validate PAN card
# #         is_valid = pan_number is not None
        
# #         return {
# #             "success": True,
# #             "is_valid_pan": is_valid,
# #             "pan_number": pan_number,
# #             "name": name,
# #             "dob": dob,
# #             "raw_text": text.strip(),
# #             "confidence": "high" if pan_number and name else "low"
# #         }
        
# #     except Exception as e:
# #         return {
# #             "success": False,
# #             "error": str(e),
# #             "pan_number": None,
# #             "name": None,
# #             "dob": None,
# #             "raw_text": None
# #         }

# # if __name__ == "__main__":
# #     if len(sys.argv) != 2:
# #         print(json.dumps({
# #             "success": False,
# #             "error": "Usage: python3 pan_ocr.py <path_to_pan_image>"
# #         }))
# #         sys.exit(1)
    
# #     image_path = sys.argv[1]
# #     result = process_pan_card(image_path)
# #     print(json.dumps(result, indent=2))

# #!/usr/bin/env python3
# """
# PRODUCTION PAN OCR
# - PAN Number
# - Name
# - DOB
# PURE JSON OUTPUT (n8n safe)
# """

# import sys, json, re
# import cv2
# import pytesseract
# from pathlib import Path

# PAN_REGEX = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
# DOB_REGEX = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"

# def preprocess(img):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.bilateralFilter(gray, 11, 17, 17)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#     return thresh

# def extract_fields(text):
#     text = text.upper()

#     pan = re.search(PAN_REGEX, text)
#     dob = re.search(DOB_REGEX, text)

#     name = None
#     lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 3]
#     for i, l in enumerate(lines):
#         if "NAME" in l and i + 1 < len(lines):
#             name = lines[i + 1]
#             break

#     return {
#         "pan_number": pan.group() if pan else None,
#         "dob": dob.group() if dob else None,
#         "name": name
#     }

# def process(image_path):
#     if not Path(image_path).exists():
#         return {"success": False, "error": "Image not found"}

#     img = cv2.imread(image_path)
#     if img is None:
#         return {"success": False, "error": "Invalid image"}

#     proc = preprocess(img)

#     config = (
#         "--oem 3 --psm 4 "
#         "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/"
#     )
#     text = pytesseract.image_to_string(proc, config=config)

#     fields = extract_fields(text)

#     confidence = {
#         "pan": bool(fields["pan_number"]),
#         "name": bool(fields["name"]),
#         "dob": bool(fields["dob"])
#     }

#     return {
#         "success": True,
#         "pan_valid": confidence["pan"],
#         "pan_number": fields["pan_number"],
#         "name": fields["name"],
#         "dob": fields["dob"],
#         "confidence": confidence,
#         "raw_text": text.strip()
#     }

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print(json.dumps({"success": False, "error": "Usage: pan_ocr.py <image>"}))
#         sys.exit(1)

#     print(json.dumps(process(sys.argv[1]), indent=2))

#!/usr/bin/env python3
"""
PAN Card OCR - Optimized for Indian PAN Card Layout
Extracts: PAN Number, Name, Father's Name, Date of Birth
"""

import sys
import json
import cv2
import pytesseract
import re
import numpy as np
from pathlib import Path

def preprocess_image(img):
    """Enhanced preprocessing for PAN card images"""
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
    
    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    return thresh

def extract_pan_number(text):
    """Extract PAN number: 5 letters + 4 digits + 1 letter"""
    # Multiple patterns to catch variations
    patterns = [
        r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b',
        r'[A-Z]{5}\s?[0-9]{4}\s?[A-Z]{1}',
        r'PAN[:\s]+([A-Z]{5}[0-9]{4}[A-Z]{1})'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text.upper())
        if matches:
            pan = matches[0].replace(' ', '')
            if len(pan) == 10:
                return pan
    return None

def extract_name(text, pan_number=None):
    """Extract name from PAN card"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Name typically appears after "Name" keyword or after PAN number
    for i, line in enumerate(lines):
        if 'NAME' in line.upper() and i + 1 < len(lines):
            name_candidate = lines[i + 1]
            # Clean up the name
            name_candidate = re.sub(r'[^A-Za-z\s]', '', name_candidate)
            if len(name_candidate) > 3:
                return name_candidate.strip().title()
        
        # If PAN number found in line, next line might be name
        if pan_number and pan_number in line and i + 1 < len(lines):
            name_candidate = lines[i + 1]
            name_candidate = re.sub(r'[^A-Za-z\s]', '', name_candidate)
            if len(name_candidate) > 3:
                return name_candidate.strip().title()
    
    return None

def extract_father_name(text):
    """Extract father's name"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    for i, line in enumerate(lines):
        if 'FATHER' in line.upper() and i + 1 < len(lines):
            father_name = lines[i + 1]
            father_name = re.sub(r'[^A-Za-z\s]', '', father_name)
            if len(father_name) > 3:
                return father_name.strip().title()
    
    return None

def extract_dob(text):
    """Extract date of birth - multiple formats"""
    patterns = [
        r'\b\d{2}[/-]\d{2}[/-]\d{4}\b',  # DD/MM/YYYY or DD-MM-YYYY
        r'\b\d{4}[/-]\d{2}[/-]\d{2}\b',  # YYYY/MM/DD
        r'\b\d{2}\s+\d{2}\s+\d{4}\b'     # DD MM YYYY with spaces
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0].replace(' ', '/')
    
    return None

def extract_text_from_regions(img):
    """Extract text from specific regions of PAN card for better accuracy"""
    height, width = img.shape[:2]
    
    # Define regions (adjust based on standard PAN card layout)
    regions = {
        'pan_region': img[int(height*0.25):int(height*0.45), int(width*0.15):int(width*0.70)],
        'name_region': img[int(height*0.40):int(height*0.60), int(width*0.05):int(width*0.65)],
        'father_region': img[int(height*0.55):int(height*0.70), int(width*0.05):int(width*0.65)],
        'dob_region': img[int(height*0.70):int(height*0.90), int(width*0.05):int(width*0.50)]
    }
    
    extracted_data = {}
    for region_name, region_img in regions.items():
        if region_img.size > 0:
            text = pytesseract.image_to_string(
                region_img, 
                config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/- '
            )
            extracted_data[region_name] = text.strip()
    
    return extracted_data

def process_pan_card(image_path):
    """Main processing function for PAN card"""
    try:
        # Read image
        if not Path(image_path).exists():
            return {
                "success": False,
                "error": "Image file not found",
                "pan_number": None,
                "name": None,
                "father_name": None,
                "dob": None,
                "raw_text": None
            }
        
        img = cv2.imread(image_path)
        if img is None:
            return {
                "success": False,
                "error": "Failed to read image",
                "pan_number": None,
                "name": None,
                "father_name": None,
                "dob": None,
                "raw_text": None
            }
        
        # Preprocess
        processed = preprocess_image(img)
        
        # Full card OCR
        full_text = pytesseract.image_to_string(processed, config='--psm 6')
        
        # Region-based OCR for better accuracy
        region_data = extract_text_from_regions(processed)
        combined_text = full_text + "\n" + "\n".join(region_data.values())
        
        # Extract information
        pan_number = extract_pan_number(combined_text)
        name = extract_name(combined_text, pan_number)
        father_name = extract_father_name(combined_text)
        dob = extract_dob(combined_text)
        
        # Validate PAN card
        is_valid = pan_number is not None
        
        # Confidence scoring
        confidence_score = 0
        if pan_number: confidence_score += 40
        if name: confidence_score += 25
        if father_name: confidence_score += 20
        if dob: confidence_score += 15
        
        confidence = "high" if confidence_score >= 70 else "medium" if confidence_score >= 50 else "low"
        
        return {
            "success": True,
            "is_valid_pan": is_valid,
            "pan_number": pan_number,
            "name": name,
            "father_name": father_name,
            "dob": dob,
            "confidence": confidence,
            "confidence_score": confidence_score,
            "raw_text": full_text.strip()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "pan_number": None,
            "name": None,
            "father_name": None,
            "dob": None,
            "raw_text": None
        }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: python3 pan_ocr.py <path_to_pan_image>"
        }))
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = process_pan_card(image_path)
    print(json.dumps(result, indent=2))
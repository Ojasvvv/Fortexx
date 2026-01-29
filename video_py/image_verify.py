import sys
import os
import json
import numpy as np
import imageio.v3 as iio
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
from video_utils import content_hash

def verify_image(image_path: str, public_key_path: str = "keys/public_key.pem"):
    report = {
        "file": image_path,
        "status": "UNKNOWN",
        "failure_type": None,
        "mismatched_blocks": [],
        "tamper_map": None
    }

    # 1. Load Public Key
    try:
        with open(public_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
    except Exception as e:
        report["status"] = "ERROR"
        report["failure_type"] = f"Key Load Failed: {e}"
        return report

    # 2. Load Provenance Data
    try:
        with open("provenance/image_hashes.json", "r") as f:
            # We load as string first to verify signature, then parse
            prov_json_str = f.read()
            prov_data = json.loads(prov_json_str)

        with open("provenance/image_sig.bin", "rb") as f:
            signature = f.read()
            
        # Re-serialize exactly as signed (sorted keys)
        data_to_verify = json.dumps(prov_data, sort_keys=True).encode()
        
        public_key.verify(signature, data_to_verify, ec.ECDSA(hashes.SHA256()))
        # Signature valid -> Trust the hash map
        
    except InvalidSignature:
        report["status"] = "FAILED"
        report["failure_type"] = "SIGNATURE_MISMATCH"
        return report
    except FileNotFoundError:
        report["status"] = "FAILED"
        report["failure_type"] = "NO_PROVENANCE_FOUND"
        return report

    # 3. Load & Process Image
    try:
        image = iio.imread(image_path)
    except Exception:
        report["status"] = "ERROR" 
        return report

    # Handle RGBA
    if image.shape[-1] == 4:
        image = image[..., :3]

    h, w, _ = image.shape
    GRID_ROWS, GRID_COLS = prov_data["grid"]
    stored_hashes = prov_data["hashes"]
    
    block_h = h // GRID_ROWS
    block_w = w // GRID_COLS

    mismatches = []
    
    # We will create a tamper map regardless, starting as a copy of the image
    tamper_map = image.copy()
    has_tamper = False

    idx = 0
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            # Define Region (Same logic as signer)
            y1 = r * block_h
            y2 = (r + 1) * block_h if r < GRID_ROWS - 1 else h
            x1 = c * block_w
            x2 = (c + 1) * block_w if c < GRID_COLS - 1 else w
            
            # Extract
            block = image[y1:y2, x1:x2]
            block_bytes = block.astype(np.uint8).tobytes()
            curr_hash = content_hash(block_bytes).hex()
            
            # Compare
            if curr_hash != stored_hashes[idx]:
                has_tamper = True
                mismatches.append(idx)
                
                # DRAW RED OVERLAY
                # Alpha blend: 0.5 original + 0.5 Red (255, 0, 0)
                roi = tamper_map[y1:y2, x1:x2].astype(float)
                red_overlay = np.zeros_like(roi)
                red_overlay[:] = [255, 0, 0]
                
                # Blend
                blended = roi * 0.6 + red_overlay * 0.4
                tamper_map[y1:y2, x1:x2] = blended.astype(np.uint8)
                
                # Draw Border
                border = 2
                tamper_map[y1:y1+border, x1:x2] = [255, 0, 0]
                tamper_map[y2-border:y2, x1:x2] = [255, 0, 0]
                tamper_map[y1:y2, x1:x1+border] = [255, 0, 0]
                tamper_map[y1:y2, x2-border:x2] = [255, 0, 0]

            idx += 1

    if has_tamper:
        report["status"] = "TAMPERED"
        report["failure_type"] = "BLOCK_HASH_MISMATCH"
        report["mismatched_blocks"] = mismatches
        
        # Save Map
        map_path = "provenance/tamper_map.png"
        iio.imwrite(map_path, tamper_map)
        report["tamper_map"] = map_path
        print(f"Tamper detected. Map saved to {map_path}")
    else:
        report["status"] = "VERIFIED"
        print("Image verified successfully.")

    return report

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python image_verify.py <image.png>")
        sys.exit(1)
    print(json.dumps(verify_image(sys.argv[1]), indent=2))

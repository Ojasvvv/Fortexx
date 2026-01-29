import os
import sys
from flask import Flask, request, send_file, send_from_directory

# Add CWD to system path so we can import video_py modules if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Also add the video_py subdirectory so 'import video_utils' works inside those scripts
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video_py'))

# Import Video Backend
VIDEO_IMPORT_ERROR = None
try:
    # Import directly since we added video_py to path
    import video_sign
    import video_verify
    import image_sign
    import image_verify
    VIDEO_BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Video backend not available: {e}")
    VIDEO_IMPORT_ERROR = str(e)
    VIDEO_BACKEND_AVAILABLE = False

app = Flask(__name__, static_folder='ui', static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB Limit

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(BASE_DIR, 'keys')
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, 'private_key.pem')
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, 'public_key.pem')

# Ensure Device Keys Exist on Startup
if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
    print("Generating Device Identity Keys...")
    try:
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives import serialization
        from pathlib import Path
        
        Path(KEYS_DIR).mkdir(exist_ok=True)
        
        private_key = ec.generate_private_key(ec.SECP256R1())
        
        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            ))
            
        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(private_key.public_key().public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            ))
        print("✔ Device Identity Created")
    except Exception as e:
        print(f"Failed to generate keys: {e}")

@app.route('/')
def serve_index():
    return send_from_directory('ui', 'index.html')

@app.route('/provenance/<path:filename>')
def serve_provenance(filename):
    return send_from_directory('provenance', filename)

@app.route('/api/protect', methods=['POST'])
def protect_media():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400

    filename = file.filename
    # Determine extension to serve back correctly or just default to mp4/jpg
    ext = os.path.splitext(filename)[1].lower()
    mimetype = 'video/mp4' # Default for video backend output if unchanged
    if ext in ['.jpg', '.jpeg', '.png']:
        mimetype = 'image/jpeg' 

    if not VIDEO_BACKEND_AVAILABLE:
        return {'error': 'Backend not available', 'details': VIDEO_IMPORT_ERROR}, 501
        
    # Save input
    input_path = os.path.join(BASE_DIR, f'input{ext}')
    file.save(input_path)
    
    try:
        # Call the unified backend function
        if mimetype == 'image/jpeg':
             image_sign.sign_image(input_path)
        else:
             video_sign.sign_video(input_path)
        
        # Return the original file (provenance is stored separately on disk)
        # In a real app we might zip them or embed metadata.
        # For this prototype, we just return the file availability.
        return send_file(input_path, mimetype=mimetype)

    except Exception as e:
        print(f"Processing Error: {e}")
        return {'error': 'Processing failed', 'details': str(e)}, 500

@app.route('/api/verify', methods=['POST'])
def verify_media():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    input_path = os.path.join(BASE_DIR, f'input{ext}')
    file.save(input_path)

    mimetype = 'video/mp4'
    if ext in ['.jpg', '.jpeg', '.png']:
        mimetype = 'image/jpeg'

    # Handle Optional Public Key from User (Same for both Video and Image)
    # Default to Device Identity
    verify_key_path = PUBLIC_KEY_PATH
    
    if 'key' in request.form and request.form['key'].strip():
        try:
            user_key = request.form['key'].strip()
            # Simple validation: check header/footer
            if "BEGIN PUBLIC KEY" in user_key:
                # Video backend: Use a TEMP file, do NOT overwrite Device Identity
                temp_key_path = os.path.join(BASE_DIR, 'temp_verify_key.pem')
                with open(temp_key_path, 'w') as f:
                    f.write(user_key)
                
                verify_key_path = temp_key_path
                print("Using provided user public key (Temporary).")
                

                    
        except Exception as e:
            print(f"Error saving user key: {e}")



    if not VIDEO_BACKEND_AVAILABLE:
        return {'error': 'Backend not available', 'details': VIDEO_IMPORT_ERROR}, 501

    try:
        # Unified Verification
        if mimetype == 'image/jpeg':
            report = image_verify.verify_image(input_path, public_key_path=verify_key_path)
        else:
            report = video_verify.verify_video(input_path, public_key_path=verify_key_path)
        
        status = report.get('status', 'UNKNOWN')
        # Map internal status to API status if needed, or pass through
        # Current UI expects: VERIFIED, AUTHENTIC, or TAMPERED (or FAILED)
        
        # video_verify returns: VERIFIED (success), FAILED (hash mismatch), or throws for Sig failure
        # Let's align with UI expectations
        if status == "VERIFIED":
             # "VERIFIED" is good.
             pass
        elif status == "FAILED":
            status = "TAMPERED" # UI treats non-verified as Tamper Detected usually
        
        return {'status': status, 'details': report}

    except Exception as e:
        print(f"Verification Error: {e}")
        # If signature fails, it might raise InvalidSignature
        return {'status': 'TAMPERED', 'details': str(e)}

@app.route('/api/public-key')
def get_public_key():
    # Always return the Device Identity Key
    key_path = PUBLIC_KEY_PATH
    
    if os.path.exists(key_path):
        with open(key_path, 'r') as f:
            return {'key': f.read()}
    return {'key': '-----BEGIN PUBLIC KEY-----\nNo Key Generated Yet\n-----END PUBLIC KEY-----'}

if __name__ == '__main__':
    print("Starting Hemlock Server on http://localhost:5000")
    app.run(debug=True, port=5000)

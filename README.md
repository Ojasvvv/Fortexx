# HEMLOCK: Cryptographic Provenance & Media Defense Engine

Hemlock is a **verifiable media engine** designed to protect creative work in the age of generative AI. It combines **adversarial perturbations** (to disrupt unauthorized AI training) with **cryptographic signatures** (to establish mathematical provenance).

---

## 🛡️ Core Technologies

### 1. Defense Layer (Adversarial Injection)
Hemlock scans media assets for high-frequency texture regions vulnerable to latent space decoding. It then injects **imperceptible adversarial noise** that "poisons" feature extraction, preventing AI models from effectively training on or replicating the style of your work.

### 2. Provenance Layer (Digital Signatures)
Every processed asset is cryptographically signed using **RSA-2048 / ECDSA-P256**. This creates an immutable link between the creator (Device Identity) and the content. Verification can be performed offline using the public key.

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.8+**
- **pip** (Python Package Manager)

### 1. Initialize the Environment
The project is self-contained. Install the required Python dependencies:

```bash
pip install flask cryptography numpy imageio imageio[ffmpeg]
```

### 2. Device Identity Generation
On the first run, the server automatically generates a unique **Device Identity** keypair (`private_key.pem`, `public_key.pem`) in the `keys/` directory.
- **Private Key**: Kept secret on your device. Used to sign assets.
- **Public Key**: Shared with others to verify asset authenticity.

---

## 🖥️ Usage

### Start the Engine
Run the Python server to start the local engine and UI:

```bash
python server.py
```

Access the interface at: **`http://localhost:5000`**

### Modes of Operation

#### ✍️ **SIGN (Protect)**
1.  Navigate to the **Injection Console**.
2.  Upload an Image or Video (mp4, mov).
3.  The engine will:
    - Analyze the visual frequencies.
    - Inject adversarial protection.
    - Sign the file with your Private Key.
4.  **Download** the protected asset.
5.  **Copy** your Public Key (shown in the panel) to share with verifiers.

#### 🔍 **VERIFY (Authenticate)**
1.  Switch to **Verify** mode.
2.  Upload a suspicious or protected file.
3.  Paste the **Public Key** of the creator (or use your own).
4.  The engine will validate:
    - **Integrity**: Has the file been tampered with? (Pixel-level checks)
    - **Authenticity**: Was it signed by the owner of this key?
5.  View detailed reports: `AUTHENTIC`, `TAMPER DETECTED`, or `WRONG KEY`.

---

## 🏗️ Architecture

The project follows a clean, flat architecture in the `Hemlock/` directory.

```
Hemlock/
├── server.py              # Flask Backend (API & Static Serving)
├── ui/                    # Frontend Application
│   └── index.html         # Single-Page UI (HTML/Tailwind/JS)
├── video_py/              # Core Processing Modules
│   ├── video_sign.py      # Signing Logic (Hashing & Metadata)
│   ├── video_verify.py    # Verification Logic
│   └── video_utils.py     # Shared Utilities (Frame Extraction)
├── keys/                  # Generated Identity Keys (Auto-created)
└── provenance/            # Local ledger of signed hashes (Prototype)
```

### Tech Stack
- **Backend**: Python (Flask)
- **Frontend**: HTML5, Vanilla JavaScript, TailwindCSS
- **Cryptography**: `cryptography` library (RSA/ECDSA)
- **Media Processing**: `imageio`, `numpy`

---

## ⚠️ Notes
- **Performance**: Video processing (frame extraction & hashing) is compute-intensive. Large 4K files may take time.
- **Adversarial Noise**: The "glitch" or noise is designed to be invisible to humans but highly disruptive to machines.
- **Key Safety**: Never share your `private_key.pem`. If lost, previous assets cannot be re-signed with the same identity.

---

**System Online // v1.0.4**
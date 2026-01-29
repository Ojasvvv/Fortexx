# 🎙️ Hemlock: 6-Page Hackathon Pitch Deck

This content is designed to answer judge questions *before* they ask them.

---

## Slide 1: The Crisis (The "Why Now?")
**Headline: The Internet Has Lost Its Memory of What Is Real.**

*   **The Status Quo:** 
    *   3.2 Billion images are shared daily.
    *   AI models scrape 100% of them without consent.
    *   Deepfakes cost the global economy $10B+ annually in fraud.
*   **The Hard Truth:** We can no longer trust our eyes. From fake news in elections to style theft in art, the digital world is suffering an **Identity Crisis**.
*   **The Gap:** Current solutions (watermarks) are easily removed. Metadata is stripped by social media.
*   **The Hook:** "We need a solution that protects the *creator* from AI theft and the *viewer* from AI lies."

---

## Slide 2: The Solution (Meet Hemlock)
**Headline: Shield & Seal. The Dual-Layer Defense.**

*   **Hemlock is the first system to combine:**
    1.  **🛡️ Adversarial Defense (The Shield):** Injects invisible mathematical noise into images.
        *   *Effect:* Humans see a masterpiece. AI models see static/garbage. It prevents style cloning at the source.
    2.  **🔐 Cryptographic Provenance (The Seal):** Signs the file with a private key (RSA-2048).
        *   *Effect:* Creates an immutable chain of custody. If a pixel changes, the signature breaks.

*   **Visual Metaphor:** "Think of it like a bank note: It has **anti-counterfeit ink** (Adversarial Noise) and a **serial number** (Cryptographic Signature)."

---

## Slide 3: How It Works (The Tech)
**Headline: From Pixels to Proof.**

*   **Step 1: Scan & Inject**
    *   We use *Psychovisual Masking* to hide defense noise in complex texture regions (hair, grass) where the human eye can't see it.
*   **Step 2: Sign**
    *   We hash the file (SHA-256) and sign it with the Creator's Private Key.
*   **Step 3: Verify**
    *   Anyone (News, Courts, Twitter) can check the file against the Creator's Public Key.
    *   **Green Check:** Authentic.
    *   **Red Alert:** Tampered (features a Heat Map showing *exactly* where the fake pixels are).

---

## Slide 4: Use Cases (The Market)
**Headline: Verified Truth for Every Sector.**

1.  **🏛️ Governance & News (The "Truth" Layer)**
    *   *Scenario:* A deepfake video of a President declaring war.
    *   *Hemlock:* News agencies check the signature. No official Gov key? **It's Fake.** Crisis averted.
2.  **🎨 Creative Economy (The "Protection" Layer)**
    *   *Scenario:* Artists losing jobs because AI clones their style.
    *   *Hemlock:* They "poison" their portfolios. AI training fails. Their style remains theirs.
3.  **🏥 Insurance & Legal (The "Integrity" Layer)**
    *   *Scenario:* "Photoshop Fraud" on car accident photos.
    *   *Hemlock:* Photos are signed at the scene. Tampering is mathematically impossible.

---

## Slide 5: The Gauntlet (Answering Doubts)
**Headline: We Know What You're Thinking.**

*   **Q: "What if a hacker signs a fake with their own key?"**
    *   **A:** A signature proves *Identity*. If I sign a fake Apple press release, it verifies as "Signed by Ojasv," not "Signed by Apple." The math doesn't lie.
*   **Q: "Does the noise ruin quality?"**
    *   **A:** No. Our masking algorithm ensures the noise is imperceptible to humans (below the Just Noticeable Difference threshold).
*   **Q: "What about the Analog Gap (taking a photo of a screen)?"**
    *   **A:** This breaks the cryptographic seal (Good! It's no longer verified). The adversarial defense, however, often *survives* re-compression, keeping the style protected even in screenshots.
*   **Q: "Why not C2PA/Adobe?"**
    *   **A:** C2PA is hardware-heavy and bureaucratic. Hemlock is software-first, open-source, and democratized for *everyone*.

---

## Slide 6: The Vision (The Close)
**Headline: The "SSL" for Content.**

*   **The Past:** In the 90s, you couldn't trust credit cards online until **SSL (the Green Padlock)** arrived.
*   **The Future:** In 2026, you won't trust media without **Hemlock**.
*   **Our Goal:** To make the "Hemlock Verified" badge the global standard for digital truth.
*   **Call to Action:** "Let's make the internet human again."

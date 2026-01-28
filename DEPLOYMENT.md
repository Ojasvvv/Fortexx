# Deployment Guide for Hemlock

Hemlock is a Python Flask application that uses local filesystem storage for keys and media processing.

## 🚀 Recommended Hosting: Render.com (Easiest)
Render offers a free tier (for web services) and supports persistent disks (required for your keys).

### Option A: Quick Deploy (No Permanent Keys)
If you just want to demo the app and don't care if the "Device Identity" changes every time the server restarts:

1.  Push this `Hemlock/` folder to a **GitHub Repository**.
2.  Go to [Render.com](https://render.com) -> New **Web Service**.
3.  Connect your GitHub repo.
4.  **Critical Step**: In the settings, find **Root Directory** and set it to: `Hemlock`
5.  Use these settings:
    - **Runtime**: Python 3
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn server:app`
5.  Click **Create Web Service**.

### Option B: Persistent Keys (Real Usage)
To keep your `private_key.pem` safe and persistent:

1.  Follow steps 1-4 above.
2.  In Render, go to **Disks** -> Add Disk.
    - Name: `hemlock-data`
    - Mount Path: `/opt/render/project/src/keys`
    - Size: 1 GB
3.  This ensures your keys survive restarts.

---

## ☁️ Alternative: Heroku
1.  Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
2.  Login: `heroku login`
3.  Create app: `heroku create hemlock-app`
4.  Deploy: `git push heroku main`
5.  **Note**: Heroku uses an ephemeral filesystem. Your generated keys will be deleted every 24 hours. You must use **Config Vars** to store keys in production.

---

## 💻 Alternative: VPS (DigitalOcean, AWS EC2)
1.  SSH into your server.
2.  Clone your repo.
3.  Install dependencies:
    ```bash
    sudo apt install python3-pip ffmpeg
    pip3 install -r requirements.txt
    ```
4.  Run with Gunicorn:
    ```bash
    gunicorn --workers 3 --bind 0.0.0.0:80 server:app
    ```

---

## ⚠️ Important Note on FFMPEG
Hemlock uses `imageio` which often needs `ffmpeg`.
- On **Render/Heroku**: The `imageio[ffmpeg]` dependency usually handles binary downloads automatically.
- If you see errors about "ffmpeg not found", you may need to add a "Buildpack".
    - **Render**: Add environment variable `RENDER` = `true`.

## ❓ FAQ

### 1. Does the Free Tier sleep?
**Yes.** On Render (and Heroku) free tiers, the server "spins down" after 15 minutes of inactivity to save resources.
- **Consequence**: The first time you visit the site after a break, it might take **30-50 seconds** to load while the server wakes up.
- **Fix**: Upgrade to a paid plan ($7/mo) for 24/7 uptime, or use a free uptime monitor (like UptimeRobot) to ping it every 10 mins.

### 2. How do I integrate the Frontend?
**It is already integrated.**
- You do **not** need to host the HTML separately (e.g., on Vercel or Netlify).
- The Python backend (`server.py`) is configured to serve your `ui/index.html` file as the main page.
- When you deploy this repository, you get both the API and the Website in one URL.

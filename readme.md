# MovieBox API – Render Ready (v2.5.3)

Host on **Render** (or Railway) → use in your Android / iOS / Web app.

Every stream now returns a ready **`proxy_url`** so your app can play video without setting headers.

---

## 🚀 Deploy on Render (Free)

1. Push this folder to a GitHub repo  
   **OR** just drag-drop the zip on Render (Blueprint)

2. On [render.com](https://render.com) → **New → Web Service**

3. Settings:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

4. After deploy finishes, copy your URL  
   Example: `https://moviebox-api-xxxx.onrender.com`

5. (Recommended) Add Environment Variable:
   ```
   PUBLIC_BASE_URL = https://moviebox-api-xxxx.onrender.com
   ```
   Then **Manual Deploy** once.

Done. API live.

---

## 📱 How to use in your App

### 1. Search movie
```
GET https://your-app.onrender.com/search?q=Animal
```

Response:
```json
[
  {
    "subject_id": "1234567890",
    "title": "Animal",
    "type": "Movie",
    "release_date": "2023-...",
    "imdb_rating": "6.2"
  }
]
```

### 2. Get streams (all qualities + proxy links)
```
GET https://your-app.onrender.com/api/stream/1234567890
```

For series:
```
GET https://your-app.onrender.com/api/stream/1234567890?se=1&ep=3
```

Response example:
```json
{
  "subject_id": "1234567890",
  "count": 4,
  "streams": [
    {
      "quality": "1080p",
      "format": "MP4",
      "size_mb": 1850.4,
      "url": "https://cdn.../video.mp4?sign=...",
      "headers": {
        "Referer": "https://123moviesfree.club/",
        "User-Agent": "Mozilla/5.0 ..."
      },
      "proxy_url": "https://your-app.onrender.com/proxy?url=https%3A%2F%2Fcdn...&referer=https%3A%2F%2F123moviesfree.club%2F"
    },
    {
      "quality": "720p",
      "proxy_url": "https://your-app.onrender.com/proxy?url=..."
    }
  ]
}
```

### 3. Play in app

**Best way (recommended):**
```
player.setDataSource(stream.proxy_url)
```
No need to set any headers. Proxy handles Referer + Origin.

**Alternative (direct):**
Use `stream.url` + set header `Referer: stream.headers.Referer`

---

## Useful Endpoints

| Endpoint | Description |
|----------|-------------|
| `/search?q=` | Search movies / series |
| `/api/stream/{id}` | All qualities + **proxy_url** |
| `/api/stream/{id}?se=1&ep=2` | Series episode |
| `/api/stream/{id}/captions` | Subtitles |
| `/detail/{id}` | Full metadata |
| `/episodes/{id}` | Season list |
| `/proxy?url=...&referer=...` | Video proxy |
| `/health` | Health check (for uptime monitors) |
| `/` | Web dashboard (testing) |

---

## Local Test

```bash
pip install -r requirements.txt
python main.py
# → http://127.0.0.1:8000
```

CLI (optional):
```bash
python cli.py
```

---

## Important Notes for Free Render

- Free instances sleep after ~15 min inactivity → first request may take 30-50 sec
- Video proxy works, but very long videos may hit free-tier limits
- For production apps, paid instance ($7) is more stable
- MovieBox is geo-sensitive → works best when Render region can reach the upstream (or use India VPN on server if needed)

---

## Files

- `api.py` – main FastAPI app
- `main.py` – entrypoint (uses $PORT)
- `Procfile` – Render / Heroku
- `render.yaml` – Blueprint
- `cli.py` – optional local CLI
- `requirements.txt`

MIT License

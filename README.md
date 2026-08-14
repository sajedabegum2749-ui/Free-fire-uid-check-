# 🎮 Free Fire UID API

Get player info by UID for **all regions** with special BD (Bangladesh) support.

## Supported Regions
`IND` `SG` `BR` `BD` `ID` `TH` `VN` `TW` `US` `ME` `PK` `RU` `CIS`

---

## Endpoints

### `GET /` — API info & endpoint list

### `GET /regions` — List all regions

### `GET /player/info` — Full player profile
| Param | Required | Default | Description |
|-------|----------|---------|-------------|
| `uid` | ✅ | — | Player UID |
| `region` | ❌ | `BD` | Server region |
| `gallery` | ❌ | `false` | Include gallery info |
| `blacklist` | ❌ | `false` | Include blacklist info |
| `spark` | ❌ | `false` | Include spark info |

**Example:**
```
GET /player/info?uid=123456789&region=BD
GET /player/info?uid=123456789&region=IND&gallery=true
```

### `GET /player/stats/br` — Battle Royale stats
| Param | Required | Default | Description |
|-------|----------|---------|-------------|
| `uid` | ✅ | — | Player UID |
| `region` | ❌ | `BD` | Server region |
| `mode` | ❌ | `career` | `career` / `normal` / `ranked` |

**Example:**
```
GET /player/stats/br?uid=123456789&region=BD&mode=ranked
```

### `GET /player/stats/cs` — Clash Squad stats
Same params as `/player/stats/br`

### `GET /player/search` — Search players by name
| Param | Required | Default | Description |
|-------|----------|---------|-------------|
| `keyword` | ✅ | — | Min 3 chars |
| `region` | ❌ | `BD` | Server region |

**Example:**
```
GET /player/search?keyword=ProSniper&region=BD
```

---

## Response Format

```json
{
  "success": true,
  "region": "BD",
  "uid": 123456789,
  "data": { ... }
}
```

---

## Deploy on Render

1. Push this folder to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT`
6. Done ✅

## Deploy on Vercel

```bash
npm i -g vercel
vercel deploy
```

---

## Local Run

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

"""
Free Fire UID Info API
Supports all regions: IND, SG, BR, BD, ID, TH, VN, TW, US, ME, PK, RU, CIS
Special focus: BD (Bangladesh) region
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from Utilities.utils import load_accounts
from Api.auth import authenticate
from Api.player import (
    get_player_info,
    get_player_br_stats,
    get_player_cs_stats,
    search_by_name,
)

# ── App Setup ─────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

ACCOUNTS = load_accounts()
REGIONS   = list(ACCOUNTS.keys())

BR_MATCHMODE  = {"career": 0, "normal": 1, "ranked": 2}
CS_MATCHMODE  = {"career": 0, "normal": 1, "ranked": 6}


# ── Helpers ───────────────────────────────────────────────────────────────────
def error(msg: str, code: int = 400):
    return jsonify({"success": False, "error": msg}), code


def validate_uid(uid_str: str):
    if not uid_str:
        return None, "uid is required"
    if not uid_str.isdigit():
        return None, "uid must be numeric"
    uid = int(uid_str)
    if uid <= 0:
        return None, "uid must be a positive integer"
    return uid, None


def validate_region(region: str):
    region = region.upper()
    if region not in REGIONS:
        return None, f"Invalid region '{region}'. Available: {REGIONS}"
    return region, None


def do_auth(region: str):
    session = authenticate(ACCOUNTS, region)
    if not session or 'token' not in session or 'serverUrl' not in session:
        return None, None, "Authentication failed for region " + region
    return session['token'], session['serverUrl'], None


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "Free Fire UID API",
        "version": "1.0.0",
        "regions": REGIONS,
        "endpoints": {
            "GET /player/info":     "?uid=&region= — full profile",
            "GET /player/stats/br": "?uid=&region=&mode= — BR stats (mode: career|normal|ranked)",
            "GET /player/stats/cs": "?uid=&region=&mode= — CS stats (mode: career|normal|ranked)",
            "GET /player/search":   "?keyword=&region= — search by name",
            "GET /regions":         "list all supported regions",
        }
    })


@app.route("/regions", methods=["GET"])
def list_regions():
    return jsonify({"success": True, "regions": REGIONS, "total": len(REGIONS)})


# ── /player/info ─────────────────────────────────────────────────────────────
@app.route("/player/info", methods=["GET"])
def player_info():
    uid_str = request.args.get("uid", "").strip()
    region  = request.args.get("region", "BD").strip()

    uid, err = validate_uid(uid_str)
    if err:
        return error(err)

    region, err = validate_region(region)
    if err:
        return error(err)

    need_gallery   = request.args.get("gallery",   "false").lower() == "true"
    need_blacklist = request.args.get("blacklist",  "false").lower() == "true"
    need_spark     = request.args.get("spark",      "false").lower() == "true"

    token, server_url, err = do_auth(region)
    if err:
        return error(err, 502)

    data = get_player_info(server_url, token, uid, need_gallery, need_blacklist, need_spark)
    if not data:
        return error(f"No data found for UID {uid} in region {region}", 404)

    return app.response_class(
        response=json.dumps({"success": True, "region": region, "uid": uid, "data": data},
                            ensure_ascii=False, indent=2),
        status=200,
        mimetype="application/json"
    )


# ── /player/stats/br ─────────────────────────────────────────────────────────
@app.route("/player/stats/br", methods=["GET"])
def player_br_stats():
    uid_str = request.args.get("uid", "").strip()
    region  = request.args.get("region", "BD").strip()
    mode    = request.args.get("mode", "career").strip().lower()

    uid, err = validate_uid(uid_str)
    if err:
        return error(err)

    region, err = validate_region(region)
    if err:
        return error(err)

    if mode not in BR_MATCHMODE:
        return error(f"Invalid mode '{mode}'. Use: career, normal, ranked")

    token, server_url, err = do_auth(region)
    if err:
        return error(err, 502)

    data = get_player_br_stats(server_url, token, uid, BR_MATCHMODE[mode])
    if not data:
        return error(f"No BR stats found for UID {uid}", 404)

    return app.response_class(
        response=json.dumps({"success": True, "region": region, "uid": uid,
                             "mode": mode, "data": data},
                            ensure_ascii=False, indent=2),
        status=200,
        mimetype="application/json"
    )


# ── /player/stats/cs ─────────────────────────────────────────────────────────
@app.route("/player/stats/cs", methods=["GET"])
def player_cs_stats():
    uid_str = request.args.get("uid", "").strip()
    region  = request.args.get("region", "BD").strip()
    mode    = request.args.get("mode", "career").strip().lower()

    uid, err = validate_uid(uid_str)
    if err:
        return error(err)

    region, err = validate_region(region)
    if err:
        return error(err)

    if mode not in CS_MATCHMODE:
        return error(f"Invalid mode '{mode}'. Use: career, normal, ranked")

    token, server_url, err = do_auth(region)
    if err:
        return error(err, 502)

    data = get_player_cs_stats(server_url, token, uid, CS_MATCHMODE[mode])
    if not data:
        return error(f"No CS stats found for UID {uid}", 404)

    return app.response_class(
        response=json.dumps({"success": True, "region": region, "uid": uid,
                             "mode": mode, "data": data},
                            ensure_ascii=False, indent=2),
        status=200,
        mimetype="application/json"
    )


# ── /player/search ───────────────────────────────────────────────────────────
@app.route("/player/search", methods=["GET"])
def player_search():
    keyword = request.args.get("keyword", "").strip()
    region  = request.args.get("region", "BD").strip()

    if not keyword:
        return error("keyword is required")
    if len(keyword) < 3:
        return error("keyword must be at least 3 characters")

    region, err = validate_region(region)
    if err:
        return error(err)

    token, server_url, err = do_auth(region)
    if err:
        return error(err, 502)

    data = search_by_name(server_url, token, keyword)
    if not data:
        return error("Search failed or no results found", 404)

    return app.response_class(
        response=json.dumps({"success": True, "region": region,
                             "keyword": keyword, "data": data},
                            ensure_ascii=False, indent=2),
        status=200,
        mimetype="application/json"
    )


# ── Error handlers ────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Route not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)

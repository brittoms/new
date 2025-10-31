#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_file
import requests
import os

app = Flask(__name__)

CLUBHOUSE_API = "https://www.clubhouseapi.com/api"

def ch_request(endpoint, token, data=None):
    headers = {
        "Authorization": token,
        "CH-Languages": "en",
        "User-Agent": "clubhouse/2024 (iPhone; iOS 17.0; Scale/3.00)"
    }
    url = f"{CLUBHOUSE_API}/{endpoint}"
    r = requests.post(url, headers=headers, json=data or {})
    try:
        return r.json()
    except:
        return {"error": "Invalid response"}

@app.route("/me", methods=["POST"])
def get_me():
    token = request.json.get("token")
    return jsonify(ch_request("me", token))

@app.route("/update", methods=["POST"])
def update():
    token = request.json.get("token")
    action = request.json.get("action")
    value = request.json.get("value")

    endpoints = {
        "update_name": "update_name",
        "update_username": "update_username",
        "update_alias": "update_displayname",
        "update_bio": "update_bio",
        "update_email": "update_email",
        "update_phone": "update_phone_number",
        "remove_alias": "remove_displayname",
        "remove_bio": "remove_bio"
    }

    if action not in endpoints:
        return jsonify({"error": "Invalid action"})

    res = ch_request(endpoints[action], token, {"value": value})
    return jsonify(res)

@app.route("/profile_info", methods=["POST"])
def profile_info():
    username = request.json.get("username")
    token = "ac00e6e71f99fde1b7780229f7022000e493605d"  # your internal token
    data = {"username": username}
    res = ch_request("get_profile", token, data)
    return jsonify(res)

@app.route("/download_picture", methods=["POST"])
def download_picture():
    username = request.json.get("username")
    token = "ac00e6e71f99fde1b7780229f7022000e493605d"
    res = ch_request("get_profile", token, {"username": username})
    pic_url = res.get("user_profile", {}).get("photo_url")
    if not pic_url:
        return jsonify({"error": "No profile picture found"})

    img = requests.get(pic_url)
    file_path = f"/tmp/{username}.jpg"
    with open(file_path, "wb") as f:
        f.write(img.content)
    return send_file(file_path, as_attachment=True, download_name=f"{username}.jpg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

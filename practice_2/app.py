from flask import Flask, render_template, request
import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("Missing environment variable: API_KEY")
    sys.exit(1)


@app.route("/", methods=["GET"])
def index():
    search_query = request.args.get("search")
    items = []
    error = None

    if search_query:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": search_query}

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "organic" in data:
                items = data["organic"]
            else:
                error = "No results found."

        except requests.exceptions.HTTPError as e:
            error = f"HTTP error: {e}"
        except requests.exceptions.RequestException as e:
            error = f"An unexpected error occurred: {e}"

    return render_template("index.html", items=items, error=error)


if __name__ == "__main__":
    app.run(debug=True, port=3000)

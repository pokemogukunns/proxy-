import os
import requests
import shutil
from flask import Flask, request, render_template_string
from urllib.parse import urljoin

app = Flask(__name__)

# ThingProxy URL
PROXY_URL = "https://thingproxy.freeboard.io/fetch/"

@app.route("/home", methods=["GET"])
def home():
    html_form = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Proxy URL Input</title>
    </head>
    <body>
      <h1>URLを入力してください</h1>
      <form action="/proxy" method="get">
        <label for="url">URL:</label>
        <input type="text" id="url" name="url" placeholder="https://example.com" required>
        <button type="submit">送信</button>
      </form>
    </body>
    </html>
    """
    return render_template_string(html_form)

@app.route("/proxy", methods=["GET"])
def proxy():
    target_url = request.args.get("url")
    if not target_url:
        return "<h1>エラー: URLパラメータが必要です。</h1>", 400

    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        return "<h1>エラー: URLはhttp://またはhttps://で始まる必要があります。</h1>", 400

    # ThingProxy URLに変換
    proxy_url = PROXY_URL + target_url

    # curl コマンドを生成
    curl_command = f"curl -X GET {proxy_url}"

    # 実際にリソースを取得して表示
    try:
        response = requests.get(proxy_url)
        response.raise_for_status()

        # 取得したHTMLを表示
        return f"""
        <h2>curl コマンド:</h2>
        <pre>{curl_command}</pre>
        <h2>取得したリソース:</h2>
        <pre>{response.text}</pre>
        """

    except Exception as e:
        return f"<h1>エラーが発生しました。</h1><p>{str(e)}</p>", 500

if __name__ == "__main__":
    app.run(debug=True)


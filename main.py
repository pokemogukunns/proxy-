import subprocess
from flask import Flask, request, jsonify, render_template_string, escape

app = Flask(__name__)

# /home でテキストボックスを表示
@app.route("/home", methods=["GET"])
def home():
    html = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>URLプロキシ</title>
    </head>
    <body>
        <h1>URLからコードを取得</h1>
        <form method="get" action="./proxy">
            <label for="url">取得するURLを入力してください:</label><br>
            <input type="text" id="url" name="url" placeholder="https://example.com" style="width: 80%;"><br><br>
            <button type="submit">取得</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)

# /proxy で指定されたURLの内容を取得
@app.route("/proxy", methods=["GET"])
def proxy():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # curlコマンドを実行
        command = ["curl", "-s", url]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # HTMLをエスケープして安全に表示
        escaped_content = escape(result.stdout)
        html = f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <title>取得結果</title>
        </head>
        <body>
            <h1>取得したコード</h1>
            <pre style="background-color: #f4f4f4; padding: 10px; border: 1px solid #ddd;">{escaped_content}</pre>
            <a href="/home">戻る</a>
        </body>
        </html>
        """
        return html
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to fetch URL. {e}"}), 500

# / にアクセスされた場合は404エラーを返す
@app.route("/", methods=["GET"])
def root():
    return "404 Not Found", 404

if __name__ == "__main__":
    app.run(debug=True)

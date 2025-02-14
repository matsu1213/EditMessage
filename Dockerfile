# ベースイメージとしてPython 3.11を使用
FROM python:3.11

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# Botのコードをコピー
COPY . .

# コンテナ起動時にBotを実行
CMD ["python", "bot.py"]
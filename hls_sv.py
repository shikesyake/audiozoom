#!/usr/bin/env python3
# キャッシュ無効のHTTPサーバー（CORS対応、ストリーミング対応）

from http.server import SimpleHTTPRequestHandler, HTTPServer
import sys
import os
from datetime import datetime
from urllib.parse import unquote

from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
import mysql.connector
import pymysql
import pymysql.cursors
import os

app = Flask(
    __name__,
    template_folder='client',
    static_folder='client',
    static_url_path=''
)
app.secret_key = 'your_secret_key_here' # 本番環境では安全なキーに変更してください

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mysql'
    )

def getConnection():
    """PyMySQLでの接続 - Flask入門編3用"""
    return pymysql.connect(
        host="localhost",
        db="user",
        user="root",
        password="",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    connection = getConnection()
    sql = "SELECT id, media_name, relative_path, media_type FROM `broadcast_media` WHERE is_active = 1 ORDER BY id"
    cursor = connection.cursor()
    cursor.execute(sql)
    media_list = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', media_list=media_list)

@app.route('/admin/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user and check_password_hash(user['password'], password):
        session['logged_in'] = True
        session['username'] = user['username']
        return redirect(url_for('admin'))

    flash('ユーザー名またはパスワードが正しくありません。')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('admin'))
@app.route('/livevid')
def livevid():
    return render_template('livevid.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        media_ip = request.form.get('media_ip', '').strip()
        media_path = request.form.get('media_path', '').strip()
        media_type = request.form.get('media_type', '').strip()
        if media_ip and media_path:
            connection = getConnection()
            sql = "INSERT INTO `broadcast_media` (stream_id, media_name, media_type, relative_path, file_format, is_active) VALUES (NULL, %s, %s, %s, %s, 1)"
            cursor = connection.cursor()
            media_name = f"{media_ip} - {media_path}"
            file_format = media_type if media_type in ('hls', 'video', 'audio') else 'unknown'
            cursor.execute(sql, (media_name, media_type, media_path, file_format))
            connection.commit()
            cursor.close()
            connection.close()
            flash('メディアソースを登録しました。')
        else:
            flash('IPアドレス/URL とメディアパスを入力してください。')
        return redirect(url_for('admin'))
    
    connection = getConnection()
    sql = "SELECT id, media_name, media_type, relative_path, file_format FROM `broadcast_media` WHERE is_active = 1 ORDER BY id DESC"
    cursor = connection.cursor()
    cursor.execute(sql)
    media_list = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('admin.html', media_list=media_list)

@app.route('/admin/media/update/<int:media_id>', methods=['POST'])
def update_media(media_id):
    media_name = request.form.get('media_name', '').strip()
    relative_path = request.form.get('relative_path', '').strip()
    file_format = request.form.get('file_format', '').strip()
    if media_name and relative_path:
        connection = getConnection()
        sql = "UPDATE `broadcast_media` SET media_name = %s, relative_path = %s, file_format = %s WHERE id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (media_name, relative_path, file_format, media_id))
        connection.commit()
        cursor.close()
        connection.close()
        flash('メディアを更新しました。')
    else:
        flash('メディア名とパスは必須です。')
    return redirect(url_for('admin'))

@app.route('/admin/media/delete/<int:media_id>', methods=['POST'])
def delete_media(media_id):
    connection = getConnection()
    sql = "DELETE FROM `broadcast_media` WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(sql, (media_id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash('メディアを削除しました。')
    return redirect(url_for('admin'))

@app.route('/live/video/<path:filename>')
def video(filename):
    return send_from_directory('live/video', filename)

@app.route('/live/audio/<path:filename>')
def audio(filename):
    return send_from_directory('live/audio', filename)

@app.route('/live/<path:filename>')
def live(filename):
    return send_from_directory('live', filename)

# ============ Flask入門編3: データベース学習用エンドポイント ============

@app.route('/users/list')
@app.route('/users_bak')
@app.route('/users')
def users():
    """ユーザー一覧を表示（LEFT JOINでjobsテーブルと結合）"""
    connection = getConnection()
    
    # LEFT JOINを使用してuserとjobsを結合
    # DictCursorを使うため、カラム名の重複を避ける
    sql = """
        SELECT 
            `user`.id as user_id,
            `user`.name as user_name,
            `user`.level as user_level,
            jobs.job_name as job_name
        FROM `user`
        LEFT JOIN jobs ON `user`.job_id = jobs.id
        ORDER BY `user`.id
    """
    
    cursor = connection.cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template("users_bak.html", users=users)

@app.route('/users/search')
def search_users():
    """レベル範囲でユーザーを検索（GETパラメータ使用）"""
    min_level = request.args.get("min_level", 0)
    max_level = request.args.get("max_level", 100)
    
    connection = getConnection()
    
    # プレースホルダを使用して安全にSQLを構築
    sql = """
        SELECT 
            `user`.id as user_id,
            `user`.name as user_name,
            `user`.level as user_level,
            jobs.job_name as job_name
        FROM `user`
        LEFT JOIN jobs ON `user`.job_id = jobs.id
        WHERE `user`.level >= %s AND `user`.level <= %s
        ORDER BY `user`.id
    """
    
    cursor = connection.cursor()
    cursor.execute(sql, (min_level, max_level))
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template("users_search.html", users=users, 
                          min_level=min_level, max_level=max_level)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    """ユーザーを追加"""
    if request.method == 'POST':
        # POSTパラメータを受け取る
        name = request.form["name"]
        level = request.form["level"]
        job_id = request.form.get("job_id")
        
        connection = getConnection()
        
        # プレースホルダを使用してINSERT
        if job_id and job_id != "":
            sql = "INSERT INTO `user` (name, level, job_id) VALUES (%s, %s, %s)"
            cursor = connection.cursor()
            cursor.execute(sql, (name, level, job_id))
        else:
            sql = "INSERT INTO `user` (name, level) VALUES (%s, %s)"
            cursor = connection.cursor()
            cursor.execute(sql, (name, level))
        
        # トランザクションをコミット
        connection.commit()
        cursor.close()
        connection.close()
        
        return redirect(url_for('users'))
    
    else:
        # GETリクエスト: フォームを表示するため職業リストを取得
        connection = getConnection()
        sql = "SELECT * FROM jobs ORDER BY id"
        cursor = connection.cursor()
        cursor.execute(sql)
        jobs = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return render_template("users_add.html", jobs=jobs)

@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """ユーザーを削除"""
    connection = getConnection()
    sql = "DELETE FROM `user` WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(sql, (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('users'))

@app.route('/result', methods=['POST'])
def result():
    """シンプルなフォーム送信結果（教材サンプル）"""
    name = request.form["name"]
    level = request.form["level"]
    
    connection = getConnection()
    sql = "INSERT INTO `user` (name, level) VALUES (%s, %s)"
    cursor = connection.cursor()
    cursor.execute(sql, (name, level))
    connection.commit()
    cursor.close()
    connection.close()
    
    return name + level


class NoCacheHTTPRequestHandler(SimpleHTTPRequestHandler):
    
    # リクエストログを簡潔にする
    request_count = {'m3u8': 0, 'ts': 0, 'other': 0}
    
    # def translate_path(self, path):
    #     """パスを実際のファイルパスに変換"""
    #     # クエリパラメータを除去
    #     path = path.split('?', 1)[0]
    #     path = path.split('#', 1)[0]
    #     path = unquote(path)
        
    #     # ルーティング処理
    #     if path == '/':
    #         path = '/client/index.html'
    #     elif path == '/admin':
    #         path = '/client/admin.html'
    #     elif path.startswith('/js/') or path.startswith('/css/') or path.endswith('.css'):
    #         # /js/や/css/で始まるパス、.cssで終わるパスを/client/配下に変換
    #         if not path.startswith('/client/'):
    #             path = '/client' + path
        
    #     # 絶対パスに変換
    #     words = path.split('/')
    #     words = filter(None, words)
    #     path = os.getcwd()
    #     for word in words:
    #         if os.path.dirname(word) or word in (os.curdir, os.pardir):
    #             continue
    #         path = os.path.join(path, word)
    #     return path
    
    def end_headers(self):
        # キャッシュを無効にするヘッダー
        self.send_header('Cache-Control', 'no-store, no-cache')
        
        # CORS対応ヘッダー
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'origin, range, hdntl, hdnts')
        self.send_header('Access-Control-Expose-Headers', 'x-cdn, access-control-allow-origin, x-amz-meta-hash, date')
        
        # Range requestsのサポート
        self.send_header('Accept-Ranges', 'bytes')
        
        super().end_headers()
    
    def do_OPTIONS(self):
        """OPTIONSメソッドの処理（preflight request対応）"""
        self.send_response(200)
        self.end_headers()
    
    def guess_type(self, path):
        """MIMEタイプの推測（m3u8とtsファイルのサポート追加）"""
        mimetype = super().guess_type(path)
        
        # HLS関連ファイルのMIMEタイプを明示的に設定
        if path.endswith('.m3u8'): # type: ignore
            return 'application/vnd.apple.mpegurl'
        elif path.endswith('.ts'): # type: ignore
            return 'video/mp2t'
        
        return mimetype
    
    def log_message(self, format, *args):
        """リクエストログをカスタマイズ（HLSストリーミングのログを簡潔に）"""
        path = args[0].split()[0] if args else ''
        
        # リクエストタイプをカウント
        if '.m3u8' in path:
            self.request_count['m3u8'] += 1
            # m3u8のリクエストは10回に1回だけログ出力
            if self.request_count['m3u8'] % 10 == 1:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] m3u8リクエスト: {self.request_count['m3u8']}回目")
        elif '.ts' in path:
            self.request_count['ts'] += 1
            # tsファイルは最初と以降5回ごとにログ出力
            if self.request_count['ts'] <= 5 or self.request_count['ts'] % 5 == 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] セグメント {path.split('/')[-1]}: {self.request_count['ts']}個目")
        else:
            self.request_count['other'] += 1
            # その他のファイルは通常通りログ出力
            super().log_message(format, *args)

def run(server_class=HTTPServer, handler_class=NoCacheHTTPRequestHandler, port=8080):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f'サーバーを起動: http://0.0.0.0:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run(port=port)

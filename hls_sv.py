#!/usr/bin/env python3
# キャッシュ無効のHTTPサーバー（CORS対応、ストリーミング対応）

from http.server import SimpleHTTPRequestHandler, HTTPServer
import sys
import os
from datetime import datetime
from urllib.parse import unquote

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

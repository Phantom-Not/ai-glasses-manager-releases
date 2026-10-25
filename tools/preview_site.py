"""Serve the GitHub Pages project path locally, without dependencies."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
BASE=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))['base_url']
PREFIX='/'+'/'.join(BASE.split('/')[3:])
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT/'docs'),**kwargs)
    def do_GET(self):
        if self.path=='/':
            self.send_response(302);self.send_header('Location',PREFIX+'/');self.end_headers();return
        if self.path==PREFIX:self.path=PREFIX+'/'
        if self.path.startswith(PREFIX+'/'):self.path=self.path[len(PREFIX):]
        super().do_GET()
if __name__=='__main__':
    print('Local: http://127.0.0.1:4173'+PREFIX+'/',flush=True)
    ThreadingHTTPServer(('127.0.0.1',4173),Handler).serve_forever()

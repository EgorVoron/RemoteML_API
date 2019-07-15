from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from sql_parser import PostParser, GetParser
from urllib import parse


class Server(BaseHTTPRequestHandler):
    def get_message(self):
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        return message

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_head(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        self.send_response(200)
        if "?" in self.path:
            arguments = dict(parse.parse_qsl(self.path.split("?")[1], True))
            parser = GetParser(arguments)
            self.wfile.write(json.dumps(parser.run()).encode())

    def do_POST(self):
        self._set_headers()
        message = self.get_message()
        sql_parser = PostParser(self.headers)
        sql_parser.delete()
        sql_parser.save_model_info(message)
        self.wfile.write(json.dumps({'result': 'success'}).encode())


def run_server(server_class=HTTPServer, handler_class=Server, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server(port=5000)

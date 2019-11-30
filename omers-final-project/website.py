import functools
import http.server
import re


class Website:
    def __init__(self):
        self.urls = {}

    def route(self, path):
        def decorator(f):
            self.urls[f'^{path}$'] = f
            @functools.wraps(f)
            def wrappper(*args, **kwargs):
                f(*args, **kwargs)
            return wrappper
        return decorator

    def run(self, address):
        class GetHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(handler_self):
                matched_pattern = ''
                params = []
                for url_pattern in self.urls:
                    search_res = re.search(url_pattern, handler_self.path)
                    if search_res:
                        matched_pattern = url_pattern
                        match_group = search_res.groups()
                        params = match_group
                if matched_pattern:
                    view = self.urls[matched_pattern]
                    status, data = view(*params)
                    handler_self.send_response(status)
                    handler_self.send_header("Content-type", "text/html")
                    handler_self.end_headers()
                    handler_self.wfile.write(bytes(data, encoding='ASCII'))
                else:
                    handler_self.send_response(404)
                    handler_self.end_headers()

        http_server = http.server.HTTPServer(address, GetHandler)
        http_server.serve_forever()

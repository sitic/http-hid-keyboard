import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer


def RequestHandlerFactory(actions, auth_token=None):
    """
    Factory for creating request handlers for the HTTP server.

    :param actions: Dictionary of actions to be executed when a request is received.
    :param auth_token: Authorization token to be used to authenticate requests (`Authorization` header value).
    :return: Request handler class."""

    class RequestHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.logger = logging.getLogger("WebServer")
            self.auth_token = auth_token
            self.actions = actions
            super().__init__(*args, **kwargs)

        def do_POST(self):
            if self.auth_token and self.headers.get("Authorization") != self.auth_token:
                self._send_response({"error": "Invalid authorization"}, code=401)
                return

            try:
                length = int(self.headers["content-length"])
                message = json.loads(self.rfile.read(length))
            except Exception as e:
                self._send_response({"error": "Invalid JSON"}, code=400)
                return

            action = message.get("action")
            if action in self.actions:
                try:
                    self.actions[action]()
                    self._send_response({"status": "success"})
                except BrokenPipeError as e:
                    msg = {
                        "status": "error",
                        "error": "Keypress failed",
                        "details": "Keyboard not connected, verify USB connection",
                    }
                    self._send_response(msg, code=500)
                    return
                except Exception as e:
                    self.logger.exception(e)
                    msg = {
                        "status": "error",
                        "error": "Keypress failed",
                        "details": f"{e}",
                    }
                    self._send_response(msg, code=500)
                    return
            else:
                self.logger.warning(f"Invalid action: {action}")
                self._send_response({"error": "Invalid action"}, code=400)
                return

        def _send_response(self, message, code=200):
            self.send_response(code)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(message).encode("utf8"))

            if code >= 400:
                self.logger.error(f"Error {code}: {message}")

        def log_request(self, code="-", size="-"):
            self.logger.debug(
                f'{self.address_string()} - "{self.requestline}" {code} {size}'
            )

        def log_error(self, format, *args):
            self.logger.error(format % args)

        def log_message(self, format, *args):
            self.logger.info(format % args)

    return RequestHandler


class WebServer:
    def __init__(self, actions, addr="", port=8222, auth_token=""):
        self.logger = logging.getLogger("WebServer")
        server_address = (addr, port)
        request_handler = RequestHandlerFactory(actions, auth_token=auth_token)
        self.server = HTTPServer(server_address, request_handler)

    def run(self):
        self.logger.info(f"Starting http server on port {self.server.server_port}")
        self.server.serve_forever()

    def stop(self):
        self.logger.info("http server shutting down")
        self.server.shutdown()

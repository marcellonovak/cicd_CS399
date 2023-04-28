"""
Super Simple HTTP Server in Python .. not for production just for learning and fun
Author: Wolf Paulus (https://wolfpaulus.com)
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import asctime
from main import is_prime
import json

hostName = "0.0.0.0"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/health":
            status, content = 200, "OK"

        # API magic!
        elif self.path == "/api/is_prime":
            # Set the response code to 200 (OK)
            self.send_response(200)

            # Set the response headers
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            # Get the number from the header
            number = int(self.headers['X-Number'])

            # Check if the number is prime
            result = is_prime(number)

            # Create the response (dictionary and json)
            response = {'number': number, 'is_prime': result}
            self.wfile.write(json.dumps(response).encode())

        # Okay resuming the code I basically stole from Canvas...
        elif self.path == "/" or self.path.startswith("/?number="):
            status = 200
            number = self.path.split("=")[1] if self.path.startswith("/?number=") else ""
            result = f"{number} is {'prime' if is_prime(int(number)) else 'not prime'}." if number.isnumeric() else ""
            with open('./src/response.html', 'r') as f:
                # read the html template and fill in the parameters: path, time and result
                content = f.read().format(path=self.path, time=asctime(), result=result)
        else:
            status, content = 404, "Not Found"
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")

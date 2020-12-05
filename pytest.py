#!/usr/bin/env python3

"""
Very simple HTTP server in python (Updated for Python 3.7)

Usage:

    ./dummy-web-server.py -h
    ./dummy-web-server.py -l localhost -p 8000

Send a GET request:

    curl http://localhost:8000

Send a HEAD request:

    curl -I http://localhost:8000

Send a POST request:

    curl -d "foo=bar&bin=baz" http://localhost:8000

"""
import argparse
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

"""
What is a Note:
* creation date
* type: (Note, TODO, calendar)
* text
* done
* start, end date

"""

class S(BaseHTTPRequestHandler):
    def load_notes(self):
        with open('notes.json') as file_handle:
            return json.load(file_handle)

    def store_notes(self, notes):
        with open('notes.json', 'w') as file_handle:
            file_handle.write(json.dumps(notes, indent=2))
            file_handle.write('\n')

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.

        """
        content = f"<html><body>{message}</body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        notes = self.load_notes()

        js_script = """
        <script>
          function submit_new_entry() {
            text = document.getElementById("new_text");
            console.log(text);
          }
          
          function myFunction() {
              document.getElementById("myForm").submit();
            }
        </script>
        
        """

        response = js_script + """<table><tr>
                        <th>Type</th>
                        <th>text</th>
                      </tr>"""

        for note in notes:
            response = response + f"""
              <tr>
                <td>{note['type']}</td>
                <td>{note['text']}</td>
              </tr>
              """

        # new button
        response += f"""
          <tr>
            <td><button type="button" onclick="submit_new_entry()">New</button></td>
            <td>
                <input type="text" id="new_text" name="new_text"><br><br>
            </td>
          </tr>
        """

        response += """
                <form id="myForm" action="/action_page.php">
          First name: <input type="text" name="fname"><br>
          Last name: <input type="text" name="lname"><br><br>
          <input type="button" onclick="myFunction()" value="Submit form">
        </form>
        
        """

        self.wfile.write(self._html(response))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(self._html("POST!"))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)

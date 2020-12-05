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
import sys

from http.server import HTTPServer, BaseHTTPRequestHandler



"""
What is a Note:
* creation date
* type: (Note, TODO, calendar)
* text
* done
* start, end date

"""


class NoteTaking:
    def load_notes(self):
        with open('notes.json') as file_handle:
            return json.load(file_handle)

    def store_notes(self, notes):
        with open('notes.json', 'w') as file_handle:
            file_handle.write(json.dumps(notes, indent=2))
            file_handle.write('\n')

    def list_all_notes(self):
        notes = self.load_notes()
        for note in notes:
            print(note)


class S(BaseHTTPRequestHandler, NoteTaking):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = f"<html><body>{message}</body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        notes = self.load_notes()

        js_script = """
        <script>
          function submit_new_entry() {
            form = document.getElementById("new_entry")
            console.log(form);
            form.submit();
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
        <form id="new_entry" action="/new_entry">
          <tr>
            <td><button type="button" onclick="submit_new_entry()">New</button></td>
            <td>
                <input type="text" id="new_text" name="new_text"><br><br>
            </td>
          </tr>
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

    parser = argparse.ArgumentParser(description="A notetaking server/client")
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
    parser.add_argument(
        "-c",
        "--client",
        action="store_const",
        dest='client',
        default=False,
        const=True,
        help="Use as a commandline client",
    )
    args = parser.parse_args()

    if args.client:
        CLI_Client().run_as_cli()
    else:
        run(addr=args.listen, port=args.port)

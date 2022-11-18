from cgi import parse_header, parse_multipart
from random import choice
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from hashlib import sha256
from datetime import datetime


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    cats = [
        "images/cat1.png",
        "images/cat2.png",
        "images/unrelated1.png",
        "images/unrelated2.png",
        "images/critical1.png",
        "images/critical2.png",
    ]

    def do_GET(self):

        if self.path.startswith("/landing"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(open("htmls/landing.html", "rb").read())

        elif self.path.startswith("/presurvey"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(open("htmls/presurvey.html", "rb").read())

        elif self.path.startswith("/cats-"):
            self.send_response(200)
            self.end_headers()

            pid = self.path.split("-")[-1]
            html_page = open("htmls/show_cats.html", "r").read().replace("PID", pid)
            self.wfile.write(html_page.encode())

        elif self.path.startswith("/images"):
            self.send_response(200)
            self.end_headers()

            file_name = self.path[1:]
            if os.path.isfile(file_name):
                self.wfile.write(open(file_name, "rb").read())

        elif self.path.startswith("/recall-"):
            self.send_response(200)
            self.end_headers()

            pid = self.path.split("-")[-1]
            html_page = open("htmls/recall.html", "r").read().replace("PID", pid)
            self.wfile.write(html_page.encode())

        elif self.path.startswith("/youtube-"):
            self.send_response(200)
            self.end_headers()

            pid = self.path.split("-")[-1]
            html_page = open("htmls/youtube.html", "r").read().replace("PID", pid)
            self.wfile.write(html_page.encode())

        elif self.path.startswith("/show-000000-"):
            self.send_response(200)
            self.end_headers()

            pid = self.path.split("-")[-1]
            index = choice(list(range(len(self.cats))))
            bits = "000000"
            bits = "".join(b if i != index else "1" for i, b in enumerate(bits))
            next_url = "/show-{}-{}".format(bits, pid)
            html_page = (
                open("htmls/show.html", "r")
                .read()
                .replace("NAME", self.cats[index][7:-4])
                .replace("IMAGE", self.cats[index])
                .replace("NEXT", next_url)
            )
            self.wfile.write(html_page.encode())

        elif self.path.startswith("/favicon"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(open("images/favicon.ico", "rb").read())

        else:
            self.send_response(400)
            self.end_headers()

    def do_POST(self):

        if self.path.startswith("/submit_background"):
            self.send_response(200)
            self.end_headers()

            results = {k.decode(): v[0].decode() for k, v in self.parse_POST().items()}
            pid = sha256(
                (str(datetime.now()) + str(self.connection.getpeername())).encode()
            ).hexdigest()[::2]

            html_page = (
                open("htmls/presurvey_submit.html", "r").read().replace("PID", pid)
            )
            self.wfile.write(html_page.encode())
            json.dump(results, open("surveys/{}.json".format(pid), "w"))

        elif self.path.startswith("/show-111111-"):
            self.send_response(200)
            self.end_headers()

            pid = self.path.split("-")[-1]
            html_page = open("htmls/final.html", "r").read().replace("PID", pid)
            self.wfile.write(html_page.encode())
            results = {k.decode(): v[0].decode() for k, v in self.parse_POST().items()}
            open("results/{}.json".format(pid), "a+").write(json.dumps(results))

        elif self.path.startswith("/show-"):
            self.send_response(200)
            self.end_headers()

            _, bits, pid = self.path.split("-")
            index = choice([i for i, b in enumerate(bits) if b == "0"])
            bits = "".join(b if i != index else "1" for i, b in enumerate(bits))
            next_url = "/show-{}-{}".format(bits, pid)
            html_page = (
                open("htmls/show.html", "r")
                .read()
                .replace("NAME", self.cats[index][7:-4])
                .replace("IMAGE", self.cats[index])
                .replace("NEXT", next_url)
            )
            self.wfile.write(html_page.encode())

            results = {k.decode(): v[0].decode() for k, v in self.parse_POST().items()}
            open("results/{}.json".format(pid), "a+").write(json.dumps(results))

        elif self.path.startswith("/thanks-"):
            self.send_response(200)
            self.end_headers()

            pid = self.path.split("-")[-1]
            self.wfile.write(open("htmls/thanks.html", "rb").read())

            results = {k.decode(): v[0].decode() for k, v in self.parse_POST().items()}
            open("results/{}.json".format(pid), "a+").write(json.dumps(results))

        else:
            self.send_response(400)
            self.end_headers()

    def parse_POST(self):

        ctype, pdict = parse_header(self.headers["content-type"])
        if ctype == "multipart/form-data":
            return parse_multipart(self.rfile, pdict)
        elif ctype == "application/x-www-form-urlencoded":
            length = int(self.headers["content-length"])
            return parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            print("unsupported ctype: ", ctype)
            return {}


if __name__ == "__main__":
    httpd = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()

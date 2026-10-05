from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

USERNAME = "admin"
PASSWORD = "password123"


class Handler(BaseHTTPRequestHandler):

    def send_html(self, html, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def do_GET(self):
        if self.path == "/":
            self.send_html("""
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body {
            font-family: Arial;
            background: #f2f2f2;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .login {
            background: white;
            padding: 30px;
            width: 320px;
            border-radius: 10px;
            box-shadow: 0 5px 20px #aaa;
        }

        input {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 10px;
            background: #333;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>

<div class="login">
    <h2>Login</h2>

    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">

        <button type="submit">Login</button>
    </form>
</div>

</body>
</html>
""")

        elif self.path == "/dashboard":
            self.send_html("""
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body>
    <h1>Welcome to the Dashboard</h1>
    <p>You successfully logged in.</p>
    
</body>
</html>
""")

        else:
            self.send_html("404 Not Found", 404)

    def do_POST(self):
        if self.path == "/login":

            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length).decode()

            form = parse_qs(data)

            username = form.get("username", [""])[0]
            password = form.get("password", [""])[0]

           

            if username == USERNAME and password == PASSWORD:
                self.send_response(302)
                self.send_header("Location", "/dashboard")
                self.end_headers()
            else:
                self.send_html("""
                <h2>Login Failed</h2>
                <a href="/">Try again</a>
                """, 401)


server = HTTPServer(("127.0.0.1", 8080), Handler)


print("Open: http://127.0.0.1:8080")

server.serve_forever()
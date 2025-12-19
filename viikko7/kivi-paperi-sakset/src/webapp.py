# -*- coding: utf-8 -*-
"""
Simple WSGI web application for the kivi-paperi-sakset project.

This file provides a minimal web UI that reuses the project's existing
game logic: Tuomari, Tekoaly and TekoalyParannettu.

Endpoints:
- GET  /                 -> index page (choose mode, create a new game)
- POST /start            -> create a new game and redirect to /game/<id>
- GET  /game/<id>        -> show game state and form to submit moves
- POST /game/<id>/move   -> submit moves (for PvP both moves required, for PvAI only first)

When executed directly, the module starts a WSGI server on port 8000.
"""

import html
import os
import sys
from urllib.parse import parse_qs
from uuid import uuid4
from wsgiref.simple_server import make_server

# Ensure we can import local modules in the same src folder
_THIS_DIR = os.path.dirname(__file__)
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from tuomari import Tuomari

# In-memory games store. Structure:
# games[game_id] = {
#   'type': 'a'|'b'|'c',
#   'tuomari': Tuomari(),
#   'ai': None|Tekoaly|TekoalyParannettu,
#   'finished': bool
# }
games = {}


def _render_template(body: str, title: str = "Kivi-Paperi-Sakset") -> str:
    # Use a plain string template and replace placeholders to avoid f-string brace interpolation
    template = """<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{TITLE}</title>
  <style>
    :root {
      --bg: #f6f8fa;
      --card: #ffffff;
      --accent: #2b8ef6;
      --muted: #6b7280;
      --success: #16a34a;
      --danger: #ef4444;
      --shadow: 0 4px 12px rgba(16,24,40,0.08);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }
    html,body {
      height: 100%;
      margin: 0;
      background: linear-gradient(180deg, #eef2ff 0%, var(--bg) 100%);
      color: #0f172a;
    }
    .wrap {
      min-height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 32px;
      box-sizing: border-box;
    }
    .card {
      width: 100%;
      max-width: 820px;
      background: var(--card);
      border-radius: 12px;
      box-shadow: var(--shadow);
      padding: 24px;
      box-sizing: border-box;
    }
    header.app-header {
      display:flex;
      align-items:center;
      gap:16px;
      margin-bottom: 8px;
    }
    header.app-header h1 {
      margin: 0;
      font-size: 20px;
    }
    .lead { color: var(--muted); margin-bottom: 18px; }
    .controls { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:18px; }
    .btn {
      display:inline-block;
      padding:10px 14px;
      border-radius:8px;
      background:var(--accent);
      color:white;
      text-decoration:none;
      border:none;
      cursor:pointer;
      font-weight:600;
    }
    .btn.secondary {
      background:#eef2ff;
      color:var(--accent);
      border:1px solid rgba(43,142,246,0.12);
    }
    .score { font-family: monospace; background:#f8fafc; padding:10px; border-radius:8px; display:inline-block; }
    .winner { margin-top:12px; font-weight:700; }
    .winner.success { color: var(--success); }
    .winner.danger { color: var(--danger); }
    .form-row { display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
    label.inline { display:inline-flex; gap:8px; align-items:center; padding:6px 8px; border-radius:8px; background:#fbfdff; border:1px solid #eef2ff; }
    footer { margin-top:16px; color:var(--muted); font-size:13px; }
    @media (max-width:560px) {
      .card { padding:16px; }
      header.app-header h1 { font-size:18px; }
      .controls { gap:8px; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <header class="app-header">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false">
          <rect width="24" height="24" rx="6" fill="#eef2ff"/>
          <path d="M5 12h14M12 5v14" stroke="#2b8ef6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div>
          <h1>{TITLE}</h1>
          <div class="lead">Pelaa nopeasti: k = kivi, p = paperi, s = sakset. Muulla syötteellä peli loppuu.</div>
        </div>
      </header>
      {BODY}
      <footer>Kevyt web-rajapinta, pelit pidetään muistissa vain tämän prosessin aikana.</footer>
    </div>
  </div>
</body>
</html>"""
    # Replace placeholders with escaped title and provided body (body may contain HTML)
    return template.replace("{TITLE}", html.escape(title)).replace("{BODY}", body)


def index_page() -> str:
    # nicer action buttons and brief instructions
    body = """
<div>
  <p class="lead">Valitse pelityyppi ja aloita uusi peli:</p>

  <div class="controls">
    <form method="post" action="/start" style="margin:0;">
      <input type="hidden" name="type" value="a" />
      <button class="btn" type="submit">Ihminen vs Ihminen</button>
    </form>

    <form method="post" action="/start" style="margin:0;">
      <input type="hidden" name="type" value="b" />
      <button class="btn secondary" type="submit">Ihminen vs Tekoäly</button>
    </form>

    <form method="post" action="/start" style="margin:0;">
      <input type="hidden" name="type" value="c" />
      <button class="btn secondary" type="submit">Ihminen vs Parannettu tekoäly</button>
    </form>
  </div>

  <section>
    <h3 style="margin-top:8px;margin-bottom:6px">Ohjeet</h3>
    <p class="lead" style="margin:0">Syötä yksi kirjain: <strong>k</strong> (kivi), <strong>p</strong> (paperi) tai <strong>s</strong> (sakset). Muulla syötteellä peli päättyy.</p>
  </section>
</div>
"""
    return _render_template(body)


def render_game_page(game_id: str, game: dict) -> str:
    tuomari = game["tuomari"]
    score_html = html.escape(str(tuomari)).replace("\n", "<br />")

    if game.get("finished", False):
        # display a clearer finished card with winner highlight
        winner = (
            game["tuomari"].voittaja() if hasattr(game["tuomari"], "voittaja") else None
        )
        if winner == "eka":
            winner_text = "Ensimmäinen pelaaja voitti pelin!"
            winner_class = "winner success"
        elif winner == "toka":
            winner_text = "Toinen pelaaja voitti pelin!"
            winner_class = "winner danger"
        else:
            winner_text = "Peli päättyi."
            winner_class = "winner"

        body = f"""
<div>
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
    <div>
      <h2 style="margin:0">Peli {html.escape(game_id)}</h2>
      <div class="score" style="margin-top:8px">{score_html}</div>
    </div>
    <div style="text-align:right">
      <h3 class="{winner_class}" style="margin:0">{html.escape(winner_text)}</h3>
      <div style="margin-top:10px"><a class="btn" href="/">Aloita uusi peli</a></div>
    </div>
  </div>
</div>
"""
        return _render_template(body)

    # form differs by game type
    if game["type"] == "a":
        # human vs human - allow submitting both moves
        form = f"""
<form method="post" action="/game/{html.escape(game_id)}/move">
  <label>Ensimmäisen pelaajan siirto: <input name="p1" /></label><br />
  <label>Toisen pelaajan siirto: <input name="p2" /></label><br />
  <button type="submit">Pelaa</button>
</form>
"""
    else:
        # human vs ai - only first player input
        form = f"""
<form method="post" action="/game/{html.escape(game_id)}/move">
  <label>Ensimmäisen pelaajan siirto: <input name="p1" /></label><br />
  <button type="submit">Pelaa</button>
</form>
"""

    body = f"""
<h1>Peli {html.escape(game_id)}</h1>
<p>{score_html}</p>
{form}
<p><a href="/">Takaisin</a></p>
"""
    return _render_template(body)


def parse_post_body(environ):
    try:
        length = int(environ.get("CONTENT_LENGTH", "0") or 0)
    except (ValueError, TypeError):
        length = 0
    body = b""
    wsgi_input = environ.get("wsgi.input")
    if wsgi_input is not None:
        if length:
            body = wsgi_input.read(length)
        else:
            # read all available if no length provided
            body = wsgi_input.read() or b""
    text = body.decode("utf-8", errors="ignore")
    return {
        k: v[0] if isinstance(v, list) else v
        for k, v in parse_qs(text, keep_blank_values=True).items()
    }


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET").upper()
    path = environ.get("PATH_INFO", "/")

    try:
        # Index
        if method == "GET" and path == "/":
            body = index_page().encode("utf-8")
            start_response(
                "200 OK",
                [
                    ("Content-Type", "text/html; charset=utf-8"),
                    ("Content-Length", str(len(body))),
                ],
            )
            return [body]

        # Start a new game
        if method == "POST" and path == "/start":
            form = parse_post_body(environ)
            t = form.get("type", "a")
            gid = str(uuid4())
            state = {"type": t, "tuomari": Tuomari(), "ai": None, "finished": False}
            if t == "b":
                state["ai"] = Tekoaly()
            elif t == "c":
                state["ai"] = TekoalyParannettu(20)
            games[gid] = state
            # redirect to game page
            start_response("303 See Other", [("Location", f"/game/{gid}")])
            return [b""]

        # Game pages and moves
        if path.startswith("/game/"):
            parts = path.strip("/").split("/")
            if len(parts) >= 2:
                gid = parts[1]
                game = games.get(gid)
                if game is None:
                    body = "Peliä ei löytynyt".encode("utf-8")
                    start_response(
                        "404 Not Found",
                        [
                            ("Content-Type", "text/plain; charset=utf-8"),
                            ("Content-Length", str(len(body))),
                        ],
                    )
                    return [body]

                # GET /game/<id>
                if method == "GET" and len(parts) == 2:
                    body = render_game_page(gid, game).encode("utf-8")
                    start_response(
                        "200 OK",
                        [
                            ("Content-Type", "text/html; charset=utf-8"),
                            ("Content-Length", str(len(body))),
                        ],
                    )
                    return [body]

                # POST /game/<id>/move
                if method == "POST" and len(parts) == 3 and parts[2] == "move":
                    form = parse_post_body(environ)
                    p1 = (form.get("p1") or "").strip()
                    p2 = (form.get("p2") or "").strip() if "p2" in form else None

                    ok_moves = ("k", "p", "s")

                    if game["type"] == "a":
                        # human vs human: require both moves
                        if p1 not in ok_moves or p2 not in ok_moves:
                            game["finished"] = True
                        else:
                            game["tuomari"].kirjaa_siirto(p1, p2)
                            # if either player reached the win threshold, mark the game finished
                            if game["tuomari"].onko_voittaja():
                                game["finished"] = True
                    else:
                        # modes b or c (ai variants)
                        if p1 not in ok_moves:
                            game["finished"] = True
                        else:
                            ai = game["ai"]
                            if ai is None:
                                # defensive: create a default AI
                                ai = Tekoaly()
                                game["ai"] = ai
                            ai_move = ai.anna_siirto()
                            # teach improved ai the human move if supported
                            if hasattr(ai, "aseta_siirto"):
                                try:
                                    ai.aseta_siirto(p1)
                                except Exception:
                                    pass
                            game["tuomari"].kirjaa_siirto(p1, ai_move)
                            # if either player reached the win threshold, mark the game finished
                            if game["tuomari"].onko_voittaja():
                                game["finished"] = True

                    # after processing, redirect back to the game page
                    start_response("303 See Other", [("Location", f"/game/{gid}")])
                    return [b""]

        # Not found
        body = "Not Found".encode("utf-8")
        start_response(
            "404 Not Found",
            [
                ("Content-Type", "text/plain; charset=utf-8"),
                ("Content-Length", str(len(body))),
            ],
        )
        return [body]

    except Exception as e:
        # Return minimal error info; avoid exposing internals but provide message
        msg = f"Internal Server Error: {html.escape(str(e))}"
        body = msg.encode("utf-8")
        start_response(
            "500 Internal Server Error",
            [
                ("Content-Type", "text/plain; charset=utf-8"),
                ("Content-Length", str(len(body))),
            ],
        )
        return [body]


def run_server(port: int = 8000):
    print(f"Starting server on http://localhost:{port}/")
    httpd = make_server("", port, application)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down")


def _call_wsgi(
    method: str,
    path: str,
    body_bytes: bytes = b"",
    content_type: str = "application/x-www-form-urlencoded",
):
    """
    Minimal helper to call the WSGI application directly (used by the smoke test).
    Returns (status, headers, body_bytes).
    """
    from io import BytesIO

    status_headers = []

    def start_response(status, headers):
        status_headers.append((status, headers))

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "80",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": "http",
        "wsgi.input": BytesIO(body_bytes),
        "wsgi.errors": BytesIO(),
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
        "CONTENT_LENGTH": str(len(body_bytes)),
        "CONTENT_TYPE": content_type,
    }

    result = application(environ, start_response)
    body = b"".join(result)
    if status_headers:
        status, headers = status_headers[0]
    else:
        status, headers = ("500 Internal Server Error", [])
    return status, headers, body


def _smoke_test():
    """
    Run a short, non-blocking set of checks against the WSGI app.
    This does not start the HTTP server; it calls the WSGI `application`
    callable directly and prints concise output (suitable for CI or local checks).
    """
    print("Smoke test: GET /")
    status, headers, body = _call_wsgi("GET", "/")
    print(" ->", status)
    # print a short excerpt of the body for quick verification
    try:
        text = body.decode("utf-8", errors="replace")
    except Exception:
        text = str(body)
    print(text[:600].replace("\n", " ") + ("..." if len(text) > 600 else ""))
    print()

    print("Smoke test: POST /start (create game type a)")
    status, headers, body = _call_wsgi(
        "POST", "/start", b"type=a", content_type="application/x-www-form-urlencoded"
    )
    print(" ->", status)
    # Expect a redirect (303) to /game/<id>
    if status.startswith("303"):
        # find location header
        loc = None
        for k, v in headers:
            if k.lower() == "location":
                loc = v
                break
        print(" Redirect ->", loc)
        if loc:
            print("Fetching created game page for brief verification...")
            status2, headers2, body2 = _call_wsgi("GET", loc)
            print(" ->", status2)
            try:
                t2 = body2.decode("utf-8", errors="replace")
            except Exception:
                t2 = str(body2)
            print(t2[:600].replace("\n", " ") + ("..." if len(t2) > 600 else ""))
    else:
        print(" Unexpected response when creating a game.")
    print()

    print("Smoke test: basic move against AI")
    # create game type b (AI) and then play one move
    status, headers, body = _call_wsgi(
        "POST", "/start", b"type=b", content_type="application/x-www-form-urlencoded"
    )
    print(" -> create:", status)
    loc = None
    if status.startswith("303"):
        for k, v in headers:
            if k.lower() == "location":
                loc = v
                break
    if loc:
        # POST a move p1=k to /game/<id>/move
        move_path = loc.rstrip("/") + "/move"
        print(" Posting move to", move_path)
        status_m, headers_m, body_m = _call_wsgi(
            "POST", move_path, b"p1=k", content_type="application/x-www-form-urlencoded"
        )
        print(" ->", status_m)
        # follow redirect and get final page
        if status_m.startswith("303"):
            loc2 = None
            for k, v in headers_m:
                if k.lower() == "location":
                    loc2 = v
                    break
            if loc2:
                status_g, headers_g, body_g = _call_wsgi("GET", loc2)
                print(" -> game page:", status_g)
                try:
                    tg = body_g.decode("utf-8", errors="replace")
                except Exception:
                    tg = str(body_g)
                print(tg[:800].replace("\n", " ") + ("..." if len(tg) > 800 else ""))
    else:
        print(" Could not determine game location from create response.")

    print("\nSmoke tests completed.")


if __name__ == "__main__":
    import sys

    # Support a lightweight smoke-test mode that runs WSGI-level checks without blocking
    if "--smoke" in sys.argv:
        _smoke_test()
    else:
        # allow an optional --port=N argument
        port = 8000
        for arg in sys.argv[1:]:
            if arg.startswith("--port="):
                try:
                    port = int(arg.split("=", 1)[1])
                except Exception:
                    pass
        run_server(port)


if __name__ == "__main__":
    run_server(8000)

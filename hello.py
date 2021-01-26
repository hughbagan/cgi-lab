#!/usr/bin/env python3
import os, json, sys
import templates
import secret

# print(os.environ) # all environment variables


# Serve cgi_server.py, then curl/browse localhost:8080/hello.py
def serve_env():
    print('Content-Type: application/json') # help the browser to display it
    print()
    print(json.dumps(dict(os.environ), indent=2))


def serve_html_info():
    # Read POST data if we got any. Thank you Hazel! ╰(◕ ᗜ ◕ )╯
    posted_bytes = os.environ.get("CONTENT_LENGTH", 0)
    posted = None
    if posted_bytes:
        posted = sys.stdin.read(int(posted_bytes))
        # cardboard-thin authentication!
        if secret.username in posted and secret.password in posted:
            # set a cookie
            print('Set-Cookie: auth='+str(True))
    
    print('Content-Type: text/html')
    print()
    print("""
    <!doctype html>
    <html>
    <body>
    <h1>Lab 3</h1>""")

    # Display browser info
    print(f"<p>HTTP_USER_AGENT: {os.environ['HTTP_USER_AGENT']}</p>")

    # Display query string info
    # example query: ?name="hugh"&second="two"
    print(f"<p>QUERY_STRING: {os.environ['QUERY_STRING']}</p>")
    query = os.environ['QUERY_STRING']
    if '&' in query and '=' in query:
        print("<ul>")
        for parameter in os.environ['QUERY_STRING'].split('&'):
            (name, value) = parameter.split('=')
            print(f"<li><em>{name}</em> = {value}</li>")
        print(f"</ul>")

    # Display the POST from the form
    if posted:
        print(f"<p>POSTED: <pre>")
        for line in posted.splitlines():
            print(line)
        print("</pre></p>")

    # Display a login form OR a secret page if we're logged in
    if os.environ['HTTP_COOKIE']:
        # NOTE: only works for one cookie
        (cookie, value) = os.environ['HTTP_COOKIE'].split('=')
        if cookie=="auth" and value=="True":
            # probably incorrect (should pass from `posted` instead?)
            print(templates.secret_page(secret.username, secret.password))
        else:
            print("<p>Cookie is incorrect somehow</p>")
    else:
        this_script = __file__.split('/')[-1:][0] # E.Big stackoverflow.com/a/46390072
        print(templates.login_page(this_script)) # pass in this script's name
    
    print("""
    </body>
    </html>
    """)
    

#serve_env()
serve_html_info()

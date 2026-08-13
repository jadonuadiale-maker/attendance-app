from livereload import Server
from app import app

server = Server(app.wsgi_app)

# Watch templates and static files
server.watch('templates/')
server.watch('static/')
server.watch('static/css/custom.css')

# Start livereload server ONCE
server.serve(port=5000, host='0.0.0.0')
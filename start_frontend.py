"""
Simple HTTP Server for Frontend Testing
Run this to serve the app.html file properly
"""
import http.server
import socketserver
import os

# Change to the directory containing app.html
os.chdir(r"C:\Users\cheeh\Desktop\webservice ramadan\app\schemas\frontend webservice site")

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

print("=" * 60)
print("🌐 FRONTEND SERVER STARTING")
print("=" * 60)
print(f"📂 Serving files from:")
print(f"   {os.getcwd()}")
print(f"")
print(f"🌐 Open your browser and go to:")
print(f"   http://localhost:{PORT}/app.html")
print(f"")
print(f"✅ Backend should be running on:")
print(f"   http://localhost:8000")
print(f"")
print(f"Press Ctrl+C to stop the server")
print("=" * 60)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")

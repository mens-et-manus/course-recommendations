from flask import Flask, render_template, request
import json
 
app = Flask(__name__)
 
@app.route('/')
def index(user=None):
    return render_template('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

if __name__ == '__main__':
    app.run()
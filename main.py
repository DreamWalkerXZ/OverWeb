import os
import time
import uuid
import random
import threading
from flask import Flask, render_template, url_for


app = Flask(__name__)


def expireContainer(name):
    print('%s will be removed in 10 minutes' % (name))
    time.sleep(10*60)
    print('Stopping %s' % (name))
    os.system('docker stop %s' % (name))
    print('Removing %s' % (name))
    os.system('docker rm %s' % (name))

def createTmpContainer(port, password, name):
    print('Creating %s' % (name))
    os.system('docker run -d -p %d:6901 -e VNC_PW=%s -e VNC_RESOLUTION=720x720 --name %s consol/ubuntu-icewm-vnc chromium-browser https://www.google.com/' % (port, password, name))
    threading.Thread(target=expireContainer, args=(name,)).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/go')
def go():
    port = 10000 + random.randint(0, 50000)
    password = str(uuid.uuid4())
    name = str(uuid.uuid4())
    createTmpContainer(port, password, name)
    return render_template('go.html', link='http://localhost:%d/?password=%s' % (port, password))

@app.route('/about')
def about():
    return render_template('about.html')

def main():
    app.run(host='127.0.0.1', port=8080, debug=True)

if __name__ == '__main__':
    main()

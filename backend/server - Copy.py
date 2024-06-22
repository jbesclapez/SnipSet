from app import create_app

app = create_app()

@app.route('/')
def hello_world():
    return 'Hello, SnipSet!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')

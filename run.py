from ecobee import create_app
from log_data import log

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

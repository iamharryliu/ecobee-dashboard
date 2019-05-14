from ecobee import create_app, db
from ecobee.main.models import apis


def main():
    app = create_app()
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    main()

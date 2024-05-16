from app import create_app, db

app = create_app()


def initiate_table():
    db.create_all()

if __name__ == "__main__":
    # initiate_table()
    app.run(debug=True)

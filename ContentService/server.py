from contents.app import create_app
from contents.db import db, db_config

app = create_app(db, db_config)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

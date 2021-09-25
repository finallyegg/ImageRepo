import sys
from sqlalchemy import create_engine
from backend.imageRepo import app
from backend.models.base import Base


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--reinstall-schema":
        conn = app.config["DATABASE_URI"]
        engine = create_engine(conn, echo=False)
        Base.metadata.reflect(engine)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print("DB Resetted")
        exit()
    app.run(port=5666)

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Database Setup ---
DATABASE_URL = "sqlite:///miscrits.db"  # creates miscrits.db in current dir

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- Model ---
class Miscrit(Base):
    __tablename__ = "miscrits"

    Miscrit_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Rarity = Column(String)

# --- Create Tables ---
Base.metadata.create_all(bind=engine)

# --- Insert & Query ---
def add_and_show():
    session = SessionLocal()

    # Add a miscrit
    new_miscrit = Miscrit(Miscrit_ID=1, Name="Flue", Rarity="Common")
    session.add(new_miscrit)
    session.commit()

    # Query it back
    miscrits = session.query(Miscrit).all()
    for m in miscrits:
        print(f"ID: {m.Miscrit_ID}, Name: {m.Name}, Rarity: {m.Rarity}")

    session.close()

if __name__ == "__main__":
    add_and_show()

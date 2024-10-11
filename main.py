from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a SQLAlchemy engine to connect to the PostgreSQL database
engine = create_engine('postgresql://user:12345@localhost/mydatabase')

# Create a base class for declarative models
Base = declarative_base()

# Define the Address model
class Address(Base):
    __tablename__ = 'address'
    address_id = Column(Integer, primary_key=True)
    street_address = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    person_id = Column(Integer)

# Define the Person model
class Person(Base):
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    email = Column(String)
    phone_number = Column(String)
    gender = Column(String)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Sample query to retrieve all persons and their addresses
persons_with_addresses = session.query(Person, Address).filter(Person.person_id == Address.person_id).all()

for person, address in persons_with_addresses:
    print(f"Person: {person.first_name} {person.last_name}")
    print(f"Address: {address.street_address}, {address.city}, {address.state}, {address.postal_code}")
    print("------")

from flask import Flask, request, jsonify

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:12345@localhost/mydatabase'
db = SQLAlchemy(app)
Base = declarative_base()

class Address(Base):
    __tablename__ = 'address'
    address_id = Column(Integer, primary_key=True)
    street_address = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    person_id = Column(Integer)

class Person(Base):
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))  # Adjust the length as needed
    last_name = Column(String(50))   # Adjust the length as needed
    date_of_birth = Column(Date)
    email = Column(String(100))  # Adjust the length as needed
    phone_number = Column(String(15))  # Adjust the length as needed
    gender = Column(String(10))  # Adjust the length as needed


@app.route('/persons', methods=['GET'])
def get_persons():
    # Query all persons
    persons = Person.query.all()
    result = [{'first_name': person.first_name, 'last_name': person.last_name} for person in persons]
    return jsonify(result)

@app.route('/persons', methods=['POST'])
def create_person():
    data = request.get_json()
    try:
        new_person = Person(**data)
        db.session.add(new_person)
        db.session.commit()
        return jsonify({'message': 'Person created successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Person already exists'}), 409

@app.route('/persons/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.get_json()
    person = Person.query.get(person_id)
    if person is None:
        return jsonify({'error': 'Person not found'}), 404
    person.update(data)
    db.session.commit()
    return jsonify({'message': 'Person updated successfully'})

@app.route('/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    person = Person.query.get(person_id)
    if person is None:
        return jsonify({'error': 'Person not found'}), 404
    db.session.delete(person)
    db.session.commit()
    return jsonify({'message': 'Person deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

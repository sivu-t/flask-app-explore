from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# conn = sqlite.connect('student.db')
# c = conn.cursor()
# c.execute("""CREATE TABLE Students""")
#Init api
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db =SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)
#student Class/Model
class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True)
	physics = db.Column(db.Integer)
	maths = db.Column(db.Integer)
	chemistry = db.Column(db.Integer)

	def __repr__ (self):
		return f"Student('{self.name}','{self.physics}','{self.maths}','{self.chemistry}')"
	# def __init__(self, name, physics, maths, chemistry):
	# 	self.name = name
	# 	self.physics = physics
	# 	self.maths = maths
	# 	self.chemistry = chemistry

#Schema
class StudentSchema(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'physics', 'maths', 'chemistry')
#init Schema
student_schema = StudentSchema(strict=True)
students_schema = StudentSchema(many=True, strict=True)


#create student
@app.route('/results', methods=['POST'])
def add_results():
	name = request.json['name']
	physics = request.json['physics']
	maths = request.json['maths']
	chemistry = request.json['chemistry']

	new_student = Student(name, physics, maths,chemistry)

	db.session.add(new_student)
	db.session.commit()

	return	student_schema.jsonify(new_student)
#Get students
@app.route('/results', methods=['GET'])
def get_results():
	all_students = Student.query.all()
	result = students_schema.dump(all_students)
	return	jsonify(result.data)

@app.route('/results/<id>', methods=['GET'])
def aStudent(id):
	a_student = Student.query.get(id)
	return	student_schema.jsonify(a_student)


#update student
@app.route('/results/<id>', methods=['PUT'])
def update_results(id):
	the_Student = Student.query.get(id)
	name = request.json['name']
	physics = request.json['physics']
	maths = request.json['maths']
	chemistry = request.json['chemistry']

	the_Student.name = name
	the_Student.physics = physics
	the_Student.maths = maths
	the_Student.chemistry = chemistry


	db.session.commit()
	return	student_schema.jsonify(the_Student)

@app.route('/results/<id>', methods=['DELETE'])
def delete_results(id):
	student = Student.query.get(id)
	db.session.delete(student)
	db.session.commit()
	return	student_schema.jsonify(student)

if __name__ == '__main__':
	app.run(debug=True)
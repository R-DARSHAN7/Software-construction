from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/Academic_Evaluvator"
mongo = PyMongo(app)

# Route to show all students
@app.route('/')
def index():
    students = mongo.db.students.find()  # Fetching all students from the database
    return render_template('index.html', students=students)

# Route to add a new student
@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        grade = request.form['grade']
        
        # Insert the new student data into the MongoDB database
        mongo.db.students.insert_one({
            'name': name,
            'email': email,
            'age': age,
            'grade': grade
        })
        
        # Redirect to the homepage to display the updated list of students
        return redirect(url_for('index'))

# Route to delete a student by their ID
@app.route('/delete_student/<student_id>', methods=['GET'])
def delete_student(student_id):
    mongo.db.students.delete_one({'_id': mongo.db.ObjectId(student_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

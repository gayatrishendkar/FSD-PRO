from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)


# Database Connection
def get_db_connection():
    connection = psycopg2.connect(
        dbname="college_feedback_db",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    return connection


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Submit Feedback
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():

    student_name = request.form['student_name']
    email = request.form['email']
    course = request.form['course']
    semester = request.form['semester']
    subject_name = request.form['subject_name']
    faculty_name = request.form['faculty_name']
    rating = request.form['rating']
    message = request.form['message']

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO feedback
        (student_name, email, course, semester, subject_name,
        faculty_name, rating, message)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            student_name,
            email,
            course,
            semester,
            subject_name,
            faculty_name,
            rating,
            message
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('view_feedback'))


# View All Feedback
@app.route('/feedback')
def view_feedback():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM feedback
        ORDER BY id DESC
    """)

    feedbacks = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        'feedback_list.html',
        feedbacks=feedbacks
    )


# Delete Feedback
@app.route('/delete/<int:id>')
def delete_feedback(id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM feedback WHERE id = %s",
        (id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('view_feedback'))


if __name__ == '__main__':
    app.run(debug=True)
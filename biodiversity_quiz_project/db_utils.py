# Content of db_utils.py:
import mysql.connector
from mysql.connector import Error
from db_utils import create_connection, close_connection
from quiz_logic import get_random_question, check_answer


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='biodiversity_quiz',
            user='quiz_user',
            password='33216188Bri.*'
        )
        if connection.is_connected():
            print('Connected to MySQL database')
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print('MySQL connection is closed')


def main():
    connection = create_connection()
    if connection is None:
        return

    try:
        # Your main application logic here
        question = get_random_question(connection)
        print(question)
        # More code to handle user input, check answers, etc.
    finally:
        close_connection(connection)


if __name__ == "__main__":
    main()


# Content of quiz_logic.py:
def get_random_question(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions ORDER BY RAND() LIMIT 1")
    question = cursor.fetchone()
    cursor.close()
    return question


def check_answer(connection, question_id, user_answer):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT correct_answer FROM questions WHERE question_id = %s"
    cursor.execute(query, (question_id,))
    correct_answer = cursor.fetchone()['correct_answer']
    cursor.close()
    return user_answer.upper() == correct_answer


# Content of requirements.txt:
mysql-connector-python == 8.0.26

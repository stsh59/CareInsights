from app.db import mysql

class TodoModel:
    @staticmethod
    def get_all_todos():
        try:
            cursor = mysql.connection.cursor()
            query = "SELECT * FROM todos"
            cursor.execute(query)
            todos = cursor.fetchall()
            cursor.close()
            return todos
        except Exception as e:
            print(f"Error fetching todos: {e}")
            return None

    @staticmethod
    def add_todo(title):
        try:
            cursor = mysql.connection.cursor()
            query = "INSERT INTO todos (title) VALUES (%s)"
            cursor.execute(query, [title])
            mysql.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error adding todo: {e}")
            return False

    @staticmethod
    def delete_todo(todo_id):
        try:
            cursor = mysql.connection.cursor()
            query = "DELETE FROM todos WHERE id = %s"
            cursor.execute(query, [todo_id])
            mysql.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error deleting todo: {e}")
            return False

    @staticmethod
    def update_todo_status(todo_id, completed):
        try:
            cursor = mysql.connection.cursor()
            query = "UPDATE todos SET completed = %s WHERE id = %s"
            cursor.execute(query, [completed, todo_id])
            mysql.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error updating todo status: {e}")
            return False

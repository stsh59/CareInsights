from flask import Blueprint, request, jsonify, render_template
from app.models.todo_model import TodoModel

todo_bp = Blueprint('todo_bp', __name__)

@todo_bp.route('/api/todos', methods=['GET'])
def get_todos():
    todos = TodoModel.get_all_todos()
    if todos is None:
        return jsonify({'message': 'Error fetching todos'}), 500
    return jsonify(todos), 200

@todo_bp.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    title = data.get('title')
    if TodoModel.add_todo(title):
        return jsonify({'message': 'Todo added successfully'}), 201
    else:
        return jsonify({'message': 'Error adding todo'}), 500

@todo_bp.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if TodoModel.delete_todo(todo_id):
        return jsonify({'message': 'Todo deleted successfully'}), 200
    else:
        return jsonify({'message': 'Error deleting todo'}), 500

@todo_bp.route('/api/todos/<int:todo_id>', methods=['PATCH'])
def update_todo_status(todo_id):
    data = request.get_json()
    completed = data.get('completed')
    if TodoModel.update_todo_status(todo_id, completed):
        return jsonify({'message': 'Todo status updated successfully'}), 200
    else:
        return jsonify({'message': 'Error updating todo status'}), 500

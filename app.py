from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# JSON database file path
DB_FILE = 'data.json'

def init_db():
    """Initialize the database file if it doesn't exist"""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({
                "items": [],
                "users": [],
                "comments": []
            }, f)

def read_db():
    """Read data from JSON file"""
    try:
        with open(DB_FILE, 'r') as f:
            data = json.load(f)
            # Ensure all required keys exist
            if 'users' not in data:
                data['users'] = []
            if 'comments' not in data:
                data['comments'] = []
            if 'items' not in data:
                data['items'] = []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"items": [], "users": [], "comments": []}

def write_db(data):
    """Write data to JSON file"""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/users')
def users_page():
    """Render the users management page"""
    return render_template('users.html')

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    """Render the task detail page"""
    return render_template('task_detail.html', task_id=task_id)

@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all items"""
    db = read_db()
    return jsonify(db.get('items', [])), 200

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item by ID"""
    db = read_db()
    items = db.get('items', [])
    item = next((i for i in items if i['id'] == item_id), None)
    
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/items', methods=['POST'])
def create_item():
    """Create a new item"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    db = read_db()
    items = db.get('items', [])
    
    # Generate new ID
    new_id = max([i['id'] for i in items], default=0) + 1
    
    new_item = {
        "id": new_id,
        "title": data['title'],
        "description": data.get('description', ''),
        "completed": data.get('completed', False),
        "assigned_to": data.get('assigned_to', None),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    items.append(new_item)
    db['items'] = items
    write_db(db)
    
    return jsonify(new_item), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item"""
    data = request.get_json()
    
    db = read_db()
    items = db.get('items', [])
    item = next((i for i in items if i['id'] == item_id), None)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    # Update fields
    if 'title' in data:
        item['title'] = data['title']
    if 'description' in data:
        item['description'] = data['description']
    if 'completed' in data:
        item['completed'] = data['completed']
    if 'assigned_to' in data:
        item['assigned_to'] = data['assigned_to']
    item['updated_at'] = datetime.now().isoformat()
    
    write_db(db)
    
    return jsonify(item), 200

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item"""
    db = read_db()
    items = db.get('items', [])
    
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    items = [i for i in items if i['id'] != item_id]
    db['items'] = items
    write_db(db)
    
    return jsonify({"message": "Item deleted successfully"}), 200

# User Management APIs
@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    db = read_db()
    return jsonify(db.get('users', [])), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    db = read_db()
    users = db.get('users', [])
    
    # Check if user already exists
    if any(u['name'].lower() == data['name'].lower() for u in users):
        return jsonify({"error": "User already exists"}), 400
    
    # Generate new ID
    new_id = max([u['id'] for u in users], default=0) + 1
    
    new_user = {
        "id": new_id,
        "name": data['name'],
        "email": data.get('email', ''),
        "created_at": datetime.now().isoformat()
    }
    
    users.append(new_user)
    db['users'] = users
    write_db(db)
    
    return jsonify(new_user), 201

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    db = read_db()
    users = db.get('users', [])
    
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Unassign user from all tasks
    items = db.get('items', [])
    for item in items:
        if item.get('assigned_to') == user_id:
            item['assigned_to'] = None
    
    users = [u for u in users if u['id'] != user_id]
    db['users'] = users
    db['items'] = items
    write_db(db)
    
    return jsonify({"message": "User deleted successfully"}), 200

# Comments APIs
@app.route('/api/tasks/<int:task_id>/comments', methods=['GET'])
def get_comments(task_id):
    """Get all comments for a task"""
    db = read_db()
    comments = db.get('comments', [])
    task_comments = [c for c in comments if c.get('task_id') == task_id]
    return jsonify(task_comments), 200

@app.route('/api/tasks/<int:task_id>/comments', methods=['POST'])
def create_comment(task_id):
    """Create a new comment for a task"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Comment text is required"}), 400
    
    db = read_db()
    items = db.get('items', [])
    task = next((t for t in items if t['id'] == task_id), None)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    comments = db.get('comments', [])
    new_id = max([c['id'] for c in comments], default=0) + 1
    
    new_comment = {
        "id": new_id,
        "task_id": task_id,
        "text": data['text'],
        "author": data.get('author', 'Anonymous'),
        "created_at": datetime.now().isoformat()
    }
    
    comments.append(new_comment)
    db['comments'] = comments
    write_db(db)
    
    return jsonify(new_comment), 201

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment"""
    db = read_db()
    comments = db.get('comments', [])
    
    comment = next((c for c in comments if c['id'] == comment_id), None)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    
    comments = [c for c in comments if c['id'] != comment_id]
    db['comments'] = comments
    write_db(db)
    
    return jsonify({"message": "Comment deleted successfully"}), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


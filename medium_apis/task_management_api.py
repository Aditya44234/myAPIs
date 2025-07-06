from flask import Flask, request, jsonify
import uuid
import datetime
from functools import wraps

app = Flask(__name__)

# In-memory storage
projects = {}
tasks = {}
users = {}
assignments = {}
task_comments = {}

def generate_id():
    return str(uuid.uuid4())

# Sample data
sample_users = [
    {'id': 'user1', 'name': 'John Doe', 'email': 'john@example.com'},
    {'id': 'user2', 'name': 'Jane Smith', 'email': 'jane@example.com'},
    {'id': 'user3', 'name': 'Bob Johnson', 'email': 'bob@example.com'}
]

for user in sample_users:
    users[user['id']] = user

sample_projects = [
    {
        'id': 'proj1',
        'name': 'Website Redesign',
        'description': 'Redesign company website with modern UI/UX',
        'owner_id': 'user1',
        'status': 'active',
        'priority': 'high',
        'start_date': '2024-01-01',
        'end_date': '2024-03-31',
        'created_at': '2024-01-01T09:00:00',
        'updated_at': '2024-01-01T09:00:00'
    },
    {
        'id': 'proj2',
        'name': 'Mobile App Development',
        'description': 'Develop iOS and Android mobile application',
        'owner_id': 'user2',
        'status': 'planning',
        'priority': 'medium',
        'start_date': '2024-02-01',
        'end_date': '2024-06-30',
        'created_at': '2024-01-15T10:00:00',
        'updated_at': '2024-01-15T10:00:00'
    }
]

for project in sample_projects:
    projects[project['id']] = project

sample_tasks = [
    {
        'id': 'task1',
        'title': 'Design Homepage',
        'description': 'Create wireframes and mockups for homepage',
        'project_id': 'proj1',
        'assigned_to': 'user2',
        'status': 'in_progress',
        'priority': 'high',
        'due_date': '2024-01-15',
        'created_at': '2024-01-01T09:00:00',
        'updated_at': '2024-01-01T09:00:00',
        'estimated_hours': 8,
        'actual_hours': 4
    },
    {
        'id': 'task2',
        'title': 'Implement Navigation',
        'description': 'Code the main navigation component',
        'project_id': 'proj1',
        'assigned_to': 'user3',
        'status': 'todo',
        'priority': 'medium',
        'due_date': '2024-01-20',
        'created_at': '2024-01-02T10:00:00',
        'updated_at': '2024-01-02T10:00:00',
        'estimated_hours': 6,
        'actual_hours': 0
    }
]

for task in sample_tasks:
    tasks[task['id']] = task

# 1. Get All Projects
@app.route('/api/projects', methods=['GET'])
def get_projects():
    status = request.args.get('status')
    owner_id = request.args.get('owner_id')
    priority = request.args.get('priority')
    
    filtered_projects = []
    
    for project in projects.values():
        if status and project['status'] != status:
            continue
        if owner_id and project['owner_id'] != owner_id:
            continue
        if priority and project['priority'] != priority:
            continue
        
        filtered_projects.append(project)
    
    return jsonify({'projects': filtered_projects})

# 2. Get Single Project
@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    project = projects.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Get project tasks
    project_tasks = [task for task in tasks.values() if task['project_id'] == project_id]
    
    # Calculate progress
    total_tasks = len(project_tasks)
    completed_tasks = len([task for task in project_tasks if task['status'] == 'completed'])
    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return jsonify({
        'project': project,
        'tasks': project_tasks,
        'progress': round(progress, 2),
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks
    })

# 3. Create Project
@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['name', 'description', 'owner_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if data['owner_id'] not in users:
        return jsonify({'error': 'Invalid owner ID'}), 400
    
    project_id = generate_id()
    project = {
        'id': project_id,
        'name': data['name'],
        'description': data['description'],
        'owner_id': data['owner_id'],
        'status': data.get('status', 'planning'),
        'priority': data.get('priority', 'medium'),
        'start_date': data.get('start_date'),
        'end_date': data.get('end_date'),
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    }
    
    projects[project_id] = project
    
    return jsonify({
        'message': 'Project created successfully',
        'project': project
    }), 201

# 4. Update Project
@app.route('/api/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    project = projects.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Update fields
    for field in ['name', 'description', 'status', 'priority', 'start_date', 'end_date']:
        if field in data:
            project[field] = data[field]
    
    project['updated_at'] = datetime.datetime.now().isoformat()
    
    return jsonify({
        'message': 'Project updated successfully',
        'project': project
    })

# 5. Delete Project
@app.route('/api/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    if project_id not in projects:
        return jsonify({'error': 'Project not found'}), 404
    
    # Delete associated tasks
    tasks_to_delete = [task_id for task_id, task in tasks.items() 
                      if task['project_id'] == project_id]
    for task_id in tasks_to_delete:
        del tasks[task_id]
    
    del projects[project_id]
    return jsonify({'message': 'Project deleted successfully'})

# 6. Get All Tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    project_id = request.args.get('project_id')
    assigned_to = request.args.get('assigned_to')
    status = request.args.get('status')
    priority = request.args.get('priority')
    
    filtered_tasks = []
    
    for task in tasks.values():
        if project_id and task['project_id'] != project_id:
            continue
        if assigned_to and task['assigned_to'] != assigned_to:
            continue
        if status and task['status'] != status:
            continue
        if priority and task['priority'] != priority:
            continue
        
        filtered_tasks.append(task)
    
    return jsonify({'tasks': filtered_tasks})

# 7. Get Single Task
@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Get task comments
    task_comments_list = [comment for comment in task_comments.values() 
                         if comment['task_id'] == task_id]
    
    return jsonify({
        'task': task,
        'comments': task_comments_list
    })

# 8. Create Task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['title', 'description', 'project_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if data['project_id'] not in projects:
        return jsonify({'error': 'Invalid project ID'}), 400
    
    task_id = generate_id()
    task = {
        'id': task_id,
        'title': data['title'],
        'description': data['description'],
        'project_id': data['project_id'],
        'assigned_to': data.get('assigned_to'),
        'status': data.get('status', 'todo'),
        'priority': data.get('priority', 'medium'),
        'due_date': data.get('due_date'),
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
        'estimated_hours': data.get('estimated_hours', 0),
        'actual_hours': data.get('actual_hours', 0)
    }
    
    tasks[task_id] = task
    
    return jsonify({
        'message': 'Task created successfully',
        'task': task
    }), 201

# 9. Update Task
@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Update fields
    for field in ['title', 'description', 'assigned_to', 'status', 'priority', 
                  'due_date', 'estimated_hours', 'actual_hours']:
        if field in data:
            task[field] = data[field]
    
    task['updated_at'] = datetime.datetime.now().isoformat()
    
    return jsonify({
        'message': 'Task updated successfully',
        'task': task
    })

# 10. Delete Task
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    # Delete associated comments
    comments_to_delete = [comment_id for comment_id, comment in task_comments.items() 
                         if comment['task_id'] == task_id]
    for comment_id in comments_to_delete:
        del task_comments[comment_id]
    
    del tasks[task_id]
    return jsonify({'message': 'Task deleted successfully'})

# 11. Add Comment to Task
@app.route('/api/tasks/<task_id>/comments', methods=['POST'])
def add_task_comment(task_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    content = data.get('content')
    user_id = data.get('user_id')
    
    if not all([content, user_id]):
        return jsonify({'error': 'Content and user_id required'}), 400
    
    comment_id = generate_id()
    comment = {
        'id': comment_id,
        'task_id': task_id,
        'content': content,
        'user_id': user_id,
        'created_at': datetime.datetime.now().isoformat()
    }
    
    task_comments[comment_id] = comment
    
    return jsonify({
        'message': 'Comment added successfully',
        'comment': comment
    }), 201

# 12. Get User Dashboard
@app.route('/api/dashboard/<user_id>', methods=['GET'])
def get_user_dashboard(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user's tasks
    user_tasks = [task for task in tasks.values() if task['assigned_to'] == user_id]
    
    # Get user's projects
    user_projects = [project for project in projects.values() if project['owner_id'] == user_id]
    
    # Calculate stats
    total_tasks = len(user_tasks)
    completed_tasks = len([task for task in user_tasks if task['status'] == 'completed'])
    overdue_tasks = len([task for task in user_tasks 
                        if task['due_date'] and task['status'] != 'completed' and 
                        task['due_date'] < datetime.datetime.now().strftime('%Y-%m-%d')])
    
    return jsonify({
        'user': users[user_id],
        'tasks': user_tasks,
        'projects': user_projects,
        'stats': {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'overdue_tasks': overdue_tasks,
            'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
    })

# 13. Get Project Progress
@app.route('/api/projects/<project_id>/progress', methods=['GET'])
def get_project_progress(project_id):
    project = projects.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    project_tasks = [task for task in tasks.values() if task['project_id'] == project_id]
    
    status_counts = {}
    priority_counts = {}
    total_estimated = 0
    total_actual = 0
    
    for task in project_tasks:
        status_counts[task['status']] = status_counts.get(task['status'], 0) + 1
        priority_counts[task['priority']] = priority_counts.get(task['priority'], 0) + 1
        total_estimated += task['estimated_hours']
        total_actual += task['actual_hours']
    
    return jsonify({
        'project': project,
        'total_tasks': len(project_tasks),
        'status_breakdown': status_counts,
        'priority_breakdown': priority_counts,
        'hours': {
            'estimated': total_estimated,
            'actual': total_actual,
            'variance': total_actual - total_estimated
        }
    })

# 14. Get All Users
@app.route('/api/users', methods=['GET'])
def get_users_list():
    return jsonify({'users': list(users.values())})

# 15. Get Task Statistics
@app.route('/api/stats/tasks', methods=['GET'])
def get_task_stats():
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks.values() if task['status'] == 'completed'])
    overdue_tasks = len([task for task in tasks.values() 
                        if task['due_date'] and task['status'] != 'completed' and 
                        task['due_date'] < datetime.datetime.now().strftime('%Y-%m-%d')])
    
    status_counts = {}
    priority_counts = {}
    
    for task in tasks.values():
        status_counts[task['status']] = status_counts.get(task['status'], 0) + 1
        priority_counts[task['priority']] = priority_counts.get(task['priority'], 0) + 1
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'status_breakdown': status_counts,
        'priority_breakdown': priority_counts
    })

if __name__ == '__main__':
    app.run(debug=True, port=5004) 
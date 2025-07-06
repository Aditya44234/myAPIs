from flask import Flask, request, jsonify
import uuid
import datetime
from functools import wraps

app = Flask(__name__)

# In-memory storage
posts = {}
comments = {}
categories = {
    'technology': 'Technology and programming',
    'lifestyle': 'Lifestyle and personal development',
    'travel': 'Travel experiences and tips',
    'food': 'Food and cooking',
    'business': 'Business and entrepreneurship'
}
tags = set()
likes = {}

def generate_id():
    return str(uuid.uuid4())

# Sample posts
sample_posts = [
    {
        'id': '1',
        'title': 'Getting Started with Flask',
        'content': 'Flask is a lightweight web framework for Python...',
        'author_id': 'user1',
        'author_name': 'John Doe',
        'category': 'technology',
        'tags': ['python', 'flask', 'web-development'],
        'status': 'published',
        'created_at': '2024-01-15T10:00:00',
        'updated_at': '2024-01-15T10:00:00',
        'read_time': 5,
        'featured': True
    },
    {
        'id': '2',
        'title': '10 Travel Tips for Beginners',
        'content': 'Traveling can be overwhelming for first-timers...',
        'author_id': 'user2',
        'author_name': 'Jane Smith',
        'category': 'travel',
        'tags': ['travel', 'tips', 'beginners'],
        'status': 'published',
        'created_at': '2024-01-14T15:30:00',
        'updated_at': '2024-01-14T15:30:00',
        'read_time': 8,
        'featured': False
    }
]

for post in sample_posts:
    posts[post['id']] = post
    tags.update(post['tags'])

# 1. Get All Posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    category = request.args.get('category')
    author_id = request.args.get('author_id')
    status = request.args.get('status', 'published')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    search = request.args.get('search', '').lower()
    
    filtered_posts = []
    
    for post in posts.values():
        # Status filter
        if post['status'] != status:
            continue
        
        # Category filter
        if category and post['category'] != category:
            continue
        
        # Author filter
        if author_id and post['author_id'] != author_id:
            continue
        
        # Search filter
        if search and (search not in post['title'].lower() and 
                      search not in post['content'].lower()):
            continue
        
        filtered_posts.append(post)
    
    # Sort by created_at (newest first)
    filtered_posts.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_posts = filtered_posts[start:end]
    
    return jsonify({
        'posts': paginated_posts,
        'total': len(filtered_posts),
        'page': page,
        'limit': limit,
        'pages': (len(filtered_posts) + limit - 1) // limit
    })

# 2. Get Single Post
@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = posts.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    # Get comments for this post
    post_comments = [comment for comment in comments.values() 
                    if comment['post_id'] == post_id]
    
    # Get like count
    like_count = len([like for like in likes.values() 
                     if like['post_id'] == post_id])
    
    return jsonify({
        'post': post,
        'comments': post_comments,
        'like_count': like_count
    })

# 3. Create Post
@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['title', 'content', 'author_id', 'author_name', 'category']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if data['category'] not in categories:
        return jsonify({'error': 'Invalid category'}), 400
    
    post_id = generate_id()
    post = {
        'id': post_id,
        'title': data['title'],
        'content': data['content'],
        'author_id': data['author_id'],
        'author_name': data['author_name'],
        'category': data['category'],
        'tags': data.get('tags', []),
        'status': data.get('status', 'draft'),
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
        'read_time': len(data['content'].split()) // 200 + 1,  # Rough estimate
        'featured': data.get('featured', False)
    }
    
    posts[post_id] = post
    tags.update(post['tags'])
    
    return jsonify({
        'message': 'Post created successfully',
        'post': post
    }), 201

# 4. Update Post
@app.route('/api/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    post = posts.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    # Update fields
    for field in ['title', 'content', 'category', 'tags', 'status', 'featured']:
        if field in data:
            if field == 'category' and data[field] not in categories:
                return jsonify({'error': 'Invalid category'}), 400
            post[field] = data[field]
    
    post['updated_at'] = datetime.datetime.now().isoformat()
    if 'content' in data:
        post['read_time'] = len(data['content'].split()) // 200 + 1
    
    tags.update(post['tags'])
    
    return jsonify({
        'message': 'Post updated successfully',
        'post': post
    })

# 5. Delete Post
@app.route('/api/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    if post_id not in posts:
        return jsonify({'error': 'Post not found'}), 404
    
    # Delete associated comments
    comments_to_delete = [comment_id for comment_id, comment in comments.items() 
                         if comment['post_id'] == post_id]
    for comment_id in comments_to_delete:
        del comments[comment_id]
    
    # Delete associated likes
    likes_to_delete = [like_id for like_id, like in likes.items() 
                      if like['post_id'] == post_id]
    for like_id in likes_to_delete:
        del likes[like_id]
    
    del posts[post_id]
    return jsonify({'message': 'Post deleted successfully'})

# 6. Add Comment
@app.route('/api/posts/<post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if post_id not in posts:
        return jsonify({'error': 'Post not found'}), 404
    
    content = data.get('content')
    author_id = data.get('author_id')
    author_name = data.get('author_name')
    
    if not all([content, author_id, author_name]):
        return jsonify({'error': 'Content, author_id, and author_name required'}), 400
    
    comment_id = generate_id()
    comment = {
        'id': comment_id,
        'post_id': post_id,
        'content': content,
        'author_id': author_id,
        'author_name': author_name,
        'created_at': datetime.datetime.now().isoformat(),
        'parent_id': data.get('parent_id')  # For nested comments
    }
    
    comments[comment_id] = comment
    
    return jsonify({
        'message': 'Comment added successfully',
        'comment': comment
    }), 201

# 7. Get Comments for Post
@app.route('/api/posts/<post_id>/comments', methods=['GET'])
def get_comments(post_id):
    if post_id not in posts:
        return jsonify({'error': 'Post not found'}), 404
    
    post_comments = [comment for comment in comments.values() 
                    if comment['post_id'] == post_id]
    
    # Sort by created_at (newest first)
    post_comments.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({'comments': post_comments})

# 8. Like/Unlike Post
@app.route('/api/posts/<post_id>/like', methods=['POST'])
def toggle_like(post_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if post_id not in posts:
        return jsonify({'error': 'Post not found'}), 404
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400
    
    like_key = f"{user_id}_{post_id}"
    
    if like_key in likes:
        del likes[like_key]
        action = 'unliked'
    else:
        likes[like_key] = {
            'user_id': user_id,
            'post_id': post_id,
            'created_at': datetime.datetime.now().isoformat()
        }
        action = 'liked'
    
    like_count = len([like for like in likes.values() 
                     if like['post_id'] == post_id])
    
    return jsonify({
        'message': f'Post {action}',
        'action': action,
        'like_count': like_count
    })

# 9. Get Categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': categories})

# 10. Get Tags
@app.route('/api/tags', methods=['GET'])
def get_tags():
    return jsonify({'tags': list(tags)})

# 11. Get Posts by Tag
@app.route('/api/tags/<tag>', methods=['GET'])
def get_posts_by_tag(tag):
    tagged_posts = [post for post in posts.values() 
                   if tag in post['tags'] and post['status'] == 'published']
    
    return jsonify({
        'tag': tag,
        'posts': tagged_posts,
        'count': len(tagged_posts)
    })

# 12. Search Posts
@app.route('/api/search', methods=['GET'])
def search_posts():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    results = []
    for post in posts.values():
        if (query in post['title'].lower() or 
            query in post['content'].lower() or
            any(query in tag.lower() for tag in post['tags'])):
            results.append(post)
    
    return jsonify({
        'query': query,
        'results': results,
        'count': len(results)
    })

# 13. Get Featured Posts
@app.route('/api/posts/featured', methods=['GET'])
def get_featured_posts():
    featured_posts = [post for post in posts.values() 
                     if post['featured'] and post['status'] == 'published']
    
    return jsonify({'featured_posts': featured_posts})

# 14. Get Author Posts
@app.route('/api/authors/<author_id>/posts', methods=['GET'])
def get_author_posts(author_id):
    author_posts = [post for post in posts.values() 
                   if post['author_id'] == author_id and post['status'] == 'published']
    
    return jsonify({
        'author_id': author_id,
        'posts': author_posts,
        'count': len(author_posts)
    })

# 15. Get Blog Stats
@app.route('/api/stats', methods=['GET'])
def get_blog_stats():
    total_posts = len(posts)
    published_posts = len([p for p in posts.values() if p['status'] == 'published'])
    total_comments = len(comments)
    total_likes = len(likes)
    
    category_counts = {}
    for post in posts.values():
        cat = post['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    return jsonify({
        'total_posts': total_posts,
        'published_posts': published_posts,
        'total_comments': total_comments,
        'total_likes': total_likes,
        'categories': category_counts,
        'tags': len(tags)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5003) 
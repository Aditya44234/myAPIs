# Medium-Level Flask APIs

A collection of practical, real-world Flask APIs for learning and integration with frontend applications.

## 🚀 Available APIs

### 1. User Management API (`user_management_api.py`)
**Port: 5001**

Complete user authentication and profile management system.

**Endpoints:**
- `POST /api/register` - User registration
- `POST /api/login` - User login with JWT
- `GET /api/profile` - Get user profile (authenticated)
- `PUT /api/profile` - Update user profile (authenticated)
- `POST /api/change-password` - Change password (authenticated)
- `GET /api/users` - Get all users (admin only)
- `DELETE /api/account` - Delete account (authenticated)
- `GET /api/users/search` - Search users (authenticated)
- `POST /api/avatar` - Upload avatar (authenticated)
- `GET /api/stats` - Get user statistics (authenticated)

**Features:**
- JWT authentication
- Password hashing
- User profiles with bio, avatar, phone, address
- User search functionality
- Account management

### 2. E-commerce API (`ecommerce_api.py`)
**Port: 5002**

Full-featured e-commerce system with products, cart, and orders.

**Endpoints:**
- `GET /api/products` - Get all products with filtering
- `GET /api/products/<id>` - Get single product
- `POST /api/products` - Add new product (admin)
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product
- `POST /api/cart/add` - Add to cart
- `GET /api/cart` - Get user cart
- `PUT /api/cart/<id>` - Update cart item
- `DELETE /api/cart/<id>` - Remove from cart
- `POST /api/orders` - Create order
- `GET /api/orders` - Get user orders
- `GET /api/orders/<id>` - Get order details
- `PUT /api/orders/<id>/status` - Update order status
- `GET /api/categories` - Get product categories
- `GET /api/inventory/stats` - Get inventory statistics

**Features:**
- Product catalog with categories
- Shopping cart functionality
- Order management
- Inventory tracking
- Price filtering and search

### 3. Blog API (`blog_api.py`)
**Port: 5003**

Complete blogging platform with posts, comments, and user interactions.

**Endpoints:**
- `GET /api/posts` - Get all posts with pagination
- `GET /api/posts/<id>` - Get single post with comments
- `POST /api/posts` - Create new post
- `PUT /api/posts/<id>` - Update post
- `DELETE /api/posts/<id>` - Delete post
- `POST /api/posts/<id>/comments` - Add comment
- `GET /api/posts/<id>/comments` - Get post comments
- `POST /api/posts/<id>/like` - Like/unlike post
- `GET /api/categories` - Get post categories
- `GET /api/tags` - Get all tags
- `GET /api/tags/<tag>` - Get posts by tag
- `GET /api/search` - Search posts
- `GET /api/posts/featured` - Get featured posts
- `GET /api/authors/<id>/posts` - Get author posts
- `GET /api/stats` - Get blog statistics

**Features:**
- Post management with categories and tags
- Comment system
- Like/unlike functionality
- Search and filtering
- Featured posts
- Author profiles

### 4. Task Management API (`task_management_api.py`)
**Port: 5004**

Project and task management system with assignments and progress tracking.

**Endpoints:**
- `GET /api/projects` - Get all projects
- `GET /api/projects/<id>` - Get project with tasks and progress
- `POST /api/projects` - Create new project
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project
- `GET /api/tasks` - Get all tasks with filtering
- `GET /api/tasks/<id>` - Get single task with comments
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task
- `POST /api/tasks/<id>/comments` - Add task comment
- `GET /api/dashboard/<user_id>` - Get user dashboard
- `GET /api/projects/<id>/progress` - Get project progress
- `GET /api/users` - Get all users
- `GET /api/stats/tasks` - Get task statistics

**Features:**
- Project management
- Task assignment and tracking
- Progress monitoring
- User dashboards
- Time tracking (estimated vs actual hours)
- Priority and status management

### 5. Weather API (`weather_api.py`)
**Port: 5005**

Weather information system with current conditions and forecasts.

**Endpoints:**
- `GET /api/weather/current` - Get current weather
- `GET /api/weather/forecast` - Get weather forecast
- `GET /api/weather/coordinates` - Get weather by coordinates
- `GET /api/weather/multiple` - Get weather for multiple cities
- `GET /api/weather/alerts` - Get weather alerts
- `GET /api/weather/historical` - Get historical weather
- `GET /api/weather/stats` - Get weather statistics
- `GET /api/weather/cities` - Search cities
- `GET /api/weather/map` - Get weather map data
- `GET /api/weather/air-quality` - Get air quality
- `GET /api/weather/sun-times` - Get sunrise/sunset times
- `GET /api/weather/compare` - Compare weather between cities
- `GET /api/weather/trends` - Get weather trends
- `GET /api/weather/recommendations` - Get weather recommendations
- `GET /api/weather/status` - Get API status

**Features:**
- Current weather conditions
- 5-day forecasts
- Weather alerts
- Air quality data
- Sunrise/sunset times
- Weather comparisons
- Clothing and activity recommendations

## 🛠️ Installation & Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Individual APIs:**
   ```bash
   # User Management API
   python user_management_api.py
   
   # E-commerce API
   python ecommerce_api.py
   
   # Blog API
   python blog_api.py
   
   # Task Management API
   python task_management_api.py
   
   # Weather API
   python weather_api.py
   ```

3. **Test the APIs:**
   - User Management: http://localhost:5001
   - E-commerce: http://localhost:5002
   - Blog: http://localhost:5003
   - Task Management: http://localhost:5004
   - Weather: http://localhost:5005

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the `medium_apis` directory:

```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### JWT Configuration
For the User Management API, update the secret key in `user_management_api.py`:
```python
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
```

## 📝 API Usage Examples

### User Management API
```bash
# Register a new user
curl -X POST http://localhost:5001/api/register \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "password123"}'

# Get profile (with token)
curl -X GET http://localhost:5001/api/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### E-commerce API
```bash
# Get all products
curl http://localhost:5002/api/products

# Add to cart
curl -X POST http://localhost:5002/api/cart/add \
  -H "Content-Type: application/json" \
  -d '{"product_id": "1", "quantity": 2, "user_id": "user123"}'

# Create order
curl -X POST http://localhost:5002/api/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "shipping_address": "123 Main St"}'
```

### Blog API
```bash
# Get all posts
curl http://localhost:5003/api/posts

# Create a post
curl -X POST http://localhost:5003/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello World!", "author_id": "user1", "author_name": "John Doe", "category": "technology"}'

# Like a post
curl -X POST http://localhost:5003/api/posts/1/like \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user1"}'
```

### Task Management API
```bash
# Get all projects
curl http://localhost:5004/api/projects

# Create a project
curl -X POST http://localhost:5004/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Website Redesign", "description": "Redesign company website", "owner_id": "user1"}'

# Create a task
curl -X POST http://localhost:5004/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Design Homepage", "description": "Create wireframes", "project_id": "proj1", "assigned_to": "user2"}'
```

### Weather API
```bash
# Get current weather
curl "http://localhost:5005/api/weather/current?city=New%20York"

# Get forecast
curl "http://localhost:5005/api/weather/forecast?city=London&days=3"

# Get weather by coordinates
curl "http://localhost:5005/api/weather/coordinates?lat=40.7128&lon=-74.0060"
```

## 🔒 Authentication

Most APIs use JWT tokens for authentication. To use protected endpoints:

1. Login to get a token
2. Include the token in the Authorization header:
   ```
   Authorization: Bearer YOUR_JWT_TOKEN
   ```

## 📊 Data Storage

All APIs use in-memory storage for demonstration purposes. In production:

1. Replace with a proper database (PostgreSQL, MongoDB, etc.)
2. Implement proper data persistence
3. Add data validation and sanitization
4. Implement proper error handling

## 🚀 Frontend Integration

These APIs are designed to work seamlessly with frontend frameworks:

- **React/Vue/Angular**: Use fetch or axios for HTTP requests
- **Mobile Apps**: Use the same REST endpoints
- **Desktop Apps**: Integrate via HTTP client libraries

## 🔧 Customization

Each API can be customized for your specific needs:

1. **Add new endpoints** for specific functionality
2. **Modify data models** to match your requirements
3. **Add validation** for better data integrity
4. **Implement caching** for better performance
5. **Add rate limiting** for API protection

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [JWT Authentication](https://jwt.io/)
- [REST API Best Practices](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)

## 🤝 Contributing

Feel free to:
- Add new features
- Improve existing endpoints
- Fix bugs
- Add better documentation
- Create new API modules

## 📄 License

This project is open source and available under the MIT License. 
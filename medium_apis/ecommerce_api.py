from flask import Flask, request, jsonify
import uuid
import datetime
from functools import wraps

app = Flask(__name__)

# In-memory storage
products = {}
cart_items = {}
orders = {}
categories = {
    'electronics': 'Electronic devices and gadgets',
    'clothing': 'Fashion and apparel',
    'books': 'Books and literature',
    'home': 'Home and garden',
    'sports': 'Sports and fitness'
}

def generate_id():
    return str(uuid.uuid4())

# Sample products
sample_products = [
    {
        'id': '1',
        'name': 'iPhone 15 Pro',
        'description': 'Latest iPhone with advanced features',
        'price': 999.99,
        'category': 'electronics',
        'stock': 50,
        'images': ['iphone1.jpg', 'iphone2.jpg'],
        'rating': 4.8,
        'reviews': 1250
    },
    {
        'id': '2',
        'name': 'Nike Air Max',
        'description': 'Comfortable running shoes',
        'price': 129.99,
        'category': 'sports',
        'stock': 100,
        'images': ['nike1.jpg'],
        'rating': 4.5,
        'reviews': 890
    }
]

for product in sample_products:
    products[product['id']] = product

# 1. Get All Products
@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    search = request.args.get('search', '').lower()
    
    filtered_products = []
    
    for product in products.values():
        # Category filter
        if category and product['category'] != category:
            continue
        
        # Price filter
        if min_price and product['price'] < min_price:
            continue
        if max_price and product['price'] > max_price:
            continue
        
        # Search filter
        if search and search not in product['name'].lower():
            continue
        
        filtered_products.append(product)
    
    return jsonify({
        'products': filtered_products,
        'total': len(filtered_products)
    })

# 2. Get Single Product
@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({'product': product})

# 3. Add Product to Cart
@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    user_id = data.get('user_id', 'anonymous')
    
    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400
    
    product = products.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    if product['stock'] < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    cart_key = f"{user_id}_{product_id}"
    
    if cart_key in cart_items:
        cart_items[cart_key]['quantity'] += quantity
    else:
        cart_items[cart_key] = {
            'user_id': user_id,
            'product_id': product_id,
            'quantity': quantity,
            'added_at': datetime.datetime.now().isoformat()
        }
    
    return jsonify({
        'message': 'Product added to cart',
        'cart_item': cart_items[cart_key]
    })

# 4. Get Cart
@app.route('/api/cart', methods=['GET'])
def get_cart():
    user_id = request.args.get('user_id', 'anonymous')
    
    user_cart = []
    total = 0
    
    for cart_key, item in cart_items.items():
        if item['user_id'] == user_id:
            product = products.get(item['product_id'])
            if product:
                cart_item = {
                    'id': cart_key,
                    'product': product,
                    'quantity': item['quantity'],
                    'subtotal': product['price'] * item['quantity'],
                    'added_at': item['added_at']
                }
                user_cart.append(cart_item)
                total += cart_item['subtotal']
    
    return jsonify({
        'cart_items': user_cart,
        'total': total,
        'item_count': len(user_cart)
    })

# 5. Update Cart Item
@app.route('/api/cart/<cart_item_id>', methods=['PUT'])
def update_cart_item(cart_item_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    quantity = data.get('quantity')
    if quantity is None:
        return jsonify({'error': 'Quantity required'}), 400
    
    if cart_item_id not in cart_items:
        return jsonify({'error': 'Cart item not found'}), 404
    
    cart_item = cart_items[cart_item_id]
    product = products.get(cart_item['product_id'])
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    if product['stock'] < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    if quantity <= 0:
        del cart_items[cart_item_id]
        return jsonify({'message': 'Item removed from cart'})
    
    cart_item['quantity'] = quantity
    return jsonify({
        'message': 'Cart updated',
        'cart_item': cart_item
    })

# 6. Remove from Cart
@app.route('/api/cart/<cart_item_id>', methods=['DELETE'])
def remove_from_cart(cart_item_id):
    if cart_item_id not in cart_items:
        return jsonify({'error': 'Cart item not found'}), 404
    
    del cart_items[cart_item_id]
    return jsonify({'message': 'Item removed from cart'})

# 7. Create Order
@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    user_id = data.get('user_id')
    shipping_address = data.get('shipping_address')
    
    if not all([user_id, shipping_address]):
        return jsonify({'error': 'User ID and shipping address required'}), 400
    
    # Get user's cart
    user_cart = []
    total = 0
    
    for cart_key, item in cart_items.items():
        if item['user_id'] == user_id:
            product = products.get(item['product_id'])
            if product:
                if product['stock'] < item['quantity']:
                    return jsonify({'error': f'Insufficient stock for {product["name"]}'}), 400
                
                user_cart.append({
                    'product_id': item['product_id'],
                    'quantity': item['quantity'],
                    'price': product['price'],
                    'subtotal': product['price'] * item['quantity']
                })
                total += product['price'] * item['quantity']
    
    if not user_cart:
        return jsonify({'error': 'Cart is empty'}), 400
    
    # Create order
    order_id = generate_id()
    order = {
        'id': order_id,
        'user_id': user_id,
        'items': user_cart,
        'total': total,
        'shipping_address': shipping_address,
        'status': 'pending',
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    }
    
    orders[order_id] = order
    
    # Update stock
    for item in user_cart:
        product = products[item['product_id']]
        product['stock'] -= item['quantity']
    
    # Clear cart
    cart_keys_to_remove = [key for key, item in cart_items.items() if item['user_id'] == user_id]
    for key in cart_keys_to_remove:
        del cart_items[key]
    
    return jsonify({
        'message': 'Order created successfully',
        'order': order
    }), 201

# 8. Get User Orders
@app.route('/api/orders', methods=['GET'])
def get_orders():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400
    
    user_orders = [order for order in orders.values() if order['user_id'] == user_id]
    return jsonify({'orders': user_orders})

# 9. Get Order Details
@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify({'order': order})

# 10. Update Order Status
@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    status = data.get('status')
    if not status:
        return jsonify({'error': 'Status required'}), 400
    
    order = orders.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    order['status'] = status
    order['updated_at'] = datetime.datetime.now().isoformat()
    
    return jsonify({
        'message': 'Order status updated',
        'order': order
    })

# 11. Get Categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': categories})

# 12. Add Product (Admin)
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['name', 'description', 'price', 'category', 'stock']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if data['category'] not in categories:
        return jsonify({'error': 'Invalid category'}), 400
    
    product_id = generate_id()
    product = {
        'id': product_id,
        'name': data['name'],
        'description': data['description'],
        'price': float(data['price']),
        'category': data['category'],
        'stock': int(data['stock']),
        'images': data.get('images', []),
        'rating': 0.0,
        'reviews': 0
    }
    
    products[product_id] = product
    
    return jsonify({
        'message': 'Product added successfully',
        'product': product
    }), 201

# 13. Update Product
@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    product = products.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Update fields
    for field in ['name', 'description', 'price', 'category', 'stock', 'images']:
        if field in data:
            if field == 'price':
                product[field] = float(data[field])
            elif field == 'stock':
                product[field] = int(data[field])
            else:
                product[field] = data[field]
    
    return jsonify({
        'message': 'Product updated successfully',
        'product': product
    })

# 14. Delete Product
@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    if product_id not in products:
        return jsonify({'error': 'Product not found'}), 404
    
    del products[product_id]
    return jsonify({'message': 'Product deleted successfully'})

# 15. Get Inventory Stats
@app.route('/api/inventory/stats', methods=['GET'])
def get_inventory_stats():
    total_products = len(products)
    total_stock = sum(product['stock'] for product in products.values())
    low_stock = len([p for p in products.values() if p['stock'] < 10])
    
    category_stats = {}
    for product in products.values():
        cat = product['category']
        if cat not in category_stats:
            category_stats[cat] = {'count': 0, 'stock': 0}
        category_stats[cat]['count'] += 1
        category_stats[cat]['stock'] += product['stock']
    
    return jsonify({
        'total_products': total_products,
        'total_stock': total_stock,
        'low_stock_items': low_stock,
        'category_stats': category_stats
    })

if __name__ == '__main__':
    app.run(debug=True, port=5002) 
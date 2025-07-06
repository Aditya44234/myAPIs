from flask import Flask, request, jsonify
import requests
import datetime
import random
from functools import wraps

app = Flask(__name__)

# Mock weather data (in real app, use actual weather API)
weather_data = {
    'New York': {
        'current': {
            'temperature': 22,
            'feels_like': 24,
            'humidity': 65,
            'wind_speed': 12,
            'description': 'Partly cloudy',
            'icon': 'partly-cloudy-day'
        },
        'forecast': [
            {'date': '2024-01-16', 'high': 25, 'low': 18, 'description': 'Sunny'},
            {'date': '2024-01-17', 'high': 28, 'low': 20, 'description': 'Partly cloudy'},
            {'date': '2024-01-18', 'high': 22, 'low': 15, 'description': 'Rainy'},
            {'date': '2024-01-19', 'high': 26, 'low': 19, 'description': 'Clear'},
            {'date': '2024-01-20', 'high': 24, 'low': 17, 'description': 'Cloudy'}
        ]
    },
    'London': {
        'current': {
            'temperature': 8,
            'feels_like': 6,
            'humidity': 80,
            'wind_speed': 15,
            'description': 'Rainy',
            'icon': 'rain'
        },
        'forecast': [
            {'date': '2024-01-16', 'high': 10, 'low': 5, 'description': 'Rainy'},
            {'date': '2024-01-17', 'high': 12, 'low': 7, 'description': 'Cloudy'},
            {'date': '2024-01-18', 'high': 9, 'low': 4, 'description': 'Rainy'},
            {'date': '2024-01-19', 'high': 11, 'low': 6, 'description': 'Partly cloudy'},
            {'date': '2024-01-20', 'high': 13, 'low': 8, 'description': 'Sunny'}
        ]
    },
    'Tokyo': {
        'current': {
            'temperature': 15,
            'feels_like': 16,
            'humidity': 70,
            'wind_speed': 8,
            'description': 'Clear',
            'icon': 'clear-day'
        },
        'forecast': [
            {'date': '2024-01-16', 'high': 18, 'low': 12, 'description': 'Clear'},
            {'date': '2024-01-17', 'high': 20, 'low': 14, 'description': 'Sunny'},
            {'date': '2024-01-18', 'high': 16, 'low': 10, 'description': 'Cloudy'},
            {'date': '2024-01-19', 'high': 19, 'low': 13, 'description': 'Partly cloudy'},
            {'date': '2024-01-20', 'high': 17, 'low': 11, 'description': 'Rainy'}
        ]
    }
}

# 1. Get Current Weather
@app.route('/api/weather/current', methods=['GET'])
def get_current_weather():
    city = request.args.get('city', 'New York')
    
    if city not in weather_data:
        return jsonify({'error': 'City not found'}), 404
    
    current = weather_data[city]['current']
    current['city'] = city
    current['timestamp'] = datetime.datetime.now().isoformat()
    
    return jsonify({'weather': current})

# 2. Get Weather Forecast
@app.route('/api/weather/forecast', methods=['GET'])
def get_weather_forecast():
    city = request.args.get('city', 'New York')
    days = request.args.get('days', 5, type=int)
    
    if city not in weather_data:
        return jsonify({'error': 'City not found'}), 404
    
    forecast = weather_data[city]['forecast'][:days]
    
    return jsonify({
        'city': city,
        'forecast': forecast,
        'days': len(forecast)
    })

# 3. Get Weather by Coordinates
@app.route('/api/weather/coordinates', methods=['GET'])
def get_weather_by_coordinates():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude required'}), 400
    
    # Mock: find nearest city (in real app, use reverse geocoding)
    # For demo, return New York weather
    city = 'New York'
    current = weather_data[city]['current']
    current['city'] = city
    current['coordinates'] = {'lat': lat, 'lon': lon}
    current['timestamp'] = datetime.datetime.now().isoformat()
    
    return jsonify({'weather': current})

# 4. Get Multiple Cities Weather
@app.route('/api/weather/multiple', methods=['GET'])
def get_multiple_cities_weather():
    cities = request.args.get('cities', 'New York,London,Tokyo').split(',')
    
    result = []
    for city in cities:
        city = city.strip()
        if city in weather_data:
            current = weather_data[city]['current'].copy()
            current['city'] = city
            current['timestamp'] = datetime.datetime.now().isoformat()
            result.append(current)
    
    return jsonify({'weather': result})

# 5. Get Weather Alerts
@app.route('/api/weather/alerts', methods=['GET'])
def get_weather_alerts():
    city = request.args.get('city', 'New York')
    
    # Mock alerts
    alerts = []
    if city == 'London':
        alerts.append({
            'type': 'rain',
            'severity': 'moderate',
            'description': 'Heavy rain expected',
            'start_time': '2024-01-16T10:00:00',
            'end_time': '2024-01-16T18:00:00'
        })
    elif city == 'Tokyo':
        alerts.append({
            'type': 'wind',
            'severity': 'low',
            'description': 'Strong winds expected',
            'start_time': '2024-01-17T14:00:00',
            'end_time': '2024-01-17T20:00:00'
        })
    
    return jsonify({
        'city': city,
        'alerts': alerts,
        'count': len(alerts)
    })

# 6. Get Historical Weather
@app.route('/api/weather/historical', methods=['GET'])
def get_historical_weather():
    city = request.args.get('city', 'New York')
    date = request.args.get('date')
    
    if not date:
        return jsonify({'error': 'Date required'}), 400
    
    # Mock historical data
    historical = {
        'city': city,
        'date': date,
        'temperature': {
            'max': random.randint(20, 30),
            'min': random.randint(10, 20),
            'average': random.randint(15, 25)
        },
        'precipitation': random.randint(0, 50),
        'humidity': random.randint(40, 90),
        'wind_speed': random.randint(5, 25)
    }
    
    return jsonify({'historical': historical})

# 7. Get Weather Statistics
@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    city = request.args.get('city', 'New York')
    
    if city not in weather_data:
        return jsonify({'error': 'City not found'}), 404
    
    forecast = weather_data[city]['forecast']
    current = weather_data[city]['current']
    
    temperatures = [day['high'] for day in forecast] + [current['temperature']]
    
    stats = {
        'city': city,
        'current_temperature': current['temperature'],
        'average_high': sum(temperatures) / len(temperatures),
        'max_high': max(temperatures),
        'min_high': min(temperatures),
        'current_humidity': current['humidity'],
        'current_wind_speed': current['wind_speed']
    }
    
    return jsonify({'stats': stats})

# 8. Search Cities
@app.route('/api/weather/cities', methods=['GET'])
def search_cities():
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    matching_cities = [city for city in weather_data.keys() 
                      if query in city.lower()]
    
    return jsonify({
        'query': query,
        'cities': matching_cities,
        'count': len(matching_cities)
    })

# 9. Get Weather Map Data
@app.route('/api/weather/map', methods=['GET'])
def get_weather_map_data():
    # Mock map data with multiple cities
    map_data = []
    
    for city, data in weather_data.items():
        map_data.append({
            'city': city,
            'temperature': data['current']['temperature'],
            'description': data['current']['description'],
            'icon': data['current']['icon'],
            'coordinates': {
                'New York': {'lat': 40.7128, 'lon': -74.0060},
                'London': {'lat': 51.5074, 'lon': -0.1278},
                'Tokyo': {'lat': 35.6762, 'lon': 139.6503}
            }.get(city, {'lat': 0, 'lon': 0})
        })
    
    return jsonify({'map_data': map_data})

# 10. Get Air Quality
@app.route('/api/weather/air-quality', methods=['GET'])
def get_air_quality():
    city = request.args.get('city', 'New York')
    
    # Mock air quality data
    aqi_data = {
        'city': city,
        'aqi': random.randint(20, 150),
        'category': random.choice(['Good', 'Moderate', 'Unhealthy for Sensitive Groups']),
        'pollutants': {
            'pm25': random.randint(5, 35),
            'pm10': random.randint(10, 50),
            'o3': random.randint(20, 80),
            'no2': random.randint(10, 40)
        },
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    return jsonify({'air_quality': aqi_data})

# 11. Get Sunrise/Sunset Times
@app.route('/api/weather/sun-times', methods=['GET'])
def get_sun_times():
    city = request.args.get('city', 'New York')
    date = request.args.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))
    
    # Mock sun times
    sun_times = {
        'city': city,
        'date': date,
        'sunrise': '06:30',
        'sunset': '17:45',
        'day_length': '11h 15m',
        'civil_twilight_begin': '06:05',
        'civil_twilight_end': '18:10'
    }
    
    return jsonify({'sun_times': sun_times})

# 12. Get Weather Comparison
@app.route('/api/weather/compare', methods=['GET'])
def compare_weather():
    cities = request.args.get('cities', 'New York,London').split(',')
    
    if len(cities) < 2:
        return jsonify({'error': 'At least 2 cities required'}), 400
    
    comparison = []
    for city in cities:
        city = city.strip()
        if city in weather_data:
            current = weather_data[city]['current'].copy()
            current['city'] = city
            comparison.append(current)
    
    return jsonify({'comparison': comparison})

# 13. Get Weather Trends
@app.route('/api/weather/trends', methods=['GET'])
def get_weather_trends():
    city = request.args.get('city', 'New York')
    days = request.args.get('days', 7, type=int)
    
    if city not in weather_data:
        return jsonify({'error': 'City not found'}), 404
    
    # Mock trend data
    trends = []
    base_temp = weather_data[city]['current']['temperature']
    
    for i in range(days):
        date = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        temp_change = random.randint(-5, 5)
        trends.append({
            'date': date,
            'temperature': base_temp + temp_change,
            'trend': 'increasing' if temp_change > 0 else 'decreasing' if temp_change < 0 else 'stable'
        })
    
    return jsonify({
        'city': city,
        'trends': trends,
        'days': days
    })

# 14. Get Weather Recommendations
@app.route('/api/weather/recommendations', methods=['GET'])
def get_weather_recommendations():
    city = request.args.get('city', 'New York')
    
    if city not in weather_data:
        return jsonify({'error': 'City not found'}), 404
    
    current = weather_data[city]['current']
    temp = current['temperature']
    description = current['description'].lower()
    
    recommendations = {
        'city': city,
        'clothing': [],
        'activities': [],
        'precautions': []
    }
    
    # Clothing recommendations
    if temp < 10:
        recommendations['clothing'].extend(['Heavy coat', 'Scarf', 'Gloves'])
    elif temp < 20:
        recommendations['clothing'].extend(['Light jacket', 'Long sleeves'])
    else:
        recommendations['clothing'].extend(['T-shirt', 'Shorts'])
    
    # Activity recommendations
    if 'rain' in description:
        recommendations['activities'].extend(['Indoor activities', 'Reading', 'Movies'])
        recommendations['precautions'].append('Bring umbrella')
    elif 'sunny' in description or 'clear' in description:
        recommendations['activities'].extend(['Outdoor sports', 'Picnic', 'Walking'])
        recommendations['precautions'].append('Use sunscreen')
    else:
        recommendations['activities'].extend(['Light outdoor activities', 'Shopping'])
    
    return jsonify({'recommendations': recommendations})

# 15. Get Weather API Status
@app.route('/api/weather/status', methods=['GET'])
def get_weather_api_status():
    return jsonify({
        'status': 'operational',
        'version': '1.0.0',
        'available_cities': list(weather_data.keys()),
        'last_updated': datetime.datetime.now().isoformat(),
        'features': [
            'Current weather',
            '5-day forecast',
            'Weather alerts',
            'Air quality',
            'Sun times',
            'Historical data'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5005) 
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ecosort']

# Seed admin user
db.users.insert_one({
    'email': 'admin@example.com',
    'password': 'admin123',  # In production, hash the password
    'location': 'admin',
    'is_admin': True
})

# Seed regular users
db.users.insert_many([
    {
        'email': 'user1@example.com',
        'password': 'user123',
        'location': 'New York',
        'bio_waste': 5,
        'non_bio_waste': 3,
        'drives': 2
    },
    {
        'email': 'user2@example.com',
        'password': 'user456',
        'location': 'San Francisco',
        'bio_waste': 2,
        'non_bio_waste': 6,
        'drives': 1
    }
])

# Seed events
db.events.insert_many([
    {
        'title': 'Beach Cleanup Drive',
        'location': 'New York',
        'date': '2025-02-10',
        'time': '10:00 AM'
    },
    {
        'title': 'Park Restoration',
        'location': 'San Francisco',
        'date': '2025-02-15',
        'time': '09:00 AM'
    }
])

print("Data seeded successfully!")

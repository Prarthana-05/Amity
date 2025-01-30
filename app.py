# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from pymongo import MongoClient

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# # MongoDB setup
# client = MongoClient('mongodb://localhost:27017/')
# db = client['ecosort']
# users_collection = db['users']
# events_collection = db['events']

# # Routes
# @app.route('/')
# def index():
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         # Admin login
#         if email == 'admin@example.com' and password == 'admin123':
#             session['email'] = email
#             session['is_admin'] = True
#             return redirect(url_for('admin_dashboard'))

#         # User login
#         user = users_collection.find_one({'email': email, 'password': password})
#         if user:
#             session['email'] = email
#             session['is_admin'] = False
#             session['location'] = user['location']
#             return redirect(url_for('user_dashboard'))

#         flash('Invalid credentials', 'danger')
#         return redirect(url_for('login'))
#     return render_template('login.html')

# @app.route('/user/dashboard')
# def user_dashboard():
#     if 'email' in session and not session.get('is_admin'):
#         return render_template('user_dashboard.html')
#     return redirect(url_for('login'))

# @app.route('/admin/dashboard')
# def admin_dashboard():
#     if 'email' in session and session.get('is_admin'):
#         users = users_collection.find()
#         return render_template('admin_dashboard.html', users=users)
#     return redirect(url_for('login'))

# @app.route('/admin/update/<email>', methods=['GET', 'POST'])
# def update_user(email):
#     if 'email' in session and session.get('is_admin'):
#         user = users_collection.find_one({'email': email})
#         if request.method == 'POST':
#             bio_waste = request.form['bio_waste']
#             non_bio_waste = request.form['non_bio_waste']
#             drives = request.form['drives']

#             users_collection.update_one({'email': email}, {
#                 '$set': {'bio_waste': int(bio_waste), 'non_bio_waste': int(non_bio_waste), 'drives': int(drives)}
#             })
#             flash('User data updated', 'success')
#             return redirect(url_for('admin_dashboard'))

#         return render_template('update_user.html', user=user)
#     return redirect(url_for('login'))

# @app.route('/rewards', methods=['GET', 'POST'])
# def rewards():
#     if 'email' in session and not session.get('is_admin'):
#         user = users_collection.find_one({'email': session['email']})
#         if request.method == 'POST':
#             bio_waste = int(request.form['bio_waste'])
#             non_bio_waste = int(request.form['non_bio_waste'])

#             if bio_waste > non_bio_waste:
#                 reward_message = "Great job! You've earned 5 stars for focusing on biodegradable waste."
#             else:
#                 reward_message = "Try to focus on reducing non-biodegradable waste. You've earned 2 stars."

#             return render_template('rewards.html', message=reward_message)

#         return render_template('rewards.html', user=user)
#     return redirect(url_for('login'))

# @app.route('/tips')
# def tips():
#     if 'email' in session and not session.get('is_admin'):
#         user = users_collection.find_one({'email': session['email']})
#         if user['bio_waste'] > user['non_bio_waste']:
#             tips_message = "Focus on composting your biodegradable waste efficiently."
#         else:
#             tips_message = "Try to recycle non-biodegradable waste like plastic and glass."

#         return render_template('tips.html', tips_message=tips_message)
#     return redirect(url_for('login'))

# @app.route('/events')
# def events():
#     if 'email' in session and not session.get('is_admin'):
#         location = session['location']
#         events = events_collection.find({'location': location})
#         return render_template('events.html', events=events)
#     return redirect(url_for('login'))

# @app.route('/segregation_guide', methods=['GET', 'POST'])
# def segregation_guide():
#     if 'email' in session and not session.get('is_admin'):
#         if request.method == 'POST':
#             item = request.form['item'].lower()
#             if item in ['vegetable waste', 'fruit peels', 'paper']:
#                 response = "Yes, it's biodegradable. You can compost it!"
#             else:
#                 response = "No, it's not biodegradable. Please recycle it appropriately."
#             return render_template('segregation_guide.html', response=response)

#         return render_template('segregation_guide.html')
#     return redirect(url_for('login'))

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['ecosort']
users_collection = db['users']
events_collection = db['events']
tips_collection = db['tips']
segregation_guide_collection = db['segregation_guide']

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Admin login
        if email == 'admin@example.com' and password == 'admin123':
            session['email'] = email
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))

        # User login
        user = users_collection.find_one({'email': email, 'password': password})
        if user:
            session['email'] = email
            session['is_admin'] = False
            session['location'] = user['location']
            return redirect(url_for('user_dashboard'))

        flash('Invalid credentials', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/user/dashboard')
def user_dashboard():
    if 'email' in session and not session.get('is_admin'):
        return render_template('user_dashboard.html')
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'email' in session and session.get('is_admin'):
        users = users_collection.find()
        return render_template('admin_dashboard.html', users=users)
    return redirect(url_for('login'))

@app.route('/admin/update/<email>', methods=['GET', 'POST'])
def update_user(email):
    if 'email' in session and session.get('is_admin'):
        user = users_collection.find_one({'email': email})
        if request.method == 'POST':
            bio_waste = int(request.form['bio_waste'])
            non_bio_waste = int(request.form['non_bio_waste'])
            drives = int(request.form['drives'])

            users_collection.update_one({'email': email}, {
                '$set': {'bio_waste': bio_waste, 'non_bio_waste': non_bio_waste, 'drives': drives}
            })
            flash('User data updated', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('update_user.html', user=user)
    return redirect(url_for('login'))


@app.route('/rewards', methods=['GET', 'POST'])
def rewards():
    if request.method == 'POST':
        bio_waste = int(request.form['bio_waste'])
        non_bio_waste = int(request.form['non_bio_waste'])

        # Check if the user is logged in
        if 'email' in session:
            user_email = session['email']

            # Save bio_waste and non_bio_waste in the user's record
            users_collection.update_one(
                {'email': user_email},
                {'$set': {'bio_waste': bio_waste, 'non_bio_waste': non_bio_waste}}
            )

        # Redirect to reload rewards page with updated data
        return redirect(url_for('rewards'))

    if 'email' in session:
        user = users_collection.find_one({'email': session['email']})

        # Fetch bio_waste and non_bio_waste from user's data
        bio_waste = user.get('bio_waste', 0)
        non_bio_waste = user.get('non_bio_waste', 0)

        # Rewards logic
        if bio_waste > non_bio_waste:
            reward_message = f"Great job! You earned {int(bio_waste * 10)} stars for managing {bio_waste} kg of biodegradable waste!"
        else:
            reward_message = f"You generated more non-biodegradable waste ({non_bio_waste} kg). Try to reduce it to earn more stars!"

        return render_template('rewards.html', reward_message=reward_message, bio_waste=bio_waste, non_bio_waste=non_bio_waste)

    return redirect(url_for('login'))



@app.route('/events')
def events():
    if 'email' in session and not session.get('is_admin'):
        location = session['location']
        events = events_collection.find({'location': location})
        return render_template('events.html', events=events)
    return redirect(url_for('login'))

@app.route('/segregation_guide', methods=['GET', 'POST'])
def segregation_guide():
    if 'email' in session and not session.get('is_admin'):
        if request.method == 'POST':
            item = request.form['item'].lower()
            category = request.form['category'].lower()

            if category == 'biodegradable':
                composting_tips = segregation_guide_collection.find_one({'category': 'biodegradable', 'item': item})
                if composting_tips:
                    response = f"Yes, {item} is biodegradable. Here's how to compost it: {composting_tips['guide']}"
                else:
                    response = "This is biodegradable, but no specific composting guide is available."
            elif category == 'non-biodegradable':
                recycling_tips = segregation_guide_collection.find_one({'category': 'non-biodegradable', 'item': item})
                if recycling_tips:
                    response = f"No, {item} is not biodegradable. Please dispose of it properly: {recycling_tips['guide']}"
                else:
                    response = "This is non-biodegradable, but no specific disposal guide is available."
            else:
                response = "Please specify whether the item is biodegradable or non-biodegradable."

            return render_template('segregation_guide.html', response=response)

        return render_template('segregation_guide.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)





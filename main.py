from website import create_app, db
from website.models import Interest
# from website import socketio
import time
import psycopg2
import os


while True:
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        conn.close()
        print("✅ Postgres is ready!")
        break
    except:
        print("Waiting for Postgres...")
        time.sleep(2)

print("Starting app...")
app = create_app()

# interests = [
#     # Hobbies & Activities
#     "Traveling", "Hiking / Nature", "Camping", "Photography",
#     "Reading / Books", "Writing / Journaling", "Cooking / Baking",
#     "Gardening", "Painting / Drawing", "DIY / Crafts", "Dancing",
#     "Singing / Music", "Playing instruments", "Gaming (Video / Board)",
#     "Yoga / Meditation", "Fitness / Gym", "Sports", "Biking / Cycling",
#     "Running / Marathon", "Swimming", "Adventure sports",

#     # Lifestyle & Personality
#     "Night owl", "Early bird", "Introvert", "Extrovert",
#     "Ambitious", "Funny / Humor", "Romantic", "Geek / Nerd",
#     "Creative", "Intellectual / Curious", "Fashion / Style",
#     "Vegan / Vegetarian", "Foodie", "Traveler",

#     # Entertainment & Media
#     "Movies", "TV Series / Netflix", "Anime / Manga",
#     "Comics / Graphic Novels", "Music", "Podcasts",
#     "Gaming (PC, Console, Mobile)", "Theater / Performing Arts",

#     # Social & Community Interests
#     "Volunteering", "Charity work", "Environmental activism",
#     "Social justice / Causes", "Tech / Startups",
#     "Entrepreneurship", "Networking", "Politics / Debates",

#     # Romantic / Dating Preferences
#     "Casual dating", "Serious relationship", "Open-minded",
#     "Polyamory", "LGBTQ+ friendly", "Kisses & cuddles",
#     "Intellectual connection", "Adventure partner",

#     # Random / Fun Interests
#     "Memes / Internet culture", "Astrology / Zodiac", "Coffee / Tea lover",
#     "Cats / Dogs / Pets", "Board games / Puzzles", "Cars / Motorcycles",
#     "Travel photography", "Festivals / Concerts", "Wine / Beer tasting"
# ]

# categories = [
#     ("Hobbies & Activities", 21),
#     ("Lifestyle & Personality", 14),
#     ("Entertainment & Media", 8),
#     ("Social & Community Interests", 8),
#     ("Romantic / Dating Preferences", 8),
#     ("Random / Fun Interests", 9)
# ]

# with app.app_context():
#     start = 0
#     for cat_name, count in categories:
#         for interest_name in interests[start:start+count]:
#             interest = Interest(name=interest_name, category=cat_name)
#             db.session.add(interest)
#         start += count
#     db.session.commit()
#     print("Interests added!")
    
    
if __name__ == '__main__':
    # socketio.run(app, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)

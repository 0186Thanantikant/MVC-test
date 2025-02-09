from flask import Flask, render_template, request, jsonify
import json
import random

web = Flask(__name__)

db_file = "database.json"

# M - about database keep data connect data
class SuitModel:
    @staticmethod
    def load_database():
        with open(db_file, "r") as file:
            return json.load(file)

    @staticmethod
    def save_database(data):
        with open(db_file, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def generate_sample_data():
        suits = []
        types = ["ชุดทรงพลัง", "ชุดลอบเร้น", "ชุดปกปิดตัวตน"]
        for i in range(50):
            suit_id = str(random.randint(1, 9)) + str(random.randint(10000, 99999))
            suit_type = random.choice(types)
            durability = random.randint(0, 100)
            suits.append({"id": suit_id, "type": suit_type, "durability": durability})
        SuitModel.save_database(suits)

    @staticmethod
    def validate_suit(suit):
        if suit["type"] == "ชุดทรงพลัง" and suit["durability"] < 70:
            return False
        if suit["type"] == "ชุดลอบเร้น" and suit["durability"] < 50:
            return False
        if suit["type"] == "ชุดปกปิดตัวตน" and str(suit["durability"])[-1] in ["3", "7"]:
            return False
        return True

# C - input from user and process 
@web.route("/")
def home():
    return render_template("index.html")

@web.route("/check", methods=["POST"])
def check_suit():
    suit_id = request.form.get("suit_id")
    database = SuitModel.load_database()
    suit = next((s for s in database if s["id"] == suit_id), None)
    
    if not suit:
        return render_template("result.html", error="ชุดไม่พบในฐานข้อมูล")
    
    is_valid = SuitModel.validate_suit(suit)
    return render_template("result.html", suit=suit, valid=is_valid)

@web.route("/repair", methods=["POST"])
def repair_suit():
    suit_id = request.form.get("suit_id")
    database = SuitModel.load_database()
    
    for suit in database:
        if suit["id"] == suit_id:
            suit["durability"] = min(suit["durability"] + 25, 100)
            SuitModel.save_database(database)
            return render_template("result.html", suit=suit, repaired=True)
    
    return render_template("result.html", error="ชุดไม่พบในฐานข้อมูล")

if __name__ == "__main__":
    SuitModel.generate_sample_data()
    web.run(debug=True)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://inv_user:securepassword@localhost/investment_tracker"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Define models for Users, Portfolios, Transactions, and Market Data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolio.id"), nullable=False)
    asset_type = db.Column(db.String(50))
    asset_name = db.Column(db.String(100))
    quantity = db.Column(db.Numeric)
    purchase_price = db.Column(db.Numeric)
    purchase_date = db.Column(db.DateTime)


class MarketData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_type = db.Column(db.String(50))
    asset_name = db.Column(db.String(100))
    current_price = db.Column(db.Numeric)
    last_updated = db.Column(db.DateTime)


db.create_all()

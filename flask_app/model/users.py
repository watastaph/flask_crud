from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Users:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['txt-pword']) <= 6:
            flash("Password must be at least 7 characters long!")
            is_valid = False
        if not EMAIL_REGEX.match(user['txt-email']):
            flash("Invalid Email!")
            is_valid = False
        if len(user['txt-name']) <= 9:
            flash("Name must be at least 10 characters long!")
            is_valid = False
        return is_valid
    

    @classmethod
    def all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("sample_db").query_db(query)
        posts = []
        for post in results:
            posts.append(cls(post))
        return posts

    @classmethod
    def add_users(cls, data):
        query = "INSERT INTO users (name, email, password, created_at, updated_at) VALUES (%(name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL("sample_db").query_db(query, data)
    
    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        print(query)
        return connectToMySQL("sample_db").query_db(query, data)
    
    @classmethod
    def retrieve_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("sample_db").query_db(query, data)
        print(results)
        if len(results) <1:
            return False
        return cls(results[0])
    
    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET name=%(name)s, email=%(email)s, password=%(password)s, updated_at=NOW() WHERE id = %(id)s;"
        print(query)
        return connectToMySQL("sample_db").query_db(query, data)
    
    @classmethod
    def login_user(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("sample_db").query_db(query, data)
        print(results)
        if len(results)<1:
            return False
        return cls(results[0])
    
    @classmethod
    def all_post(cls):
        query = "SELECT posts.id, users.id, users.name, posts.post FROM posts LEFT JOIN users ON users.id = posts.user_id"
        results = connectToMySQL("sample_db").query_db(query)
        posts = []
        for post in results:
            data = {
                "id": post["id"],
                "users_id": post["users.id"],
                "name": post["name"],
                "post": post["post"]
            }
            posts.append(data)
        print(posts)
        return posts
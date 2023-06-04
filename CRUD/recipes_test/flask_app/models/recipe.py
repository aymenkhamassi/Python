from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user

class Recipe :
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date = data['date']
        self.under = data['under']
        self.poster = user.User.get_by_id({'id':self.user_id}).first_name

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM recipe;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        recp = []
        for row in results:
            recp.append(cls(row))
        return recp

    @classmethod
    def add_recipe(cls, data):
        query = """
        INSERT INTO recipe (user_id, name, description,instruction,date,under) 
        VALUES (%(user_id)s,%(name)s,%(description)s,%(instruction)s,%(date)s,%(under)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['name'])< 2:
            flash("Name must be at least 3")
            is_valid = False
        if len(data['description'])< 10:
            flash("Description too short")
            is_valid = False
        if len(data['instruction'])< 10:
            flash("Instructions too short")
            is_valid = False
        if data["date"] == "":
            flash("Date is required")
            is_valid = False
        return is_valid
    
    @classmethod
    def delete(cls, data):
        query = """
        delete from recipe where id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def edit_recipe(cls, data):
        query = """
        UPDATE recipe SET name = %(name)s, description = %(description)s, instructions= %(instruction)s , date = %(date)s, under= %(under)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM recipe WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
    
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user



class Appointment :
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.task = data['task']
        self.date = data['date']
        self.status = data['status']
        self.poster = user.User.get_by_id({'id':self.user_id}).first_name


    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM appointements;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        appt = []
        for row in results:
            appt.append(cls(row))
        return appt
    

    @classmethod
    def add_appoint(cls, data):
        query = """
        INSERT INTO appointements (user_id,task, date,status) 
        VALUES (%(user_id)s,%(task)s,%(date)s,%(status)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    


    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM appointements WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
    

    @classmethod
    def delete(cls, data):
        query = """
        delete from appointements where id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def edit_appoint(cls, data):
        query = """
        UPDATE appointements SET task = %(task)s, date = %(date)s, status= %(status)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['task'])< 6:
            flash("Task must be at least 6")
            is_valid = False
        if data['date'] == "":
            flash("Date is required")
            is_valid = False
        return is_valid

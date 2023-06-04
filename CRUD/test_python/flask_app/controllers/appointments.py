from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.appointment import Appointment



@app.route('/appoint/new')
def new_appoint():
    if 'user_id' in session:
        return render_template("add_appointment.html")
    return redirect('/')


@app.route('/appoint/create' ,methods=['POST'])
def create_appoint():
    if(Appointment.validate(request.form)):
        data = {
            **request.form,'user_id':session['user_id']
        }
        Appointment.add_appoint(data)
        return redirect('/dashboard')
    return redirect('/appoint/new')


@app.route('/appoint/<appoint_id>/update' ,methods=['POST'])
def update_appoint(appoint_id):
    if(Appointment.validate(request.form)):
        print(request.form)
        data = {
            **request.form,'id':appoint_id
        }
        Appointment.edit_appoint(data)
        return redirect('/dashboard')
    return redirect('/appoint/'+str(appoint_id)+'/edit')


@app.route('/appoint/<appoint_id>/edit')
def edit_appoint(appoint_id):
    if 'user_id' in session:
        one_appoint=Appointment.get_by_id({'id':appoint_id})
        return render_template("edit_appointement.html", appoint=one_appoint)
    return redirect('/')


@app.route('/appoint/<appoint_id>/destroy')
def delete_appoint(appoint_id):
    if 'user_id' in session:
        Appointment.delete({'id':appoint_id})
    return redirect('/dashboard')
from flask_app import app, UPLOAD_FOLDER
from flask import render_template,request, redirect, session,flash
from flask_app.models.review import Review
from flask_app.models.company import Company

from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/reviews/new')
def new_review():
    companies = Company.get_all()
    return render_template("/user/new_review.html", companies = companies)

@app.route('/review/create', methods=["post"])
def add_review():
    file = request.files['photo']
    filename = secure_filename(file.filename)
    file.save(os.path.join("flask_app"+UPLOAD_FOLDER, filename))
    data = {
            **request.form,
            "user_id" : session["user_id"],
            "photo" : filename
        }
    Review.add_review(data)
    return redirect('/user/dashboard')


@app.route('/edit/review/<int:review_id>')
def edit_rev(review_id):
    data = {
        'id':review_id
    }
    review = Review.get_by_id(data)
    return render_template('user/edit_review.html', review = review)

@app.route('/review/<int:review_id>/update', methods=["post"])
def user_updating(review_id):
    file = request.files['photo']
    filename = secure_filename(file.filename)
    file.save(os.path.join("flask_app"+UPLOAD_FOLDER, filename))
    data ={
        **request.form,
        'id': review_id,
        'photo': filename
    }
    Review.edit_review(data)
    return redirect('/user/dashboard')


@app.route('/review/delete', methods=["post"])
def delete_rev():
    Review.delete_review({'id':request.form['review_id']})
    return redirect('/user/dashboard')

@app.route('/admin/reviews')
def see_all_reviews():
    reviews = Review.get_all()
    return render_template("admin/reviews/show_reviews.html", reviews=reviews)
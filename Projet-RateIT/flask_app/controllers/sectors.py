from flask_app import app, UPLOAD_FOLDER
from flask import render_template,request, redirect, session,flash
from flask_app.models.review import Review
from flask_app.models.company import Company
from flask_app.models.sector import Sector

from werkzeug.utils import secure_filename
import os
import urllib.request
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/sector/<int:sector_id>')
def show_sector(sector_id):
    data = {
        'id':sector_id
    }
    sector = Sector.get_by_id(data)
    companies = Company.get_all_with_sector(data)
    return render_template("list_companies_by_sector.html", companies=companies, sector=sector)


@app.route('/admin/sector/new')
def new():
    return render_template("admin/sectors/new_sector.html")


@app.route('/admin/sector/create', methods=["post"])
def create():
    file = request.files['logo']
    filename = secure_filename(file.filename)
    file.save(os.path.join("flask_app"+UPLOAD_FOLDER, filename))
    data = {
            **request.form,
            "logo" : filename
        }
    Sector.add_sector(data)
    return redirect('/admin/sectors')

@app.route('/admin/sectors')
def show_all_sectors():
    sectors = Sector.get_all()
    return render_template('admin/sectors/show_sectors.html', sectors = sectors)

@app.route('/admin/sector/<int:sector_id>/edit')
def edit(sector_id):
    sector= Sector.get_by_id({'id': sector_id})
    return render_template('admin/sectors/edit_sector.html',sector=sector)

@app.route('/admin/sector/<int:sector_id>/update', methods=['post'])
def update_sector(sector_id):
    file = request.files['logo']
    filename = secure_filename(file.filename)
    file.save(os.path.join('flask_app'+UPLOAD_FOLDER, filename))
    data = {
            **request.form,
            'id': sector_id,
            "logo" : filename
        }
    Sector.edit_sector(data)
    return redirect('/admin/sectors')

@app.route('/admin/sector/<int:sector_id>/delete', methods=["post"])
def delete(sector_id):
   data =  {
        "id" : sector_id
    }
   Sector.delete_sector(data)
   return redirect('/admin/sectors')

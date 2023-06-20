from flask_app import app, TODAY, UPLOAD_FOLDER
from flask import render_template,request, redirect, session,flash, jsonify
from flask_app.models.user import User
from flask_app.models.review import Review
from flask_app.models.company import Company
from flask_app.models.sector import Sector
from flask_app.models.adress import Adress

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# Home page
@app.route('/')
def index():
    sectors = Sector.get_all()
    companies = Company.get_for_index()
    return render_template('index.html', sectors=sectors, companies=companies)

@app.route('/about_us')
def about():
    return render_template('abouts.html')

@app.route('/rules')
def rule():
    return render_template('rules.html')

@app.route('/search', methods=["post"])
def search():
    word = request.form['word']
    data = {
        'word':"%"+word+"%"
    }
    sectors = Sector.search(data)
    print(sectors,"//**//"*20)
    companies = Company.search(data)
    reviews = Review.search(data)
    return render_template('search.html', sectors=sectors, companies=companies, reviews=reviews, word=word)

# LogReg
@app.route('/connection')
def logreg():
    sectors = Sector.get_all()
    cities = Adress.get_cities()
    return render_template("login.html", sectors = sectors, cities=cities)


@app.route('/company/dashboard')
def companydashboard():
    if 'company_id' in session:
        company= Company.get_by_id({'id': session['company_id']})
        reviews = Review.get_company_reviews({'id': session['company_id']})
        return render_template('company/company_dashboard.html', company=company, reviews= reviews)
    else:
        redirect('/connection')


@app.route('/user/dashboard')
def userdashboard():
    if 'user_id' in session:
        user= User.get_by_id({'id': session['user_id']})
        reviews = Review.get_by_user_id({'id': session['user_id']})
        return render_template('user/user_dashboard.html', user=user, reviews=reviews)
    else:
        return redirect('/connection')
    

@app.route('/admin/dashboard')
def admindashboard():
    if 'user_id' not in session:
        return redirect('/')
    user= User.get_by_id({'id': session['user_id']})
    if user.is_admin == 0:
        return redirect('/user/dashboard')
    cr = Review.count()
    cu = User.count()
    cc = Company.count()
    cs = Sector.count()
    return render_template('admin/admin_dashboard.html', user=user, cr=cr,cu=cu,cc=cc,cs=cs, date=TODAY)


@app.route('/user/register', methods=['post'])
def register():
    if not User.validate(request.form):
        return redirect('/connection')
    
    file = request.files['avatar']
    filename = secure_filename(file.filename)
    file.save(os.path.join('flask_app'+UPLOAD_FOLDER, filename))
    
    data={
        **request.form,
        'password':bcrypt.generate_password_hash(request.form['password']),
        'avatar': filename
    }
    user = User.create_user(data)
    session['user_id'] = user
    return redirect('/user/dashboard')

@app.route('/user/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email or password',"Login")
        return redirect('/connection')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password',"Login")
        return redirect('/connection')
    session['user_id']=user.id
    if user.is_admin == 1:
        return redirect('/admin/dashboard')
    else:
        return redirect('/user/dashboard')
    
@app.route('/edit_profil/<int:user_id>')
def edit_profil(user_id):
    data = {
        'id':user_id
    }
    user = User.get_by_id(data)
    return render_template("user/edit_user_profil.html", user = user)

@app.route('/user/<int:user_id>/update', methods=["post"])
def update_user(user_id):

    file = request.files['avatar']
    filename = secure_filename(file.filename)
    file.save(os.path.join('flask_app'+UPLOAD_FOLDER, filename))

    if request.form['newpsw']:
        if request.form['newpsw'] == request.form['confnewpsw']:
            data = {
                **request.form,
                'id': user_id,
                'avatar': filename,
                'password':bcrypt.generate_password_hash(request.form['newpsw'])
            }
            User.update_user(data)
            return redirect('/user/dashboard')
        else:
            flash("Your are not sure about your password?!")
            return redirect(f'/edit_profil/{user_id}')
    else:
        user = User.get_by_id({'id': user_id})
        data = {
            **request.form,
            'id': user_id,
            'avatar': filename,
            'password': user.password
        }
        User.update_user(data)
        return redirect('/user/dashboard')
        

@app.route('/admin/users')
def see_all_users():
    users = User.get_all()
    return render_template('/admin/users/show_users.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Ajax route to update user status
@app.route('/update_status', methods=['POST'])
def update_status():
    user_id = int(request.form['user_id'])
    new_status = int(request.form['new_status'])
    data = {
        'id': user_id,
        'actif': new_status
    }
    User.update_status(data)
    return jsonify(success=True)
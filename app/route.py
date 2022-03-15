from turtle import title
from app import app,db
from flask import Response, render_template, request, json, redirect, flash, url_for
from app.models import User, Course, Enroll
from app.form import LoginForm, RegisterForm

# courseData=[
#         {"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, 
#         {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, 
#         {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, 
#         {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, 
#         {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}
#         ]

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", index=True)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in", "success")
            return redirect("/index")
        else:
            flash("sorry, something went wrong", "danger")
    return render_template("login.html", user_form=form, login=True)

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term = None):
    if term is None:
        term = "Spring 2022"
    classes = Course.objects.all()
    return render_template("courses.html", courseData=classes, courses=True, term=term)

@app.route("/register" , methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects().count()
        user_id += 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id,email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!", "success")
        return redirect(url_for('index'))
    return render_template("register.html", register_form=form, register=True)

@app.route("/enrollment", methods=["GET","POST"])
def enrollment():
    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = 1
    if courseID:
        if Enroll.objects(user_id=user_id, course_id=courseID):
            flash(f'Oops! You are already registered in this course {courseTitle}!', "danger")
            return redirect(url_for("courses"))
        else:
            Enroll(user_id=user_id, course_id=courseID).save()
            flash(f'You are enrolled in {courseTitle}', "success")
    classes = list(User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'enroll', 
                    'localField': 'user_id', 
                    'foreignField': 'user_id', 
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1', 
                    'includeArrayIndex': 'r1_id', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course', 
                    'localField': 'r1.course_id', 
                    'foreignField': 'courseID', 
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'courseID': 1
                }
            }
        ]))
    return render_template("enrollment.html", enrollment=True, classes=classes, title="Enrollment")


@app.route("/api")
@app.route("/api/<idx>")
def api (idx=None):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]
    return Response(json.dumps(jdata), mimetype="application/json")


@app.route("/user")
def user():
    '''This saves data into data table of the database'''
    # User(user_id=1, first_name="John", last_name="Doe", email="john.doe@email.com", password="abc123").save()
    # User(user_id=2, first_name="Jane", last_name="Doe", email="jane.doe@email.com", password="password123").save()
    users = User.objects.all()
    return render_template("user.html", users=users)
from app import app,db
from flask import Response, render_template, request, json, redirect, flash
from app.models import User, Course, Enroll
from app.form import LoginForm, RegisterForm

courseData=[
        {"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, 
        {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, 
        {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, 
        {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, 
        {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}
        ]

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", index=True)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.form.get("email") == "test@email.com":
            flash("login successful", "success")
            return redirect("/index")
        else:
            flash("sorry, something went wrong", "danger")
    return render_template("login.html", user_form=form, login=True)

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    return render_template("courses.html", courseData=courseData, courses=True, term=term)

@app.route("/register")
def register():
    return render_template("register.html", register=True)

@app.route("/enrollment", methods=["GET","POST"])
def enrollment():
    id = request.form.get('courseID')
    title = request.form.get('title')
    term =  request.form.get('term')
    return render_template("enrollment.html", enrollment=True, data={"id":id, "title":title, "term":term})


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
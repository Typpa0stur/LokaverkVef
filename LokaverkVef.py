from flask import Flask, render_template, request, session
import pyrebase
import os
app = Flask(__name__)

config = {
    "apiKey": "AIzaSyAkJZMZgGEmev_lh_ZzW1qQVCvJl0o5UUc",
    "authDomain": "lokaverkvef.firebaseapp.com",
    "databaseURL": "https://lokaverkvef.firebaseio.com",
    "projectId": "lokaverkvef",
    "storageBucket": "lokaverkvef.appspot.com",
    "messagingSenderId": "173027969263",
    "appId": "1:173027969263:web:e9e1b9c4d65b581769f31a",
    "measurementId": "G-7HV7GSS5MN"
    }

fb = pyrebase.initialize_app(config)
db = fb.database()

app.secret_key = os.urandom(5)

@app.route('/')
def index():
    #db.child("recipe").push({"id":0,"uname":"gummi","rename":"onion", "description":"onion"})
    return render_template("index.html")

@app.route('/dologin', methods=['GET','POST'])
def dologin():
    tf = False
    u = db.child("user").get().val()
    lst = list(u.items())
    if request.method == 'POST':
        uname = request.form['uname']
        pword = request.form['pword'] 
        for i in range(len(lst)):
            if uname == lst[i][1]['uname'] and pword == lst[i][1]['pword']:
                tf = True
        if tf == True:  
            session['user'] = uname
            return render_template("seacret.html",uname = uname)     
        else:
           return "<h3>Wrong username or password!!<h3> <a href='/'>Home</a>"
    else:
        return "<h1>Má ekki !</h1> <a href='/'>Home</a>"

@app.route('/user')
def user():
    if 'user' in session:
        uname = session['user']
        return render_template("seacret.html",uname=uname)
    else:
        return '<h1>You need to login.</h1><h3><a href="/">Home</a></h3>'

@app.route('/off')
def sessionoff():
    if 'user' in session:
        session.pop('user', None)
        return '<h3>You have logged out.</h3><h3><a href="/">Home</a></h3>'
    else:
        return '<h3>Session was not set</h3><h3><a href="/">Home</a></h3>'

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/doregister', methods=['GET','POST'])
def doregister():
    allusernames = [] 
    u = db.child("user").get().val()
    lst = list(u.items())
    if request.method == 'POST':
        uname = request.form['uname']
        pword = request.form['pword']

        for i in range(len(lst)):
            allusernames.append(lst[i][1]['uname']) # Mokum öllum userum í listann

        
        # Ef user er til í database leyfum við ekki push í grunninn / ef user ekki til leyfum við push...
        if uname not in  allusernames:
            # user ekki til
            db.child("user").push({"uname":uname, "pword":pword}) 
            return "<h3>New user in database!!<h3> <a href='/'>Home</a>"
        else:
            # user er til
            return "<h3>Username exists in database, try again!!<h3> <a href='/'>Home</a>"
    else:
        return render_template("register.html")


@app.route('/add')
def add():
    return render_template("insetning.html")

@app.route('/addtodb', methods=['GET','POST'])
def addtodb():
    if 'user' in session:
        uname = session['user']
        id = 0
        u = db.child("user").get().val()
        lst = list(u.items())
        allrecipes = []
        r = db.child("recipe").get().val()
        blst = list(r.items())
        for i in range(len(blst)):
            allrecipes.append(blst[i][1]['rename'])
            if id < blst[i][1]['id']:
                id = blst[i][1]['id']
        if request.method == 'POST':
            #uname  = request.form['uname']
            id = id + 1
            rename = request.form['rename']
            description = request.form['description']
            #for i in range(len(lst)):
            #    allusernames.append(lst[i][1]['uname'])
            #if uname not in  allusernames:
            #    return "<h3>ERROR user not in database.</h3> <a href='/add'>Return</a>"
            if rename == "" or description == "":
                return "<h3>ERROR missing name of recipe or description.</h3> <a href='/add'>Return</a>"
            else:
                db.child("recipe").push({"id":id,"uname":uname,"rename":rename, "description":description})
                return "<h3>New recipe added.</h3> <a href='/add'>Return</a>" 
        else:
            return "<h3>ERROR.</h3> <a href='/add'>Return</a>"
    else:
        return "<h3>ERROR.</h3> <a href='/add'>Return</a>"

@app.route('/see')
def see():
    allrecipes = [[]]
    u = db.child("recipe").get().val()
    lst = list(u.items())
    for i in range(len(lst)):
        allrecipes.append([lst[i][1]['id'],lst[i][1]['rename']])
    return render_template("extendo.html", allrecipes=allrecipes)

@app.route('/see/<int:id>')
def seeing(id):
    allrecipes = []
    u = db.child("recipe").get().val()
    lst = list(u.items())
    for i in range(len(lst)):
        if lst[i][1]['id'] == id:
            allrecipes.append(lst[i][1]['id'])
            allrecipes.append(lst[i][1]['rename'])
            allrecipes.append(lst[i][1]['description'])
            allrecipes.append(lst[i][1]['uname'])
    return render_template("extendoinfo.html",allrecipes=allrecipes)

@app.route('/eyda')
def eyda():
    if 'user' in session:
        allrecipes = [[]]
        u = db.child("recipe").get().val()
        lst = list(u.items())
        for i in range(len(lst)):
            if session['user'] == lst[i][1]['uname']:
                allrecipes.append([lst[i][1]['id'],lst[i][1]['rename']])
        return render_template("eydadb.html",allrecipes=allrecipes)
    else:
        return '<h1>You need to login.</h1><h3><a href="/">Home</a></h3>'

@app.route('/eydago', methods=['GET','POST'])
def eydago():
    u = db.child("recipe").get().val()
    lst = list(u.items())
    lykill = ""
    go = False
    if request.method == 'POST':
        id = request.form['robo']
        for i in range(len(lst)):
            if int(id) == lst[i][1]['id']:
                lykill,rusl = lst[i]
                go = True
        if go == True:
            db.child("recipe").child(lykill).remove()
            return "<h1>Recipe has been deleted.</h1> <a href='/'>Home</a>"
        else:
            return "<h1>ERROR.</h1><h3><a href='/'>Home</a></h3>"
    else:
        return "<h1>ERROR.</h1><h3><a href='/'>Home</a></h3>"

@app.route("/breyta")
def breyta():
    if 'user' in session:
        allrecipes = [[]]
        u = db.child("recipe").get().val()
        lst = list(u.items())
        for i in range(len(lst)):
            if session['user'] == lst[i][1]['uname']:
                allrecipes.append([lst[i][1]['id'],lst[i][1]['rename']])
        return render_template("breytadb.html",allrecipes=allrecipes)
    else:
        return "<h1>ERROR.</h1><h3><a href='/'>Home</a></h3>"

@app.route('/breytago', methods=['GET','POST'])
def breytago():
    u = db.child("recipe").get().val()
    lst = list(u.items())
    lykill = ""
    go = False
    if request.method == 'POST':
        id = request.form['robo']
        rename = request.form['rename']
        description = request.form['description']
        for i in range(len(lst)):
            if int(id) == lst[i][1]['id']:
                lykill,rusl = lst[i]
                go = True
        if go == True:
            db.child("recipe").child(lykill).update({"rename":rename, "description":description})
            return "<h1>Recipe has been changed.</h1> <a href='/user'>Account</a>"
    else:
        return "<h1>ERROR.</h1><h3><a href='/'>Home</a></h3>"

#@app.errorhandler(404)
#def error404():
#    return "<h1>Wrong page entered</h1> <br /><a href="/"><h3>Home</h3></a>"

if __name__ == "__main__":
    app.run(debug=True)
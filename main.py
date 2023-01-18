from flask import Flask ,render_template,request,redirect,url_for, session, flash
import sqlite3

app=Flask(__name__)
app.config['SECRET_KEY'] = 'abdulrzaq'




import json as j

file=open("firstjson.json")
data = j.load(file)

class Preson :
    countrys:list 
    def __init__(self ,countrys):
        self.countrys = countrys 

p1 = Preson(**data )

countries=[" 1)syria\n","2)Germany(locked)\n","3)Italy(locked)\n","4)Russia(locked)\n","5)Japan(locked)\n"]

def newcountry(the_countrie):
    if the_countrie=="1":
        countries.remove(countries[1])
        countries.insert(1,"2)Germany(locked)\n")
        countries.remove(countries[2])
        countries.insert(2,"3)Italy(locked)\n")
        countries.remove(countries[3])
        countries.insert(3,"4)Russia(locked)\n")
        countries.remove(countries[4])
        countries.insert(4,"5)Japan(locked)\n")
    elif the_countrie=="2":
        countries.remove(countries[1])
        countries.insert(1,"2)Germany\n")
        countries.remove(countries[2])
        countries.insert(2,"3)Italy(locked)\n")
        countries.remove(countries[3])
        countries.insert(3,"4)Russia(locked)\n")
        countries.remove(countries[4])
        countries.insert(4,"5)Japan(locked)\n")
    elif the_countrie=="3":
        newcountry("2")
        countries.remove(countries[2])
        countries.insert(2,"3)Italy\n")
        countries.remove(countries[3])
        countries.insert(3,"4)Russia(locked)\n")
        countries.remove(countries[4])
        countries.insert(4,"5)Japan(locked)\n")
    elif the_countrie=="4":
        newcountry("2")
        newcountry("3")
        countries.remove(countries[3])
        countries.insert(3,"4)Russia\n")
        countries.remove(countries[4])
        countries.insert(4,"5)Japan(locked)\n")
    elif the_countrie=="5":
        countries.remove(countries[4])
        countries.insert(4,"5)Japan\n")
        newcountry("2")
        newcountry("3")
        newcountry("4")


db = sqlite3.connect("app.db")
cr=db.cursor()


cr.execute("create table if not exists users(name text, password text, progres integer)")
db.close()

@app.route("/login", methods=['POST','GET'])
def find():
    if request.method=='POST':
        the_n=request.form["Name"]
        session['name']=the_n
        the_password=request.form["password1"]
        db = sqlite3.connect("app.db")
        cr=db.cursor()
        cr.execute("select name from users")
        results = cr.fetchall()
        for i in range(len(results)):
            if the_n == results[i][0]:
                cr.execute(f"select password from users where name ='{the_n}'")
                result = cr.fetchone()
                if result[0]==the_password:
                    cr.execute(f"select progres from users where name ='{the_n}'")
                    resul = cr.fetchall()
                    resul=resul[0][0]
                    newcountry(f"{resul}")
                    db.close()
                    flash('log in success', category='success')
                    return redirect(url_for('lista'))
                    break
        else :
            flash('the password ou user name is wrong', category='error')
            return  render_template("log_in.html")

    else:
        if 'name' in session:
            return  redirect(url_for('lista'))
        return render_template("log_in.html",c=session)


@app.route("/", methods=['POST','GET'])
def signup():
    if request.method=='POST':
        db = sqlite3.connect("app.db")
        cr=db.cursor()
        name=request.form["Name"]
        cr.execute("select name from users")
        results = cr.fetchall()
        for i in range(len(results)):
            if name == results[i][0]:
                flash("this name used try anthor name", category='error')
                return  render_template("sign_up.html")
        password1=request.form["password1"]
        password2=request.form["password2"]
        if password1!=password2:
            flash("password don't match", category='error')
            return  render_template("sign_up.html")
        elif len(name)<2:
            flash("the name short", category='error')
            return  render_template("sign_up.html")
        elif len(password1)<5:
            flash("the password short", category='error')
            return  render_template("sign_up.html")
        else :
            cr.execute(f"insert into users(name,password,progres) values('{name}', '{password1}','1')")
            db.commit()
            db.close()

            flash('you sign up ', category='success')
            return redirect(url_for('find'))
    else:    
        return render_template("sign_up.html",c=session)
        
@app.route("/list", methods=['POST','GET'])
def lista():
    if 'name' in session:
        if request.method=='POST':
            Country_Number=request.form.get('Country_Number')
            if countries[int(Country_Number)-1][-2]==")":
                flash('this cuontry is locked', category='error')
                return  render_template("list.html",lisa=countries)
            elif int(Country_Number)==1:
                return render_template("quesion.html",g=p1.countrys[0]['questions'],b=0,country_name="syria")
            elif int(Country_Number)==2:
                return render_template("quesion.html",g=p1.countrys[1]['questions'],b=1,country_name="Germany")
            elif int(Country_Number)==3:
                return render_template("quesion.html",g=p1.countrys[2]['questions'],b=2,country_name="Italy")
            elif int(Country_Number)==4:
                return render_template("quesion.html",g=p1.countrys[3]['questions'],b=3,country_name="Russia")
            elif int(Country_Number)==5:
                return render_template("quesion.html",g=p1.countrys[4]['questions'],b=4,country_name="Japan")
        else :
            return  render_template("list.html",lisa=countries,c=session)
    else:
        return redirect(url_for('find'))

@app.route("/logout",methods=['POST','GET'])
def logout():
    session.pop('name',None)
    return redirect(url_for('find'))


@app.route("/quesion",methods=['POST','GET'])
def quesion():
    if 'name' in session:
        SCOREE = 0
        if request.method=='POST':
            b=int(request.form["gg"])
            for i in range(20):
                question_id = str(i)
                selected_option = request.form[question_id]
                correct_option = p1.countrys[b]['questions'][i]['answer']
                if int(selected_option) == correct_option:
                    SCOREE+=1
            if SCOREE >= 9:
                if b==4:
                    flash(f"you finech the game your mark in jaban is: {SCOREE}/20", category='success')
                    return redirect(url_for('lista'))
                db = sqlite3.connect("app.db")
                cr=db.cursor()
                n=session['name']
                cr.execute(f"update users set progres = '{b+2}' where name = '{n}'")
                db.commit()
                db.close()
                newcountry(f"{b+2}")
                flash(f'you open a ney country, your mark is: {SCOREE}/20', category='success')
                return redirect(url_for('lista'))
            elif SCOREE < 9:
                flash(f'your right answers less thin 10, your mark is: {SCOREE}/20', category='error')
                return redirect(url_for('lista'))
        else :
            return render_template("quesion.html",c=session)
    else:
        return redirect(url_for('find'))

if __name__ == "__main__":
    app.run(debug=True)
    
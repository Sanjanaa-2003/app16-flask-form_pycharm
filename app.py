from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from  flask_mail import Mail, Message

app=Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "sanjanaarj2003@gmail.com"        #This is sender's mail; whatever is filled in the form is receiver mail
app.config["MAIL_PASSWORD"] = "blkd kopp rrle nmkr"
# db=SQLAlchemy(app)

db=SQLAlchemy(app)
mail=Mail(app)

class Form(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(80))
    last_name=db.Column(db.String(80))
    email=db.Column(db.String(80))
    date=db.Column(db.Date)
    occupation=db.Column(db.String(80))


@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj =datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]
        print(first_name,last_name,email,date,occupation)

        form=Form(first_name=first_name, last_name=last_name,
                  email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body=f"Thank you for your submission, {first_name} ."\
                     f"Here are your data:\n{first_name}\n{last_name}\n{date}\n" \
                     f"Thank you!"
        message=Message("New form submission",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email],
        body=message_body)
        mail.send(message)

        flash(f"{first_name}, your form was submitted successfully!","Success")

#First run the program, the webpage opens, then In the "return render_template("index.html") place a breakpoint
# and click on debug, go to the webpage fill all details, this will show the status of the details in the console. The name email id, wtc

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()     #Creates data.db file; open db browser and go to open database: select app16;go to instances, the data.db file will be visible
        app.run(debug=True, port=5001)
app.run(debug=False, port =5001)


# 1. Run the app.py file
# 2. In the link that appears in console, type the details, with the database open in db browser(DB Browser for SQLite--open database--
# E--app16--instances--data.db file open)
# 3. Browse data to see what has been filled is entered
# 4. When submit is pressed it displays a message below it and a mail isinstance(sent immediately to the mail id specified
# while filling the form)
# Note: If any error, close and reopen db browser, rerun the app file.

# In Flask, setting debug=False can sometimes help with debugging by providing a more stable environment while debugging your code. When debug=True, the Flask server automatically reloads whenever changes are made, which can occasionally interfere with the debugging process. By setting debug=False, you create a more reliable server setup that allows for smoother debugging. However, do keep in mind that the necessity of this setting may vary depending on your specific setup and requirements.
#
# Remember, these issues aren't specific to Windows 10 and can happen on any operating system. It's a good idea to carefully review your code, configuration settings, and ensure that you're following the correct debugging procedures within PyCharm.
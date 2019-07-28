import os #os Python library, which will allow us to access paths on
            #our file system relative to our project directory.

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))
#we figure out where our project path is and set up a database file with its full path
# and the sqlite:/// prefix to tell SQLAlchemy which database engine we're using.

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file #we tell our web application
                                                        #where our database will be stored.

#we initialize a connection to the database and keep this in the db variable.
db = SQLAlchemy(app)

class Book(db.Model): #This will make SQLAlchemy create a table called book,
                        #which it will use to store our Book objects.
    
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    #column name in our book table
    
    def __repr__(self):
        return "<Title: {}>".format(self.title)

#By default, Flask routes only accept HTTP GET requests.

@app.route('/', methods=["GET", "POST"])
def home():
    books = None
    if request.form:
        try:
            book = Book(title=request.form.get("title"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    books = Book.query.all()
    return render_template("home.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")
  
if __name__ == "__main__":
    app.run(debug=True)


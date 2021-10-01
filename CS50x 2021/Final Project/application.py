from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL
from random import randint
from werkzeug.security import check_password_hash, generate_password_hash

from functions import get_coms_count, get_pages_count
import pagination

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///problem.db")

# Set a constant number of problems per page as 10
PER_PAGE = 10


# Main page of the website
@app.route("/", defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):

    # Return error if user wants to view page with a negative id
    if page <= 0:
        return render_template("404.html")

    # Find a database id of the first problem on the page
    row = PER_PAGE * (page - 1)

    # Find how many problems are there in the database
    problems_count = db.execute("SELECT COUNT(*) AS length FROM problems")[0]["length"]

    # Select nessesary problems from database
    problems = db.execute("SELECT * FROM problems ORDER BY id DESC LIMIT :row_number, :count", row_number=row, count=PER_PAGE)

    # Return error if there are no problems on the page with given id
    if not problems and page != 1:
        return render_template("404.html")

    # Find how many comments are there under each problem
    for problem in problems:
        get_coms_count(problem)

    # Create pagination
    pag = pagination.Pagination(page, PER_PAGE, problems_count)

    pages_count = get_pages_count(problems_count)

    return render_template("index.html", pagination=pag, problems=problems, pages_count=pages_count, current_page=page, from_where="index")


# Add a problem
@app.route("/add", methods=["GET", "POST"])
def add():

    cap_1 = randint(1, 10)
    cap_2 = 10 - cap_1

    try:
        user_id = session["user_id"]
    except:
        user_id = None

    if request.method == "POST":
        email = request.form.get("email")
        problem = request.form.get("problem")
        captcha = request.form.get("captcha")

        if not email and not user_id:
            return render_template("add.html", error=1, problem=problem, cap_1=cap_1, cap_2=cap_2, user_id=user_id)

        if not problem:
            return render_template("add.html", error=2, email=email, cap_1=cap_1, cap_2=cap_2, user_id=user_id)

        if not captcha:
            return render_template("add.html", error=3, problem=problem, email=email, cap_1=cap_1, cap_2=cap_2, user_id=user_id)

        if captcha != "10":
            return render_template("add.html", error=4, problem=problem, email=email, cap_1=cap_1, cap_2=cap_2, user_id=user_id)

        db.execute("INSERT INTO 'problems' (text) VALUES (:problem)", problem=problem)
        return redirect("/")

    return render_template("add.html", error=None, cap_1=cap_1, cap_2=cap_2, user_id=user_id)


# View one problem with comments
@app.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):
    message = request.form.get("message")
    if request.method == "POST" and message:
        user_id = session["user_id"]
        sql = "INSERT INTO comments (text, post_id, user_id) VALUES (:message, :post_id, :user_id)"
        db.execute(sql, message=message, post_id=id, user_id=user_id)
        return redirect("/post/{}".format(id))
    else:
        problem = db.execute("SELECT * FROM problems WHERE id=:id", id=id)
        comments = db.execute("SELECT * FROM comments WHERE post_id=:id", id=id)
        print(session)
        if session.get("user_id") is None:
            username = None
        else:
            user = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])
            username = user[0]["username"]
        if len(comments) > 0:
            for comment in comments:
                commentator_name = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=comment["user_id"])
                comment["username"] = commentator_name[0]["username"]
            com_count = len(comments)
        else:
            comments = None
            com_count = 0

        if request.method == "GET":
            error = None
        else:
            error = 1

        return render_template("post.html", problem=problem[0], comments=comments, com_count=com_count, username=username, error=error)


# Like a problem
@app.route("/like/<int:post_id>/<from_where>")
def like(post_id, from_where):
    likes = db.execute("SELECT likes FROM problems WHERE id=:post_id", post_id=post_id)[0]["likes"]
    db.execute("UPDATE problems SET likes = :likes WHERE id = :post_id", likes=likes + 1, post_id=post_id)
    if from_where == "post":
        return redirect("/post/{}".format(post_id))
    elif from_where == "index":
        return redirect("/")
    else:
        return redirect("/{}".format(from_where))


# Dislike a problem
@app.route("/dislike/<int:post_id>/<from_where>")
def dislike(post_id, from_where):
    likes = db.execute("SELECT likes FROM problems WHERE id=:post_id", post_id=post_id)[0]["likes"]
    db.execute("UPDATE problems SET likes = :likes WHERE id = :post_id", likes=likes - 1, post_id=post_id)
    if from_where == "post":
        return redirect("/post/{}".format(post_id))
    elif from_where == "index":
        return redirect("/")
    else:
        return redirect("/{}".format(from_where))


# Like a comment
@app.route("/com_like/<int:com_id>")
def com_like(com_id):
    comment = db.execute("SELECT likes, post_id FROM comments WHERE id=:com_id", com_id=com_id)[0]
    post_id = comment["post_id"]
    likes = comment["likes"]
    db.execute("UPDATE comments SET likes = :likes WHERE id = :com_id", likes=likes + 1, com_id=com_id)
    return redirect("/post/{}".format(post_id))


# Dislike a comment
@app.route("/com_dislike/<int:com_id>")
def com_dislike(com_id):
    comment = db.execute("SELECT likes, post_id FROM comments WHERE id=:com_id", com_id=com_id)[0]
    post_id = comment["post_id"]
    likes = comment["likes"]
    db.execute("UPDATE comments SET likes = :likes WHERE id = :com_id", likes=likes - 1, com_id=com_id)
    return redirect("/post/{}".format(post_id))


# Top section
@app.route("/top", defaults={'page': 1})
@app.route('/top/page/<int:page>')
def top(page):
    print("page = {}".format(page))

    if page <= 0:
        return render_template("404.html")

    row = PER_PAGE * (page - 1)

    problems_count = db.execute("SELECT COUNT(*) AS length FROM problems")[0]["length"]
    problems = db.execute("SELECT * FROM problems ORDER BY likes DESC LIMIT :row_number, :count", row_number=row, count=PER_PAGE)

    if not problems and page != 1:
        return render_template("404.html")

    for problem in problems:
        get_coms_count(problem)

    pag = pagination.Pagination(page, PER_PAGE, problems_count)

    pages_count = get_pages_count(problems_count)

    return render_template("index.html", pagination=pag, problems=problems, pages_count=pages_count, current_page=page, from_where="top")


# Login to the website
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get email
        email = request.form.get("email")

        # Ensure email was submitted
        if not email:
            return render_template("login.html", error=1)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error=2, email=email)

        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = :email", email=request.form.get("email"))

        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", error=3)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to main page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html", error=None)


# Logout from the website
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# Sign up on the website
@app.route("/signup", methods=["GET", "POST"])
def signup():
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        confirmation = request.form.get("confirmation")

        if not email:
            return render_template("signup.html", error=1, username=username, text="Please provide email")

        if not username:
            return render_template("signup.html", error=2, email=email, text="Please provide username")

        if not password:
            return render_template("signup.html", error=3, email=email, username=username, text="Please provide password")

        if not confirmation:
            return render_template("signup.html", error=4, email=email, username=username, text="Please provide password twice")

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if len(rows) == 1:
            return render_template("signup.html", error=2, email=email, text="Username taken")

        rows = db.execute("SELECT * FROM users WHERE email = :email", email=email)
        if len(rows) == 1:
            return render_template("signup.html", error=1, username=username, text="There's already an account with this email")

        if password != confirmation:
            return render_template("signup.html", error=4, username=username, email=email, text="Passwords don't match")

        sql = "INSERT INTO users (username, email, hash) VALUES (:username, :email, :password_hash)"
        result = db.execute(sql, username=username, email=email, password_hash=generate_password_hash(password))

        session["user_id"] = result

        return redirect("/")

    return render_template("signup.html", error=None)


# Search a problem with particular words
@app.route("/search", methods=["GET"])
@app.route('/search/<int:page>')
def search():
    subject = request.args.get("subject")

    if not subject:
        return render_template("search_failure.html", text="Empty search query")

    response = db.execute("SELECT * FROM problems WHERE text like :text1 ORDER BY id DESC", text1='%' + subject + '%')

    if response == []:
        return render_template("search_failure.html", text="There were no results matching the query")

    for problem in response:
        get_coms_count(problem)

    return render_template("index.html", problems=response, pages_count=1, from_where="search?subject={subject}")


# Info about the website
@app.route("/about")
def about():
    problems_count = len(db.execute("SELECT * FROM problems"))
    users_count = len(db.execute("SELECT * FROM users"))
    comments_count = len(db.execute("SELECT * FROM comments"))
    return render_template("about.html", problems_count=problems_count, users_count=users_count, comments_count=comments_count)
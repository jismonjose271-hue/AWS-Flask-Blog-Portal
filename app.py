from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MYSQL_HOST"] = "news-portal-db.cxui0ui2sbwk.ap-south-1.rds.amazonaws.com"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_USER"] = "admin"
app.config["MYSQL_PASSWORD"] = "gokul1234"
app.config["MYSQL_DB"] = "my_blogdb"

mysql = MySQL(app)

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",
            (username, email, password)
        )
        mysql.connection.commit()
        cur.close()

        flash("Registration Successful ✨")
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", [username])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):
            session["username"] = username
            flash("Login Successful 🚀")
            return redirect("/dashboard")

        return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    return render_template("dashboard.html", username=session["username"])

@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]
        username = session["username"]

        image = request.files.get("image")
        filename = ""

        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO posts(title,content,created_at,category,image,username,likes) VALUES(%s,%s,NOW(),%s,%s,%s,0)",
            (title, content, category, filename, username)
        )
        mysql.connection.commit()
        cur.close()

        flash("Post Published Successfully ✨")
        return redirect("/posts")

    return render_template("create_post.html")

@app.route("/posts")
def posts():
    if "username" not in session:
        return redirect("/login")

    search = request.args.get("search")
    cur = mysql.connection.cursor()

    if search:
        cur.execute(
            "SELECT * FROM posts WHERE title LIKE %s OR content LIKE %s ORDER BY id DESC",
            ("%" + search + "%", "%" + search + "%")
        )
    else:
        cur.execute("SELECT * FROM posts ORDER BY id DESC")

    all_posts = cur.fetchall()

    cur.execute("SELECT * FROM comments ORDER BY id DESC")
    all_comments = cur.fetchall()

    comments_by_post = {}
    for comment in all_comments:
        post_id = comment[1]
        if post_id not in comments_by_post:
            comments_by_post[post_id] = []
        comments_by_post[post_id].append(comment)

    cur.close()

    return render_template(
        "posts.html",
        posts=all_posts,
        comments_by_post=comments_by_post
    )

@app.route("/add_comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):
    if "username" not in session:
        return redirect("/login")

    comment = request.form["comment"]
    username = session["username"]

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO comments(post_id, username, comment) VALUES(%s,%s,%s)",
        (post_id, username, comment)
    )
    mysql.connection.commit()
    cur.close()

    flash("Comment Added 💬")
    return redirect("/posts")

@app.route("/edit_post/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    if "username" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        cur.execute(
            "UPDATE posts SET title=%s, content=%s WHERE id=%s",
            (title, content, id)
        )
        mysql.connection.commit()
        cur.close()

        flash("Post Updated ✏️")
        return redirect("/posts")

    cur.execute("SELECT * FROM posts WHERE id=%s", [id])
    post = cur.fetchone()
    cur.close()

    return render_template("edit_post.html", post=post)

@app.route("/delete_post/<int:id>")
def delete_post(id):
    if "username" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM comments WHERE post_id=%s", [id])
    cur.execute("DELETE FROM posts WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()

    flash("Post Deleted 🗑️")
    return redirect("/posts")

@app.route("/like_post/<int:id>")
def like_post(id):
    if "username" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()
    cur.execute("UPDATE posts SET likes = likes + 1 WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()

    return redirect("/posts")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    cur = mysql.connection.cursor()

    if request.method == "POST":
        bio = request.form["bio"]
        image = request.files.get("profile_pic")

        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            cur.execute(
                "UPDATE users SET bio=%s, profile_pic=%s WHERE username=%s",
                (bio, filename, username)
            )
        else:
            cur.execute(
                "UPDATE users SET bio=%s WHERE username=%s",
                (bio, username)
            )

        mysql.connection.commit()
        cur.close()

        flash("Profile Updated 👤")
        return redirect("/profile")

    cur.execute("SELECT * FROM users WHERE username=%s", [username])
    user = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM posts WHERE username=%s", [username])
    total_posts = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(likes),0) FROM posts WHERE username=%s", [username])
    total_likes = cur.fetchone()[0]

    cur.close()

    return render_template(
        "profile.html",
        user=user,
        total_posts=total_posts,
        total_likes=total_likes
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

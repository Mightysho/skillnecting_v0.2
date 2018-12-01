from flask import render_template, request, Blueprint, jsonify
from skillnecting.models import Post, User
from flask import render_template, request, Blueprint, jsonify
from skillnecting.models import Post, User
from sqlalchemy import func

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
	#users = User.query.all()
	users = User.query.order_by(func.random()).limit(3).all()
	print(dir(users))
	return render_template("landing-page.html", users=users)

@main.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("blog.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title='About')

"""
@main.route("/api/users", methods=['GET', 'POST'])
def api_users():
        users = User.query.all()
        user_list = []
        print(users)
        if request.method == 'GET':
                for users in  users:
                        user_list.append(users.username)
                return jsonify({"usernames": user_list}), 201
"""

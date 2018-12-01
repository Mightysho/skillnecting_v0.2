from flask import request, Blueprint, jsonify, render_template
from skillnecting.models import User, Post

api = Blueprint('api', __name__)


@api.route("/api")
def api_route():
	return render_template("api.html")

@api.route("/api/users", methods=['GET', 'POST'])
def api_users():
    users = User.query.all()
    user_dict = {}
    print(users)
    if request.method == 'GET':
        for users in  users:
            user_dict[users.username] = users.github_username
        total_users = {'Total Users': len(user_dict)}
        return jsonify(user_dict, total_users), 201


@api.route("/api/users/techskills", methods=['GET', 'POST'])
def api_techskills():
	users = User.query.all()
	user_techskills = {}
	tech_list = []
	if request.method == 'GET':
		for users in  users:
			user_techskills[users.username] = str(users.techskills)
		total_users = {'Total Users': len(user_techskills)}
		return jsonify	(user_techskills, total_users), 201


@api.route("/api/users/posts", methods=['GET', 'POST'])
def api_posts():
	posts = Post.query.all()
	post_dict = {}
	author_post = []
	if request.method == 'GET':
		for items in posts:
			author_post.append(items.title)
			post_dict[items.author.github_username] = author_post
			#print(items.author.github_username)
		return jsonify(post_dict), 201
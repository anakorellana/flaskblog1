from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.published_at.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/nyc")
def nyc():
    return render_template('nyc.html', title='NYC')


@main.route("/paris")
def paris():
    return render_template('paris.html', title='Paris')


@main.route("/mxcity")
def mexico_city():
    return render_template('mxcity.html', title='Mexico City')


@main.route("/little_gems")
def little_gems():
    return render_template('little_gems.html', title='Little Gems')


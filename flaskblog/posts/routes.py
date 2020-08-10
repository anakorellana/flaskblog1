import os
from werkzeug.utils import secure_filename
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comments, User
from flaskblog.posts.forms import PostForm, CommentForm

APP_PHOTO_ROOT = "/Users/notcharles/Projects/flaskblog1/flaskblog/static"

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(APP_PHOTO_ROOT, "photos", filename))
        post = Post(title=form.title.data, content=form.content.data, author=current_user, image=filename)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='NewPost', form=form, legend="New Post")


@posts.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    import pdb
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print('Form Validated')
            comments = Comments(body=form.body.data, parent_id=post_id, author_id=current_user.get_id())
            db.session.add(comments)
            db.session.commit()
            flash('Your comment has been published.')
            return redirect(url_for('posts.post', post_id=post_id, page=1))
        else:
            print('Form not validated')
            print(form.errors)

    comments = []
    user_comments = Comments.query.all()
    for comment in user_comments:
        id = comment.author_id
        author = {"username": "Anonymous"}
        if id is not None:
            author = User.query.filter_by(id=id).first_or_404()
            print(author)

        comments.append({"comment": comment, "author": author})
 
    return render_template('post.html', title=post.title, post=post,
                           form=form, comments=comments)

# post = Post.query.filter_by(slug=slug).first()
    # comment = Comments.query.filter_by(post_id=post.id).filter_by(feature=True).all()
    # # post.views = post.views + 1
    # # db.session.commit()
    # # Thanks = ""
    # if request.method == "POST":
    #     pdb.set_trace()
    #     # post_id = post.id
    #     name = request.form.get('name')
    #     email = request.form.get('email')
    #     message = request.form.get('message')
    #     comment = Comments(username=name, email=email, message=message, post_id=post.id)
    #     db.session.add(comment)
    #     posts.comments = posts.comments + 1
    #     db.session.commit()
    #     flash('Your comment has been submitted will be published', 'success')
    #     return redirect(url_for('posts.post', post_id=post.id))
    #
    # return render_template('post.html', post=post, posts=posts)

    # return render_template('post.html', title=post.title, post=post)


# @posts.route('/post/<string:slug>/news', methods=['POST', 'GET'])
# def news(slug):
#     post = Post.query.filter_by(slug=slug).first()
#     comment = Comments.query.filter_by(post_id=post.id).filter_by(feature=True).all()
#     # post.views = post.views + 1
#     db.session.commit()
#     Thanks =""
#     if request.method == "POST":
#         post_id = post.id
#         name = request.form.get('username')
#         email = request.form.get('email')
#         message = request.form.get('message')
#         comment = Comments(username=name, email=email, message=message, post_id=post_id)
#         db.session.add(comment)
#         post.comments = post.comments + 1
#         db.session.commit()
#         flash('Your comment has been submitted will be published upon approval of admin', 'success')
#         return redirect(request.url)
#
#     return render_template('post.html', post=post, comment=comment, Thanks=Thanks)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/comments", methods=["GET", "POST"])
@login_required
def comments():
    comments = Comments.query.all()
    return redirect(url_for('post.html', ))
    return render_template('post.html', comments=comments)


@posts.route("/post/<int:post_id>/check/", methods=["GET", "POST"])
@login_required
def check(post_id, slug):
    comment = Comments.query.get_or_404(post_id)
    if comment.feature == True:
        comment.feature = False
        db.session.commit()
    else:
        comment.feature = True
        db.session.commit()
        flash("Your comment has been added to the post", "success")
        return redirect(url_for('posts.comments'))
    return redirect(url_for('posts.comments'))


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route('/post/<int:id>/delcomment')
@login_required
def delcomment(post_id):
    comment = Comments.query.get_or_404(post_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment has been deleted ', 'success')
    return redirect(url_for('main.home'))
#
# @posts.route('/post/<int:id>/imagepost')
# @login_required
# def image(post_id):
# #
# @posts.route("/post/<int:post_id>/comment/", methods=["GET", "POST"])
# @login_required
# def comments(post_id, slug):
#     comments = Comments.query.get_or_404(post_id)
#     form = AddCommentForm()
#     if form.validate_on_submit():
#         db.create_all()
#         comment = Comment(body=form.body.data, author=current_user)
#         db.session.add(comment)
#         db.session.commit()
#         flash("Your comment has been added to the post", "success")
#         return redirect(url_for('posts.post', post_id=post.id))
#     return render_template('comment.html', title='CommentPost', form=form, legend='New Comment')



# @posts.route('/post/messages')
# def messages():
#     result = firebase.get('/post/messages', None)
#     return render_template('main.list.html', messages=result)


# @posts.route('/post/submit_message', methods=['POST'])
# def submit_message():
#     message = {
#     'body': request.form['message'],
#     'who': request.form['who']
#   }
#   firebase.post('/post/messages', message)
#   return redirect(url_for('/post/messages'))



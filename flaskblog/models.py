import sqlalchemy
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_wtf.csrf import CSRFProtect
from flaskblog import db, login_manager
from flask_login import UserMixin
from .config import Config



from slugify import slugify

csrf = CSRFProtect()
def create_app():
    app = current_app
    csrf.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    password = db.Column(db.String(60), nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.cofig['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text(10240), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.String(150), nullable=True, default='no-image.jpg')
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    published = db.Column(db.Boolean, nullable=True, default=True)
    published_at = db.Column(db.DateTime, index=True,)
    feature = db.Column(db.String, default=1, nullable=True)
    slug = db.Column(db.String(128), nullable=True)
    comments = db.relationship('Comments', backref='posts', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    # @staticmethod
    # def generate_slug(target, value, oldvalue, initiator):
    #     if value and (not target.slug or value != oldvalue):
    #         target.slug = slugify(value)
    # db.event.listen(title, 'set', generate_slug, retval=False)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)

    body = db.Column(db.String(10240), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)


    # def save(self):
    #     URL = Config.SQLALCHEMY_DATABASE_URI
    #     engine = sqlalchemy.create_engine(URL)
    #     conn = engine.connect()
    #     sql = 'Insert into comments("id", "parent_id", "body", "author_id", "created_at", "modified_at") values (%s, %s, %s, %s, %s, %s)' \
    #           % (self.id, self.parent_id, self.body, self.author_id, self.created_at, self.modified_at)
    #     print(self.author_id)
    #     conn.execute(sql)



        # session.add(self.id, parent_id, body, author_id, created_at, modified_at)
        # db.session.commit()
        # db.session.execute



    def __repr__(self):
        return f"Comments('{self.body}', '{self.created_at}')"
#
# class Comments(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
#
#     body = db.Column(db.String(10240), nullable=True)
#     post_id = db.Column(db.Integer)
#     feature = db.Column(db.String, default=1, nullable=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     modified_at = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return f"Comment('{self.body}', '{self.created_at}')"

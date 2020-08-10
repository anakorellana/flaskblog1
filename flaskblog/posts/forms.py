from flask_wtf import FlaskForm
# from flask_wtf.file import FileAllowed
# from flask_uploads import UploadSet, IMAGES
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length

# images = UploadSet("images", IMAGES)


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Image')
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Submit')

# validators=[FileAllowed(images, "images only")

from flask_wtf import FlaskForm

from wtforms import StringField,  SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from pinterest.models import Category


class NewCategory(FlaskForm):
    """New Category Form"""
    category_name=StringField('Category Name',validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add')

    def validate_category_name(self, category_name):
        """for validation of unique category"""
        category = Category.query.filter_by(category_name=category_name.data).first()
        if category:
            raise ValidationError('Oops,Category already exists!')

from functools import wraps
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from pinterest.admin.forms import NewCategory
from flask_login import login_required, current_user
from pinterest import db
from pinterest.models import Category, User, Pins

admin = Blueprint('admin', __name__)


def admin_access(f):
    """ A decorator used for giving access only to admins for specific pages"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            return f(*args, **kwargs)
        else:
            flash('Only Admin have rights to access this page', 'error')
            abort(403)

    return decorated_function


@admin.route("/adminhome")
@login_required
@admin_access
def home():
    """Admin Home Page"""
    return render_template('admin.html')


@admin.route("/category")
@login_required
@admin_access
def category():
    """Category Home Page"""
    return render_template('category.html')


@admin.route("/addcategory", methods=['GET', 'POST'])
@login_required
@admin_access
def add_category():
    """ For adding New Category """
    form = NewCategory()
    if form.validate_on_submit():
        category = Category(category_name=form.category_name.data)
        db.session.add(category)
        db.session.commit()
        flash("Category added successfully", category='success')
        return redirect(url_for('admin.category'))
    return render_template('new_category.html', form=form, legend='New Category')


@admin.route("/viewcategory", methods=['GET'])
@login_required
@admin_access
def view_category():
    """ Viewing Categories """
    categories = Category.query.order_by(Category.category_name.asc())
    return render_template('view_category.html', categories=categories)


@admin.route("/viewcategory/delete/<category_id>", methods=['GET', 'POST'])
@login_required
@admin_access
def delete_category(category_id):
    """ Deleting Categories """
    category = Category.query.get_or_404(category_id)
    pins = Pins.query.filter_by(category_id=category_id).all()
    if pins:
        flash("You cannot delete this category", category='danger')
        return redirect(url_for('admin.view_category'))
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category has been deleted', 'success')
        return redirect(url_for('admin.view_category'))


@admin.route("/viewcategory/update/<category_id>", methods=['GET', 'POST'])
@login_required
@admin_access
def update_category(category_id):
    """Updating existing categories """
    category = Category.query.get_or_404(category_id)
    form = NewCategory()
    if form.validate_on_submit():
        category.category_name = form.category_name.data
        db.session.commit()
        flash('Your Category has been updated', 'success')
        return redirect(url_for('admin.view_category'))
    elif request.method == 'GET':
        form.category_name.data = category.category_name  # for filling values
    return render_template('new_category.html', legend='Update Category', form=form)


@admin.route("/user_info", methods=['GET', 'POST'])
@login_required
@admin_access
def view_user_info():
    """Shows user info like email,username,and total pins created by respective user"""
    # pin=db.session.query(Pins.user_id, func.count(Pins.id)).group_by(Pins.user_id).all()
    users = User.query.all()
    return render_template('user_info.html', users=users)

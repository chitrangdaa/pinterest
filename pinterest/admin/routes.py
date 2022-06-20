from flask import render_template, url_for, flash, redirect, request, Blueprint, abort


from pinterest.admin.forms import NewCategory
from flask_login import login_required, current_user
from pinterest import db
from pinterest.models import Category, User, Pins

admin = Blueprint('admin', __name__)


@admin.route("/adminhome")
def home():
    """Admin Home Page"""
    if not current_user.is_admin:
        abort(403)
    return render_template('admin.html')


@admin.route("/category")
def category():
    """Category Home Page"""
    if not current_user.is_admin:
        abort(403)
    return render_template('category.html')


@login_required
@admin.route("/addcategory", methods=['GET', 'POST'])
def add_category():
    """ For adding New Category """
    if not current_user.is_admin:
        abort(403)
    form = NewCategory()
    if form.validate_on_submit():
        category = Category(category_name=form.category_name.data)
        db.session.add(category)
        db.session.commit()
        flash("Category added successfully", category='success')
        return redirect(url_for('admin.category'))

    return render_template('new_category.html', form=form, legend='New Category')


@login_required
@admin.route("/viewcategory", methods=['GET'])
def view_category():
    """ Viewing Categories """
    if not current_user.is_admin:
        abort(403)
    categories = Category.query.order_by(Category.category_name.asc())
    return render_template('view_category.html', categories=categories)


@login_required
@admin.route("/viewcategory/delete/<category_id>", methods=['GET', 'POST'])
def delete_category(category_id):
    """ Deleting Categories """
    if not current_user.is_admin:
        abort(403)
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category has been deleted', 'success')
    return redirect(url_for('admin.view_category'))


@login_required
@admin.route("/viewcategory/update/<category_id>", methods=['GET', 'POST'])
def update_category(category_id):
    """Updating existing categories """
    if not current_user.is_admin:
        abort(403)
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


@login_required
@admin.route("/user_info", methods=['GET', 'POST'])
def view_user_info():
    """Shows user info like email,username,and total pins created by respective user"""
    #pinnn=db.session.query(Pins.user_id, func.count(Pins.id)).group_by(Pins.user_id).all()
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()

    return render_template('user_info.html', users=users)

from flask import render_template, redirect, url_for, request

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, current_user, logout_user, login_required

from config import app, db, login_manager
from models import User, Review
from forms import UserForm, LoginForm, ReviewForm, ReviewUpdateForm

from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



# Регистрация новых пользователей
@app.route('/register', methods=['GET', 'POST'])
def register():
    userForm = UserForm()

    if userForm.validate_on_submit():
        username = userForm.username.data
        password = userForm.password.data
        age = userForm.age.data
        
        hashed_password = generate_password_hash(password)
        
        user = User(
            username=username,
            hashed_password=hashed_password,
            age=age
        )
        db.session.add(user)
        db.session.commit()
    
    return render_template('register.html', form=userForm)


@app.route('/auth', methods=['GET', 'POST'])
def auth_view():
    login_form = LoginForm()

    username = login_form.username.data
    password = login_form.password.data
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.hashed_password, password):
        login_user(user)
        return redirect( url_for('user_info') )

    return render_template('auth.html', form=login_form)


@app.route('/user_info')
@login_required
def user_info():
    users = User.query.all()
    return render_template('user_info.html', users=users)
    

# Сбросить авторизацию
@app.route('/logout')
def logout():
    logout_user()
    return  redirect( url_for('user_info') )


# Вывести все отзывы
@app.route('/', methods=['GET', 'POST'])
def reviews_view():
    reviews = Review.query.all()
    return render_template('index.html', reviews=reviews)


# Добавляем новые отзывы
@app.route('/reviews/add', methods=['GET', 'POST'])
@login_required
def reviews_add():
    reviewForm = ReviewForm()

    if reviewForm.validate_on_submit():
        title = reviewForm.title.data
        content = reviewForm.content.data
        date = datetime.now()
        
        review = Review(
            title=title,
            content=content,
            date=date,
            user_id=current_user.id
        )
    
        db.session.add(review)
        db.session.commit()
    
    return render_template('reviews-add.html', form=reviewForm)


# Показать детальную страницу отзыва
@app.route('/reviews/<int:review_id>')
def get_post(review_id):
    review = Review.query.get_or_404(review_id)
    return render_template('single-review.html', review=review)


@app.route('/reviews/delete/<int:review_id>', methods=['GET', 'POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/reviews/update/<int:review_id>', methods=['GET', 'POST'])
@login_required
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
        
    form = ReviewUpdateForm()

    if form.validate_on_submit():
        review.title = form.title.data
        review.content = form.content.data
        db.session.commit()
        
        return redirect(url_for('reviews', review_id=review.id))
    
    elif request.method == 'GET':
        
        form.title.data = review.title
        form.content.data = review.content

    return render_template('reviews-update.html', form=form)



# Обработчик ошибки 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404


# Обработчик ошибки 403
@app.errorhandler(403)
def not_permitted(error):
    return render_template('403.html', error=error), 403

# Обработчик ошибки 401
@app.errorhandler(401)
def not_permitted(error):
    return render_template('401.html', error=error), 401


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=8080, debug=True)

from flask import Flask, flash, redirect, render_template, request, url_for
from models import db, Content, Category
from forms import ContentForm, CategoryForm
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

import pymysql
pymysql.install_as_MySQLdb()

# Load environment variables from .env file
load_dotenv()

# Folder where uploaded images will be saved
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql://{os.getenv('RDS_USERNAME')}:{os.getenv('RDS_PASSWORD')}"f"@{os.getenv('RDS_ENDPOINT')}/{os.getenv('RDS_DB_NAME')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db.init_app(app)


@app.route('/', methods=['GET'])
def dashboard():
    total_posts = Content.query.count()
    total_categories = Category.query.count()

    # Query to get the number of posts in each category and convert to a list of tuples
    posts_by_category = db.session.query(Category.name, db.func.count(Content.content_id))\
                                   .join(Content, Category.category_id == Content.category_id)\
                                   .group_by(Category.name).all()

    # Convert the result into a list of tuples for Google Charts
    posts_by_category_list = [['Category', 'Number of Posts']]  # Header for Google Charts
    posts_by_category_list += [(row[0], row[1]) for row in posts_by_category]

    return render_template('dashboard.html', 
                           total_posts=total_posts, 
                           total_categories=total_categories, 
                           posts_by_category=posts_by_category_list)


@app.route('/content')
def content():
    contents = Content.query.all()
    print(contents[0].content_id)
    print(contents[0].image_path)
    return render_template('content.html', contents=contents)


# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_content', methods=['GET', 'POST'])
def add_content():
    form = ContentForm()

    # Populate the category choices
    form.category_id.choices = [(c.category_id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        # Handle image upload
        image_file = request.files['image']
        if image_file and allowed_file(image_file.filename):
            # Secure the filename and save the file
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Save the content with the uploaded image path
            new_content = Content(
                title=form.title.data,
                body=form.body.data,
                author=form.author.data,
                category_id=form.category_id.data,
                image_path=filename  # Save the filename to the database
            )
            db.session.add(new_content)
            db.session.commit()
            
            flash('Content added successfully!', 'success')
            return redirect(url_for('content'))

    return render_template('add_content.html', form=form)


@app.route('/edit_content/<int:content_id>', methods=['GET', 'POST'])
def edit_content(content_id):
    content = Content.query.get_or_404(content_id)
    # content = db.session.get(Content, content.content_id)
    form = ContentForm(obj=content)
    # form = ContentForm()
    # form.category_id.choices = [(c.category_id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        # Handle image upload
        image_file = request.files['image']
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            content.image_path = filename  # Update the image path if a new image is uploaded

        # Update content fields
        content.title = form.title.data
        content.body = form.body.data
        content.author = form.author.data
        content.category_id = form.category_id.data

        # Save the updated content
        db.session.commit()
        flash('Content updated successfully!', 'success')
        return redirect(url_for('content'))

    # Populate form with existing content values if GET request
    form.title.data = content.title
    form.body.data = content.body
    form.author.data = content.author
    form.category_id.data = content.category_id

    return render_template('edit_content.html', form=form, content=content)

@app.route('/content/delete/<int:content_id>', methods=['POST'])
def delete_content(content_id):
    content = Content.query.get_or_404(content_id)
    # content = db.session.get(Content, content.content_id)

    try:
        db.session.delete(content)
        db.session.commit()
        flash('Content deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('content'))

@app.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()  # Fetch all categories
    return render_template('category_list.html', categories=categories)

@app.route('/categories/new', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()

    if form.validate_on_submit():
        new_category = Category(
            name=form.name.data,
            description=form.description.data
        )
        try:
            db.session.add(new_category)
            db.session.commit()
            flash('Category added successfully!', 'success')
            return redirect(url_for('list_categories'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('add_category.html', form=form)

@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        try:
            category.name = form.name.data
            category.description = form.description.data

            db.session.commit()
            flash('Category updated successfully!', 'success')
            return redirect(url_for('list_categories'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('edit_category.html', form=form, category=category)

@app.route('/categories/delete/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    try:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('list_categories'))


# Blog List Page (all contents)
@app.route('/blog')
def blog():
    contents = Content.query.order_by(Content.updated_at.desc()).all()
    categories = Category.query.all()  # Fetch all categories from the database
    return render_template('blog.html', contents=contents, categories=categories)


# Content Detail Page (individual post)
@app.route('/content/<int:content_id>')
def content_detail(content_id):
    content = Content.query.get_or_404(content_id)
    # content = db.session.get(Content, content.content_id)
    return render_template('content_detail.html', content=content)

@app.route('/category/<int:category_id>')
def category_posts(category_id):
    # category = Category.query.get_or_404(category_id)
    contents = Content.query.filter_by(category_id=category_id).all()
    return render_template('blog.html', contents=contents, categories=Category.query.all())

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('text')
    contents = Content.query.filter(Content.body.like(f'%{search_query}%')).all()
    return render_template('blog.html', contents=contents, categories=Category.query.all())


if __name__ == '__main__':
    app.run(debug=True)

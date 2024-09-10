from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Content Model
class Content(db.Model):
    __tablename__ = 'Content'
    
    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    status = db.Column(db.String(50), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.category_id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)

# Category Model
class Category(db.Model):
    __tablename__ = 'Category'
    
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    contents = db.relationship('Content', backref='category', lazy=True)  # Relationship with Content


    

    

# Content Management System (CMS)

## Overview
This Content Management System allows users to manage and organize content with associated categories. It provides functionality to add, edit, delete, and view content and categories, including uploading images and viewing detailed analytics of content by category.

## Features
1. **Dashboard**: Overview of the total content and categories, with analytics for the number of posts per category.
2. **Content Management**:
   - Add, Edit, Delete content.
3. **Category Management**:
   - Add, Edit, Delete categories.
   - View all categories.
4. **Search and Filters**:
   - Search content by keywords.
   - View posts by specific categories.
5. **Content Display**:
   - Blog-style display of content with category filtering.
   - Individual content detail pages.

## Installation and Setup

### Prerequisites
- Python 3.x
- Flask and its dependencies
- AWS RDS Database
- `.env` file with database configuration and secret key.

### Installation
1. Clone the repository or download the project files.
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with the following structure:
   ```
   SECRET_KEY=your_secret_key
   RDS_USERNAME=your_db_username
   RDS_PASSWORD=your_db_password
   RDS_ENDPOINT=your_db_endpoint
   RDS_DB_NAME=your_database_name
   ```

### Running the Application
1. Start the application:
   ```bash
   python app.py
   ```
2. Access the application at `http://localhost:5000`.

---

## Usage Instructions

### Dashboard
- Access the dashboard from the root URL `/`.
- View total posts, total categories, and a visual breakdown of posts per category.

### Content Management
1. **Add Content**:
   - Navigate to `/add_content`.
   - Fill out the form, upload an image (optional), and click "Submit".
2. **Edit Content**:
   - Navigate to `/edit_content/<content_id>`.
   - Update the fields as needed, including uploading a new image if desired.
3. **Delete Content**:
   - Navigate to `/content/delete/<content_id>`.
   - Confirm the deletion.

### Category Management
1. **Add Category**:
   - Navigate to `/categories/new`.
   - Enter category name and description and click "Submit".
2. **Edit Category**:
   - Navigate to `/categories/edit/<category_id>`.
   - Update the fields and click "Submit".
3. **Delete Category**:
   - Navigate to `/categories/delete/<category_id>` and confirm the deletion.

### View Posts
- View all content at `/blog`.
- View posts in a specific category at `/category/<category_id>`.
- View individual post details at `/content/<content_id>`.

### Search Content
- Use the search bar at `/search?text=<your_search_query>`.

---

## Folder Structure
- `app.py`: Main Flask application.
- `forms.py`: Defines the forms for adding/editing content and categories.
- `models.py`: Database models for `Content` and `Category`.

---

## Database Schema

### Tables
1. **Content**:
   - `content_id` (Primary Key)
   - `title`
   - `body`
   - `author`
   - `created_at`
   - `updated_at`
   - `status`
   - `category_id` (Foreign Key)
   - `image_path`
2. **Category**:
   - `category_id` (Primary Key)
   - `name`
   - `description`

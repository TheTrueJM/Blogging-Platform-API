# Blogging Platform API
A solution to the [Blogging Platform API](https://roadmap.sh/projects/blogging-platform-api) project available on [roadmap.sh](https://roadmap.sh).

This project...

## Features
- **Create Blog Post:** Create post with a title, content, category, and list of tags
- **View Blog Posts:** All posts can be viewed with their details
- **Search Blog Posts:** Ability to search for a specific post by id, or filter posts by a specific search term
- **Update Blog Post:** Update the details of an exisiting post
- **Delete Blog Post:** Delete an existing post from the database

## Installation
```
git clone https://github.com/TheTrueJM/Blogging-Platform-API.git
cd Blogging-Platform-API
py -m venv .venv

# For Windows
source .venv/Scripts/activate
# For Linux / MacOS
source .venv/bin/activate

pip install -r requirements.txt
py ./main.py
```

## Usage
### API Requests
> Create new blog post
```
POST /posts
{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"]
}
```
> Update existing blog post
```
PUT /posts/1
{
  "title": "My Updated Blog Post",
  "content": "This is the updated content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"]
}
```
> Delete existing blog post
```
DELETE /posts/1
```
> Get all blog posts
```
GET /posts
```
> Get all blog posts which contain a search term
```
GET /posts?term=tech
```
> Get existing blog post with id
```
GET /posts/1
```

### API Responses
> 200 OK
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"],
  "createdAt": "2021-09-01T12:00:00Z",
  "updatedAt": "2021-09-01T12:00:00Z"
}
```
```json
[
  {
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post.",
    "category": "Technology",
    "tags": ["Tech", "Programming"],
    "createdAt": "2021-09-01T12:00:00Z",
    "updatedAt": "2021-09-01T12:00:00Z"
  },
  {
    "id": 2,
    "title": "My Second Blog Post",
    "content": "This is the content of my second blog post.",
    "category": "Technology",
    "tags": ["Tech", "Programming"],
    "createdAt": "2021-09-01T12:30:00Z",
    "updatedAt": "2021-09-01T12:30:00Z"
  }
]
```
> 201 Created
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"],
  "createdAt": "2021-09-01T12:00:00Z",
  "updatedAt": "2021-09-01T12:00:00Z"
}
```
> 204 No Content

> 400 Bad Request
```json
{"message": {"title": "Post requires title"}}
```
> 404 Not Found
```json
{"message": "Post (id=1) not found"}
```

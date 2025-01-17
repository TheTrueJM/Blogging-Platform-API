from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from os.path import isfile
from datetime import datetime



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blogposts.db"
db = SQLAlchemy(app)
routes = Api(app)


# Table structure for posts in the database
class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    category = db.Column(db.String)
    tags = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# JSON fields/arguments to be recieved in an API request
post_args = reqparse.RequestParser()
post_args.add_argument("title", type=str, required=True, help="Post requires title")
post_args.add_argument("content", type=str, required=True, help="Post requires content")
post_args.add_argument("category", type=str, required=True, help="Post requires category")
post_args.add_argument("tags", type=str, action="append", required=True, help="Post requires tag(s)")

# Custom field to convert a string of comma seperated tag values into a list
class TagsField(fields.Raw):
    def output(self, key, posts):
        return posts.tags.split(",") if type(posts) == PostModel else []

# JSON fields/arguments to be sent in API responses
post_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "category": fields.String,
    "tags": TagsField,
    "createdAt": fields.DateTime(dt_format="iso8601"),
    "updatedAt": fields.DateTime(dt_format="iso8601")
}


class Posts(Resource):
    @marshal_with(post_fields)
    def get(self):
        if request.args.get("term"):
            term = "%" + request.args.get("term") + "%"
            posts = PostModel.query.filter(PostModel.title.like(term) | PostModel.content.like(term) | PostModel.category.like(term)).all()
        else:
            posts = PostModel.query.all()
        return posts, 200
    
    @marshal_with(post_fields)
    def post(self):
        args = post_args.parse_args()
        post = PostModel(title=args["title"], content=args["content"], category=args["category"], tags=",".join(args["tags"]))
        db.session.add(post)
        db.session.commit()
        return post, 201


def validate_post(id: int, post: PostModel | None) -> None:
    if not post:
        abort(404, message=f"Post (id={id}) not found")

class Post(Resource):
    @marshal_with(post_fields)
    def get(self, id: int):
        post = PostModel.query.filter_by(id=id).first()
        validate_post(id, post)
        return post, 200
    
    @marshal_with(post_fields)
    def put(self, id: int):
        post = PostModel.query.filter_by(id=id).first()
        validate_post(id, post)
        args = post_args.parse_args()
        post.title = args["title"]
        post.content = args["content"]
        post.category = args["category"]
        post.tags = ",".join(args["tags"])
        db.session.commit()
        return post, 200
    
    @marshal_with(post_fields)
    def delete(self, id: int):
        post = PostModel.query.filter_by(id=id).first()
        validate_post(id, post)
        db.session.delete(post)
        db.session.commit()
        return None, 204


routes.add_resource(Posts, "/posts")
routes.add_resource(Post, "/posts/<int:id>")



if __name__ == "__main__":
    # Create the database file if it does not exist
    if not isfile(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "./instance/")):
        with app.app_context():
            db.create_all()
    app.run()
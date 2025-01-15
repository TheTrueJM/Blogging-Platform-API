from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blogposts.db"
db = SQLAlchemy(app)
api = Api(app)



class PostsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    category = db.Column(db.String)
    tags = db.Column(db.String)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

class TagField(fields.Raw):
    def output(self, key, posts):
        return posts.tags.split(",") if type(posts) == PostsModel else []

post_args = reqparse.RequestParser()
post_args.add_argument("title", type=str, required=True, help="Post requires title")
post_args.add_argument("content", type=str, required=True, help="Post requires content")
post_args.add_argument("category", type=str, required=True, help="Post requires category")
post_args.add_argument("tags", type=str, action="append", required=True, help="Post requires tag(s)")

post_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "category": fields.String,
    "tags": TagField,
    "createdAt": fields.DateTime(dt_format="iso8601"),
    "updatedAt": fields.DateTime(dt_format="iso8601")
}



class Posts(Resource):
    @marshal_with(post_fields)
    def get(self):
        term = f"%{request.args.get("term") or ''}%"
        posts = PostsModel.query.filter(PostsModel.title.like(term) | PostsModel.content.like(term) | PostsModel.category.like(term)).all()
        return posts, 200
    
    @marshal_with(post_fields)
    def post(self):
        args = post_args.parse_args()
        dt = datetime.now()
        post = PostsModel(title=args["title"], content=args["content"], category=args["category"], tags=",".join(args["tags"]), createdAt=dt, updatedAt=dt)
        db.session.add(post)
        db.session.commit()
        return post, 201


class Post(Resource):
    @marshal_with(post_fields)
    def get(self, id: int):
        post = PostsModel.query.filter_by(id=id).first()
        if not post:
            abort(404, message=f"Post (id={id}) not found") ##
        return post, 200
    
    @marshal_with(post_fields)
    def put(self, id: int):
        post = PostsModel.query.filter_by(id=id).first()
        if not post:
            abort(404, message=f"Post (id={id}) not found")

        args = post_args.parse_args()
        post.title = args["title"]
        post.content = args["content"]
        post.category = args["category"]
        post.tags = ",".join(args["tags"])
        post.updatedAt = datetime.now()
        db.session.commit()
        return post, 200
    
    @marshal_with(post_fields)
    def delete(self, id: int):
        post = PostsModel.query.filter_by(id=id).first()
        if not post:
            abort(404, message=f"Post (id={id}) not found")
        db.session.delete(post)
        db.session.commit()
        return None, 204


api.add_resource(Posts, "/posts")
api.add_resource(Post, "/posts/<int:id>")



if __name__ == "__main__":
    app.run(debug = True) ## Remove Debug
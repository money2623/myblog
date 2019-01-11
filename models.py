from start_utils import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique=True,nullable=False)
	email = db.Column(db.String(120), unique=True,nullable=False)
	image_file = db.Column(db.String(20),nullable=False, default='default.jpg')
	password = db.Column(db.String(60),nullable=False)
	email_verified = db.Column(db.Integer,default=0)
	posts = db.relationship('Post', backref='author',lazy=True)
	posts_liked_by_user = db.relationship('PostLikes', backref='postlikes',lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None

		return User.query.get(user_id)


	def like_post(self, post):
		if not self.has_liked_post(post):
			like = PostLikes(user_id=self.id, post_id=post.id)
			db.session.add(like)

	def unlike_post(self, post):
		if self.has_liked_post(post):
			PostLikes.query.filter_by(
				user_id=self.id,
				post_id=post.id).delete()

	def has_liked_post(self, post):
		return PostLikes.query.filter(
			PostLikes.user_id == self.id,
			PostLikes.post_id == post.id).count() > 0

	def __repr__(self):
		return "User('{}','{}','{}')".format(self.username,self.email,self.image_file)


class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	likes = db.relationship('PostLikes', backref='post', lazy=True)

	def __repr__(self):
		return "Post('{}','{}')".format(self.title,self.date_posted)



class PostLikes(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

	def __repr__(self):
		return "PostLikes('{}','{}')".format(self.user_id,self.post_id)
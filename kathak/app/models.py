# from app import db
# from flask_login import UserMixin

# class Text(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.Text)
#     content = db.Column(db.Text)
#     date = db.Column(db.Text)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __init__(self,title,content,date,user_id):
#         self.title = title
#         self.content = content
#         self.date = date
#         self.user_id = user_id
    
#     @property
#     def serialize(self):
#         return {
#            'text_id':int(self.id),
#            'title':self.title,
#            'content':self.content,
#            'date':self.date
#         }

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     fullname = db.Column(db.Text)
#     username = db.Column(db.Text, unique=True)
#     password = db.Column(db.Text)
#     texts = db.relationship('Text',backref='user',lazy=True)

#     def __init__(self,fullname,username,password):
#         self.fullname = fullname
#         self.username = username
#         self.password = password
    
#     @property
#     def serialize(self):
#         return {
#            'user_id':int(self.id),       
#            'fullname':self.fullname,
#            'username':self.username,
#            'password':self.password,
#         }
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:khanh123@@@localhost:5432/auction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    items = db.relationship("Item", backref="user")
    bids = db.relationship("Bid", backref="user")


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    start_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bid = db.relationship("Bid", backref="item")


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))


db.create_all()
khanh = User(username="khanh pham", password="phamkhanh")
ahihi = User(username="ahihi", password="hehe")
ihaha = User(username="ihaha", password="hoho")

ball = Item(name="baseball", description="baseball", user=khanh)
coca = Item(name=" cocacola", description="a bottle of cocacola")
khanh.items.append(coca)

khanh_bid = Bid(price=22.1, item=ball, user=khanh)
ahihi_bid = Bid(price=18.0, item=ball, user=ahihi)
ihaha_bid = Bid(price=21.3, item=ball, user=ihaha)

#db.session.add(khanh)
#db.session.add(ahihi)
#db.session.add(ihaha)
#db.session.add(ball)
#db.session.add(coca)
#db.session.add()
db.session.add_all([khanh, ahihi, ihaha, ball, coca, khanh_bid, ahihi_bid, ihaha_bid])

db.session.commit()
hb = db.session.query(User.username, Bid.price).join(Bid, Item).filter(Item.name =="baseball").order_by(Bid.price).all()
print("{0[0]}: placed the highest bid of ${0[1]}".format(hb[-1]))
#db.drop_all()
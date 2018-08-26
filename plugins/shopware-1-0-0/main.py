import click
from datetime import datetime
from datetime import timedelta
from pony.orm import *
from framework.Core import Core
from framework.analysis.chat.Chat import Chat
from framework.analysis.chat.Conversation import Conversation
from framework.analysis.chat.Message import Message as FrameworkMessage
from framework.analysis.chat.Participant import Participant
from framework.analysis.purchases.Article import Article as FrameworkArticle
from framework.analysis.purchases.Purchases import Purchases
from framework.analysis.purchases.ShoppingCard import ShoppingCard
from framework.analysis.timeline.Timeline import Timeline
from framework.analysis.timeline.TimelineElement import TimelineElement

# Entity definitions


class User(Core.instance.db.Entity):
    _table_ = "s_user"
    id = PrimaryKey(int)
    email = Required(str)
    firstname = Required(str)
    lastname = Required(str)
    orders = Set("Order", reverse="user")


class Order(Core.instance.db.Entity):
    _table_ = "s_order"
    id = PrimaryKey(int)
    user = Required("User", reverse="orders", column="userID")
    ordertime = Required(str)
    invoice_shipping = Required(str)
    billing_address = Optional("BillingAddress")
    shipping_address = Optional("ShippingAddress")
    order_details = Set("OrderDetail", reverse="order")


class Article(Core.instance.db.Entity):
    _table_ = "s_articles"
    id = PrimaryKey(int)
    name = Required(str)
    description = Optional(str)
    order_details = Set("OrderDetail", reverse="article")


class BillingAddress(Core.instance.db.Entity):
    _table_ = "s_order_billingaddress"
    id = PrimaryKey(int)
    firstname = Required(str)
    lastname = Required(str)
    street = Required(str)
    zipcode = Required(str)
    city = Required(str)
    phone = Optional(str)
    order = Optional("Order", column="orderID")


class ShippingAddress(Core.instance.db.Entity):
    _table_ = "s_order_shippingaddress"
    id = PrimaryKey(int)
    firstname = Required(str)
    lastname = Required(str)
    street = Required(str)
    zipcode = Required(str)
    city = Required(str)
    phone = Optional(str)
    order = Optional("Order", column="orderID")


class OrderDetail(Core.instance.db.Entity):
    _table_ = "s_order_details"
    id = PrimaryKey(int)
    name = Required(str)
    quantity = Required(str)
    price = Required(str)
    unit = Optional(str)
    order = Required("Order", reverse="order_details", column="orderID")
    article = Required("Article", reverse="order_details", column="articleID")

# Command definitions


@click.group()
@click.pass_context
def cli(ctx):
    """ This plugin extracts chats and participants. """
    Core.instance.db.generate_mapping()


@cli.command(name="users:list")
@click.pass_context
@db_session
def list_users(ctx):
    """ Lists all users. """
    users = select(u for u in User)[:]
    for user in users:
        print({
            "id": user.id,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname
        })


@cli.command()
@click.argument('id')
@click.pass_context
@db_session
def extract(ctx, id):
    """ Generates orders for a given user id. """
    user = User[id]
    purchases = Purchases("Purchases of " + user.firstname + " " + user.lastname)
    orders = user.orders
    for order in orders:
        shipping_address = order.shipping_address.firstname + " " \
                           + order.shipping_address.lastname + " " \
                           + order.shipping_address.street + " "\
                           + order.shipping_address.zipcode + " "\
                           + order.shipping_address.city
        invoice_address = order.billing_address.firstname + " " \
                           + order.billing_address.lastname + " " \
                           + order.billing_address.street + " "\
                           + order.billing_address.zipcode + " "\
                           + order.billing_address.city
        card = ShoppingCard(invoice_address, shipping_address, order.invoice_shipping)
        details = order.order_details.order_by(OrderDetail.id)
        for detail in details:
            article = FrameworkArticle(detail.name, detail.article.description + ", " + detail.unit, detail.quantity, detail.price)
            card.add(article)
        purchases.add(card)
    Core.instance.render(purchases)


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


class SW_User(Core.instance.db.Entity):
    _table_ = "s_user"
    id = PrimaryKey(int)
    email = Required(str)
    firstname = Required(str)
    lastname = Required(str)
    orders = Set("SW_Order", reverse="user")


class SW_Order(Core.instance.db.Entity):
    _table_ = "s_order"
    id = PrimaryKey(int)
    user = Required("SW_User", reverse="orders", column="userID")
    ordertime = Required(str)
    invoice_shipping = Required(str)
    billing_address = Optional("SW_BillingAddress")
    shipping_address = Optional("SW_ShippingAddress")
    order_details = Set("SW_OrderDetail", reverse="order")


class SW_Article(Core.instance.db.Entity):
    _table_ = "s_articles"
    id = PrimaryKey(int)
    name = Required(str)
    description = Optional(str)
    order_details = Set("SW_OrderDetail", reverse="article")


class SW_BillingAddress(Core.instance.db.Entity):
    _table_ = "s_order_billingaddress"
    id = PrimaryKey(int)
    firstname = Required(str)
    lastname = Required(str)
    street = Required(str)
    zipcode = Required(str)
    city = Required(str)
    phone = Optional(str)
    order = Optional("SW_Order", column="orderID")


class SW_ShippingAddress(Core.instance.db.Entity):
    _table_ = "s_order_shippingaddress"
    id = PrimaryKey(int)
    firstname = Required(str)
    lastname = Required(str)
    street = Required(str)
    zipcode = Required(str)
    city = Required(str)
    phone = Optional(str)
    order = Optional("SW_Order", column="orderID")


class SW_OrderDetail(Core.instance.db.Entity):
    _table_ = "s_order_details"
    id = PrimaryKey(int)
    name = Required(str)
    quantity = Required(str)
    price = Required(str)
    unit = Optional(str)
    order = Required("SW_Order", reverse="order_details", column="orderID")
    article = Required("SW_Article", reverse="order_details", column="articleID")

# Command definitions


@click.group()
@click.pass_context
def cli(ctx):
    """ This plugin extracts purchases. """
    Core.instance.db.generate_mapping()


@cli.command(name="users:list")
@click.pass_context
@db_session
def list_users(ctx):
    """ Lists all users. """
    users = select(u for u in SW_User)[:]
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
    user = SW_User[id]
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
        details = order.order_details.order_by(SW_OrderDetail.id)
        for detail in details:
            article = FrameworkArticle(detail.name, detail.article.description + ", " + detail.unit, detail.quantity, detail.price)
            card.add(article)
        purchases.add(card)
    Core.instance.render(purchases)


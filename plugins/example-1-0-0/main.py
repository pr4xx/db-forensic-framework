import click
from datetime import datetime
from datetime import timedelta
from pony.orm import *
from framework.Core import Core
from framework.analysis.chat.Chat import Chat
from framework.analysis.chat.Conversation import Conversation
from framework.analysis.chat.Message import Message
from framework.analysis.chat.Participant import Participant
from framework.analysis.purchases.Article import Article
from framework.analysis.purchases.Purchases import Purchases
from framework.analysis.purchases.ShoppingCard import ShoppingCard
from framework.analysis.timeline.Timeline import Timeline
from framework.analysis.timeline.TimelineElement import TimelineElement

# Entity definitions


class Folder(Core.instance.db.Entity):
    _table_ = "folders"
    thread_key = PrimaryKey(str)

# Command definitions


@click.group()
@click.pass_context
def cli(ctx):
    """ Sample plugin description. """
    Core.instance.db.generate_mapping()


@cli.command()
@click.pass_context
@db_session
def sync(ctx):
    timeline = Timeline("my timeline")
    timeline.add(TimelineElement(datetime.now(), "header 1", "content 1"))
    timeline.add(TimelineElement(datetime.now(), "header 2", "content 2"))
    timeline.add(TimelineElement(datetime.now(), "header 3", "content 3"))
    timeline.add(TimelineElement(datetime.now() + timedelta(days=1), "header 3", "content 3"))
    timeline.add(TimelineElement(datetime.now() + timedelta(days=2), "header 3", "content 3"))
    Core.instance.render(timeline)


@cli.command()
@click.pass_context
@db_session
def sync2(ctx):
    chat = Chat("my chat")
    alice = Participant("Alice")
    bob = Participant("Bob")
    oscar = Participant("Oscar")
    conversation = Conversation()
    conversation.add(Message(alice, datetime.now(), "Hello Bob!"))
    conversation.add(Message(bob, datetime.now(), "Hello Alice! How are you?"))
    conversation.add(Message(alice, datetime.now() + timedelta(minutes=5), "I am fine!"))
    chat.add(conversation)

    conversation = Conversation()
    conversation.add(Message(alice, datetime.now(), "222Hello Bob!"))
    conversation.add(Message(bob, datetime.now(), "222Hello Alice! How are you?"))
    conversation.add(Message(alice, datetime.now() + timedelta(minutes=5), "222I am fine!"))
    conversation.add(Message(oscar, datetime.now() + timedelta(minutes=7), "Hey there"))
    chat.add(conversation)

    Core.instance.render(chat)


@cli.command()
@click.pass_context
@db_session
def sync3(ctx):
    purchases = Purchases("my purchases")
    card = ShoppingCard("Street 1 Berlin", "Street 2 Berlin", 5)
    drugs = Article("Weed", "Best quality, grams", 50, 300)
    weapons = Article("Knive", "Stainless steel, piece", 1, 55.2)
    card.add(drugs)
    card.add(weapons)
    purchases.add(card)

    Core.instance.render(purchases)

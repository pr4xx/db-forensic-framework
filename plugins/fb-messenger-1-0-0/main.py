import click
from datetime import datetime
from pony.orm import *
from framework.Core import Core
from framework.analysis.chat.Chat import Chat
from framework.analysis.chat.Conversation import Conversation
from framework.analysis.chat.Message import Message as FrameworkMessage
from framework.analysis.chat.Participant import Participant

# Entity definitions


class F_User(Core.instance.db.Entity):
    _table_ = "thread_users"
    user_key = PrimaryKey(str)
    name = Required(str)


class F_Thread(Core.instance.db.Entity):
    _table_ = "threads"
    thread_key = PrimaryKey(str)
    messages = Set("F_Message", reverse="thread")


class F_Message(Core.instance.db.Entity):
    _table_ = "messages"
    msg_id = PrimaryKey(str)
    thread = Required("F_Thread", reverse="messages", column="thread_key")
    sender = Optional(Json)
    text = Optional(str)
    timestamp_ms = Required(int)


# Command definitions


@click.group()
@click.pass_context
def cli(ctx):
    """ This plugin extracts chats and participants. """
    Core.instance.db.generate_mapping()


@cli.command()
@click.pass_context
@db_session
def extract(ctx):
    """ Generates multiple chats. """
    chat = Chat("Facebook Messenger")

    # Fetch all users and key by id
    users = {}
    db_users = select(u for u in F_User)[:]
    for user in db_users:
        users[user.user_key] = {
            "db_user": user,
            "chat_user": Participant(user.name)
        }

    # Fetch all threads
    threads = select(t for t in F_Thread)[:]
    for thread in threads:
        conversation = Conversation()
        # Fetch all messages of this thread
        messages = thread.messages.order_by(F_Message.timestamp_ms)
        for message in messages:
            if not message.sender:
                continue
            user_key = message.sender['user_key']
            time = datetime.fromtimestamp(message.timestamp_ms / 1000)
            conversation.add(FrameworkMessage(users[user_key]['chat_user'], time, message.text))
        chat.add(conversation)
    Core.instance.render(chat)


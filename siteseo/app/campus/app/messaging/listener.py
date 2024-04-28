from sqlalchemy import event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapper
from .models import Message
import json
import asyncio

message_queue = asyncio.Queue()
@event.listens_for(Message, 'after_insert')
def msg_create_alert(mapper: Mapper, connection: Connection, target):
    """Publish a message for Message insert. """
    msg_dict = {'content': target.content, 'sender': target.sender}
    m = f"You have a message: {json.dumps(msg_dict)}"
    asyncio.create_task(message_queue.put(m))
    # sse_client.send(json.dumps(target.as_dict()), type='message')
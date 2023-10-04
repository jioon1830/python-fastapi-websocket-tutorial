import asyncio
from fastapi import WebSocket


class Chat:
    members: dict[str, WebSocket]

    """Represents the chatting room."""

    def __init__(self):
        self.members = {}

    async def join(self, user: str, websocket: WebSocket):
        """Connect to the user and add user to the members on success."""

        ######### [ TODO ] #########
        # TODO Establish connection
        ############################
        await websocket.accept()


        ######### [ TODO ] #########
        # TODO Close connection on duplicate and exit method.
        ############################

        if user == "system" or user in self.members.keys():
            await websocket.close(reason=f"User {user} already exists")


        ######### [ TODO ] #########
        # TODO Otherwise, add user to the members.
        ############################
        self.members[user] = websocket
        ######### [ TODO ] #########
        # TODO Optionally, broadcast the system message that the user joined the chat.
        ############################
        message = {
            "type": "system",
            "msg": f"User {user} joined the chat"
        }
        tasks = []
        for member, member_ws in self.members.items():
            task = asyncio.create_task(member_ws.send_json(message))
            tasks.append(task)
        for task in tasks:
            await task
    async def leave(self, user: str):
        """Remove user from the members."""

        ######### [ TODO ] #########
        # TODO Remove user from the members.
        ############################
        self.members.pop(user)
        ######### [ TODO ] #########
        # TODO Optionally, broadcast the system message that the user left the chat.
        ############################
        message = {
            "from": "system",
            "msg": f"User {user} left the chat"
        }
        tasks = []
        for member, member_ws in self.members.items():
            task = asyncio.create_task(member_ws.send_json(message))
            tasks.append(task)
        for task in tasks:
            await task
    async def handle_message(self, user: str, message: dict[str, str]):
        """Handler message from user."""

        ######### [ TODO ] #########
        # TODO Check the message type and receiver.
        ############################
        message_type = message["type"]
        receiver = message['to']
        msg = message["msg"]
        ######### [ TODO ] #########
        # TODO If the valid receiver does not exist, send error message back to the sender.
        ############################
        message_from_server = {
            "from": f"{user}",
            "msg": f"{msg}"
        }
        error_message = {
            "from": "system",
            "msg": f"User {receiver} does not exist"
        }
        if message_type == "broadcast":
            tasks = []
            for member, member_ws in self.members.items():
                if member != user :
                    task = asyncio.create_task(member_ws.send_json(message_from_server))
                    tasks.append(task)
            for task in tasks:
                await task
        if message_type == "direct":
            toWebsocket = self.members.get(receiver, 0)
            if toWebsocket != 0:
                await toWebsocket.send_json(message_from_server)
            if self.members.get(receiver, 0) == 0:
                websocket = self.members.get(user)
                await websocket.send_json(error_message)

        ######### [ TODO ] #########
        # TODO Otherwise, forward the message to the receiver.
        # If broadcasting the message, DO NOT send to the original sender.
        ############################




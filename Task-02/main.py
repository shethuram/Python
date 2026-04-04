from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from database import save_message, get_messages, search_messages

app = FastAPI()

#  Global state
rooms = {}           # room -> [websockets]
usernames = {}       # websocket -> username
user_sockets = {}    # username -> websocket


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    current_room = None

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            msg_type = message.get("type")

            # 🔹 JOIN ROOM
            if msg_type == "join":
                username = message.get("username")
                room = message.get("room")

                if not username or not room:
                    continue

                current_room = room

                # store mappings
                usernames[websocket] = username
                user_sockets[username] = websocket

                if room not in rooms:
                    rooms[room] = []

                rooms[room].append(websocket)

                print(f"{username} joined {room}")

                # 🔥 SEND OLD MESSAGES (ROOM BASED)
                for user, msg in get_messages(room):
                    await websocket.send_text(json.dumps({
                        "type": "chat",
                        "username": user,
                        "message": msg
                    }))

                #  BROADCAST JOIN
                await broadcast(room, {
                    "type": "system",
                    "message": f"{username} joined {room}"
                })

                #  SEND ONLINE USERS
                await send_user_list(room)

            #  CHAT MESSAGE
            elif msg_type == "chat":
                username = usernames.get(websocket)
                msg = message.get("message")

                if not current_room or not username or not msg:
                    continue

                # save to DB
                save_message(current_room, username, msg)

                await broadcast(current_room, {
                    "type": "chat",
                    "username": username,
                    "message": msg
                })

            #  TYPING INDICATOR
            elif msg_type == "typing":
                username = usernames.get(websocket)

                if not current_room or not username:
                    continue

                await broadcast(current_room, {
                    "type": "typing",
                    "username": username
                }, exclude=websocket)

            #  PRIVATE MESSAGE
            elif msg_type == "private":
                sender = usernames.get(websocket)
                receiver = message.get("to")
                msg = message.get("message")

                if not sender or not receiver or not msg:
                    continue

                receiver_ws = user_sockets.get(receiver)

                if receiver_ws:
                    # send to receiver
                    await receiver_ws.send_text(json.dumps({
                        "type": "private",
                        "from": sender,
                        "message": msg
                    }))

                    # send back to sender (confirmation)
                    await websocket.send_text(json.dumps({
                        "type": "private",
                        "from": sender,
                        "message": msg,
                        "self": True
                    }))
        
                else:
                    # user not found / offline
                    await websocket.send_text(json.dumps({
                        "type": "system",
                        "message": f"{receiver} is not online"
                    }))


            elif msg_type == "search":
                room = current_room
                keyword = message.get("keyword")

                results = search_messages(room, keyword)

                # send only to requester
                await websocket.send_text(json.dumps({
                    "type": "search_results",
                    "results": [
                        {"username": user, "message": msg}
                        for user, msg in results
                    ]
                }))        

    except WebSocketDisconnect:
        username = usernames.get(websocket, "User")

        print(f"{username} disconnected")

        #  REMOVE FROM ROOM
        if current_room and websocket in rooms.get(current_room, []):
            rooms[current_room].remove(websocket)

        #  REMOVE FROM MAPPINGS
        if websocket in usernames:
            del usernames[websocket]

        if username in user_sockets:
            del user_sockets[username]

        #  BROADCAST LEAVE
        if current_room:
            await broadcast(current_room, {
                "type": "system",
                "message": f"{username} left the chat"
            })

            await send_user_list(current_room)


#  HELPER FUNCTIONS

async def broadcast(room, message, exclude=None):
    for conn in rooms.get(room, []):
        if conn != exclude:
            try:
                await conn.send_text(json.dumps(message))
            except:
                pass  # ignore broken connections


async def send_user_list(room):
    users = [usernames.get(ws) for ws in rooms.get(room, []) if ws in usernames]

    for conn in rooms.get(room, []):
        try:
            await conn.send_text(json.dumps({
                "type": "users",
                "users": users
            }))
        except:
            pass
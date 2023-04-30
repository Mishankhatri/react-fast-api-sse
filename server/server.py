from fastapi import FastAPI,Request
from pydantic import BaseModel
from typing import Union
from sse_starlette.sse import EventSourceResponse

from datetime import datetime
import sqlite3
import asyncio
import json


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


conn = sqlite3.connect('notifications.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
conn.close()


class Notification(BaseModel):
    name: str
    description: Union[str, None] = None

@app.get("/notification")
async def get_notifications():
    conn = sqlite3.connect('notifications.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, created_at FROM notifications ORDER BY created_at")
    rows = cursor.fetchall()
    notifications = [{"id":row[0],"name": row[1], "description": row[2], "created_at": row[3]} for row in rows]
    return {"data":notifications,"count":len(notifications)}

@app.post("/notification")
async def create_notification(notification:Notification):
    conn = sqlite3.connect('notifications.db')

    conn.execute('''
    INSERT INTO notifications (name, description) VALUES (?, ?)
    ''', (notification.name, notification.description))

    conn.commit()

    conn.close()

    return {"notification": "notification created successfully"}

@app.delete("/notification")
async def delete_notification(id:str):
    conn = sqlite3.connect('notifications.db')

    conn.execute('''
    DELETE FROM notifications WHERE id = ?
    ''', (id ))

    conn.commit()

    conn.close()

    return {"notification": f"notification with id-{id} deleted successfully"}


STREAM_DELAY = 3 # in seconds
RETRY_TIMEOUT = 15000  # in millisecond




@app.get('/stream')
async def message_stream(request: Request):
    async def event_generator():
        last_notification_id = 0
        while True:
            conn = sqlite3.connect('notifications.db')

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM notifications ORDER BY id DESC LIMIT 1')
            row = cursor.fetchone()
            if row is not None:
                notification_id, name, description, created_at = row
                if notification_id != last_notification_id:
                    last_notification_id = notification_id
                    message = {
                        "id": datetime.now().isoformat(),
                        "event": "message",
                        "retry": RETRY_TIMEOUT,
                        "data": {
                            "id": notification_id,
                            "name": name,
                            "description": description,
                            "created_at": created_at
                        }
                    }
                    yield json.dumps(message)
            else:
                last_notification_id = 0

            conn.close()

            yield {
                "id": datetime.now(),
                "event": "stale",
                "retry": RETRY_TIMEOUT,
                "data": None
            }
            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())
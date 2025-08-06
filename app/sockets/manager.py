import socketio
from fastapi import FastAPI
from socketio import ASGIApp

sio = socketio.AsyncServer(cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.on("send_message")
async def handle_send_message(sid, data):
    print(f"Message received: {data}")
    await sio.emit("receive_message", data)
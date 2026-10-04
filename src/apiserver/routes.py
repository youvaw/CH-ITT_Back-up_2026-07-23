"""
=========================================
CHITT - API Routes
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


# ---------------------------------
# Request Models
# ---------------------------------

class ChatRequest(BaseModel):

    message: str


class VoiceRequest(BaseModel):

    text: str


class VisionRequest(BaseModel):

    image: str


# ---------------------------------
# Home
# ---------------------------------

@router.get("/")
async def home():

    return {

        "project": "CHITT",

        "version": "1.0.0",

        "status": "running"

    }


# ---------------------------------
# Status
# ---------------------------------

@router.get("/status")
async def status():

    return {

        "status": "online",

        "api": "active"

    }


# ---------------------------------
# Chat
# ---------------------------------

@router.post("/chat")
async def chat(data: ChatRequest):

    return {

        "success": True,

        "reply": f"Received: {data.message}"

    }


# ---------------------------------
# Voice
# ---------------------------------

@router.post("/voice")
async def voice(data: VoiceRequest):

    return {

        "success": True,

        "text": data.text

    }


# ---------------------------------
# Vision
# ---------------------------------

@router.post("/vision")
async def vision(data: VisionRequest):

    return {

        "success": True,

        "image": data.image

    }


# ---------------------------------
# Memory
# ---------------------------------

@router.get("/memory")
async def memory():

    return {

        "success": True,

        "message": "Memory module connected."

    }


# ---------------------------------
# Automation
# ---------------------------------

@router.get("/automation")
async def automation():

    return {

        "success": True,

        "message": "Automation module connected."

    }


# ---------------------------------
# Restart
# ---------------------------------

@router.post("/restart")
async def restart():

    return {

        "success": True,

        "message": "Restart requested."

    }


# ---------------------------------
# Shutdown
# ---------------------------------

@router.post("/shutdown")
async def shutdown():

    return {

        "success": True,

        "message": "Shutdown requested."

    }
from api_server.routes import router

self.app.include_router(router)


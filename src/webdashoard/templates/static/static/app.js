/*
CHITT Dashboard - Frontend Controller
Version : 1.0.0
*/
"use strict";

/* 
=========================================
CHITT - Dashboard Frontend
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
*/

const CHITT = {

    apiBase: "/dashboard",

    websocket: null,

    connected: false,

    // ---------------------------------
    // Initialize
    // ---------------------------------

    init() {

        this.bindEvents();

        this.checkStatus();

        this.connectWebSocket();

    },

    // ---------------------------------
    // DOM Helpers
    // ---------------------------------

    element(id) {

        return document.getElementById(id);

    },

    // ---------------------------------
    // Events
    // ---------------------------------

    bindEvents() {

        const sendButton =
            this.element("send-button");

        const chatInput =
            this.element("chat-input");

        if (sendButton) {

            sendButton.addEventListener(
                "click",
                () => this.sendChat()
            );

        }

        if (chatInput) {

            chatInput.addEventListener(
                "keydown",
                (event) => {

                    if (
                        event.key === "Enter"
                    ) {

                        this.sendChat();

                    }

                }
            );

        }

        const voiceButton =
            this.element("voice-button");

        if (voiceButton) {

            voiceButton.addEventListener(
                "click",
                () => this.startVoice()
            );

        }

    },

    // ---------------------------------
    // API Request
    // ---------------------------------

    async request(

        endpoint,

        options = {}

    ) {

        const response = await fetch(

            `${this.apiBase}${endpoint}`,

            {

                headers: {

                    "Content-Type":
                        "application/json"

                },

                ...options

            }

        );

        if (!response.ok) {

            throw new Error(

                `HTTP ${response.status}`

            );

        }

        return response.json();

    },

    // ---------------------------------
    // Status
    // ---------------------------------

    async checkStatus() {

        try {

            const data =
                await this.request(
                    "/status"
                );

            this.setOnline(

                data.success === true

            );

            const apiStatus =
                this.element(
                    "api-status"
                );

            if (apiStatus) {

                apiStatus.textContent =
                    "Available";

            }

        } catch (error) {

            this.setOnline(false);

            const apiStatus =
                this.element(
                    "api-status"
                );

            if (apiStatus) {

                apiStatus.textContent =
                    "Unavailable";

            }

            console.error(
                "Status error:",
                error
            );

        }

    },

    // ---------------------------------
    // Online Indicator
    // ---------------------------------

    setOnline(online) {

        const indicator =
            this.element(
                "status-indicator"
            );

        const text =
            this.element(
                "status-text"
            );

        if (indicator) {

            indicator.classList.toggle(
                "online",
                online
            );

        }

        if (text) {

            text.textContent =
                online
                    ? "Online"
                    : "Offline";

        }

    },

    // ---------------------------------
    // Chat
    // ---------------------------------

    async sendChat() {

        const input =
            this.element(
                "chat-input"
            );

        if (!input) {

            return;

        }

        const message =
            input.value.trim();

        if (!message) {

            return;

        }

        this.addMessage(
            message,
            "user"
        );

        input.value = "";

        try {

            const data =
                await this.request(
                    "/chat",
                    {

                        method: "POST",

                        body: JSON.stringify({

                            message: message

                        })

                    }
                );

            if (data.reply) {

                this.addMessage(
                    data.reply,
                    "assistant"
                );

            }

        } catch (error) {

            this.addMessage(
                "Unable to connect to CHITT API.",
                "system"
            );

            console.error(
                "Chat error:",
                error
            );

        }

    },

    // ---------------------------------
    // Add Chat Message
    // ---------------------------------

    addMessage(

        text,

        type

    ) {

        const output =
            this.element(
                "chat-output"
            );

        if (!output) {

            return;

        }

        const message =
            document.createElement(
                "div"
            );

        message.className =
            `message ${type}`;

        message.textContent =
            text;

        output.appendChild(
            message
        );

        output.scrollTop =
            output.scrollHeight;

    },

    // ---------------------------------
    // Voice
    // ---------------------------------

    startVoice() {

        const status =
            this.element(
                "voice-status"
            );

        if (!("webkitSpeechRecognition"
            in window)) {

            if (status) {

                status.textContent =
                    "Speech recognition unavailable.";

            }

            return;

        }

        const Recognition =
            window.webkitSpeechRecognition;

        const recognition =
            new Recognition();

        recognition.lang = "en-IN";

        recognition.interimResults =
            false;

        recognition.onstart = () => {

            if (status) {

                status.textContent =
                    "Listening...";

            }

        };

        recognition.onresult = (

            event

        ) => {

            const text =
                event.results[0][0].transcript;

            if (status) {

                status.textContent =
                    text;

            }

            const input =
                this.element(
                    "chat-input"
                );

            if (input) {

                input.value = text;

            }

        };

        recognition.onerror = () => {

            if (status) {

                status.textContent =
                    "Voice recognition error.";

            }

        };

        recognition.onend = () => {

            if (status) {

                status.textContent =
                    "Voice system ready";

            }

        };

        recognition.start();

    },

    // ---------------------------------
    // WebSocket
    // ---------------------------------

    connectWebSocket() {

        const protocol =
            location.protocol === "https:"
                ? "wss:"
                : "ws:";

        const url =
            `${protocol}//${location.host}/ws`;

        try {

            this.websocket =
                new WebSocket(url);

            this.websocket.onopen = () => {

                this.connected = true;

            };

            this.websocket.onmessage = (

                event

            ) => {

                this.addMessage(
                    event.data,
                    "assistant"
                );

            };

            this.websocket.onclose = () => {

                this.connected = false;

                setTimeout(
                    () => this.connectWebSocket(),
                    3000
                );

            };

            this.websocket.onerror = (
                error
            ) => {

                console.error(
                    "WebSocket error:",
                    error
                );

            };

        } catch (error) {

            console.error(
                "WebSocket connection failed:",
                error
            );

        }

    }

};


// ---------------------------------
// Start Dashboard
// ---------------------------------

document.addEventListener(

    "DOMContentLoaded",

    () => {

        CHITT.init();

    }

);

const statusText = document.getElementById("status-text");
const apiStatus = document.getElementById("api-status");
const chatOutput = document.getElementById("chat-output");
const chatInput = document.getElementById("chat-input");
const sendButton = document.getElementById("send-button");

async function checkAPI() {
    try {
        const response = await fetch("/health");

        if (!response.ok) {
            throw new Error("API unavailable");
        }

        const data = await response.json();

        statusText.textContent = "Connected";
        apiStatus.textContent = "Online";

        return data;
    } catch (error) {
        statusText.textContent = "Disconnected";
        apiStatus.textContent = "Offline";
        console.error("API error:", error);
    }
}

function addMessage(text, type = "system") {
    const message = document.createElement("div");

    message.className = `message ${type}`;
    message.textContent = text;

    chatOutput.appendChild(message);
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

async function sendMessage() {
    const message = chatInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");
    chatInput.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        if (!response.ok) {
            throw new Error("Chat API unavailable");
        }

        const data = await response.json();

        addMessage(
            data.response || "CHITT received your message.",
            "assistant"
        );
    } catch (error) {
        console.error("Chat error:", error);
        addMessage(
            "CHITT API is not connected yet.",
            "system"
        );
    }
}

sendButton.addEventListener("click", sendMessage);

chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});

checkAPI();

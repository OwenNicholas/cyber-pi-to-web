package com.example

import io.ktor.server.application.*
import io.ktor.server.http.content.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.http.*
import io.ktor.server.websocket.*
import io.ktor.websocket.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import java.time.Duration

// Simulated data store for messages
val messages = mutableListOf(
    Message(1, "Hello from CyberPi!"),
    Message(2, "System is running smoothly.")
)

// Define Message data class for serialization
@Serializable
data class Message(val id: Int, val content: String)

fun Application.configureRouting() {
    // Install WebSockets
    install(WebSockets) {
        pingPeriod = Duration.ofSeconds(15) // Optional: Keep WebSocket alive
    }

    routing {
        // Serve static files from the 'static' directory in resources
        staticResources("/", "static")

        // HTTP Endpoint: Fetch all messages
        get("/get_messages") {
            call.respond(messages)
        }

        // HTTP Endpoint: Fetch a specific message by ID
        get("/get_message/{id}") {
            try {
                val id = call.parameters["id"]?.toIntOrNull()
                if (id == null) {
                    call.respond(HttpStatusCode.BadRequest, "Invalid or missing ID")
                    return@get
                }

                val message = messages.find { it.id == id }
                if (message == null) {
                    call.respond(HttpStatusCode.NotFound, "Message not found")
                } else {
                    call.respond(message)
                }
            } catch (e: Exception) {
                println("Error occurred: ${e.message}")
                call.respond(HttpStatusCode.InternalServerError, "An error occurred")
            }
        }

        // HTTP Endpoint: Add a new message
        post("/send_message") {
            try {
                val rawRequest = call.receiveText()
                println("Raw request body: $rawRequest")

                val messageRequest = Json.decodeFromString<Message>(rawRequest)
                val newId = (messages.maxOfOrNull { it.id } ?: 0) + 1 // Generate new ID
                val newMessage = Message(newId, messageRequest.content)
                messages.add(newMessage)
                println("Message successfully added: $newMessage")

                call.respond(HttpStatusCode.Created, "Message added successfully with ID $newId")
            } catch (e: Exception) {
                println("Error occurred: ${e.message}")
                e.printStackTrace()
                call.respond(HttpStatusCode.BadRequest, "Invalid request payload.")
            }
        }

        // WebSocket Endpoint: Real-time communication
        webSocket("/ws") {
            send("WebSocket connection established!")
            println("WebSocket client connected.")

            // Listen for incoming messages
            for (frame in incoming) {
                when (frame) {
                    is Frame.Text -> {
                        val receivedText = frame.readText()
                        println("WebSocket received: $receivedText")

                        // Handle received text as a new message
                        val newId = (messages.maxOfOrNull { it.id } ?: 0) + 1
                        val newMessage = Message(newId, receivedText)
                        messages.add(newMessage)
                        println("WebSocket added message: $newMessage")

                        // Respond with acknowledgment
                        send("Message added successfully: $newMessage")
                    }
                    else -> {
                        println("Unsupported frame type received.")
                    }
                }
            }

            println("WebSocket client disconnected.")
        }
    }
}
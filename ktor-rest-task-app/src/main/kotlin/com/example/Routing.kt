package com.example

import io.ktor.server.application.*
import io.ktor.server.http.content.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.http.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

// Simulated data store for messages
val messages = mutableListOf(
    Message(1, "Hello from CyberPi!"),
    Message(2, "System is running smoothly.")
)

// Define Message data class for serialization
@Serializable
data class Message(val id: Int, val content: String)

fun Application.configureRouting() {
    routing {
        // Serve static files from the 'static' directory in resources
        staticResources("/", "static")

        // Endpoint to fetch messages
        get("/get_messages") {
            // Respond with the list of messages in JSON format
            call.respond(messages)
        }

        // Endpoint to add a message
        post("/send_message") {
            try {
                // Expecting a JSON payload
                val messageRequest = call.receive<Message>()
                // Create a new message with a unique ID
                val newMessage = Message(messages.size + 1, messageRequest.content)
                // Add the new message to the list
                messages.add(newMessage)
                call.respond(HttpStatusCode.Created, "Message added successfully.")
            } catch (e: Exception) {
                call.respond(HttpStatusCode.BadRequest, "Invalid request payload.")
            }
        }
    }
}
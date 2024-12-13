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
    Message("Hello from CyberPi!"),
    Message("System is running smoothly.")
)

// Define Message data class for serialization
@Serializable
data class Message(val content: String)

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
                // Log raw request body
                val rawRequest = call.receiveText()
                println("Raw request body: $rawRequest")
                
                // Attempt to parse the JSON payload
                val messageRequest = Json.decodeFromString<Message>(rawRequest)
                println("Parsed message: $messageRequest")
                
                // Add the message to the list
                val newMessage = Message(messageRequest.content)
                messages.add(newMessage)
                println("Message successfully added: $newMessage")
                
                call.respond(HttpStatusCode.Created, "Message added successfully.")
            } catch (e: Exception) {
                println("Error occurred: ${e.message}")
                e.printStackTrace()
                call.respond(HttpStatusCode.BadRequest, "Invalid request payload.")
            }
        }
    }
}
package com.example

import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.http.*
import kotlinx.serialization.Serializable
import org.litote.kmongo.coroutine.coroutine
import org.litote.kmongo.eq
import org.litote.kmongo.reactivestreams.KMongo
import kotlinx.serialization.json.Json

// Initialize MongoDB client and database
val client = KMongo.createClient().coroutine
val database = client.getDatabase("message_db") // Replace with your DB name
val collection = database.getCollection<Message>("messages")

@Serializable
data class Message(val id: Int = 0, val content: String)

fun Application.configureRouting() {
    routing {
        // Fetch all messages
        get("/get_messages") {
            val allMessages = collection.find().toList() // Retrieve all messages from MongoDB
            call.respond(allMessages)
        }

        // Fetch a single message by ID
        get("/get_message/{id}") {
            val id = call.parameters["id"]?.toIntOrNull()
            if (id == null) {
                call.respond(HttpStatusCode.BadRequest, "Invalid or missing ID")
                return@get
            }

            val message = collection.findOne(Message::id eq id)
            if (message == null) {
                call.respond(HttpStatusCode.NotFound, "Message not found")
            } else {
                call.respond(message)
            }
        }
        val json = Json { ignoreUnknownKeys = true }
        post("/send_message") {
            try {
                // Print raw body for debugging
                val rawRequest = call.receiveText()
                println("Raw request body: $rawRequest")
                
                // Parse incoming JSON into Message object
                val messageRequest = Json.decodeFromString<Message>(rawRequest)
                println("Parsed message: $messageRequest")
                
                // Assign an ID if it's missing or invalid
                val newId = (collection.find().toList().maxOfOrNull { it.id } ?: 0) + 1
                val newMessage = Message(newId, messageRequest.content)
                
                // Save message into MongoDB
                collection.insertOne(newMessage)
                println("Message successfully added: $newMessage")

                call.respond(HttpStatusCode.Created, "Message added successfully with ID ${newMessage.id}")
            } catch (e: Exception) {
                println("Error: ${e.message}")
                e.printStackTrace()
                call.respond(HttpStatusCode.BadRequest, "Invalid request payload.")
            }
        }
    }
}
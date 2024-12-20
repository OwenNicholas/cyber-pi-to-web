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
import org.litote.kmongo.and
import java.io.File

// Initialize MongoDB client and database
val client = KMongo.createClient().coroutine
val database = client.getDatabase("message_db") // Replace with your DB name
val collection = database.getCollection<Message>("messages")

@Serializable
data class Message(val id: Int = 0, val sensor: String, val value: Int)

fun Application.configureRouting() {
    routing {
        get("/"){
            val file = File("src/main/resources/static/dashboard.html")
            if (file.exists()) {
                call.respondFile(file)
            } else {
                call.respondText("Dashboard page not found!", status = HttpStatusCode.NotFound)
            }
        }


        // Fetch all messages
        get("/get_messages") {
            val allMessages = collection.find().toList() // Retrieve all messages from MongoDB
            call.respond(allMessages)
        }

        get("/count_sensors") {
            try {
                val sensorCount = collection.countDocuments() // Count all documents in the "messages" collection
                call.respond(mapOf("count" to sensorCount))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, "Failed to fetch sensor count.")
            }
        }

        // Fetch a single message by sensor name
        get("/get_message/{sensor}") {
            val sensor = call.parameters["sensor"]
            if (sensor == null) {
                call.respond(HttpStatusCode.BadRequest, "Missing sensor name")
                return@get
            }

            val message = collection.findOne(Message::sensor eq sensor)
            if (message == null) {
                call.respond(HttpStatusCode.NotFound, "Message not found for sensor: $sensor")
            } else {
                call.respond(message)
            }
        }

        val json = Json { ignoreUnknownKeys = true }
        // Add a new message
        post("/send_message") {
            try {
                val rawRequest = call.receiveText()
                println("Raw request body: $rawRequest")

                // Parse incoming JSON into Message object
                val messageRequest = json.decodeFromString<Message>(rawRequest)

                // Check for unique sensor
                val existingMessage = collection.findOne(Message::sensor eq messageRequest.sensor)
                if (existingMessage != null) {
                    call.respond(HttpStatusCode.Conflict, "Sensor '${messageRequest.sensor}' already exists.")
                    return@post
                }

                // Assign a new ID
                val newId = (collection.find().toList().maxOfOrNull { it.id } ?: 0) + 1
                val newMessage = Message(newId, messageRequest.sensor, messageRequest.value)

                // Save message into MongoDB
                collection.insertOne(newMessage)
                println("Message successfully added: $newMessage")

                call.respond(HttpStatusCode.Created, "Message added successfully with sensor '${newMessage.sensor}'")
            } catch (e: Exception) {
                println("Error: ${e.message}")
                e.printStackTrace()
                call.respond(HttpStatusCode.BadRequest, "Invalid request payload. Ensure 'sensor' and 'value' are provided.")
            }
        }

        // Update an existing message by sensor
        put("/update_message/{sensor}") {
            val sensor = call.parameters["sensor"]
            if (sensor == null) {
                call.respond(HttpStatusCode.BadRequest, "Missing sensor name")
                return@put
            }

            try {
                val rawRequest = call.receiveText()
                println("Raw request body: $rawRequest")

                // Parse incoming JSON into Message object
                val updateRequest = json.decodeFromString<Message>(rawRequest)
                println("Parsed update request: $updateRequest")

                // Find and update the message
                val existingMessage = collection.findOne(Message::sensor eq sensor)
                if (existingMessage == null) {
                    call.respond(HttpStatusCode.NotFound, "Message not found for sensor: $sensor")
                } else {
                    val updatedMessage = existingMessage.copy(value = updateRequest.value)
                    collection.replaceOne(Message::sensor eq sensor, updatedMessage)
                    println("Message successfully updated: $updatedMessage")
                    call.respond(HttpStatusCode.OK, "Message updated successfully for sensor '${sensor}'")
                }
            } catch (e: Exception) {
                println("Error: ${e.message}")
                e.printStackTrace()
                call.respond(HttpStatusCode.BadRequest, "Invalid request payload.")
            }
        }
    }
}
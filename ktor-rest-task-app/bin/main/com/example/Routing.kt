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
val weatherCollection = database.getCollection<Weather>("weather")
val requestLogs = mutableListOf<RequestLog>()

@Serializable
data class Message(val id: Int = 0, val sensor: String, val value: Int)
@Serializable
data class Weather(val id: Int = 0, val weather: String, val temperature: Int, val city: String, val country: String)
@Serializable
data class RequestLog(val method: String, val endpoint: String, val userAgent: String, val timestamp: Long){
    // Generate the formatted log string
    fun formattedLog(): String {
        return "$userAgent sent a $method request to $endpoint"
    }
}
fun Application.configureRouting() {
    routing {
        intercept(ApplicationCallPipeline.Monitoring) {
            val method = call.request.local.method.value
            val endpoint = call.request.path()
            val userAgent = call.request.headers["User-Agent"] ?: "Unknown"
            val timestamp = System.currentTimeMillis()

            // Add the request log to the list
            requestLogs.add(RequestLog(method, endpoint, userAgent, timestamp))

            proceed()
        }

        // Serve the logs as formatted strings
        get("/logs") {
            val formattedLogs = requestLogs.map { it.formattedLog() }
            call.respond(formattedLogs)
        }
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

        post("/send_weather"){
            try{
                val rawRequest = call.receiveText()
                println("Raw request body: $rawRequest")

                // Parse incoming JSON into Weather object
                val weatherRequest = json.decodeFromString<Weather>(rawRequest)
                val newId = (weatherCollection.find().toList().maxOfOrNull { it.id } ?: 0) + 1
                val newWeather = Weather(newId, weatherRequest.weather, weatherRequest.temperature, weatherRequest.city, weatherRequest.country)

                // Insert the weather data into MongoDB
                weatherCollection.insertOne(newWeather)
                println("Weather data successfully added: $newWeather")

                call.respond(HttpStatusCode.Created, "Weather data added successfully with ID ${newWeather.id}")
            } catch (e: Exception) {
                println("Error: ${e.message}")
                e.printStackTrace()
                call.respond(HttpStatusCode.BadRequest, "Invalid request payload. Ensure 'weather' and 'temperature' are provided.")
            }
        }

        get("/get_weather") {
            val latestWeather = weatherCollection.find().toList().maxByOrNull { it.id } // Get the entry with the largest id
            if (latestWeather != null) {
                call.respond(latestWeather)
            } else {
                call.respond(HttpStatusCode.NotFound, "No weather data available.")
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
package com.example

import com.mongodb.ConnectionString
import com.mongodb.client.MongoClient
import com.mongodb.client.MongoClients
import org.litote.kmongo.KMongo
import org.litote.kmongo.getCollection

object MongoDBClient {
    private val mongoUri = "mongodb://localhost:27017" // Change to your MongoDB URI
    private val client: MongoClient = KMongo.createClient(ConnectionString(mongoUri))
    private val database = client.getDatabase("message_db") // Database name

    val messageCollection = database.getCollection<Message>() // Collection for messages
    val weatherCollection = database.getCollection<Weather>()
}
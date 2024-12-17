plugins {
    kotlin("jvm") version "1.9.22"
    id("io.ktor.plugin") version "2.3.3"
    kotlin("plugin.serialization") version "1.8.0" // Ensure this line exists
    application
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("io.ktor:ktor-server-core:2.3.3")
    implementation("io.ktor:ktor-server-netty:2.3.3")
    implementation("io.ktor:ktor-server-html-builder:2.3.3")
    implementation("io.ktor:ktor-server-content-negotiation:2.3.3")
    implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.3")
    implementation("ch.qos.logback:logback-classic:1.4.11")
    implementation("org.jetbrains.kotlinx:kotlinx-html-jvm:0.9.1")

    // Ktor client dependencies
    implementation("io.ktor:ktor-client-core:2.3.3") // Core Ktor client
    implementation("io.ktor:ktor-client-cio:2.3.3")  // CIO engine for HTTP requests

    // KMongo for MongoDB
    implementation("org.litote.kmongo:kmongo:4.9.0") // KMongo core
    implementation("org.litote.kmongo:kmongo-coroutine:4.9.0") // Coroutine support

    // Kotlinx Serialization
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0") // Latest version for JSON support

    // Test dependencies
    testImplementation("io.ktor:ktor-server-tests:2.3.3")
    testImplementation("org.jetbrains.kotlin:kotlin-test:1.9.22")
}

application {
    mainClass.set("com.example.ApplicationKt")
}


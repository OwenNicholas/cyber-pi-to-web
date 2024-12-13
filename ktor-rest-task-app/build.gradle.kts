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
    implementation("ch.qos.logback:logback-classic:1.4.11")
    implementation("io.ktor:ktor-server-core:2.3.3")
    implementation("io.ktor:ktor-server-netty:2.3.3")
    implementation("io.ktor:ktor-server-html-builder:2.3.3")
    implementation("io.ktor:ktor-server-content-negotiation:2.3.3")
    implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.3")
    implementation("org.jetbrains.kotlinx:kotlinx-html-jvm:0.7.3")
    implementation("io.ktor:ktor-client-core:2.x.x") // Core Ktor client
    implementation("io.ktor:ktor-client-cio:2.x.x") 
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.x.x")

    testImplementation("io.ktor:ktor-server-tests:2.3.3")
    testImplementation("org.jetbrains.kotlin:kotlin-test:1.9.22")
}

application {
    mainClass.set("com.example.ApplicationKt")
}


import kotlinx.serialization.Serializable
import org.bson.codecs.pojo.annotations.BsonId
import org.bson.types.ObjectId

@Serializable
data class Message(
    @BsonId val id: String = ObjectId().toString(), // MongoDB ObjectId as ID
    val content: String
)
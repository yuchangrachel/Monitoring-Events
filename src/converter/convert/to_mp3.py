import pika, json,tempfile, os
from bson.objectid import ObjectId
import moviepy.editor

def start(message, fs_videos, fs_mp3, channel):
    message = json.loads(message)

    # empty temp file
    temp = tempfile.NamedTemporaryFile()
    # get video file
    out = fs_videos.get(ObjectId(message["video_fid"]))
    temp.write(out.read())
    # create audio from temp file
    audio = moviepy.editor.AudioFileClip(temp.name).audio
    temp.close()

    # write audio to mp3 file
    temp_path = tempfile.gettempdir() + "/" + message["video_fid"] + ".mp3"
    audio.write_audiofile(temp_path)

    # save file to mongo
    f = open(temp_path, "rb")
    data = f.read()
    fid = fs_mp3.put(data)
    f.close()
    os.remove(temp_path)

    message["mp3_fid"] = str(fid)
    # send message to video queue
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as e:
        fs_mp3.delete(fid)
        return f"Failed to publish message: {e}"

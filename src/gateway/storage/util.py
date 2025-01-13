import pika, json

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as e:
        return "Internal server error", 500
    
    message = json.dumps({
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"]
    })

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as e:
        fs.delete(fid)
        return "Internal server error", 500

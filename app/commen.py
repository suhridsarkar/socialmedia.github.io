from datetime import datetime
import uuid

def greet():

    now = datetime.now()
    hour = now.hour

    if hour < 12:
        return "Good Morning"
    elif hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

def generate_id():
    unique_id = str(uuid.uuid4().int)[:10]
    return unique_id


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'])



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

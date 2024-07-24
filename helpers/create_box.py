from models.box import Box

def create_box(data, id):
    return Box(
        x=data['x'],
        y=data['y'],
        width=data['width'],
        height=data['height'],
        image_id=id
    )
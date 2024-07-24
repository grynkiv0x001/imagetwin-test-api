from flask import Blueprint, request, jsonify

from db import db

from models.image import Image
from models.box import Box

from helpers import create_box

image_bp = Blueprint('image', __name__)

@image_bp.route('/save', methods=['POST'])
def save_image():
    data = request.get_json()

    image_value = data.get('image')
    image_origin_value = data.get('origin_image')
    image_id = data.get('id')
    boxes = data.get('boxes', [])

    if not image_value:
        return jsonify({"error": "No image provided"}), 400

    if image_id:
        image = Image.query.get(image_id)
        if image:
            image.value = image_value
            Box.query.filter_by(image_id=image_id).delete()

            new_boxes = [create_box(box, image_id) for box in boxes]
            db.session.add_all(new_boxes)
            db.session.commit()

            return jsonify({"message": "Image updated", "id": image.id}), 200
        else:
            return jsonify({"error": "Image not found"}), 404
    else:
        new_image = Image(value=image_value, origin_value=image_origin_value)
        db.session.add(new_image)
        db.session.commit()

        new_boxes = [create_box(box, new_image.id) for box in boxes]
        db.session.add_all(new_boxes)
        db.session.commit()

        return jsonify({"message": "Image saved", "id": new_image.id}), 201

@image_bp.route('/load/<int:image_id>', methods=['GET'])
def load_image(image_id):
    image = Image.query.get(image_id)

    if not image:
        return jsonify({"error": "Image not found"}), 404

    boxes = Box.query.filter_by(image_id=image_id).all()
    boxes_data = [{
        "id": box.id,
        "x": box.x,
        "y": box.y,
        "width": box.width,
        "height": box.height
    } for box in boxes]

    return jsonify({
        "id": image.id,
        "image": image.value,
        "origin_image": image.origin_value,
        "boxes": boxes_data
    })

@image_bp.route('/delete/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"error": "Image not found"}), 404

    Box.query.filter_by(image_id=image_id).delete()

    db.session.delete(image)
    db.session.commit()

    return jsonify({"message": "Image deleted"}), 204

@image_bp.route('/overview', methods=['GET'])
def overview():
    images = Image.query.all()
    images_data = [{"id": img.id, "image": img.value} for img in images]

    return jsonify(images_data)

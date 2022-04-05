from flask import Blueprint
from app.controllers import anime_controller


bp = Blueprint("animes", __name__, url_prefix="/animes")


bp.get("")(anime_controller.get_all)
bp.post("")(anime_controller.create)
bp.get("/<int:anime_id>")(anime_controller.get_by_id)
bp.delete("/<int:anime_id>")(anime_controller.delete)
bp.patch("/<int:anime_id>")(anime_controller.update)

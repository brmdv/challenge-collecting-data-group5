from dataclasses import dataclass
from typing import Dict


@dataclass
class Property:
    """Dataclass that represents a property."""

    locality: str = None
    property_type: str = None
    property_subtype: str = None
    price: float = None
    sale_type: str = None
    number_rooms: int = None
    area: float = None
    fully_equipped_kitchen: bool = None
    is_furnished: bool = None
    has_open_fire: bool = None
    has_terrace: bool = None
    terrace_area: float = None
    has_garden: bool = None
    garden_area: float = None
    land_surface: float = None
    land_plot_area: float = None
    number_facades: int = None
    has_swimming_pool: bool = None
    building_state: str = None

    def __str__(self) -> str:
        return (
            f"Property {self.id}" + f" ({self.property_type})"
            if self.property_type
            else ""
        )

    def to_csv(self) -> str:
        pass

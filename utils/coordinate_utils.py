def validate_coordinates(coordinates: tuple[int, int]) -> None:
    """
    Validates that the provided coordinates are non-negative.

    :param coordinates: A tuple containing the x and y coordinates.
    :raises ValueError: If any coordinate is negative.
    """
    x, y = coordinates
    if x < 0 or y < 0:
        raise ValueError(f"Invalid coordinates: ({x}, {y}). Coordinates must be non-negative.")

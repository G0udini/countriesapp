ADDITIONAL_NOT_FOUND_CITY_SCHEMA = {
    404: {
        "description": "The item was not found",
        "content": {
            "application/json": {"example": {"detail": "City 'Moscow' was not found"}}
        },
    }
}

ADDITIONAL_CONFLICT_CITY_SCHEMA = {
    409: {
        "description": "The item already exists",
        "content": {
            "application/json": {"example": {"detail": "City 'Moscow' already exists"}}
        },
    }
}


ADDITIONAL_NOT_FOUND_SIGHT_SCHEMA = {
    404: {
        "description": "The item was not found",
        "content": {
            "application/json": {
                "example": {"detail": "City 'Red Square' was not found"}
            }
        },
    }
}

ADDITIONAL_CONFLICT_SIGHT_SCHEMA = {
    409: {
        "description": "The item already exists",
        "content": {
            "application/json": {
                "example": {"detail": "Sight 'Red Square' already exists"}
            }
        },
    }
}

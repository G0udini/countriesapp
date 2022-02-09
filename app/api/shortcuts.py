ADDITIONAL_NOT_FOUND_SCHEMA = {
    404: {
        "description": "The item was not found",
        "content": {
            "application/json": {"example": {"detail": "City Moscow was not found"}}
        },
    }
}

ADDITIONAL_CONFLICT_SCHEMA = {
    409: {
        "description": "The item already exists",
        "content": {
            "application/json": {"example": {"detail": "City Moscow already exists"}}
        },
    }
}

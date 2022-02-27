# City additional schemas
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

# Sights additional schemas
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

# User additional schemas
ADDITIONAL_INACTIVE_USER_SCHEMA = {
    400: {
        "description": "Inactive user",
        "content": {"application/json": {"example": {"detail": "Inactive user"}}},
    }
}

ADDITIONAL_UNAUTHORIZED_INCORRECT_SCHEMA = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {"detail": "Incorrect username or password"}
            }
        },
    }
}

ADDITIONAL_CONFLICT_USER_SCHEMA = {
    409: {
        "description": "User already exists",
        "content": {
            "application/json": {"example": {"detail": "User 'Ruslan' already exists"}}
        },
    }
}

ADDITIONAL_SUCCESSFUL_CREATED_USER_SCHEMA = {
    200: {
        "description": "Successfully",
        "content": {
            "application/json": {"example": {"detail": "User successfully created"}}
        },
    }
}

ADDITIONAL_NOT_FOUND_USER_SCHEMA = {
    404: {
        "description": "User was not found",
        "content": {
            "application/json": {"example": {"detail": "User 'Ruslan' was not found"}}
        },
    }
}


ADDITIONAL_PERMISSION_SCHEMA = {
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {"example": {"detail": "Not enough permissions"}}
        },
    }
}

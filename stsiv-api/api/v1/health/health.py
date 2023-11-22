"""
Thise module contains some service routes need for application check-ups
"""
from fastapi import APIRouter, status, HTTPException
# from src.containers.base_container import BaseContainer

health_router = APIRouter()

@health_router.get("/ishealth", status_code=status.HTTP_200_OK)
def get_health():
    """
    This route is used in shell script as PING analogue.

    Returns:
        Application status if everything were fine.
    """
    return {"status": "service is healthy"}

@health_router.get("/ping", status_code=status.HTTP_200_OK)
def ping():
    """
    Simple route to check if service is running.
    
    Returns:
        A simple 'pong' message.
    """
    return {"message": "pong"}

# @router.get("/dbcheck", status_code=status.HTTP_200_OK)
# async def check_db():
#     """
#     Checks the connectivity to the database.
    
#     Returns:
#         Status of the database connection.
#     """
#     if await BaseContainer.async_db.is_connected():
#         return {"status": "database is connected"}
#     raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                             detail="Database is not connected")

# @router.get("/fullcheck", status_code=status.HTTP_200_OK)
# def full_check():
#     """
#     Aggregated health check that checks all aspects of the service.
    
#     Returns:
#         Status of all health checks.
#     """
#     checks = {
#         "service": get_health(),
#         "database": check_db()  # Note: You might want to handle potential exceptions here.
#     }

#     # If any check fails, raise a 503 error.
#     for check, result in checks.items():
#         if result.get("status") != f"{check} is healthy":
#             raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                                                     detail=f"{check} check failed")
#     return checks

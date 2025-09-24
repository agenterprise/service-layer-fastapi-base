import logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def health(request: Request):
   return {"status": "healthy"}
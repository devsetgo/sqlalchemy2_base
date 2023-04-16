# -*- coding: utf-8 -*-

import psutil
from loguru import logger


async def get_processes() -> list:
    """
    Get running processes and filter by python processes
    Returns:
        dict -- [pid, name, username]
    """
    result = []
    proc = psutil.process_iter(attrs=["pid", "name", "username"])
    process_check = ["python", "python3", "gunicorn", "uvicorn", "hypercorn", "daphne"]

    for p in proc:
        if p.info["name"] in process_check:
            result.append(p.info)

    logger.debug(result)
    return result

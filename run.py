#!/usr/bin/env python3
import asyncio
import logging
import sys
import time

from astrolive.client import AstroLive
from astrolive.errors import AstroLiveError

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s (%(threadName)s) [%(funcName)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

COLOR_BLACK = "1;30"
COLOR_RED = "1;31"
COLOR_GREEN = "1;32"
COLOR_BROWN = "1;33"
COLOR_BLUE = "1;34"
COLOR_PURPLE = "1;35"
COLOR_CYAN = "1;36"

BANNER = (
    "\n░█████╗░░██████╗████████╗██████╗░░█████╗░██╗░░░░░██╗██╗░░░██╗███████╗\n"
    + "██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░██║██║░░░██║██╔════╝\n"
    + "███████║╚█████╗░░░░██║░░░██████╔╝██║░░██║██║░░░░░██║╚██╗░██╔╝█████╗░░\n"
    + "██╔══██║░╚═══██╗░░░██║░░░██╔══██╗██║░░██║██║░░░░░██║░╚████╔╝░██╔══╝░░\n"
    + "██║░░██║██████╔╝░░░██║░░░██║░░██║╚█████╔╝███████╗██║░░╚██╔╝░░███████╗\n"
    + "╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚══════╝╚═╝░░░╚═╝░░░╚══════╝\n"
)


def esc(code):
    return f"\033[{code}m"


async def main() -> None:
    """AstroLive Main Thread."""

    print(f"{esc(COLOR_RED)}{BANNER}{esc('0')}")

    al = AstroLive()

    start = time.time()
    await al.link_observatory()
    await al.start_looper()
    try:
        while True:
            await al.start_monitoring()
            await al.health_check()
            await asyncio.sleep(al.check_interval)
            await al.link_observatory()
    except AstroLiveError as err:
        _LOGGER.error(err)

    end = time.time()
    _LOGGER.info(f"Execution time: %s seconds", end - start)


asyncio.run(main())

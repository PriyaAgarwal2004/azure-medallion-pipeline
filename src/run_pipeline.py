import logging
import subprocess
import sys

from config import setup_logging

STAGES = ["extract.py", "transform.py", "gold.py"]


if __name__ == "__main__":
    setup_logging()
    logging.info("Pipeline started")
    for stage in STAGES:
        result = subprocess.run([sys.executable, f"src/{stage}"])
        if result.returncode != 0:
            logging.error("Stage %s failed, stopping the pipeline", stage)
            sys.exit(1)
    logging.info("Pipeline finished")
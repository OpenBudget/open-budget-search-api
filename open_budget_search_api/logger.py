import sys
import logging

logger = logging.getLogger('obudget')
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

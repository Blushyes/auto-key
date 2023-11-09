import logging

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger('GLOBAL')
logger.setLevel(logging.INFO)

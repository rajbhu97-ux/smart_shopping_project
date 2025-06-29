import logging

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s")

# stream handler to log the data in console
stream_handler = logging.StreamHandler()

#file handler to log the data in file
file_handler = logging.FileHandler("smartshopping.log")

stream_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)





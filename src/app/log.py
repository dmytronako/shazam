from loguru import logger


logger.add("app.logs", level='debug', format='{level} {time} : {message}')

import logging
import logging.handlers

def get_logger():
    """
    로깅 인스턴스 
    """

    # create logger
    logger = logging.getLogger('logger')
    # set logger level
    logger.setLevel(logging.DEBUG)

    # create consele hendler and set level to debug
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('../rsc/log/log.txt')

    # create formmater 
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s >> file::%(filename)s - line::%(lineno)s'
    )
    # add formatter to handler
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # add new_hanler to logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    # 로거 정의
    import logger 
    logger = get_logger()

    logger.debug('test debug')
    logger.info('test info')
    logger.warning('test warning')
    logger.error('test error')
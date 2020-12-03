# encoding: utf-8

"""
@project = zlr数据处理
@file_name = mlogger
@author = liang jian
@email = leungjain@qq.com
@datetime = 2020/9/21 0021 上午 11:40
@from = office desktop
"""
import logging
import datetime as dt

# from log4mongo.handlers import MongoHandler
from log4mongo.handlers import BufferedMongoHandler


class MongoFormatter(logging.Formatter):
    """
    常规的日志Formatter
    """
    DEFAULT_PROPERTIES = logging.LogRecord(
        '', '', '', '', '', '', '', '').__dict__.keys()

    def __init__(self, loggerName=None, fmt=None, datefmt=None, style='%'):
        logging.Formatter.__init__(self, fmt, datefmt, style)
        self.loggerName = loggerName

    def format(self, record):
        """Formats LogRecord into python dictionary."""
        # Standard document
        document = {
            'timestamp': dt.datetime.now(),
            'level': record.levelname,
            # 'thread': record.thread,
            # 'threadName': record.threadName,
            'message': record.getMessage(),
            'loggerName': self.loggerName,
            'fileName': record.pathname,
            'module': record.module,
            'method': record.funcName,
            'lineNumber': record.lineno
        }
        # Standard document decorated with exception info
        if record.exc_info is not None:
            document.update({
                'exception': {
                    'message': str(record.exc_info[1]),
                    'code': 0,
                    'stackTrace': self.formatException(record.exc_info)
                }
            })
        # Standard document decorated with extra contextual information
        if len(self.DEFAULT_PROPERTIES) != len(record.__dict__):
            contextual_extra = set(record.__dict__).difference(
                set(self.DEFAULT_PROPERTIES))
            if contextual_extra:
                for key in contextual_extra:
                    document[key] = record.__dict__[key]
        extra = document.pop('extra', {})
        return {**document, **extra}


class MongoRecorder(logging.Formatter):
    """
    用来记录api接口被访问的记录
    """
    DEFAULT_PROPERTIES = logging.LogRecord(
        '', '', '', '', '', '', '', '').__dict__.keys()

    def __init__(self, loggerName=None, fmt=None, datefmt=None, style='%'):
        logging.Formatter.__init__(self, fmt, datefmt, style)
        self.loggerName = loggerName

    def format(self, record):
        """Formats LogRecord into python dictionary."""
        # Standard document
        document = {
            'timestamp': dt.datetime.now(),
            'level': record.levelname,
            # 'thread': record.thread,
            # 'threadName': record.threadName,
            'message': record.getMessage(),
            'loggerName': self.loggerName,
            # 'fileName': record.pathname,
            # 'module': record.module,
            # 'method': record.funcName,
            # 'lineNumber': record.lineno
        }
        # Standard document decorated with exception info
        if record.exc_info is not None:
            document.update({
                'exception': {
                    'message': str(record.exc_info[1]),
                    'code': 0,
                    'stackTrace': self.formatException(record.exc_info)
                }
            })
        # Standard document decorated with extra contextual information
        if len(self.DEFAULT_PROPERTIES) != len(record.__dict__):
            contextual_extra = set(record.__dict__).difference(
                set(self.DEFAULT_PROPERTIES))
            if contextual_extra:
                for key in contextual_extra:
                    document[key] = record.__dict__[key]
        extra = document.pop('extra', {})
        if extra.get('provider') == 'syx-data':
            # 关键参数provider=syx-data,即认为这是一条计数的log
            return {**document, **extra}


class BufferedMongoHandler2(BufferedMongoHandler):

    def add_to_buffer(self, record):
        """Add a formatted record to buffer."""

        self.buffer_lock_acquire()

        self.last_record = record
        _ = self.format(record)
        if _:   # 这里做了一写修改，以过来在api接口访问记录中无关的log
            self.buffer.append(_)

        self.buffer_lock_release()


def getMongoLogHandler(loggerName=None, **kwargs):
    """

    :param loggerName: logger名，整个项目应该共用一个名称，
    这个很重要，为了后期按项目筛选日志
    :param kwargs: 数据库的信息
    :return:
    """
    fmt = MongoFormatter(loggerName=loggerName)

    mlh = BufferedMongoHandler(
        # host='222.178.152.79',
        # port=4316,
        # database_name='origin',
        # collection='org_logs',
        # username='rwOriginLogs',
        # password='DqLSdYKQ*849',
        # authSource='admin',
        formatter=fmt,
        # capped=True,
        buffer_size=100,  # buffer size.
        buffer_periodical_flush_timing=10.0,  # periodical flush every 10 seconds
        buffer_early_flush_level=logging.CRITICAL,   # early flush level
        **kwargs
    )

    # mlh = MongoHandler(
    #     host='222.178.152.79',
    #     port=4316,
    #     database_name='origin',
    #     collection='org_logs',
    #     username='rwOriginLogs',
    #     password='DqLSdYKQ*849',
    #     authSource='admin',
    #     formatter=fmt
    # )
    return mlh


def getMongoRecordHandler(loggerName=None, **kwargs):
    """
    logger.info('sx调用了曾用名查询接口', project='sx', provider='syx-data')  # 这条将会被记录
    logger.info('sx调用了曾用名查询接口', project='sx')  # 这条将不会被记录

    :param loggerName: logger名，整个项目应该共用一个名称，
    这个很重要，为了后期按项目筛选日志
    :param kwargs: 数据库的信息
    :return:
    """
    fmt = MongoRecorder(loggerName=loggerName)

    mlh = BufferedMongoHandler2(
        formatter=fmt,
        # capped=True,
        buffer_size=10,  # buffer size.
        buffer_periodical_flush_timing=10.0,  # periodical flush every 10 seconds
        buffer_early_flush_level=logging.CRITICAL,   # early flush level
        **kwargs
    )
    return mlh
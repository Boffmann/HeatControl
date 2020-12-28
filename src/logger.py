import logging
import logging.config
import logging.handlers
from multiprocessing import Queue, Process, Event, current_process

class __MyHandler:

    def handle(self, record):
        if record.name == "root":
            logger = logging.getLogger()
        else:
            logger = logging.getLogger(record.name)

        if logger.isEnabledFor(record.levelno):
            record.processName = '%s (for %s)' % (current_process().name, record.processName)
            logger.handle(record)

def __log_listener(queue, stop_event, config):
    logging.config.dictConfig(config)
    listener = logging.handlers.QueueListener(queue, __MyHandler())
    listener.start()
    stop_event.wait()
    listener.stop()


flask_logger_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        }
    },
    'root': {
        'handlers': ['console'],
    }
}

__config_log_listener = {
    'version': 1,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'server.log',
            'mode': 'w',
            'formatter': 'detailed'
        },
        'errors': {
            'class': 'logging.FileHandler',
            'filename': 'server-errors.log',
            'mode': 'a',
            'formatter': 'detailed',
            'level': 'ERROR'
        }
    },
    'root': {
        'handlers': ['console', 'file', 'errors'],
        'level': 'DEBUG'
    }
}

__loggingQueue = Queue()

__config_log_writer = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'queue': {
            'class': 'logging.handlers.QueueHandler',
            'queue': __loggingQueue
        }
    },
    'root': {
        'handlers': ['queue'],
        'level': 'DEBUG'
    }
}


__stop_event = Event()
__listener_process = Process(target=__log_listener, name='log_listener',
                           args=(__loggingQueue, __stop_event, __config_log_listener))
__listener_process.start()

def get_process_logger(name):
    logging.config.dictConfig(__config_log_writer)
    logger = logging.getLogger(name)
    return logger

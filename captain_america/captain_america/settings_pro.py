# -*- coding: utf-8 -*-
from settings import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hero_test',  # Or path to database file if using sqlite3.
        'USER': 'root',  # Not used with sqlite3.
        'PASSWORD': '123456',  # Not used with sqlite3.
        'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',
    }
}

LOGGING = {
    'version': 1,  # 指明dictConnfig的版本，目前就只有一个版本，哈哈
    'disable_existing_loggers': True,  # 禁用所有的已经存在的日志配置
    'formatters': {  # 格式器
        'verbose': {  # 详细
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {  # 简单
            'format': '%(levelname)s %(message)s'
        },
        'statistics': {
            'format': '%(asctime)s | %(levelname)s | %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s] - %(message)s'
        },
        'record': {
            'format': '%(message)s'
        },
    },
    'filters': {  # 过滤器
        'special': {  # 使用project.logging.SpecialFilter，别名special，可以接受其他的参数
            '()': 'project.logging.SpecialFilter',
            'foo': 'bar',  # 参数，名为foo，值为bar
        }
    },
    'handlers': {  # 处理器，在这里定义了三个处理器
        'null': {  # Null处理器，所有高于（包括）debug的消息会被传到/dev/null
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {  # 流处理器，所有的高于（包括）debug的消息会被传到stderr，使用的是simple格式器
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {  # AdminEmail处理器，所有高于（包括）而error的消息会被发送给站点管理员，使用的是special格式器
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['special']
        }
    },
    'loggers': {  # 定义了三个记录器
        'django': {  # 使用null处理器，所有高于（包括）info的消息会被发往null处理器，向父层次传递信息
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {  # 所有高于（包括）error的消息会被发往mail_admins处理器，消息不向父层次发送
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backens': {  # 所有的由请求运行的sql语句都会记录一条
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'filters': ['special']
        },
        'myproject.custom': {  # 所有高于（包括）info的消息同时会被发往console和mail_admins处理器，使用special过滤器
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'filters': ['special']
        }
    }
}


from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date  # date в этом фрагменте не используется: лишний импорт лучше удалить
from functools import wraps
from sqlalchemy import text
from sqlalchemy.orm import Session
from time import process_time
from typing import Dict, List, Tuple
from db import QRY_LAST_BALANCES, QRY_LAST_ORDERS, QRY_LAST_POSITIONS, QRY_CLTS_LIST

ACC_FILTER = {'acc_filter': 'where client_id in :ids'}

"""
Здесь структура данных немного тяжеловесная
Для читаемости удобнее хранить так: _DB_BINDS = ("csdb1", "csdb2")
"""
_DB = ({'bind': 'csdb1'}, {'bind': 'csdb2'})

""" 
_LOGSDB не используется
"""
_LOGSDB = ({'bind': 'qlogsdb1'}, {'bind': 'qlogsdb2'})

"""
ThreadPoolExecutor — спорное решение
неочевидный жизненный цикл, неудобнее контролировать ресурсы
лучше создавать _executor через context manager
"""
_executor = ThreadPoolExecutor(4)


def multidb(binds: Tuple, is_scalar: bool):
    def _completed(fn):
        @wraps(fn)
        def _gather(*args):
            """print для технических сообщений лучше заменить на logging"""
            print(process_time(), 'gather', fn.__name__, binds)

            """Session обычно потоконебезопасен"""
            _futures = {_executor.submit(fn, *args, bind=db): db['bind'] for db in binds}

            return [
                _f.result().all() if not is_scalar else _f.result().scalar()
                for _f in as_completed(_futures)
            ]
        return _gather

    return _completed


class _static(type):
    def __new__(mcs, *args, **kwargs):
        raise TypeError(f'You shouldn\'t instantiate the {mcs.__name__} class')


class ORMMonitoring(_static):
    @staticmethod
    @multidb(_DB, False) #Нет именнованой передачи
    def get_balances(db: Session, clt_ids: List[int], bind: Dict):

        """Дублирование логики, очень похожий код ниже в get_positions"""
        return db.execute(text(QRY_LAST_BALANCES % ACC_FILTER), {'ids': tuple(clt_ids)}, bind_arguments=bind) \
            if len(clt_ids) > 0 else \
            db.execute(text(QRY_LAST_BALANCES % {'acc_filter': ''}), bind_arguments=bind)

    @staticmethod
    @multidb(_DB, False) #Нет именнованой передачи
    def get_positions(db: Session, clt_ids: List[int], bind: Dict):
        """Копия get_balances"""
        return db.execute(text(QRY_LAST_POSITIONS % ACC_FILTER), {'ids': tuple(clt_ids)}, bind_arguments=bind) \
            if len(clt_ids) > 0 else \
            db.execute(text(QRY_LAST_POSITIONS % {'acc_filter': ''}), bind_arguments=bind)

    @staticmethod
    @multidb(_DB, False) #Нет именнованой передачи
    def get_clients(db: Session, bind: Dict):
        return db.execute(text(QRY_CLTS_LIST), bind_arguments=bind)

    @staticmethod
    @multidb(_DB, False)
    def get_last_orders(db: Session, clt_id: int, bind: Dict):
        return db.execute(text(QRY_LAST_ORDERS), {'clt_id': clt_id}, bind_arguments=bind)

from loguru import logger
from datetime import datetime

from generalize import generalize_web_app, generalize_wordpress

logger.add('./generalize_time.log')
start_time = datetime.now()

# 0-time_blind， 1-bool_blind， 2-illegal，3-tautology，4-union, 5-normal
for i in range(0,6):
    generalize_web_app(i, './output/web_app/')
for i in range(0,6):
    generalize_wordpress(i, './output/wordpress/')

end_time = datetime.now()
time_diff = end_time - start_time                                           # 时间差
milliseconds = time_diff.seconds * 1000 + time_diff.microseconds / 1000     # 毫秒级时间差
logger.info("Generalization time: {} ms, {} s, {} min", milliseconds, time_diff.seconds, time_diff.seconds / 60)


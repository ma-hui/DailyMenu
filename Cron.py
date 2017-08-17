from apscheduler.schedulers.blocking import  BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import  ThreadPoolExecutor, ProcessPoolExecutor
import AanlyseMenu

# executors = {
#     'default':ThreadPoolExecutor(10),
#     'processpool': ProcessPoolExecutor(3),
# }
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 3
# }
# scheduler = BackgroundScheduler(executors=executors,job_defaults=job_defaults)

scheduler = BlockingScheduler()
scheduler.add_job(AanlyseMenu.daily_cron, 'cron', day_of_week='1-5', hour=11, minute=25)
scheduler.add_job(AanlyseMenu.daily_cron, 'cron', day_of_week='1-5', hour=17, minute=25)
scheduler.start()

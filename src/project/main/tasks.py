from time import sleep
from celery import shared_task, current_task, states


@shared_task
def func1(arg):

    print(f'celery received {arg}')
    meta = {
        'status': '..working..',
        'step': 0,
    }

    for i in range(20):
        meta['step'] = i
        current_task.update_state(
            state=states.PENDING,
            meta=meta
        )
        sleep(1)
        print(i)
    return True

from time import sleep

from django.core.cache import cache


def lock(k):
    key = k
    for i in range(7):  # retry
        lock = cache.get(key)

        if not lock:
            break

        # lock 있을 때 wait
        print('wait!!')
        sleep(1)

    else:
        # for 문이 종료될때까지 락 존재 -> 비정상
        return False

    # cache set
    cache.set(key, True, 30)

    # 비즈니스 로직
    print('hi!')
    sleep(7)
    print('end')

    # release lock
    cache.delete(k)
    print('delete')

def lock_get(name):
    from redis import Redis
    conn = Redis(host='redis', db=1)
    import redis_lock

    return redis_lock.Lock(conn, name)

class Cache:
    def __init__(self):
        self.cache = {}

    def get(self, key, default=None):
        if key in self.cache:
            return self.cache[key]
        else:
            return default

    def set(self, key, value):
        self.cache[key] = value

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache.clear()


if __name__ == '__main__':
    cache = Cache()
    # cache.set("tset2",True)
    # print(cache.get("tset1"),type(cache.get("tset1")))
    cache.clear()
    print(cache.get("tset2", 123213), type(cache.get("tset2")))

    print(cache.cache_file)

"""
A simple native Python3 disk cache
"""

import time
import pickle
import os
from traceback import format_exc

# import static logger and create shortcut function
from logger import Logger

log = Logger.log


def _get_dir():
    DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep

    try:
        testfilename = DIR + "test_write.try_to_write"
        open(testfilename, "w").close()
        os.remove(testfilename)
    except IOError:
        return "/tmp/"

    return DIR


class SimpleCache:
    CACHE_FILE = "simple_cache.pickle"
    PATH = _get_dir() + CACHE_FILE

    log("Using PATH: {}".format(PATH), title="SimpleCache")

    # Looks like: {"cache_id01": {"saved_at": '#date#', "lifetime": 60 * 60 * 1000, "content": []}}
    cache_store = {}

    @staticmethod
    def init():
        try:
            # if cache file not modified in 48 hours or empty, don't load it
            if not os.path.isfile(SimpleCache.PATH):
                open(SimpleCache.PATH, "w+").close()

            if (
                time.time() - os.path.getmtime(SimpleCache.PATH) < 48 * 60 * 60
                and os.path.getsize(SimpleCache.PATH) > 0
            ):
                with open(SimpleCache.PATH, "rb") as handle:
                    SimpleCache.cache_store = pickle.load(handle)
                    log(
                        "Loaded {} cached items from disk".format(
                            len(SimpleCache.cache_store)
                        ),
                        title="SimpleCache",
                    )
                SimpleCache._garbage_collect()
            else:
                log("Nothing to load from disk", title="SimpleCache")
        except Exception as e:
            log(
                "Exception thrown: {}, traceback: {}".format(e, format_exc()),
                message_type="error",
                title="main",
            )
            # raise Exception(e)

    @staticmethod
    def save(cache_id, content, lifetime_s=24 * 60 * 60):
        cache_id = SimpleCache._chk_id(cache_id)
        if None not in [cache_id, content, lifetime_s]:
            # update cache_store
            SimpleCache.cache_store[cache_id] = {}
            SimpleCache.cache_store[cache_id]["content"] = content
            SimpleCache.cache_store[cache_id]["lifetime"] = lifetime_s
            SimpleCache.cache_store[cache_id]["saved_at"] = time.time()

            SimpleCache._sync()

    @staticmethod
    def get(cache_id):
        cache_id = SimpleCache._chk_id(cache_id)
        return (
            SimpleCache.cache_store[cache_id]["content"]
            if SimpleCache.is_cached(cache_id)
            else None
        )

    @staticmethod
    def is_cached(cache_id):
        cache_id = SimpleCache._chk_id(cache_id)
        for c_id, c_val in SimpleCache.cache_store.items():
            if (c_id == cache_id) and (time.time() - c_val["saved_at"]) < c_val[
                "lifetime"
            ]:
                return True

        # if we reach here, no match, return False
        return False

    @staticmethod
    def _chk_id(cache_id):
        return str(cache_id)

    @staticmethod
    def _del_from_dict_list(source_list, dict_id):
        """ Delete dict with 'id' = dict_id from source_list
        See https://stackoverflow.com/a/31068594

        Arguments:
            source_list {list of dicts} -- with 'id' value set
            dict_id {int} -- Used to match dict to delete with 'id' = dict_id
        """
        return [d for d in source_list if d["id"] != dict_id]

    @staticmethod
    def _sync():
        """ Save SimpleCache.cache_store to disk """
        with open(SimpleCache.PATH, "wb") as handle:
            pickle.dump(
                SimpleCache.cache_store, handle, protocol=pickle.HIGHEST_PROTOCOL
            )
            log(
                "Saved cache to disk, len {}".format(len(SimpleCache.cache_store)),
                title="SimpleCache",
            )

    @staticmethod
    def _garbage_collect():
        is_changed = False
        cache_store_out = SimpleCache.cache_store.copy()

        for c_id, c_val in SimpleCache.cache_store.items():
            # if expired, purge from cache
            if c_val["saved_at"] + c_val["lifetime"] < time.time():
                del cache_store_out[c_id]

        if is_changed is True:
            SimpleCache._sync()
            log(
                "Garbage collection: {} items removed".format(
                    len(SimpleCache.cache_store) - len(cache_store_out)
                ),
                title="SimpleCache",
            )


# run init()
SimpleCache.init()

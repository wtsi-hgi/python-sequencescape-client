from sequencescape._models import Well
from sequencescape._query import *


@wrappers.check_args_not_none
def query_all_wells_as_batch(ids, id_type):
    return query_all_as_batch(Well, ids, id_type)
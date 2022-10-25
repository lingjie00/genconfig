import logging
from typing import Any, Dict, Optional, List

logger = logging.getLogger(__name__)


def merge(
        a: Dict[Any, Any], b: Dict[Any, Any],
        path: Optional[List[str]] = None,
        a_parent: Optional[Dict[str, str]] = None,
        b_parent: Optional[Dict[str, str]] = None,
        merge_conflict: bool = True,
        raise_conflict: bool = True):
    """Merges dictionary b into dictionary a.

    Handles duplicate leaf vale

    shamelessly modified from
    https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries

    Params:
        a: master dictionary
        b: dictionary to be join with a
        path: keeping track of the current path transverse
        a_parent: keeping track of a's current parent
        b_parent: keeping track of b's current parent
        merge_conflict: when facing conflict, do we merge them using list
            structure, if set as False then we will override
        raise_conflict: if to raise issue when facing with conflict
    """
    # path tracks the current layer in dictionary
    if path is None:
        path = []
    for key in b:
        # if key exist in a
        if key in a:
            current_path = ".".join(path + [str(key)])
            # recursive merge the sub-dictionary
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)], a, b,
                      merge_conflict=merge_conflict, raise_conflict=raise_conflict)
            # do nothing if the leaf value of a, b are the same
            elif a[key] == b[key]:
                logger.debug(f"Same value at {current_path}")
                pass  # same leaf value
            # if both children are list, append them
            elif isinstance(a[key], list) and isinstance(b[key], list) and merge_conflict:
                logger.warning(f"Merger at {current_path}")
                a[key] += b[key]
            # conflict arise when the value of a and b are different
            # and they are not both sub-dictionary wich we can combine again
            # resolve by appending them to a list
            elif merge_conflict:
                logger.warning(f"Conflict at {current_path}")
                if a_parent is not None and b_parent is not None:
                    parent_key = path[-1]
                    if not isinstance(a_parent[parent_key], list):
                        a_parent[parent_key] = [a, ]
                    a_parent[parent_key].append(b)
                    logger.warning(f"Added child to parent at {current_path}")
            elif not raise_conflict:
                # if don't merge and dont raise error, then override
                logger.warning(f"Conflict at {current_path}, override the values")
                a[key] = b[key]
            else:
                # raise ValueError if do not want to merge
                raise ValueError(f"Conflict at {current_path}")
        # copy value from b if key not present in a
        else:
            a[key] = b[key]
    return a

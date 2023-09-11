
from typing import List, Tuple


def restaurantFinder(s: int, revs: List[int]) -> Tuple[ int, List[int]]:
    size = len(revs)

    # Base case if no list of revenues is provided
    if size == 0:
        return 0, []

    # Memoization
    max_rev = [0] * size
    tracking = [None] * size
    
    d = s + 1
    
    max_rev[0] = revs[0]
    tracking[0] = None

    for i in range(1, size):
        last_best_rev_i = i - d
        prev_i = i - 1
        
        if last_best_rev_i < 0:
            carry_forward = max_rev[prev_i] >= revs[i]
            max_value = max_rev[prev_i] if carry_forward else revs[i]
            pos = ((tracking[prev_i] if tracking[prev_i] is not None else prev_i) if carry_forward else None)
            
            max_rev[i] = max_value
            tracking[i] = pos
            continue
        
        by_policy_value = revs[i] + max_rev[last_best_rev_i]
        prev_value = max_rev[prev_i]
        carry_forward = by_policy_value >= prev_value
        
        max_rev[i] = by_policy_value if carry_forward else prev_value
        tracking[i] = (tracking[last_best_rev_i] if last_best_rev_i < d and tracking[last_best_rev_i] is not None else last_best_rev_i) if carry_forward else prev_i
        
    max_value, pos = find_max(max_rev)
    
    track = []
    __back_track(tracking, pos, track)
    
    return max_value, [i + 1 for i in track]


def find_max(arr: List[int]):
    max_value_i = 0
    max_value = arr[max_value_i]

    for i in range(len(arr)):
        curr_val = arr[i]
        if curr_val > max_value:
            max_value = curr_val
            max_value_i = i
    return max_value, max_value_i


def __back_track(arr: List[int], i: int, result: List[int]):
    if arr[i] is None:
        result.append(i)
        return i
    __back_track(arr, arr[i], result)
    if arr[i] != i:
        result.append(i)

    return i


if __name__ == '__main__':
    rev = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]

    d = 1
    print(d, restaurantFinder(d, rev))

        
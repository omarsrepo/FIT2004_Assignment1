from typing import List, Tuple


def restaurantFinder(d: int, revenues: List[int]) -> Tuple[int, List[int]]:
    """
    This function takes as input a list of site revenues and a distance parameter and uses dynamic programming
    to compute the most optimal set of sites to build to maximise revenue.

    Approach description:
    The approach is simple. For the first d+1 elements (where d is the distance constraint), the maximum revenue will
    be the i(th) index itself.

    :Input:
    d: the distance constraint
    revenues: list of revenues of each site

    :Output,return or post condition:
    Tuple (maximum revenue, list of site indexes in order)

    :Time complexity:
    ----------------------
    The dominant factor is the for loop which runs from 1 to len(revenues) which means it is at worst O(N) since the
    for loop scales linearly with the size of the revenues list.

    Best case = Worst case = O(N)

    :Aux space complexity:
    ----------------------
    The only auxiliary space being taken up is by the max_rev list and the tracking list which is always initiated to
    the size of the input revenues list and so it will scale linearly with the input.

    Best case = Worst case = O(N)
    """

    # Base case if no list of revenues is provided or if only one site is available
    if len(revenues) == 0 or sum(revenues) == 0:
        return 0, []
    elif len(revenues) == 1:
        return revenues[0], [len(revenues)]

    # Memoization
    max_rev = [0] * len(revenues)
    tracking = [None] * len(revenues)

    two = d + 1  # Rename this back to s later

    max_rev[0] = revenues[0]
    tracking[0] = None

    print(revenues)
    print(max_rev)
    print(tracking)
    print()

    for i in range(1, len(revenues)):
        last_best_rev_i = i - two
        prev_site_index = i - 1

        if last_best_rev_i < 0:
            if max_rev[prev_site_index] >= revenues[i]:
                max_value = max_rev[prev_site_index]
                if tracking[prev_site_index] is not None:
                    pos = tracking[prev_site_index]
                else:
                    pos = prev_site_index
            else:
                max_value = revenues[i]
                pos = None

            max_rev[i] = max_value
            tracking[i] = pos

            print(revenues)
            print(max_rev)
            print(tracking)
            print()
            continue

        by_policy_value = revenues[i] + max_rev[last_best_rev_i]
        prev_value = max_rev[prev_site_index]

        if by_policy_value >= prev_value:
            max_rev[i] = by_policy_value
            if last_best_rev_i < two and tracking[last_best_rev_i] is not None:
                tracking[i] = tracking[last_best_rev_i]
            else:
                tracking[i] = last_best_rev_i
        else:
            # We found a new max revenue, and we will add to tracking the site that lead to this new max
            max_rev[i] = prev_value
            tracking[i] = prev_site_index

        print(revenues)
        print(max_rev)
        print(tracking)
        print()

    max_value, pos = find_max(max_rev)

    track = []
    backtrack(tracking, pos, track)

    return max_value, [i + 1 for i in track]


def find_max(arr: List[int]):
    """

    :Input:

    :Output,return or post condition:


    :Time complexity:
    ----------------------

    :Aux space complexity:
    ----------------------
    """
    max_value_i = 0
    max_value = arr[max_value_i]

    for i in range(len(arr)):
        curr_val = arr[i]
        if curr_val > max_value:
            max_value = curr_val
            max_value_i = i
    return max_value, max_value_i


def backtrack(tracking: List[int], i: int, result: List[int]):
    """

    :Input:

    :Output,return or post condition:

    :Time complexity:
    ----------------------

    :Aux space complexity:
    ----------------------
    """
    if tracking[i] is None:
        result.append(i)
        return i
    backtrack(tracking, tracking[i], result)
    if tracking[i] != i:
        result.append(i)

    return i


if __name__ == '__main__':
    rev = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]
    d = 1
    print(restaurantFinder(d, rev))



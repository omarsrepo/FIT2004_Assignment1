"""
Name: Mohamed Omar Mohamed Muhseen
Student_ID: 28951743

Question1:Fast Food Chain
"""


def restaurantFinder(d: int, site_list: list[int]) -> tuple:
    """
    Function description: This function will take in a list of size N containing the annual revenue of sites
    and will use the distance parameter to return a list of which sites from the site list would be best to
    maximize the revenue as well as the predicted total revenue for the output list.

    :Input:
        :param d: distance parameter
        :param site_list: list of size N containing annual revenue
    :Output, return tuple (total_revenue,selected_sites):
    :Time-complexity:
    :Aux space-complexity:
    """
    n = len(site_list)
    selected_sites = []
    total_revenue = 0

    start = 0
    while start < n:
        max_revenue = -1
        selected_site = -1
        for i in range(start, min(start + d + 1, n)):
            if site_list[i] > max_revenue:
                max_revenue = site_list[i]
                selected_site = i
        if selected_site == -1:
            break
        selected_sites.append(selected_site + 1)  # Site numbers are 1-based
        total_revenue += max_revenue
        start = selected_site + d + 1

    return total_revenue, selected_sites


def restaurantFinder2(d, site_list):
    N = len(site_list)
    max_revenue = [0] * (N + 1)
    prev_site = [-1] * (N + 1)

    for i in range(1, N + 1):
        max_revenue[i] = site_list[i - 1]
        prev_site[i] = -1

        for j in range(1, i):
            if i - j > d:
                if max_revenue[i] < max_revenue[j] + site_list[i - 1]:
                    max_revenue[i] = max_revenue[j] + site_list[i - 1]
                    prev_site[i] = j
            else:
                break

    max_total_revenue = max(max_revenue)
    selected_sites = []
    idx = max_revenue.index(max_total_revenue)

    while idx != -1:
        selected_sites.append(idx)
        idx = prev_site[idx]

    selected_sites.reverse()
    return max_total_revenue, selected_sites


print(restaurantFinder2(1,[50, 10, 12, 65, 40, 95, 100, 12, 20, 30]))



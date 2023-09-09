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


sites = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]

x = [50]


# What is going on here:
# site_revenues    Max revenue
#     50	             50	            null
#     10	             50	            max(50, 10) ~ 1
#     12	             62	            max(12+50, 50) ~ 1
#     65	             115	        max(65+50, 62) ~ 1
#     40	             115	        max(40+62, 115) ~ 4
#     95	             210	        max(95+115, 115) ~ 4
#     100	             215	        max(100+115, 210) ~ 5
#     12	             222	        max(12+210, 215) ~ 6
#     20	             235	        max(20+215, 222) ~ 7
#     30	             252	        max(30+222, 235) ~ 8
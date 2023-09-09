"""
Question2 : Climb King
"""

"""
# 
"""


def restaurantFinder(c):
    n = len(c)
    max_revenue = [0] * (n + 1)  # Initialize max_revenue array with zeros
    max_revenue[1] = c[0]  # Set the base case for max_revenue[1]

    for i in range(2, n + 1):
        max_revenue[i] = max(max_revenue[i - 1], max_revenue[i - 2] + c[i - 1])

    return max_revenue[n], max_revenue  # Return the maximum profit for n houses


sites = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]
print(restaurantFinder(sites))

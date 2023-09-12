"""
    Assignment 1 - Testing
    FIT2004: Algorithms and Data Structures
    Ahmad Abu-Shaqra
    15/09/2023

"""

import unittest
from Question1 import restaurantFinder
from FloorGraph import FloorGraph

# Question 1: Fast Food Chain


class TestingQ1(unittest.TestCase):

    def test_01(self):

        # initialising test
        d = 0
        site_list = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 434)
        self.assertEqual(selected_sites, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    def test_02(self):

        # initialising test
        d = 1
        site_list = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 252)
        self.assertEqual(selected_sites, [1, 4, 6, 8, 10])

    def test_03(self):

        # initialising test
        d = 2
        site_list = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 245)
        self.assertEqual(selected_sites, [1, 4, 7, 10])

    def test_04(self):

        # initialising test
        d = 3
        site_list = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 175)
        self.assertEqual(selected_sites, [1, 6, 10])

    def test_05(self):

        # initialising test
        d = 7
        site_list = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 100)
        self.assertEqual(selected_sites, [7])
    
    def test_06(self):
        
        # initialising test
        d = 100
        site_list = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 100)
        self.assertEqual(selected_sites, [7])

    def test_07(self):
        
        # initialising test
        d = 1
        site_list = [1000, 900, 1000, 2000]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 3000)
        self.assertEqual(selected_sites, [1, 4])

    def test_08(self):
        
        # initialising test
        d = 10
        site_list = [100, 1, 1000]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 1000)
        self.assertEqual(selected_sites, [3])
    
    def test_09(self):
        
        # initialising test
        d = 1
        site_list = [100, 1, 100, 100, 100]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 300)
        self.assertEqual(selected_sites, [1, 3, 5])

    def test_10(self):
        
        # initialising test
        d = 10
        site_list = [100, 1, 1000, 100]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 1000)
        self.assertEqual(selected_sites, [3])
    
    def test_11(self):
        
        # initialising test
        d = 1
        site_list = [1, 1000, 1]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 1000)
        self.assertEqual(selected_sites, [2])

    def test_12(self):
        
        # initialising test
        d = 1
        site_list = [1, 4, 3, 4, 3]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 8)
        self.assertEqual(selected_sites, [2, 4])
    
    def test_13(self):
        
        # initialising test
        d = 10
        site_list = [100, 0, 2, 3, 0, 200, 0, 0, 3, 4, 2, 4, 50]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 200)
        self.assertEqual(selected_sites, [6])

    def test_14(self):
        
        # initialising test
        d = 10
        site_list = [30]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 30)
        self.assertEqual(selected_sites, [1])
    
    def test_15(self):
        
        # initialising test
        d = 2
        site_list = [50, 100, 50, 100, 50, 100]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 200)
        self.assertEqual(selected_sites, [2, 6])

    def test_16(self):
        
        # initialising test
        d = 0
        site_list = [0, 0, 0]
        total_revenue, selected_sites = restaurantFinder(d, site_list)

        # testing
        self.assertEqual(total_revenue, 0)
        self.assertIn(selected_sites, [[1, 2, 3], []])


# Question 2: Climb King

class TestingQ2(unittest.TestCase):

    def test_01(self):

        # initialising test
        paths = [(0, 1, 4), (0, 3, 2), (0, 2, 3), (2, 3, 2), (3, 0, 3)]
        keys = [(0, 5), (3, 2), (1, 3)]
        graph = FloorGraph(paths, keys)
        start = 0
        exits = [1, 2]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 7)
        self.assertEqual(route, [0, 1])

    def test_02(self):

        # initialising test
        paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2), (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2), (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
        keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
        graph = FloorGraph(paths, keys)
        start = 1
        exits = [7, 2, 4]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 9)
        self.assertEqual(route, [1, 7])

    def test_03(self):

        # initialising test
        paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2), (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2), (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
        keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
        graph = FloorGraph(paths, keys)
        start = 7
        exits = [8]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 6)
        self.assertEqual(route, [7, 8])

    def test_04(self):

        # initialising test
        paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2), (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2), (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
        keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
        graph = FloorGraph(paths, keys)
        start = 1
        exits = [3, 4]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 10)
        self.assertEqual(route, [1, 5, 6, 3])

    def test_05(self):

        # initialising test
        paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2), (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2), (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
        keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
        graph = FloorGraph(paths, keys)
        start = 1
        exits = [0, 4]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 11)
        self.assertEqual(route, [1, 5, 6, 4])

    def test_06(self):

        # initialising test
        paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2), (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2), (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
        keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
        graph = FloorGraph(paths, keys)
        start = 3
        exits = [4]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 20)
        self.assertEqual(route, [3, 4, 8, 7, 3, 4])
    
    def test_07(self):

        # initialising test
        paths = [(0, 1, 4), (0, 3, 2), (0, 2, 3), (2, 3, 2), (3, 0, 3)]
        keys = [(0, 5), (3, 2), (1, 3)]
        graph = FloorGraph(paths, keys)
        start = 1
        exits = [2]
        outcome = graph.climb(start, exits)

        # testing
        self.assertEqual(outcome, None)

    def test_08(self):

        # initialising test
        paths = [(0, 1, 4), (0, 2, 3), (1, 0, 2), (1, 3, 3), (3, 2, 3)]
        keys = [(1, 10)]
        graph = FloorGraph(paths, keys)
        start = 0
        exits = [2]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 19)
        self.assertEqual(route, [0, 1, 0, 2])
    
    def test_09(self):

        # initialising test
        paths = [(0, 1, 5)]
        keys = [(0, 5)]
        graph = FloorGraph(paths, keys)
        start = 0
        exits = [1]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 10)
        self.assertEqual(route, [0, 1])

    def test_10(self):

        # initialising test
        paths = [(0, 1, 5)]
        keys = [(0, 5)]
        graph = FloorGraph(paths, keys)
        start = 1
        exits = [0, 1]
        outcome = graph.climb(start, exits)

        # testing
        self.assertEqual(outcome, None)

    def test_11(self):

        # initialising test
        paths = [(0, 1, 3), (0, 3, 10), (0, 4, 5), (1, 2, 2), (2, 3, 4), (3, 0, 10), (3, 4, 1), (4, 0, 3)]
        keys = [(0, 10), (3, 1)]
        graph = FloorGraph(paths, keys)
        start = 0
        exits = [3]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 10)
        self.assertEqual(route, [0, 1, 2, 3])

    def test_12(self):

        # initialising test
        paths = [(0, 1, 3), (0, 3, 10), (0, 4, 5), (1, 2, 2), (2, 3, 4), (3, 0, 10), (3, 4, 1), (4, 0, 3)]
        keys = [(0, 10), (3, 1)]
        graph = FloorGraph(paths, keys)
        start = 4
        exits = [4]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 14)
        self.assertEqual(route, [4, 0, 1, 2, 3, 4])

    def test_13(self):

        # initialising test
        paths = [(0, 1, 3), (0, 3, 10), (0, 4, 5), (1, 2, 2), (2, 3, 4), (3, 0, 10), (3, 4, 1), (4, 0, 3)]
        keys = [(0, 10), (3, 1)]
        graph = FloorGraph(paths, keys)
        start = 3
        exits = [0]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 5)
        self.assertEqual(route, [3, 4, 0])

    def test_14(self):

        # initialising test
        paths = [(0, 1, 3), (0, 3, 10), (0, 4, 5), (1, 2, 2), (2, 3, 4), (3, 0, 10), (3, 4, 1), (4, 0, 3)]
        keys = [(0, 10), (3, 1)]
        graph = FloorGraph(paths, keys)
        start = 4
        exits = [1, 3]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 13)
        self.assertEqual(route, [4, 0, 1, 2, 3])

    def test_15(self):

        # initialising test
        paths = [(0, 1, 3), (0, 3, 10), (0, 4, 5), (1, 2, 2), (2, 3, 4), (3, 0, 10), (3, 4, 1), (4, 0, 3)]
        keys = [(0, 10), (3, 1)]
        graph = FloorGraph(paths, keys)
        start = 1
        exits = [0, 4]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 8)
        self.assertEqual(route, [1, 2, 3, 4])

    def test_16(self):

        # initialising test
        paths = [(0, 1, 3), (0, 3, 10), (0, 4, 5), (1, 2, 2), (2, 3, 4), (3, 0, 10), (3, 4, 1), (4, 0, 3)]
        keys = [(0, 10), (3, 1)]
        graph = FloorGraph(paths, keys)
        start = 0
        exits = [0, 1, 2, 3, 4]
        total_time, route = graph.climb(start, exits)

        # testing
        self.assertEqual(total_time, 10)
        self.assertIn(route, [[0], [0, 1, 2, 3]])

# Run Tests

if __name__ == '__main__':
    unittest.main()

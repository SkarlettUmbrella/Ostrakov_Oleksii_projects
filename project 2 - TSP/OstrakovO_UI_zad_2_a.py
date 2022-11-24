# Ostrakov Oleksii, UI zad2_c_1
import math
import random
import sys
import timeit


# class that represents city, has x coordinate, y coordinate, name
class City:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name


# generate random city, isn't used
def random_city_creator():
    city = City(random.randrange(1, 200), random.randrange(1, 200), "")
    return city


# generate random city list, isn't used
def random_city_list(size):
    city_list = []
    for i in range(size):
        city = random_city_creator()
        for j in city_list:
            if city == j:
                city.x = 0
                city.y = 0
                break
        if city.x == 0 & city.y == 0:
            i -= 1
        else:
            city_list.append(city)
    return city_list


# counts distance between cities
def distance(city_a, city_b):
    return math.sqrt(math.pow(city_a.x - city_b.x, 2) + math.pow(city_a.y - city_b.y, 2))


class Route:

    # class represent full route for algo, has order of cities and length or route
    def __init__(self):
        self.order = []
        self.length = 0

    # function to fill route from city list
    def fill_route(self, city_list):
        for i in city_list:
            if not self.order:
                self.order.append(i)
            else:
                self.length += distance(i, self.order[-1])
                self.order.append(i)
        self.length += distance(self.order[0], self.order[len(self.order) - 1])

    # function to recalculate length of route
    def recalculate_distance(self):
        self.length = 0
        for i in range(len(self.order)):
            self.length += distance(self.order[i], self.order[i - 1])

    # function to select which way of mutation to use
    def select_mutation(self, mutation):
        if mutation == 1:
            self.mutate_1()
        else:
            self.mutate_2()

    # 1st way of mutation: replace 10% of route with a random cities
    def mutate_1(self):
        rand_a = random.randrange(0, len(self.order))
        rand_b = rand_a
        while rand_b == rand_a:
            rand_b = random.randrange(0, len(self.order))
        self.order[rand_a], self.order[rand_b] = self.order[rand_b], self.order[rand_a]

    # 2nd way of mutation: replace 10% of route with next cities
    def mutate_2(self):
        rand_a = random.randrange(0, len(self.order))
        rand_b = rand_a + 1
        if rand_b == len(self.order):
            rand_b = 0
        self.order[rand_a], self.order[rand_b] = self.order[rand_b], self.order[rand_a]


class Generation:
    allRoutes = []

    # class represent main algo, has a limit for finding, generated examples, lvl of generation,
    # level of mutation when best route was found, length of best route, best route,
    # number of example that became best, way of mutation and amount of cities to swap for 10%
    def __init__(self, limit, gen_examples, algo):
        self.best_find_limit = limit
        self.generation_examples = gen_examples
        self.genLvl = 0
        self.bestMutateLvl = 0
        self.bestLength = -1
        self.bestRoute = 0
        self.bestRouteNum = 0
        self.mutation = algo
        self.maxSwap = 0

    # function to create examples for algo
    def create_gen(self, city_list):
        self.maxSwap = len(city_list) // 20

        for i in range(self.generation_examples):
            random.shuffle(city_list)
            new_route = Route()
            new_route.fill_route(city_list)
            self.allRoutes.append(new_route)

        for i in self.allRoutes:
            if i.length < self.bestLength or self.bestLength == -1:
                self.bestLength = i.length
                self.bestRoute = i
                self.bestRouteNum = self.allRoutes.index(i)
                self.bestMutateLvl = -1

    # reusable function to create a new generation and check for a new best route
    def new_gen(self):
        self.genLvl += 1
        for i in self.allRoutes:
            for j in range(self.maxSwap):
                i.select_mutation(self.mutation)
            i.recalculate_distance()
            if i.length < self.bestLength:
                self.bestLength = i.length
                self.bestRoute = i
                self.bestRouteNum = self.allRoutes.index(i)
                self.bestMutateLvl = self.genLvl

    # main function of algo, starts search for best route
    def find_best_way(self):
        best_counter = self.bestLength
        i = 0
        while i < self.best_find_limit:
            self.new_gen()
            if self.bestLength < best_counter:
                i = 0
                best_counter = self.bestLength
            else:
                i += 1


if __name__ == '__main__':

    start_city_amount = input("define amount of cities (from 20 to 40):")
    if int(start_city_amount) > 40 or int(start_city_amount) < 20:
        sys.exit("wrong amount of cities.")

    start_city_list = []
    print("write down cities x, y, and name:")
    for i in range(int(start_city_amount)):
        input_city = input().split()
        if len(input_city) != 3:
            sys.exit("wrong amount of inputs.")
        start_city = City(int(input_city[0]), int(input_city[1]), input_city[2])
        start_city_list.append(start_city)

    start_gen = input("select generation limit: ")
    start_examples = input("select amount of generation examples: ")
    start_algo = input("select mutation way: ")
    start_generation = Generation(int(start_gen), int(start_examples), int(start_algo))
    start_generation.create_gen(start_city_list)

    start = timeit.default_timer()
    start_generation.find_best_way()
    stop = timeit.default_timer()

    print("result: ")
    print("best length: ", start_generation.bestLength)
    print("the process was done in ", stop - start, " seconds.")
    print("was achieved by mutator number ", start_generation.bestRouteNum, " on mutation level ",
          start_generation.bestMutateLvl)
    print("city order by name: ")
    for i in range(int(start_city_amount)):
        print(start_generation.bestRoute.order[i].name, " (", start_generation.bestRoute.order[i].x,
              ", ", start_generation.bestRoute.order[i].y, ")")

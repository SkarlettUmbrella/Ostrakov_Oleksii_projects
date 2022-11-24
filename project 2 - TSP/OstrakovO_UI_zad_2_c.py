# Ostrakov Oleksii UI zad2_c_3
import copy
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
            self.length += distance(self.order[i], self.order[i-1])

    # mutation: replace 10% of route with a random cities
    def mutate(self):
        rand_a = random.randrange(0, len(self.order))
        rand_b = rand_a
        while rand_b == rand_a:
            rand_b = random.randrange(0, len(self.order))
        self.order[rand_a], self.order[rand_b] = self.order[rand_b], self.order[rand_a]
        self.recalculate_distance()


class Annealing:
    temperature = 30
    annealing_length = 10000
    cooling = 3

    # main class that represents algo, has several important attributes:
    # main candidate as route to work with, temperature in percentage of approving longer routes,
    # length of annealing process per temperature, cool off is decrease in temperature per cycle,
    # candidates as possible variants of route, best route, best route length,
    # number of cycle that best length was achieved in, temperature on what best route was achieved
    def __init__(self, candidate, temp, length, cool, candidates):
        self.main_candidate = candidate
        self.temperature = temp
        self.annealing_length = length
        self.cooling = cool
        self.created_candidates = candidates
        self.best_candidate = 0
        self.best_length = -1
        self.length_num = 0
        self.temp_num = 0

    # function creates candidates that are same as main route
    def create_candidates(self, start_candidate, amount):
        candidates = []
        for i in range(amount):
            new_candidate = copy.deepcopy(start_candidate)
            new_candidate.mutate()
            candidates.append(new_candidate)
        return candidates

    # forge is main function for algo, there is several cycles for temperature, length and all candidates
    # every candidate is compared to main
    # if candidate is better = it's new main
    # if not - there is a chance based on temperature that candidate will become main
    def forge(self):
        i = self.temperature
        while i >= 0:
            for j in range(self.annealing_length):
                possible_candidates = self.create_candidates(self.main_candidate, self.created_candidates)
                upgraded = 0
                for k in possible_candidates:
                    if k.length < self.main_candidate.length:
                        self.best_length = k.length
                        self.length_num = j
                        self.temp_num = i
                        self.main_candidate = k
                        upgraded = 1

                    elif random.randrange(1, 100) < i:
                        self.best_length = k.length
                        self.length_num = j
                        self.temp_num = i
                        self.main_candidate = k
                        upgraded = 1
                if upgraded == 0:
                    return

            i -= self.cooling


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

    start_route = Route()
    start_route.fill_route(start_city_list)
    random.shuffle(start_route.order)
    start_route.recalculate_distance()

    start_temp = input("select starting temperature: ")
    start_length = input("select starting length of annealing: ")
    start_cool = input("select starting temperature falloff: ")
    start_candidates = input("select amount of possible candidates to anneal: ")
    start_annealing = Annealing(start_route, int(start_temp), int(start_length), int(start_cool), int(start_candidates))

    start = timeit.default_timer()
    start_annealing.forge()
    stop = timeit.default_timer()

    print("result: ")
    print("best length: ", start_annealing.best_length)
    print("the process was done in ", stop - start, " seconds.")
    print("was achieved on temperature ", start_annealing.temp_num,
          " at process number ", start_annealing.length_num)
    print("city order by name: ")
    for i in range(int(start_city_amount)):
        print(start_annealing.main_candidate.order[i].name, " (", start_annealing.main_candidate.order[i].x,
              ", ", start_annealing.main_candidate.order[i].y, ")")


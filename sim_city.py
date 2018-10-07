class City:
    def __init__(self, base_city_tax=1000):
        self.neighborhoods = {}
        self.base_city_tax = base_city_tax

    def how_much_money(self):
        city_tax = self.base_city_tax
        for neighborhood in self.neighborhoods:
            city_tax += self.neighborhoods[neighborhood].how_much_money_neighborhood()
        return city_tax

    def build_a_neighborhood(self, neighborhood_name):
        new_neighborhood = Neighborhood()
        self.neighborhoods[neighborhood_name] = new_neighborhood
        self.base_city_tax *= 1.1

    def ruin_a_neighborhood(self, neighborhood_name):
        if neighborhood_name not in self.neighborhoods:
            return
        del self.neighborhoods[neighborhood_name]
        self.base_city_tax *= 1.05

    def build_a_house(self, neighborhood_name, family_members, size):
        if neighborhood_name not in self.neighborhoods:
            return
        self.neighborhoods[neighborhood_name].add_house(family_members, size)

    def build_a_park(self, neighborhood_name):
        if neighborhood_name not in self.neighborhoods:
            return
        self.neighborhoods[neighborhood_name].add_park()


class Neighborhood:
    def __init__(self):
        self.houses = []
        self.parks = 0

    def how_much_money_neighborhood(self):
        neighborhood_tax = (self.parks * 5) + (len(self.houses) * 3)  # base tax
        for family_members, size in self.houses:  # house is a tuple
            neighborhood_tax += family_members * size
        return neighborhood_tax

    def add_house(self, family_members, size):
        self.houses.append((family_members, size))

    def add_park(self):
        self.parks += 1


# tests
synville = City()
print(synville.neighborhoods)
print(synville.how_much_money())
synville.build_a_neighborhood('first')
synville.ruin_a_neighborhood('second')  # ruin a neighborhood that doesn't exist
print(synville.neighborhoods)
print(synville.how_much_money())
synville.build_a_house('first', 5, 5)
synville.build_a_house('first', 10, 10)
print(synville.how_much_money())
synville.build_a_park('first')
print(synville.how_much_money())
synville.build_a_park('second')  # build in neighborhood that doesn't exist
synville.build_a_house('second', 1, 1)  # build in neighborhood that doesn't exist
print(synville.how_much_money())
synville.ruin_a_neighborhood('first')
print(synville.how_much_money())
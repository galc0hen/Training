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
        neighborhood = self.neighborhoods.pop(neighborhood_name, None)
        if neighborhood is None:
            print(f'{neighborhood_name} neighborhood is not listed.')
            return
        self.base_city_tax *= 1.05

    def build_a_house(self, neighborhood_name, family_members, size):
        neighborhood = self.neighborhoods.get(neighborhood_name)
        if not neighborhood:
            print(f'{neighborhood_name} neighborhood is not listed.')
            return
        neighborhood.add_house(family_members, size)

    def build_a_park(self, neighborhood_name):
        neighborhood = self.neighborhoods.get(neighborhood_name)
        if not neighborhood:
            print(f'{neighborhood_name} neighborhood is not listed.')
            return
        neighborhood.add_park()


class Neighborhood:
    def __init__(self):
        self.houses = []
        self.parks = 0

    def how_much_money_neighborhood(self):
        neighborhood_tax = (self.parks * 5) + (len(self.houses) * 3)  # base neighborhood tax
        for house in self.houses:
            neighborhood_tax += house.how_much_money_house()
        return neighborhood_tax

    def add_house(self, family_members, size):
        new_house = House(family_members, size)
        self.houses.append(new_house)

    def add_park(self):
        self.parks += 1


class House:
    def __init__(self, family_members, size):
        self.family_members = family_members
        self.size = size

    def how_much_money_house(self):
        return self.family_members * self.size
        

def main():
    synville = City()
    print(f'Synville Tax is (expecting 1000): {synville.how_much_money()}')  # expecting 1000
    synville.build_a_neighborhood('Florentin')  # no output
    synville.ruin_a_neighborhood('Tzafon Yashan')  # expecting: "Tzafon Yashan neighborhood is not listed."
    print(f'Synville Tax is (expecting 1100): {synville.how_much_money()}')  # expecting 1100
    synville.build_a_house('Florentin', 2, 6)
    synville.build_a_park('Florentin')
    print(f'Synville Tax is (expecting 1120): {synville.how_much_money()}')  # expecting 1120
    synville.build_a_park('Tzafon Yashan')  # expecting: "Tzafon Yashan neighborhood is not listed."
    synville.build_a_house('Tzafon Yashan', 1, 1)  # expecting: "Tzafon Yashan neighborhood is not listed."
    synville.ruin_a_neighborhood('Florentin')   # no output
    synville.build_a_park('Florentin')  # expecting: "Florentin neighborhood is not listed."
    print(f'Synville Tax is (expecting 1155): {synville.how_much_money()}')  # expecting 1155


if __name__ == '__main__':
    main()

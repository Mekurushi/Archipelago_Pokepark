from . import PokeparkTest

class TestPokemonFriendshipDependencies(PokeparkTest):

    def test_bulbasaur_prisma(self) -> None:
        """Verify locations and victory conditions for Bulbasaur's Prisma unlock"""
        locations = ["Meadow Zone - Overworld - Munchlax","Meadow Zone - Overworld - Munchlax Friendship - Pokemon Unlock","Meadow Zone - Overworld - Tropius","Meadow Zone - Overworld - Bulbasaur","Victory"]
        items = [["Bulbasaur Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_venusaur_prisma(self) -> None:
        """Verify victory conditions for Venusaur's Prisma unlock"""
        locations = ["Victory"]
        items = [["Venusaur Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_pelipper_prisma(self) -> None:
        """Verify Treehouse Dash Upgrade locations and victory conditions for Pelipper's Prisma unlock"""
        locations = [f"Treehouse - Dash Upgrade {i}" for i in range(1, 4)]
        locations.append("Victory")
        #locations.append("Beach Zone - Overworld - Pelipper")
        items = [["Pelipper Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_gyarados_prisma(self) -> None:
        """Verify victory conditions for Gyarados' Prisma unlock"""
        locations = ["Victory"]
        #locations.append("Beach Zone - Overworld - Gyarados")
        items = [["Gyarados Prisma"]]
        self.assertAccessDependency(locations, items)



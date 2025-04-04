from . import PokeparkTest


class TestPrismaDependencies(PokeparkTest):

    def test_bulbasaur_prisma(self) -> None:
        """Verify locations and victory conditions for Bulbasaur's Prisma unlock"""
        locations = ["Meadow Zone - Overworld - Munchlax",
                     "Meadow Zone - Overworld - Munchlax Friendship - Pokemon Unlock",
                     "Meadow Zone - Overworld - Tropius", "Meadow Zone - Overworld - Bulbasaur", "Victory"]
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
        items = [["Pelipper Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_gyarados_prisma(self) -> None:
        """Verify victory conditions for Gyarados' Prisma unlock"""
        locations = ["Victory"]
        items = [["Gyarados Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_empoleon_prisma(self) -> None:
        """Verify victory conditions for Empoleon Prisma unlock"""
        locations = ["Victory"]
        items = [["Empoleon Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_bastiodon_prisma(self) -> None:
        """Verify victory conditions for Bastiodon Prisma unlock"""
        locations = ["Victory"]
        items = [["Bastiodon Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_rhyperior_prisma(self) -> None:
        """Verify victory conditions for Rhyperior Prisma unlock"""
        locations = ["Victory"]
        items = [["Rhyperior Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_blaziken_prisma(self) -> None:
        """Verify victory conditions for Blaziken Prisma unlock"""
        locations = ["Victory"]
        items = [["Blaziken Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_tangrowth_prisma(self) -> None:
        """Verify victory conditions for Blaziken Prisma unlock"""
        locations = ["Victory"]
        items = [["Tangrowth Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_dusknoir_prisma(self) -> None:
        """Verify victory conditions for Blaziken Prisma unlock"""
        locations = ["Victory",
                     "Haunted Zone - Overworld - Mansion - Duskull"]
        items = [["Dusknoir Prisma"]]
        self.assertAccessDependency(locations, items)

    def test_rotom_prisma(self) -> None:
        """Verify victory conditions for Blaziken Prisma unlock"""
        locations = ["Victory",
                     "Haunted Zone - Overworld - Drifloon",
                     "Haunted Zone - Overworld - Metapod",
                     "Haunted Zone - Overworld - Kakuna",
                     "Haunted Zone - Overworld - Mansion - Spinarak",
                     "Haunted Zone - Overworld - Mansion - Electrode"]
        items = [["Rotom Prisma"]]
        self.assertAccessDependency(locations, items)

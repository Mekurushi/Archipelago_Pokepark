from . import PokeparkTestBase


class TestPowerUpShop(PokeparkTestBase):
    options = {
        "power_starting_mode": 2  # start with none power items
    }

    def test_thunderbolt_upgrade_1_needs_dash_unlocked(self) -> None:
        locations = ["Treehouse - Power Up - Thunderbolt Upgrade 1"]
        items = [["Progressive Dash"], ["Double Dash"]]  # can_dash
        self.assertAccessDependency(locations, items, True)

    def test_thunderbolt_upgrade_2_needs_beach_recycle_area(self) -> None:
        locations = ["Treehouse - Power Up - Thunderbolt Upgrade 2"]
        items = [["Beach Bridge 2 Unlock"]]  # can reach recycle area
        self.assertAccessDependency(locations, items, True)

    def test_thunderbolt_upgrade_3_needs_magma_zone_and_golem(self) -> None:
        locations = ["Treehouse - Power Up - Thunderbolt Upgrade 3"]
        items = [["Bastiodon Prisma", "Golem Unlock"]]  # can reach Magma Zone Main Area + Golem Unlock
        self.assertAccessDependency(locations, items, True)

    def test_dash_upgrade_1_needs_pelipper_prisma(self) -> None:
        locations = ["Treehouse - Power Up - Dash Upgrade 1"]
        items = [["Pelipper Prisma"]]
        self.assertAccessDependency(locations, items, True)

    def test_dash_upgrade_2_and_ponyta_need_pelipper_prisma_and_recycle_area(self) -> None:
        locations = [
            "Treehouse - Power Up - Dash Upgrade 2",
            "Treehouse - Power Up - Ponyta Unlocked",
        ]
        items = [["Pelipper Prisma", "Beach Bridge 2 Unlock"]]
        self.assertAccessDependency(locations, items, True)

    def test_health_upgrade_1_needs_venusaur_prisma(self) -> None:
        locations = ["Treehouse - Power Up - Health Upgrade 1"]
        items = [["Venusaur Prisma"]]
        self.assertAccessDependency(locations, items, True)

    def test_iron_tail_upgrade_1_needs_empoleon_prisma(self) -> None:
        locations = ["Treehouse - Power Up - Iron Tail Upgrade 1"]
        items = [["Empoleon Prisma"]]
        self.assertAccessDependency(locations, items, True)

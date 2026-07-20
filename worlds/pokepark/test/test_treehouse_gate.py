from . import PokeparkTestBase


class TestTreehouseGates(PokeparkTestBase):
    options = {
        "randomize_attraction_entrances": False,
        "randomize_fast_travel_entrances": False,
        "randomize_treehouse_gates_entrances": False,
        "randomize_general_entrances": False,
        "mix_entrance_pools": False,
    }

    def test_meadow_zone_gate_needs_no_prisma(self) -> None:
        region = "Meadow Zone Main Area"
        self.assertTrue(self.can_reach_region(region))

    def test_beach_zone_gate_needs_venusaur_prisma(self) -> None:
        region = "Beach Zone Main Area"
        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name("Venusaur Prisma")
        self.assertTrue(self.can_reach_region(region))

    def test_cavern_zone_gate_needs_empoleon_prisma(self) -> None:
        region = "Cavern Zone Main Area"
        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name("Empoleon Prisma")
        self.assertTrue(self.can_reach_region(region))

    def test_haunted_zone_gate_needs_blaziken_prisma(self) -> None:
        region = "Haunted Zone Main Area"
        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name("Blaziken Prisma")
        self.assertTrue(self.can_reach_region(region))

    def test_granite_zone_gate_needs_Rotom_prisma(self) -> None:
        region = "Granite Zone Main Area"
        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name("Rotom Prisma")
        self.assertTrue(self.can_reach_region(region))

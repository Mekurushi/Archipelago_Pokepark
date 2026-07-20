from . import PokeparkTestBase


class TestFriendshipCountThresholds(PokeparkTestBase):
    options = {
        "randomize_attraction_entrances": False,
        "randomize_fast_travel_entrances": False,
        "randomize_treehouse_gates_entrances": False,
        "randomize_general_entrances": False,
        "mix_entrance_pools": False,
        # make all friendship items progressive to easify testing, since we only care about the count logic
        "goal": 1,
        "remove_attraction_locations": False
    }

    def _friendship_pool(self) -> list:
        return sorted(self.world.item_name_groups["Friendship Items"])

    def test_bastiodon_attraction_requires_exactly_50_friendships(self) -> None:
        region = "Bastiodon's Panel Crush Attraction"
        pool = self._friendship_pool()
        self.collect_all_but(pool)
        #  asserting that we can reach up to the entrance to the attraction
        self.assertTrue(self.can_reach_region("Cavern Zone Main Area"))

        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name(pool[:49])
        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name([pool[49]])
        self.assertTrue(self.can_reach_region(region))

    def test_rotom_attraction_requires_exactly_65_friendships(self) -> None:
        region = "Rotom's Spooky Shoot-'em-Up Attraction"
        pool = self._friendship_pool()
        self.collect_all_but(pool)
        #  asserting that we can reach up to the entrance to the attraction
        self.assertTrue(self.can_reach_region("Haunted Zone Rotom Area"))

        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name(pool[:64])
        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name([pool[64]])
        self.assertTrue(self.can_reach_region(region))

    def test_salamence_attraction_requires_exactly_80_friendships(self) -> None:
        region = "Salamence's Sky Race Attraction"
        pool = self._friendship_pool()
        self.collect_all_but(pool)
        #  asserting that we can reach up to the entrance to the attraction
        self.assertTrue(self.can_reach_region("Granite Zone Main Area"))

        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name(pool[:79])
        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name([pool[79]])
        self.assertTrue(self.can_reach_region(region))


class TestSkygardenPrismaGate(PokeparkTestBase):
    options = {
        "randomize_attraction_entrances": False,
        "randomize_fast_travel_entrances": False,
        "randomize_treehouse_gates_entrances": False,
        "randomize_general_entrances": False,
        "mix_entrance_pools": False,
        "num_required_prisma_count_skygarden": 3
    }

    def test_needs_exactly_the_configured_prisma_count(self) -> None:
        region = "Skygarden"
        required = 3  # keep in sync with the option above
        pool = sorted(self.world.item_name_groups["Prisma Items"])
        self.collect_all_but(pool)
        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name(pool[:required - 1])
        self.assertFalse(self.can_reach_region(region))
        self.collect_by_name([pool[required - 1]])
        self.assertTrue(self.can_reach_region(region))

from . import PokeparkTestBase


# spot checks are enough to test the abstracted logic
class TestBattleStagesDefault(PokeparkTestBase):
    """harder_enemy_ai is off"""
    options = {
        "harder_enemy_ai": False,
        "power_starting_mode": 2  # start with none power items
    }

    def test_basic_battle_needs_iron_tail_or_thunderbolt(self) -> None:
        locations = ["Meadow Zone Main Area - Mankey Battle Power Competition -- Friendship"]
        items = [["Progressive Iron Tail"], ["Progressive Thunderbolt"]]
        self.assertAccessDependency(locations, items, True)

    def test_intermediate_battle_needs_two_health_plus_one_weapon(self) -> None:
        locations = ["Beach Zone Main Area - Feraligatr Battle Power Competition -- Friendship"]
        items = [
            ["Progressive Health", "Progressive Health", "Progressive Iron Tail"],
            ["Progressive Health", "Progressive Health", "Progressive Thunderbolt"],
        ]
        self.assertAccessDependency(locations, items, True)

    def test_advanced_battle_needs_three_health_plus_two_weapon(self) -> None:
        locations = ["Granite Zone Main Area - Charizard Battle Power Competition -- Friendship"]
        items = [
            ["Progressive Health"] * 3 + ["Progressive Iron Tail"] * 2,
            ["Progressive Health"] * 3 + ["Progressive Thunderbolt"] * 2,
        ]
        self.assertAccessDependency(locations, items, True)

    def test_thunderbolt_immune_needs_health_plus_dash_or_double_dash_or_iron_tail(self) -> None:
        locations = ["Cavern Zone Main Area - Gible Battle Power Competition -- Friendship"]
        items = [
            ["Progressive Health", "Progressive Dash"],
            ["Progressive Health", "Double Dash"],
            ["Progressive Health", "Progressive Iron Tail"],
        ]
        self.assertAccessDependency(locations, items, True)


class TestBattleTiersHarderAI(PokeparkTestBase):
    """harder_enemy_ai is on"""

    options = {"harder_enemy_ai": True}

    def test_basic_battle_needs_health_plus_offensive_power(self) -> None:
        locations = ["Meadow Zone Main Area - Mankey Battle Power Competition -- Friendship"]
        items = [
            ["Progressive Health", "Progressive Iron Tail"],
            ["Progressive Health", "Progressive Thunderbolt"],
        ]
        self.assertAccessDependency(locations, items, True)

    def test_advanced_battle_needs_three_health_plus_three_offensive_powers(self) -> None:
        locations = ["Granite Zone Main Area - Charizard Battle Power Competition -- Friendship"]
        items = [
            ["Progressive Health"] * 3 + ["Progressive Iron Tail"] * 3,
            ["Progressive Health"] * 3 + ["Progressive Thunderbolt"] * 3,
        ]
        self.assertAccessDependency(locations, items, True)

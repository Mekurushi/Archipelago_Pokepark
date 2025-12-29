from dataclasses import dataclass
from typing import Any

from Options import PerGameCommonOptions, Choice, OptionGroup, Range, Toggle


class Powers(Choice):
    """
    Determines how Power Items are shuffled into the pool.
    Full: Start with all Power Items
    Thunderbolt: Start with one Thunderbolt Power
    Dash: Start with one Dash Power
    ThunderboltDash: Start with one Thunderbolt and Dash Power (Default)
    None: Start with no Powers (Thunderbolt and Dash unusable)
    """
    display_name = "Powers"
    option_full = 0
    option_thunderbolt = 1
    option_dash = 2
    option_thunderbolt_dash = 3
    option_none = 4
    default = 3


class StartFastTravel(Choice):
    """
    Determines how Fast Travel Items are shuffled into the pool
    None: Start with no Fast Travel Items (Default)
    One: Start with one random Fast Travel Item
    All: Start with all Fast Travel Items
    """
    display = "Precollect Fast Travel"
    option_none = 0
    option_one = 1
    option_all = 2
    default = 0


class Goal(Choice):
    """
    Determines World completion condition
    Mew: Beat Mew (Default)
    postgame: Complete the postgame Prisma check (needs all friends)
    """
    display = "Goal Condition"
    option_mew = 0
    option_postgame = 1


class NumRequiredBattleCount(Range):
    """
    Select the number of required consecutive Wins to challenge Battle count Pokemon e.g. Scyther
    """
    display = "Number of Battle Count"
    range_start = 0
    range_end = 10
    default = 5


class NumRequiredPrismaCountSkygarden(Range):
    """
    Select the number of required Prisma Shards to enter Skygarden with piplup in the Treehouse
    """
    display = "Number of required Prismas"
    range_start = 1
    range_end = 14
    default = 14


class RemoveBattlePowerCompLocations(Toggle):
    """
    Remove Battle Power Competition Locations. They will no longer send items but can still be used for
    gaining berries.
    WARNING: Removing too many location types may cause an OptionError if there aren't enough locations for progressive items.
    """
    default = False


class RemoveChasePowerCompLocations(Toggle):
    """
    Remove Chase Power Competition Locations. They will no longer send items but can still be used for
    gaining berries.
    WARNING: Removing too many location types may cause an OptionError if there aren't enough locations for progressive items.
    """
    default = False


class RemoveQuizPowerCompLocations(Toggle):
    """
    Remove Quiz Power Competition Locations. They will no longer send items but can still be used for
    gaining berries.
    WARNING: Removing too many location types may cause an OptionError if there aren't enough locations for progressive items.
    """
    default = True


class RemoveHideAndSeekPowerCompLocations(Toggle):
    """
    Remove Hide and Seek Power Competition Locations. They will no longer send items but can still be
    used for gaining berries.
    WARNING: Removing too many location types may cause an OptionError if there aren't enough locations for progressive items.
    """
    default = False


class RemoveErrandPowerCompLocations(Toggle):
    """
    Remove Errand Power Competition Locations. They will no longer send items but can still be used for
    gaining berries.
    WARNING: Removing too many location types may cause an OptionError if there aren't enough locations for progressive items.
    """
    default = False


class RemoveLegendaryPokemonPowerCompLocations(Toggle):
    """
    Remove Legendary Pokemon Power Competition Locations e.g. Celebi. They will no longer send items but can still be
    used for gaining berries.
    WARNING: Removing too many location types may cause an OptionError if there aren't enough locations for progressive items.
    """
    default = False


class RemoveMiscPowerCompLocations(Toggle):
    """
    Remove Miscellaneous Power Competition Locations. They will no longer send items but can still be
    used for gaining berries.
    WARNING: Removing too many location types may cause an OptionError if there aren't enough locations for progressive items.
    """
    default = False


class RemovePowerUpLocations(Toggle):
    """
    Remove Power Training Locations (e.g., Thunderbolt Upgrade Training at Electabuzz).
    WARNING: Removing too many location types may cause an OptionError if there aren't enough locations for progressive items.
    """
    default = False

class RemoveAttractionLocations(Toggle):
    """
    Remove Record clearing Attraction Locations. (each Pokemon Record is a Location)
    WARNING: Removing too many location types may cause an OptionError if there aren't enough locations for progressive items.
    """
    default = True


class RemoveAttractionPrismaLocations(Toggle):
    """
    Remove Attraction Prisma clear locations. (Vanilla first time beating Attraction Goal)
    WARNING: Removing too many location types may cause an OptionError if there aren't enough locations for progressive items.
    """
    default = False


class RemovePokemonUnlockLocations(Toggle):
    """
    Remove Pokemon Unlock Locations. e.g. Caterpie Tree, Shroomish Crate etc.
    WARNING: Removing too many location types may cause an OptionError if there aren't enough locations for progressive items.
    """
    default = False


class HarderEnemyAI(Toggle):
    """
    Pokémon always have the harder AI in Power Competition.
    WARNING: Generation currently does not account in detail for the harder enemy AI, which can lead to frustrating
    gameplay.
    """
    default = False

class RandomizeAttractionEntrances(Toggle):
    """
    Randomize Attraction Entrances with each other
    """
    default = False


class RandomizeFastTravelEntrances(Toggle):
    """
    Randomize Fast Travel Entrances with each other
    """
    default = False


class RandomizeTreehouseGatesEntrances(Toggle):
    """
    Randomize Treehouse Gate Entrances with each other
    """
    default = False


class RandomizeGeneralEntrances(Toggle):
    """
    Randomize General Entrances with each other, e.g. Meadow Zone Main Area -> Meadow Zone Venusaur Area
    """
    default = False


class MixRandomizedEntrancePools(Toggle):
    """
    Mix all toggled randomize Entrance in one Pool. Except Attraction Entrances.
    """
    default = False

class EachZone(Toggle):
    """
    Pokemon that are in multiple Zones become additional Locations. e.g. Bonsly (Meadow, Cavern, Magma Zone)
    """
    default = False


class InZoneRoadBlocks(Toggle):
    """
    Additional Road Blocks inside the Zones e.g. Beach Zone Bridges as items. Road Block Items are precollected when
    this option is deactivated.
    """
    default = True


class UnlockFastTravelWithTaxiStop(Toggle):
    """
    Unlocks Fast Travel to reachable zones when interacting with Taxi Stops beside Drifblim. This option is
    automatically disabled when the Randomized Fast Travel Entrances option is enabled.
    """
    default = True


class DeathLink(Toggle):
    """When you die, everyone who enabled death link dies. Of course, the reverse is true too."""
    display_name = "Death Link"
    rich_text_doc = True

@dataclass
class PokeparkOptions(PerGameCommonOptions):
    power_randomizer: Powers
    start_fast_travel: StartFastTravel
    goal: Goal
    num_required_battle_count: NumRequiredBattleCount
    each_zone: EachZone
    remove_battle_power_comp_locations: RemoveBattlePowerCompLocations
    remove_chase_power_comp_locations: RemoveChasePowerCompLocations
    remove_quiz_power_comp_locations: RemoveQuizPowerCompLocations
    remove_hide_and_seek_power_comp_locations: RemoveHideAndSeekPowerCompLocations
    remove_errand_power_comp_locations: RemoveErrandPowerCompLocations
    remove_misc_power_comp_locations: RemoveMiscPowerCompLocations
    remove_legendary_pokemon_power_comp_locations: RemoveLegendaryPokemonPowerCompLocations
    remove_power_training_locations: RemovePowerUpLocations
    remove_attraction_locations: RemoveAttractionLocations
    remove_attraction_prisma_locations: RemoveAttractionPrismaLocations
    remove_pokemon_unlock_locations: RemovePokemonUnlockLocations
    num_required_prisma_count_skygarden: NumRequiredPrismaCountSkygarden
    in_zone_road_blocks: InZoneRoadBlocks
    randomize_attraction_entrances: RandomizeAttractionEntrances
    randomize_fast_travel_entrances: RandomizeFastTravelEntrances
    randomize_treehouse_gates_entrances: RandomizeTreehouseGatesEntrances
    randomize_general_entrances: RandomizeGeneralEntrances
    mix_entrance_pools: MixRandomizedEntrancePools
    harder_enemy_ai: HarderEnemyAI
    unlock_fast_travel_with_taxi_stop: UnlockFastTravelWithTaxiStop
    death_link: DeathLink

    def get_output_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary of option name to value to be placed in
        the output pprk file.

        :return: Dictionary of option name to value for the output file.
        """

        # Note: these options' values must be able to be passed through
        # `yaml.safe_dump`.
        return self.as_dict(
            "goal",
            "num_required_battle_count",
            "num_required_prisma_count_skygarden",
            "remove_errand_power_comp_locations",
            "harder_enemy_ai",
            "each_zone",
            "unlock_fast_travel_with_taxi_stop"
        )


pokepark_option_groups = [
    OptionGroup("Goal", [
        Goal
    ]),
    OptionGroup(
        "Entrances", [
            RandomizeAttractionEntrances,
            RandomizeTreehouseGatesEntrances,
            RandomizeFastTravelEntrances,
            RandomizeGeneralEntrances,
            MixRandomizedEntrancePools
        ]
    ),
    OptionGroup("Misc", [
        Powers,
        StartFastTravel,
        NumRequiredBattleCount,
        NumRequiredPrismaCountSkygarden,
        InZoneRoadBlocks,
        HarderEnemyAI,
        UnlockFastTravelWithTaxiStop
    ]
                ),
    OptionGroup(
        "Locations", [
            RemoveBattlePowerCompLocations,
            RemoveChasePowerCompLocations,
            RemoveQuizPowerCompLocations,
            RemoveHideAndSeekPowerCompLocations,
            RemoveErrandPowerCompLocations,
            RemoveMiscPowerCompLocations,
            RemovePowerUpLocations,
            RemoveAttractionLocations,
            RemoveAttractionPrismaLocations,
            RemovePokemonUnlockLocations,
            RemoveLegendaryPokemonPowerCompLocations,
            EachZone
        ]
    )
]

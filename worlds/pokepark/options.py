from dataclasses import dataclass
from typing import Any

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, StartInventoryPool, Toggle


class PowerStartingMode(Choice):
    """
    Determines which Power Items are added to the starting inventory.
    For fully custom starting Powers, set this to 'None' and use the StartInventoryPool option instead

    Full: Start with all Power Items, including Double Dash.
    None: Start with no Power Items.
    Vanilla: Start with one Thunderbolt and one Dash (default).
    Thunderbolt: Start with one Thunderbolt.
    Dash: Start with one Dash.
    IronTail: Start with one Iron Tail.
    Randomize: Start with a random number of each Power Item, including Double Dash.
    """
    display_name = "Starting Power Item Preset"
    option_full = 0
    option_none = 2
    option_vanilla = 3
    option_thunderbolt = 4
    option_dash = 5
    option_iron_tail = 6
    option_randomize = 7
    default = 3


class StartFastTravel(Choice):
    """
    Determines how many Fast Travel Items are added to the starting inventory.

    None: Start with no Fast Travel Items (default).
    One: Start with one random Fast Travel Item.
    All: Start with all Fast Travel Items.
    """
    display_name = "Starting Fast Travel Items"
    option_none = 0
    option_one = 1
    option_all = 2
    default = 0


class Goal(Choice):
    """
    Determines the goal required to complete the world.

    Mew: Complete Mew's Power Competition (default).
    Postgame: Complete the postgame Prisma completion, which requires all Friendships.
    """
    display_name = "Goal"
    option_mew = 0
    option_postgame = 1


class NumRequiredBattleCount(Range):
    """
    Determines the number of required consecutive Wins to challenge Battle count Pokemon e.g. Scyther

    Set this to 0 to remove the consecutive Battle requirement.
    """
    display_name = "Required Battle Win Streak"
    range_start = 0
    range_end = 7
    default = 5


class NumRequiredPrismaCountSkygarden(Range):
    """
    Determines how many Prisma Shards are required to travel to Skygarden with Piplup in the Treehouse.
    """
    display_name = "Skygarden Prisma Requirement"
    range_start = 1
    range_end = 14
    default = 14


class RemoveBattlePowerCompLocations(Toggle):
    """
    Removes Battle Power Competition Locations. Battles can still be played to gain Berries but will no longer send
    Location Checks.

    WARNING: Removing too many Location types may leave too few Locations for the required progression Items.
    """
    display_name = "Remove Battle Power Competition Locations"
    default = False


class RemoveChasePowerCompLocations(Toggle):
    """
    Removes Chase Power Competition Locations. Chases can still be played to gain Berries but will no longer send
    Location Checks.

    WARNING: Removing too many Location types may leave too few Locations for the required progression Items.
    """
    display_name = "Remove Chase Power Competition Locations"
    default = False


class RemoveQuizPowerCompLocations(Toggle):
    """
    Removes Quiz Power Competition Locations. Quizzes can still be played to gain Berries but will no longer send
    Location Checks.

    WARNING: Removing too many Location types may leave too few Locations for the required progression Items.
    """
    display_name = "Remove Quiz Power Competition Locations"
    default = True


class RemoveHideAndSeekPowerCompLocations(Toggle):
    """
    Removes Hide and Seek Power Competition Locations. Hide and Seek can still be played to gain Berries but will no
    longer send Location Checks.

    WARNING: Removing too many Location types may leave too few Locations for the required progression Items.
    """
    display_name = "Remove Hide-and-Seek Power Competition Locations"
    default = False


class RemoveErrandPowerCompLocations(Toggle):
    """
    Removes Errand Locations. Errands can still be completed to gain Berries but will no longer send Location Checks.

    WARNING: Removing too many Location types may leave too few Locations for the required progression Items.
    """
    display_name = "Remove Errand Locations"
    default = False


class RemoveLegendaryPokemonPowerCompLocations(Toggle):
    """
    Removes Legendary Pokemon Power Competition Locations, such as Celebi. These competitions can still be played to
    gain Berries but will no longer send Location Checks.

    WARNING: Removing too many Location types may leave too few Locations for the required progression Items.
    """
    display_name = "Remove Legendary Pokemon Locations"
    default = False


class RemoveMiscPowerCompLocations(Toggle):
    """
    Removes miscellaneous Friendship Locations that do not belong to another Power Competition category. These
    activities can still be completed to gain Berries but will no longer send Location Checks.

    WARNING: Removing too many Location types may leave too few Locations for the required progression Items.
    """
    display_name = "Remove Miscellaneous Friendship Locations"
    default = False


class RemovePowerUpLocations(Toggle):
    """
    Removes Power Training Locations, such as Thunderbolt Training with Electabuzz.

    WARNING: Removing too many Location types may leave too few Locations for the required progression Items.
    """
    display_name = "Remove Power Training Locations"
    default = False

class RemoveAttractionLocations(Toggle):
    """
    Removes the individual Pokemon Record Locations from Attractions. Attractions can still be played to gain Berries,
    and their Prisma Locations are not removed by this option.

    WARNING: Removing too many Location types may leave too few Locations for the required progression Items.
    """
    display_name = "Remove Attraction Record Locations"
    default = True


class RemoveAttractionPrismaLocations(Toggle):
    """
    Removes the Prisma Location from each Attraction. Attractions can still be played to gain Berries, and their
    individual Pokemon Record Locations are not removed by this option.

    WARNING: Removing too many Location types may leave too few Locations for the required progression Items.
    """
    display_name = "Remove Attraction Prisma Locations"
    default = False


class RemovePokemonUnlockLocations(Toggle):
    """
    Removes Locations for unlocking Pokemon in the overworld, such as Caterpie's Tree and Shroomish's Crate.

    WARNING: Removing too many Location types may leave too few Locations for the required progression Items.
    """
    display_name = "Remove Pokemon Unlock Locations"
    default = False


class HarderEnemyAI(Toggle):
    """
    Pokemon always use their harder AI during Power Competitions. Logic requirements are increased to account for the
    additional difficulty, but individual matchups may still be harder depending on player skill and know-how.
    """
    display_name = "Harder Power Competition AI"
    default = False

class RandomizeAttractionEntrances(Toggle):
    """
    Randomizes Attraction Entrances among themselves. Entering an Attraction may lead to a different Attraction.
    """
    display_name = "Randomize Attraction Entrances"
    default = False


class RandomizeFastTravelEntrances(Toggle):
    """
    Randomizes Drifblim Fast Travel Entrances among themselves.

    Each Fast Travel route is randomized separately based on its starting Zone and selected destination. For example,
    traveling from the Meadow Zone to the Beach Zone may lead somewhere different than traveling from the Cavern Zone
    to the Beach Zone.

    Enabling this option automatically disables unlocking Fast Travel through Taxi Stops.
    """
    display_name = "Randomize Fast Travel Routes"
    default = False


class RandomizeTreehouseGatesEntrances(Toggle):
    """
    Randomizes the Zone Gates in the Treehouse among themselves. Entering a Gate may lead to a different Zone.
    """
    display_name = "Randomize Treehouse Gates"
    default = False


class RandomizeGeneralEntrances(Toggle):
    """
    Randomizes general overworld Entrances, such as the connection between the Meadow Zone Main Area and the Venusaur
    Area.
    """
    display_name = "Randomize General Entrances"
    default = False


class MixRandomizedEntrancePools(Toggle):
    """
    Combines all enabled Treehouse Gate, Fast Travel, and General Entrance pools into one randomized pool. Attraction
    Entrances remain in their own pool.
    """
    display_name = "Mix Entrance Randomization Pools"
    default = False

class EachZone(Toggle):
    """
    Pokemon that appear in multiple Zones become separate Locations for each Zone.

    For example, Bonsly in the Meadow, Cavern, and Magma Zones becomes three separate Locations instead of one shared
    Location.
    """
    display_name = "Separate Pokemon Locations by Zone"
    default = False


class InZoneRoadBlocks(Toggle):
    """
    Adds Roadblock Items for obstacles inside the Zones, such as the Beach Zone Bridges.

    When disabled, all affected Roadblock Items are added to the starting inventory.
    """
    display_name = "In-Zone Roadblock Items"
    default = True


class UnlockFastTravelWithTaxiStop(Toggle):
    """
    Unlocks Fast Travel to reachable Zones when interacting with the Taxi Stops beside Drifblim.

    This option is automatically disabled when Fast Travel Entrances are randomized.
    """
    display_name = "Unlock Fast Travel at Taxi Stops"
    default = True


class DeathLink(Toggle):
    """
    Sends a DeathLink when losing a Power Competition. Depending on the game version, the Power Competition's
    location, and other circumstances, some losses may not send a DeathLink right now.

    DeathLinks from other players can be received anywhere in the game. More information can be found in the
    documentation.
    """
    display_name = "Death Link"
    rich_text_doc = True


class ShowClientTextInGame(Toggle):
    """
    Displays Archipelago Client messages inside the game. This can also be toggled from the PokePark Client.
    """
    display_name = "Show Client Messages In-Game"
    default = True


class FpsEnhancementPatch(Toggle):
    """
    Unlocks the frame rate up to 60 FPS.
    """
    display_name = "60 FPS Patch"
    default = False

@dataclass
class PokeparkOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    power_starting_mode: PowerStartingMode
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
    show_client_text_ingame: ShowClientTextInGame
    fps_enhancement_patch: FpsEnhancementPatch

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
            "unlock_fast_travel_with_taxi_stop",
            "show_client_text_ingame",
            "fps_enhancement_patch"
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
        PowerStartingMode,
        StartFastTravel,
        NumRequiredBattleCount,
        NumRequiredPrismaCountSkygarden,
        InZoneRoadBlocks,
        HarderEnemyAI,
        UnlockFastTravelWithTaxiStop,
        ShowClientTextInGame,
        FpsEnhancementPatch
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

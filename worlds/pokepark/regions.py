from dataclasses import dataclass
from typing import Callable, List, TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from worlds.pokepark import PokeparkWorld
from worlds.pokepark.rules import get_entrance_rules_dict


@dataclass(frozen=True)
class Entrance:
    name: str
    parent_region: str


@dataclass(frozen=True)
class Exit:
    name: str
    region_name: str


# for generating the bi directional connection exit name is used as entrance name and the entrance name is used as
# exit name. Because bi-directional entrances often don't have the same rules both entrance name and exit name needs
# to be defined in the rules dict

GENERAL_ENTRANCES: list[Entrance] = [
    Entrance("Meadow Zone Main Area - Pokepark Entrance Gate", "Meadow Zone Main Area"),

    Entrance("Meadow Zone Main Area - Venusaur Gate", "Meadow Zone Main Area"),

    Entrance("Beach Zone Lapras Area - Beach Zone Lapras", "Beach Zone Lapras Area"),

    Entrance("Ice Zone Main Area - Empoleon Gate", "Ice Zone Main Area"),

    Entrance("Cavern Zone Main Area - Magma Zone Truck", "Cavern Zone Main Area"),

    Entrance("Magma Zone Magcargo Area - Blaziken Gate", "Magma Zone Magcargo Area"),

    Entrance("Haunted Zone Main Area - Mansion Gate", "Haunted Zone Main Area"),

    Entrance("Haunted Zone Bookshelf Area - Rotom Connection", "Haunted Zone Bookshelf Area"),

    Entrance("Granite Zone Main Area - Flower Zone Gate", "Granite Zone Main Area"),

]

TREEHOUSE_GATE_ENTRANCES: list[Entrance] = [
    Entrance("Treehouse Meadow Passage - Meadow Zone Connection", "Treehouse Meadow Passage"),
    Entrance("Treehouse Beach Passage - Beach Zone Connection", "Treehouse Beach Passage"),
    Entrance("Treehouse Cavern Passage - Cavern Zone Connection", "Treehouse Cavern Passage"),
    Entrance("Treehouse Haunted Passage - Haunted Zone Connection", "Treehouse Haunted Passage"),
    Entrance("Treehouse Granite Passage - Granite Zone Connection", "Treehouse Granite Passage"),
]

FAST_TRAVEL_ENTRANCES: list[Entrance] = [

    # Meadow Zone
    Entrance("Meadow Zone Main Area - Beach Drifblim Fast Travel", "Meadow Zone Main Area"),
    Entrance("Meadow Zone Main Area - Ice Drifblim Fast Travel", "Meadow Zone Main Area"),
    Entrance("Meadow Zone Main Area - Cavern Drifblim Fast Travel", "Meadow Zone Main Area"),
    Entrance("Meadow Zone Main Area - Magma Drifblim Fast Travel", "Meadow Zone Main Area"),
    Entrance("Meadow Zone Main Area - Haunted Drifblim Fast Travel", "Meadow Zone Main Area"),
    Entrance("Meadow Zone Main Area - Granite Drifblim Fast Travel", "Meadow Zone Main Area"),
    Entrance("Meadow Zone Main Area - Flower Drifblim Fast Travel", "Meadow Zone Main Area"),

    # Beach Zone

    Entrance("Beach Zone Main Area - Ice Drifblim Fast Travel", "Beach Zone Main Area"),
    Entrance("Beach Zone Main Area - Cavern Drifblim Fast Travel", "Beach Zone Main Area"),
    Entrance("Beach Zone Main Area - Magma Drifblim Fast Travel", "Beach Zone Main Area"),
    Entrance("Beach Zone Main Area - Haunted Drifblim Fast Travel", "Beach Zone Main Area"),
    Entrance("Beach Zone Main Area - Granite Drifblim Fast Travel", "Beach Zone Main Area"),
    Entrance("Beach Zone Main Area - Flower Drifblim Fast Travel", "Beach Zone Main Area"),

    # Ice Zone

    Entrance("Ice Zone Main Area - Cavern Drifblim Fast Travel", "Ice Zone Main Area"),
    Entrance("Ice Zone Main Area - Magma Drifblim Fast Travel", "Ice Zone Main Area"),
    Entrance("Ice Zone Main Area - Haunted Drifblim Fast Travel", "Ice Zone Main Area"),
    Entrance("Ice Zone Main Area - Granite Drifblim Fast Travel", "Ice Zone Main Area"),
    Entrance("Ice Zone Main Area - Flower Drifblim Fast Travel", "Ice Zone Main Area"),

    # Cavern Zone

    Entrance("Cavern Zone Main Area - Magma Drifblim Fast Travel", "Cavern Zone Main Area"),
    Entrance("Cavern Zone Main Area - Haunted Drifblim Fast Travel", "Cavern Zone Main Area"),
    Entrance("Cavern Zone Main Area - Granite Drifblim Fast Travel", "Cavern Zone Main Area"),
    Entrance("Cavern Zone Main Area - Flower Drifblim Fast Travel", "Cavern Zone Main Area"),

    # Magma Zone

    Entrance("Magma Zone Main Area - Haunted Drifblim Fast Travel", "Magma Zone Main Area"),
    Entrance("Magma Zone Main Area - Granite Drifblim Fast Travel", "Magma Zone Main Area"),
    Entrance("Magma Zone Main Area - Flower Drifblim Fast Travel", "Magma Zone Main Area"),

    # Haunted Zone

    Entrance("Haunted Zone Main Area - Granite Drifblim Fast Travel", "Haunted Zone Main Area"),
    Entrance("Haunted Zone Main Area - Flower Drifblim Fast Travel", "Haunted Zone Main Area"),

    # Granite Zone

    Entrance("Granite Zone Main Area - Flower Drifblim Fast Travel", "Granite Zone Main Area"),

]

STATIC_ENTRANCES: list[Entrance] = [
    Entrance("Treehouse - Meadow Zone Gate", "Treehouse"),
    Entrance("Treehouse - Beach Zone Gate", "Treehouse"),
    Entrance("Treehouse - Cavern Zone Gate", "Treehouse"),
    Entrance("Treehouse - Haunted Zone Gate", "Treehouse"),
    Entrance("Treehouse - Granite Zone Gate", "Treehouse"),

    # Treehouse Fast Travel should be static, because Treehouse should always be reachable
    Entrance("Treehouse - Meadow Drifblim Fast Travel", "Treehouse"),
    Entrance("Treehouse - Beach Drifblim Fast Travel", "Treehouse"),
    Entrance("Treehouse - Ice Drifblim Fast Travel", "Treehouse"),
    Entrance("Treehouse - Cavern Drifblim Fast Travel", "Treehouse"),
    Entrance("Treehouse - Magma Drifblim Fast Travel", "Treehouse"),
    Entrance("Treehouse - Haunted Drifblim Fast Travel", "Treehouse"),
    Entrance("Treehouse - Granite Drifblim Fast Travel", "Treehouse"),
    Entrance("Treehouse - Flower Drifblim Fast Travel", "Treehouse"),

    # Beach Zone statics
    Entrance("Beach Zone Main Area - Recycle Bridge", "Beach Zone Main Area"),
    Entrance("Beach Zone Main Area - Middle Bridge", "Beach Zone Main Area"),
    Entrance("Beach Zone Main Area - Lapras Area Rock", "Beach Zone Main Area"),

    # Ice Zone statics
    Entrance("Ice Zone Main Area - Frozen Lake", "Ice Zone Main Area"),
    Entrance("Ice Zone Main Area - Upper Lift", "Ice Zone Main Area"),

    # Magma Zone statics
    Entrance("Magma Zone Main Area - Circle Area Fire Wall", "Magma Zone Main Area"),
    Entrance("Magma Zone Circle Area - Magcargo Area Bridge", "Magma Zone Circle Area"),

    # Haunted Zone statics
    Entrance("Haunted Zone Mansion Area - White Gem Door", "Haunted Zone Mansion Area"),
    Entrance("Haunted Zone Mansion Area - Red Gem Door", "Haunted Zone Mansion Area"),
    Entrance("Haunted Zone Mansion Area - Blue Gem Door", "Haunted Zone Mansion Area"),
    Entrance("Haunted Zone Mansion Area - Green Gem Door", "Haunted Zone Mansion Area"),
    Entrance("Haunted Zone Mansion Study Area - Hidden Bookshelf", "Haunted Zone Mansion Study Area"),

    # Skygarden
    Entrance("Treehouse - Piplup Skyballoon", "Treehouse"),

]

EACH_ZONE_ENTRANCES: list[Entrance] = [
    Entrance("Treehouse - Abra", "Treehouse"),
    Entrance("Haunted Zone Mansion Antic Area - Abra", "Haunted Zone Mansion Antic Area"),

    Entrance("Meadow Zone Main Area - Spearow", "Meadow Zone Main Area"),
    Entrance("Beach Zone Main Area - Spearow", "Beach Zone Main Area"),

    Entrance("Meadow Zone Main Area - Starly", "Meadow Zone Main Area"),
    Entrance("Beach Zone Main Area - Starly", "Beach Zone Main Area"),
    Entrance("Ice Zone Main Area - Starly", "Ice Zone Main Area"),

    Entrance("Meadow Zone Main Area - Bonsly", "Meadow Zone Main Area"),
    Entrance("Meadow Zone Main Area - Bonsly Unlocks", "Meadow Zone Main Area"),
    Entrance("Cavern Zone Main Area - Bonsly", "Cavern Zone Main Area"),
    Entrance("Cavern Zone Main Area - Bonsly Unlocks", "Cavern Zone Main Area"),
    Entrance("Magma Zone Main Area - Bonsly", "Magma Zone Main Area"),

    Entrance("Meadow Zone Main Area - Chimchar", "Meadow Zone Main Area"),
    Entrance("Cavern Zone Main Area - Chimchar", "Cavern Zone Main Area"),
    Entrance("Magma Zone Main Area - Chimchar", "Magma Zone Main Area"),

    Entrance("Meadow Zone Main Area - Sudowoodo", "Meadow Zone Main Area"),
    Entrance("Cavern Zone Main Area - Sudowoodo", "Cavern Zone Main Area"),

    Entrance("Meadow Zone Main Area - Aipom", "Meadow Zone Main Area"),
    Entrance("Meadow Zone Main Area - Aipom Unlocks", "Meadow Zone Main Area"),
    Entrance("Haunted Zone Main Area - Aipom", "Haunted Zone Main Area"),
    Entrance("Haunted Zone Main Area - Aipom Unlocks", "Haunted Zone Main Area"),

    Entrance("Meadow Zone Main Area - Ambipom", "Meadow Zone Main Area"),
    Entrance("Haunted Zone Main Area - Ambipom", "Haunted Zone Main Area"),

    Entrance("Beach Zone Main Area - Krabby", "Beach Zone Main Area"),
    Entrance("Ice Zone Main Area - Krabby", "Ice Zone Main Area"),

    Entrance("Beach Zone Main Area - Mudkip", "Beach Zone Main Area"),
    Entrance("Ice Zone Main Area - Mudkip", "Ice Zone Main Area"),

    Entrance("Beach Zone Main Area - Taillow", "Beach Zone Main Area"),
    Entrance("Ice Zone Main Area - Taillow", "Ice Zone Main Area"),
    Entrance("Granite Zone Main Area - Taillow", "Granite Zone Main Area"),

    Entrance("Beach Zone Main Area - Staravia", "Beach Zone Main Area"),
    Entrance("Ice Zone Main Area - Staravia", "Ice Zone Main Area"),

    Entrance("Beach Zone Main Area - Wingull", "Beach Zone Main Area"),
    Entrance("Ice Zone Lower Lift Area - Wingull", "Ice Zone Lower Lift Area"),

    Entrance("Beach Zone Main Area - Corphish", "Beach Zone Main Area"),
    Entrance("Ice Zone Lower Lift Area - Corphish", "Ice Zone Lower Lift Area"),

    Entrance("Ice Zone Main Area - Teddiursa", "Ice Zone Main Area"),
    Entrance("Cavern Zone Main Area - Teddiursa", "Cavern Zone Main Area"),
    Entrance("Flower Zone Main Area - Teddiursa", "Flower Zone Main Area"),

    Entrance("Cavern Zone Main Area - Aron", "Cavern Zone Main Area"),
    Entrance("Magma Zone Main Area - Aron", "Magma Zone Main Area"),

    Entrance("Cavern Zone Main Area - Torchic", "Cavern Zone Main Area"),
    Entrance("Magma Zone Main Area - Torchic", "Magma Zone Main Area"),

    Entrance("Cavern Zone Main Area - Geodude", "Cavern Zone Main Area"),
    Entrance("Magma Zone Main Area - Geodude", "Magma Zone Main Area"),

    Entrance("Cavern Zone Main Area - Raichu", "Cavern Zone Main Area"),
    Entrance("Haunted Zone Main Area - Raichu", "Haunted Zone Main Area"),

    Entrance("Cavern Zone Main Area - Meowth", "Cavern Zone Main Area"),
    Entrance("Haunted Zone Main Area - Meowth", "Haunted Zone Main Area"),

    Entrance("Cavern Zone Main Area - Marowak", "Cavern Zone Main Area"),
    Entrance("Granite Zone Main Area - Marowak", "Granite Zone Main Area"),

    Entrance("Magma Zone Main Area - Baltoy", "Magma Zone Main Area"),
    Entrance("Magma Zone Main Area - Baltoy Unlocks", "Magma Zone Main Area"),
    Entrance("Granite Zone Main Area - Baltoy", "Granite Zone Main Area"),
    Entrance("Granite Zone Main Area - Baltoy Unlocks", "Granite Zone Main Area"),

    Entrance("Magma Zone Circle Area - Meditite", "Magma Zone Circle Area"),
    Entrance("Flower Zone Main Area - Meditite", "Flower Zone Main Area"),

    Entrance("Magma Zone Main Area - Claydol", "Magma Zone Main Area"),
    Entrance("Granite Zone Main Area - Claydol", "Granite Zone Main Area"),

    Entrance("Granite Zone Main Area - Drifloon", "Granite Zone Main Area"),

    Entrance("Granite Zone Main Area - Furret", "Granite Zone Main Area"),
    Entrance("Flower Zone Main Area - Furret", "Flower Zone Main Area"),

    # Drifloon
    Entrance("Haunted Zone Main Area - Drifloon", "Haunted Zone Main Area"),
    Entrance("Haunted Zone Mansion Ballroom Area - Drifloon", "Haunted Zone Mansion Ballroom Area"),

    # Riolu
    Entrance("Haunted Zone Main Area - Riolu", "Haunted Zone Main Area"),
    Entrance("Haunted Zone Mansion Area - Riolu", "Haunted Zone Mansion Area"),
]

ATTRACTION_ENTRANCES: list[Entrance] = [
    Entrance("Meadow Zone Main Area - Bulbasaur Attraction", "Meadow Zone Main Area"),
    Entrance("Meadow Zone Venusaur Area - Venusaur Attraction", "Meadow Zone Venusaur Area"),
    Entrance("Beach Zone Main Area - Pelipper Attraction", "Beach Zone Main Area"),
    Entrance("Beach Zone Recycle Area - Gyarados Attraction", "Beach Zone Recycle Area"),
    Entrance("Ice Zone Empoleon Area - Empoleon Attraction", "Ice Zone Empoleon Area"),
    Entrance("Cavern Zone Main Area - Bastiodon Attraction", "Cavern Zone Main Area"),
    Entrance("Magma Zone Circle Area - Rhyperior Attraction", "Magma Zone Circle Area"),
    Entrance("Magma Zone Blaziken Area - Blaziken Attraction", "Magma Zone Blaziken Area"),
    Entrance("Haunted Zone Main Area - Tangrowth Attraction", "Haunted Zone Main Area"),
    Entrance("Haunted Zone Mansion Area - Dusknoir Attraction", "Haunted Zone Mansion Area"),
    Entrance("Haunted Zone Rotom Area - Rotom Attraction", "Haunted Zone Rotom Area"),
    Entrance("Granite Zone Main Area - Absol Attraction", "Granite Zone Main Area"),
    Entrance("Granite Zone Main Area - Salamence Attraction", "Granite Zone Main Area"),
    Entrance("Flower Zone Main Area - Rayquaza Attraction", "Flower Zone Main Area"),
]

GENERAL_EXITS: list[Exit] = [
    Exit("Pokepark Entrance - Meadow Zone Gate", "Pokepark Entrance"),

    Exit("Meadow Zone Venusaur Area - Meadow Zone Main Gate", "Meadow Zone Venusaur Area"),

    Exit("Ice Zone Main Area - Ice Zone Lapras", "Ice Zone Main Area"),
    Exit("Ice Zone Empoleon Area - Ice Zone Main Gate", "Ice Zone Empoleon Area"),

    Exit("Magma Zone Main Area - Cavern Zone Truck", "Magma Zone Main Area"),

    Exit("Magma Zone Blaziken Area - Main Area Gate", "Magma Zone Blaziken Area"),

    Exit("Haunted Zone Mansion Area - Main Area Gate", "Haunted Zone Mansion Area"),

    Exit("Haunted Zone Rotom Area - Bookshelf Area Connection", "Haunted Zone Rotom Area"),

    Exit("Flower Zone Main Area - Granite Zone Gate", "Flower Zone Main Area"),

]

TREEHOUSE_GATE_EXITS: list[Exit] = [
    Exit("Meadow Zone Main Area - Treehouse Connection", "Meadow Zone Main Area"),
    Exit("Beach Zone Main Area - Treehouse Connection", "Beach Zone Main Area"),
    Exit("Cavern Zone Main Area - Treehouse Connection", "Cavern Zone Main Area"),
    Exit("Haunted Zone Main Area - Treehouse Connection", "Haunted Zone Main Area"),
    Exit("Granite Zone Main Area - Treehouse Connection", "Granite Zone Main Area"),
]

FAST_TRAVEL_EXITS: list[Exit] = [

    # Beach Zone
    Exit("Beach Zone Main Area - Meadow Drifblim Fast Travel", "Beach Zone Main Area"),

    # Ice Zone
    Exit("Ice Zone Main Area - Meadow Drifblim Fast Travel", "Ice Zone Main Area"),
    Exit("Ice Zone Main Area - Beach Drifblim Fast Travel", "Ice Zone Main Area"),

    # Cavern Zone
    Exit("Cavern Zone Main Area - Meadow Drifblim Fast Travel", "Cavern Zone Main Area"),
    Exit("Cavern Zone Main Area - Beach Drifblim Fast Travel", "Cavern Zone Main Area"),
    Exit("Cavern Zone Main Area - Ice Drifblim Fast Travel", "Cavern Zone Main Area"),

    # Magma Zone
    Exit("Magma Zone Main Area - Meadow Drifblim Fast Travel", "Magma Zone Main Area"),
    Exit("Magma Zone Main Area - Beach Drifblim Fast Travel", "Magma Zone Main Area"),
    Exit("Magma Zone Main Area - Ice Drifblim Fast Travel", "Magma Zone Main Area"),
    Exit("Magma Zone Main Area - Cavern Drifblim Fast Travel", "Magma Zone Main Area"),

    # Haunted Zone
    Exit("Haunted Zone Main Area - Meadow Drifblim Fast Travel", "Haunted Zone Main Area"),
    Exit("Haunted Zone Main Area - Beach Drifblim Fast Travel", "Haunted Zone Main Area"),
    Exit("Haunted Zone Main Area - Ice Drifblim Fast Travel", "Haunted Zone Main Area"),
    Exit("Haunted Zone Main Area - Cavern Drifblim Fast Travel", "Haunted Zone Main Area"),
    Exit("Haunted Zone Main Area - Magma Drifblim Fast Travel", "Haunted Zone Main Area"),

    # Granite Zone
    Exit("Granite Zone Main Area - Meadow Drifblim Fast Travel", "Granite Zone Main Area"),
    Exit("Granite Zone Main Area - Beach Drifblim Fast Travel", "Granite Zone Main Area"),
    Exit("Granite Zone Main Area - Ice Drifblim Fast Travel", "Granite Zone Main Area"),
    Exit("Granite Zone Main Area - Cavern Drifblim Fast Travel", "Granite Zone Main Area"),
    Exit("Granite Zone Main Area - Magma Drifblim Fast Travel", "Granite Zone Main Area"),
    Exit("Granite Zone Main Area - Haunted Drifblim Fast Travel", "Granite Zone Main Area"),

    # Flower Zone
    Exit("Flower Zone Main Area - Meadow Drifblim Fast Travel", "Flower Zone Main Area"),
    Exit("Flower Zone Main Area - Beach Drifblim Fast Travel", "Flower Zone Main Area"),
    Exit("Flower Zone Main Area - Ice Drifblim Fast Travel", "Flower Zone Main Area"),
    Exit("Flower Zone Main Area - Cavern Drifblim Fast Travel", "Flower Zone Main Area"),
    Exit("Flower Zone Main Area - Magma Drifblim Fast Travel", "Flower Zone Main Area"),
    Exit("Flower Zone Main Area - Haunted Drifblim Fast Travel", "Flower Zone Main Area"),
    Exit("Flower Zone Main Area - Granite Drifblim Fast Travel", "Flower Zone Main Area"),

]

STATIC_EXITS: list[Exit] = [
    Exit("Treehouse Meadow Passage - Meadow Zone Gate", "Treehouse Meadow Passage"),
    Exit("Treehouse Beach Passage - Beach Zone Gate", "Treehouse Beach Passage"),
    Exit("Treehouse Cavern Passage - Cavern Zone Gate", "Treehouse Cavern Passage"),
    Exit("Treehouse Haunted Passage - Haunted Zone Gate", "Treehouse Haunted Passage"),
    Exit("Treehouse Granite Passage - Granite Zone Gate", "Treehouse Granite Passage"),

    # Treehouse travel should be always reachable
    Exit("Meadow Zone Main Area - Treehouse Drifblim Fast Travel", "Meadow Zone Main Area"),
    Exit("Beach Zone Main Area - Treehouse Drifblim Fast Travel", "Beach Zone Main Area"),
    Exit("Ice Zone Main Area - Treehouse Drifblim Fast Travel", "Ice Zone Main Area"),
    Exit("Cavern Zone Main Area - Treehouse Drifblim Fast Travel", "Cavern Zone Main Area"),
    Exit("Magma Zone Main Area - Treehouse Drifblim Fast Travel", "Magma Zone Main Area"),
    Exit("Haunted Zone Main Area - Treehouse Drifblim Fast Travel", "Haunted Zone Main Area"),
    Exit("Granite Zone Main Area - Treehouse Drifblim Fast Travel", "Granite Zone Main Area"),
    Exit("Flower Zone Main Area - Treehouse Drifblim Fast Travel", "Flower Zone Main Area"),

    # Beach Zone statics
    Exit("Beach Zone Recycle Area - Main Bridge", "Beach Zone Recycle Area"),
    Exit("Beach Zone Middle Isle - Main Bridge", "Beach Zone Middle Isle"),
    Exit("Beach Zone Lapras Area - Main Area Rock", "Beach Zone Lapras Area"),

    # Ice Zone statics
    Exit("Ice Zone Frozen Lake Area - Frozen Lake", "Ice Zone Frozen Lake Area"),
    Exit("Ice Zone Lower Lift Area - Lower Lift", "Ice Zone Lower Lift Area"),

    # Magma Zone statics
    Exit("Magma Zone Circle Area - Main Area Fire Wall", "Magma Zone Circle Area"),
    Exit("Magma Zone Magcargo Area - Main Area Bridge", "Magma Zone Magcargo Area"),

    # Haunted Zone statics
    Exit("Haunted Zone Mansion Ballroom Area - White Gem Door", "Haunted Zone Mansion Ballroom Area"),
    Exit("Haunted Zone Mansion Study Area - Red Gem Door", "Haunted Zone Mansion Study Area"),
    Exit("Haunted Zone Mansion Gengar Area - Blue Gem Door", "Haunted Zone Mansion Gengar Area"),
    Exit("Haunted Zone Mansion Antic Area - Green Gem Door", "Haunted Zone Mansion Antic Area"),
    Exit("Haunted Zone Bookshelf Area - Hidden Bookshelf", "Haunted Zone Bookshelf Area"),

    # Skygarden
    Exit("Skygarden - Piplup Skyballoon", "Skygarden"),


]

ATTRACTION_EXITS: list[Exit] = [
    Exit("Bulbasaur's Daring Dash Attraction - Attraction Menu", "Bulbasaur's Daring Dash Attraction"),
    Exit("Venusaur's Vine Swing Attraction - Attraction Menu", "Venusaur's Vine Swing Attraction"),
    Exit("Pelipper's Circle Circuit Attraction - Attraction Menu", "Pelipper's Circle Circuit Attraction"),
    Exit("Gyarados' Aqua Dash Attraction - Attraction Menu", "Gyarados' Aqua Dash Attraction"),
    Exit("Empoleon's Snow Slide Attraction - Attraction Menu", "Empoleon's Snow Slide Attraction"),
    Exit("Bastiodon's Panel Crush Attraction - Attraction Menu", "Bastiodon's Panel Crush Attraction"),
    Exit("Rhyperior's Bumper Burn Attraction - Attraction Menu", "Rhyperior's Bumper Burn Attraction"),
    Exit("Blaziken's Boulder Bash Attraction - Attraction Menu", "Blaziken's Boulder Bash Attraction"),
    Exit("Tangrowth's Swing-Along Attraction - Attraction Menu", "Tangrowth's Swing-Along Attraction"),
    Exit("Dusknoir's Speed Slam Attraction - Attraction Menu", "Dusknoir's Speed Slam Attraction"),
    Exit("Rotom's Spooky Shoot-'em-Up Attraction - Attraction Menu", "Rotom's Spooky Shoot-'em-Up Attraction"),
    Exit("Absol's Hurdle Bounce Attraction - Attraction Menu", "Absol's Hurdle Bounce Attraction"),
    Exit("Salamence's Sky Race Attraction - Attraction Menu", "Salamence's Sky Race Attraction"),
    Exit("Rayquaza's Balloon Panic Attraction - Attraction Menu", "Rayquaza's Balloon Panic Attraction"),
]

EACH_ZONE_EXITS: list[Exit] = [
    Exit("Treehouse Abra - Friendship", "Abra"),
    Exit("Haunted Abra - Friendship", "Abra"),

    Exit("Meadow Spearow - Battle Power Competition -- Friendship", "Spearow"),
    Exit("Beach Spearow - Battle Power Competition -- Friendship", "Spearow"),

    Exit("Meadow Starly - Chase Power Competition -- Friendship", "Starly"),
    Exit("Beach Starly - Chase Power Competition -- Friendship", "Starly"),
    Exit("Ice Starly - Chase Power Competition -- Friendship", "Starly"),

    Exit("Meadow Bonsly - Hide and Seek Power Competition -- Friendship", "Bonsly"),
    Exit("Meadow Bonsly - Hide and Seek Power Competition -- Unlocks", "Bonsly Unlocks"),
    Exit("Cavern Bonsly - Hide and Seek Power Competition -- Friendship", "Bonsly"),
    Exit("Cavern Bonsly - Hide and Seek Power Competition -- Unlocks", "Bonsly Unlocks"),
    Exit("Magma Bonsly - Hide and Seek Power Competition -- Friendship", "Bonsly"),

    Exit("Meadow Chimchar - Battle Power Competition -- Friendship", "Chimchar"),
    Exit("Cavern Chimchar - Battle Power Competition -- Friendship", "Chimchar"),
    Exit("Magma Chimchar - Battle Power Competition -- Friendship", "Chimchar"),

    Exit("Meadow Sudowoodo - Hide and Seek Power Competition -- Friendship", "Sudowoodo"),
    Exit("Cavern Sudowoodo - Hide and Seek Power Competition -- Friendship", "Sudowoodo"),

    Exit("Meadow Aipom - Chase Power Competition -- Friendship", "Aipom"),
    Exit("Meadow Aipom - Chase Power Competition -- Unlocks", "Aipom Unlocks"),
    Exit("Haunted Aipom - Chase Power Competition -- Friendship", "Aipom"),
    Exit("Haunted Aipom - Chase Power Competition -- Unlocks", "Aipom Unlocks"),

    Exit("Meadow Ambipom - Battle Power Competition -- Friendship", "Ambipom"),
    Exit("Haunted Ambipom - Battle Power Competition -- Friendship", "Ambipom"),

    Exit("Beach Krabby - Chase Power Competition -- Friendship", "Krabby"),
    Exit("Ice Krabby - Chase Power Competition -- Friendship", "Krabby"),

    Exit("Beach Mudkip - Hide and Seek Power Competition -- Friendship", "Mudkip"),
    Exit("Ice Mudkip - Hide and Seek Power Competition -- Friendship", "Mudkip"),

    Exit("Beach Taillow - Chase Power Competition -- Friendship", "Taillow"),
    Exit("Ice Taillow - Chase Power Competition -- Friendship", "Taillow"),
    Exit("Granite Taillow - Chase Power Competition -- Friendship", "Taillow"),

    Exit("Beach Staravia - Battle Power Competition -- Friendship", "Staravia"),
    Exit("Ice Staravia - Battle Power Competition -- Friendship", "Staravia"),

    Exit("Beach Wingull - Chase Power Competition -- Friendship", "Wingull"),
    Exit("Ice Wingull - Chase Power Competition -- Friendship", "Wingull"),

    Exit("Beach Corphish - Battle Power Competition -- Friendship", "Corphish"),
    Exit("Ice Corphish - Battle Power Competition -- Friendship", "Corphish"),

    Exit("Ice Teddiursa - Chase Power Competition -- Friendship", "Teddiursa"),
    Exit("Cavern Teddiursa - Quiz Power Competition -- Friendship", "Teddiursa"),
    Exit("Flower Teddiursa - Chase Power Competition -- Friendship", "Teddiursa"),

    Exit("Cavern Aron - Errand -- Friendship", "Aron"),
    Exit("Magma Aron - Errand -- Friendship", "Aron"),

    Exit("Cavern Torchic - Battle Power Competition -- Friendship", "Torchic"),
    Exit("Magma Torchic - Battle Power Competition -- Friendship", "Torchic"),

    Exit("Cavern Geodude - Hide and Seek Power Competition -- Friendship", "Geodude"),
    Exit("Magma Geodude - Hide and Seek Power Competition -- Friendship", "Geodude"),

    Exit("Cavern Raichu - Chase Power Competition -- Friendship", "Raichu"),
    Exit("Haunted Raichu - Chase Power Competition -- Friendship", "Raichu"),

    Exit("Cavern Meowth - Quiz Power Competition -- Friendship", "Meowth"),
    Exit("Haunted Meowth - Quiz Power Competition -- Friendship", "Meowth"),

    Exit("Cavern Marowak - Battle Power Competition -- Friendship", "Marowak"),
    Exit("Granite Marowak - Battle Power Competition -- Friendship", "Marowak"),

    Exit("Magma Baltoy - Battle Power Competition -- Friendship", "Baltoy"),
    Exit("Magma Baltoy - Battle Power Competition -- Unlocks", "Baltoy Unlocks"),
    Exit("Granite Baltoy - Battle Power Competition -- Friendship", "Baltoy"),
    Exit("Granite Baltoy - Battle Power Competition -- Unlocks", "Baltoy Unlocks"),

    Exit("Magma Meditite - Quiz Power Competition -- Friendship", "Meditite"),
    Exit("Flower Meditite - Quiz Power Competition -- Friendship", "Meditite"),

    Exit("Magma Claydol - Battle Power Competition -- Friendship", "Claydol"),
    Exit("Granite Claydol - Battle Power Competition -- Friendship", "Claydol"),

    Exit("Granite Drifloon - Friendship", "Drifloon"),

    Exit("Granite Furret - Hide and Seek Power Competition -- Friendship", "Furret"),
    Exit("Flower Furret - Hide and Seek Power Competition -- Friendship", "Furret"),

    # additional
    Exit("Haunted Drifloon - Friendship", "Drifloon"),
    Exit("Mansion Drifloon - Friendship", "Drifloon"),

    Exit("Haunted Riolu - Battle Power Competition", "Riolu"),
    Exit("Mansion Riolu - Battle Power Competition", "Riolu"),
]

ALL_ENTRANCES: list[Entrance] = (
        GENERAL_ENTRANCES
        + ATTRACTION_ENTRANCES
        + STATIC_ENTRANCES
        + FAST_TRAVEL_ENTRANCES
        + TREEHOUSE_GATE_ENTRANCES
        + EACH_ZONE_ENTRANCES
)

ALL_EXITS: list[Exit] = (
        GENERAL_EXITS
        + ATTRACTION_EXITS
        + STATIC_EXITS
        + FAST_TRAVEL_EXITS
        + TREEHOUSE_GATE_EXITS
        + EACH_ZONE_EXITS
)

VANILLA_ENTRANCE_TO_EXIT: dict[str, str] = {
    # Pokepark Entrance <-> Meadow Zone
    "Meadow Zone Main Area - Pokepark Entrance Gate": "Pokepark Entrance - Meadow Zone Gate",
    # Meadow Zone Main <-> Venusaur
    "Meadow Zone Main Area - Venusaur Gate": "Meadow Zone Venusaur Area - Meadow Zone Main Gate",

    # Meadow Attractions
    "Meadow Zone Main Area - Bulbasaur Attraction": "Bulbasaur's Daring Dash Attraction - Attraction Menu",
    "Meadow Zone Venusaur Area - Venusaur Attraction": "Venusaur's Vine Swing Attraction - Attraction Menu",

    # Treehouse
    "Treehouse Meadow Passage - Meadow Zone Connection": "Meadow Zone Main Area - Treehouse Connection",
    "Treehouse Beach Passage - Beach Zone Connection": "Beach Zone Main Area - Treehouse Connection",
    "Treehouse Cavern Passage - Cavern Zone Connection": "Cavern Zone Main Area - Treehouse Connection",
    "Treehouse Haunted Passage - Haunted Zone Connection": "Haunted Zone Main Area - Treehouse Connection",
    "Treehouse Granite Passage - Granite Zone Connection": "Granite Zone Main Area - Treehouse Connection",

    "Treehouse - Meadow Zone Gate": "Treehouse Meadow Passage - Meadow Zone Gate",
    "Treehouse - Beach Zone Gate": "Treehouse Beach Passage - Beach Zone Gate",
    "Treehouse - Cavern Zone Gate": "Treehouse Cavern Passage - Cavern Zone Gate",
    "Treehouse - Haunted Zone Gate": "Treehouse Haunted Passage - Haunted Zone Gate",
    "Treehouse - Granite Zone Gate": "Treehouse Granite Passage - Granite Zone Gate",

    # Beach Zone
    "Beach Zone Main Area - Recycle Bridge": "Beach Zone Recycle Area - Main Bridge",
    "Beach Zone Main Area - Middle Bridge": "Beach Zone Middle Isle - Main Bridge",
    "Beach Zone Main Area - Lapras Area Rock": "Beach Zone Lapras Area - Main Area Rock",

    # Beach Attractions
    "Beach Zone Main Area - Pelipper Attraction": "Pelipper's Circle Circuit Attraction - Attraction Menu",
    "Beach Zone Recycle Area - Gyarados Attraction": "Gyarados' Aqua Dash Attraction - Attraction Menu",

    # Ice Zone
    "Beach Zone Lapras Area - Beach Zone Lapras": "Ice Zone Main Area - Ice Zone Lapras",
    "Ice Zone Main Area - Empoleon Gate": "Ice Zone Empoleon Area - Ice Zone Main Gate",

    "Ice Zone Main Area - Frozen Lake": "Ice Zone Frozen Lake Area - Frozen Lake",
    "Ice Zone Main Area - Upper Lift": "Ice Zone Lower Lift Area - Lower Lift",

    # Ice Zone Attractions
    "Ice Zone Empoleon Area - Empoleon Attraction": "Empoleon's Snow Slide Attraction - Attraction Menu",

    # Cavern Zone Attractions
    "Cavern Zone Main Area - Bastiodon Attraction": "Bastiodon's Panel Crush Attraction - Attraction Menu",

    # Magma Zone
    "Cavern Zone Main Area - Magma Zone Truck": "Magma Zone Main Area - Cavern Zone Truck",

    "Magma Zone Main Area - Circle Area Fire Wall": "Magma Zone Circle Area - Main Area Fire Wall",
    "Magma Zone Circle Area - Magcargo Area Bridge": "Magma Zone Magcargo Area - Main Area Bridge",

    "Magma Zone Magcargo Area - Blaziken Gate": "Magma Zone Blaziken Area - Main Area Gate",

    # Magma Zone Attractions
    "Magma Zone Circle Area - Rhyperior Attraction": "Rhyperior's Bumper Burn Attraction - Attraction Menu",
    "Magma Zone Blaziken Area - Blaziken Attraction": "Blaziken's Boulder Bash Attraction - Attraction Menu",

    # Haunted Zone
    "Haunted Zone Main Area - Mansion Gate": "Haunted Zone Mansion Area - Main Area Gate",

    "Haunted Zone Mansion Area - White Gem Door": "Haunted Zone Mansion Ballroom Area - White Gem Door",
    "Haunted Zone Mansion Area - Red Gem Door": "Haunted Zone Mansion Study Area - Red Gem Door",
    "Haunted Zone Mansion Area - Blue Gem Door": "Haunted Zone Mansion Gengar Area - Blue Gem Door",
    "Haunted Zone Mansion Area - Green Gem Door": "Haunted Zone Mansion Antic Area - Green Gem Door",
    "Haunted Zone Mansion Study Area - Hidden Bookshelf": "Haunted Zone Bookshelf Area - Hidden Bookshelf",
    "Haunted Zone Bookshelf Area - Rotom Connection": "Haunted Zone Rotom Area - Bookshelf Area Connection",

    # Haunted Zone Attractions
    "Haunted Zone Main Area - Tangrowth Attraction": "Tangrowth's Swing-Along Attraction - Attraction Menu",
    "Haunted Zone Mansion Area - Dusknoir Attraction": "Dusknoir's Speed Slam Attraction - Attraction Menu",
    "Haunted Zone Rotom Area - Rotom Attraction": "Rotom's Spooky Shoot-'em-Up Attraction - Attraction Menu",

    # Granite Zone Attractions
    "Granite Zone Main Area - Absol Attraction": "Absol's Hurdle Bounce Attraction - Attraction Menu",
    "Granite Zone Main Area - Salamence Attraction": "Salamence's Sky Race Attraction - Attraction Menu",

    # Flower Zone
    "Granite Zone Main Area - Flower Zone Gate": "Flower Zone Main Area - Granite Zone Gate",

    # Flower Zone Attractions
    "Flower Zone Main Area - Rayquaza Attraction": "Rayquaza's Balloon Panic Attraction - Attraction Menu",

    # Skygarden
    "Treehouse - Piplup Skyballoon": "Skygarden - Piplup Skyballoon",

    # Multi area pokemon
    "Haunted Zone Main Area - Drifloon": "Haunted Drifloon - Friendship",
    "Haunted Zone Mansion Ballroom Area - Drifloon": "Mansion Drifloon - Friendship",

    "Haunted Zone Main Area - Riolu": "Haunted Riolu - Battle Power Competition",
    "Haunted Zone Mansion Area - Riolu": "Mansion Riolu - Battle Power Competition",

    # Fast Travel
    # Fast Travel Treehouse
    "Treehouse - Meadow Drifblim Fast Travel": "Meadow Zone Main Area - Treehouse Drifblim Fast Travel",
    "Treehouse - Beach Drifblim Fast Travel": "Beach Zone Main Area - Treehouse Drifblim Fast Travel",
    "Treehouse - Ice Drifblim Fast Travel": "Ice Zone Main Area - Treehouse Drifblim Fast Travel",
    "Treehouse - Cavern Drifblim Fast Travel": "Cavern Zone Main Area - Treehouse Drifblim Fast Travel",
    "Treehouse - Magma Drifblim Fast Travel": "Magma Zone Main Area - Treehouse Drifblim Fast Travel",
    "Treehouse - Haunted Drifblim Fast Travel": "Haunted Zone Main Area - Treehouse Drifblim Fast Travel",
    "Treehouse - Granite Drifblim Fast Travel": "Granite Zone Main Area - Treehouse Drifblim Fast Travel",
    "Treehouse - Flower Drifblim Fast Travel": "Flower Zone Main Area - Treehouse Drifblim Fast Travel",

    # Fast Travel Meadow
    "Meadow Zone Main Area - Beach Drifblim Fast Travel": "Beach Zone Main Area - Meadow Drifblim Fast Travel",
    "Meadow Zone Main Area - Ice Drifblim Fast Travel": "Ice Zone Main Area - Meadow Drifblim Fast Travel",
    "Meadow Zone Main Area - Cavern Drifblim Fast Travel": "Cavern Zone Main Area - Meadow Drifblim Fast Travel",
    "Meadow Zone Main Area - Magma Drifblim Fast Travel": "Magma Zone Main Area - Meadow Drifblim Fast Travel",
    "Meadow Zone Main Area - Haunted Drifblim Fast Travel": "Haunted Zone Main Area - Meadow Drifblim Fast Travel",
    "Meadow Zone Main Area - Granite Drifblim Fast Travel": "Granite Zone Main Area - Meadow Drifblim Fast Travel",
    "Meadow Zone Main Area - Flower Drifblim Fast Travel": "Flower Zone Main Area - Meadow Drifblim Fast Travel",

    # Fast Travel Beach

    "Beach Zone Main Area - Ice Drifblim Fast Travel": "Ice Zone Main Area - Beach Drifblim Fast Travel",
    "Beach Zone Main Area - Cavern Drifblim Fast Travel": "Cavern Zone Main Area - Beach Drifblim Fast Travel",
    "Beach Zone Main Area - Magma Drifblim Fast Travel": "Magma Zone Main Area - Beach Drifblim Fast Travel",
    "Beach Zone Main Area - Haunted Drifblim Fast Travel": "Haunted Zone Main Area - Beach Drifblim Fast Travel",
    "Beach Zone Main Area - Granite Drifblim Fast Travel": "Granite Zone Main Area - Beach Drifblim Fast Travel",
    "Beach Zone Main Area - Flower Drifblim Fast Travel": "Flower Zone Main Area - Beach Drifblim Fast Travel",

    # Fast Travel Ice

    "Ice Zone Main Area - Cavern Drifblim Fast Travel": "Cavern Zone Main Area - Ice Drifblim Fast Travel",
    "Ice Zone Main Area - Magma Drifblim Fast Travel": "Magma Zone Main Area - Ice Drifblim Fast Travel",
    "Ice Zone Main Area - Haunted Drifblim Fast Travel": "Haunted Zone Main Area - Ice Drifblim Fast Travel",
    "Ice Zone Main Area - Granite Drifblim Fast Travel": "Granite Zone Main Area - Ice Drifblim Fast Travel",
    "Ice Zone Main Area - Flower Drifblim Fast Travel": "Flower Zone Main Area - Ice Drifblim Fast Travel",

    # Fast Travel Cavern

    "Cavern Zone Main Area - Magma Drifblim Fast Travel": "Magma Zone Main Area - Cavern Drifblim Fast Travel",
    "Cavern Zone Main Area - Haunted Drifblim Fast Travel": "Haunted Zone Main Area - Cavern Drifblim Fast Travel",
    "Cavern Zone Main Area - Granite Drifblim Fast Travel": "Granite Zone Main Area - Cavern Drifblim Fast Travel",
    "Cavern Zone Main Area - Flower Drifblim Fast Travel": "Flower Zone Main Area - Cavern Drifblim Fast Travel",

    # Fast Travel Magma

    "Magma Zone Main Area - Haunted Drifblim Fast Travel": "Haunted Zone Main Area - Magma Drifblim Fast Travel",
    "Magma Zone Main Area - Granite Drifblim Fast Travel": "Granite Zone Main Area - Magma Drifblim Fast Travel",
    "Magma Zone Main Area - Flower Drifblim Fast Travel": "Flower Zone Main Area - Magma Drifblim Fast Travel",

    # Fast Travel Haunted

    "Haunted Zone Main Area - Granite Drifblim Fast Travel": "Granite Zone Main Area - Haunted Drifblim Fast Travel",
    "Haunted Zone Main Area - Flower Drifblim Fast Travel": "Flower Zone Main Area - Haunted Drifblim Fast Travel",

    # Fast Travel Granite

    "Granite Zone Main Area - Flower Drifblim Fast Travel": "Flower Zone Main Area - Granite Drifblim Fast Travel",

    # Each Zone
    "Treehouse - Abra": "Treehouse Abra - Friendship",
    "Haunted Zone Mansion Antic Area - Abra": "Haunted Abra - Friendship",

    "Meadow Zone Main Area - Spearow": "Meadow Spearow - Battle Power Competition -- Friendship",
    "Beach Zone Main Area - Spearow": "Beach Spearow - Battle Power Competition -- Friendship",

    "Meadow Zone Main Area - Starly": "Meadow Starly - Chase Power Competition -- Friendship",
    "Beach Zone Main Area - Starly": "Beach Starly - Chase Power Competition -- Friendship",
    "Ice Zone Main Area - Starly": "Ice Starly - Chase Power Competition -- Friendship",

    "Meadow Zone Main Area - Bonsly": "Meadow Bonsly - Hide and Seek Power Competition -- Friendship",
    "Meadow Zone Main Area - Bonsly Unlocks": "Meadow Bonsly - Hide and Seek Power Competition -- Unlocks",
    "Cavern Zone Main Area - Bonsly": "Cavern Bonsly - Hide and Seek Power Competition -- Friendship",
    "Cavern Zone Main Area - Bonsly Unlocks": "Cavern Bonsly - Hide and Seek Power Competition -- Unlocks",
    "Magma Zone Main Area - Bonsly": "Magma Bonsly - Hide and Seek Power Competition -- Friendship",

    "Meadow Zone Main Area - Chimchar": "Meadow Chimchar - Battle Power Competition -- Friendship",
    "Cavern Zone Main Area - Chimchar": "Cavern Chimchar - Battle Power Competition -- Friendship",
    "Magma Zone Main Area - Chimchar": "Magma Chimchar - Battle Power Competition -- Friendship",

    "Meadow Zone Main Area - Sudowoodo": "Meadow Sudowoodo - Hide and Seek Power Competition -- Friendship",
    "Cavern Zone Main Area - Sudowoodo": "Cavern Sudowoodo - Hide and Seek Power Competition -- Friendship",

    "Meadow Zone Main Area - Aipom": "Meadow Aipom - Chase Power Competition -- Friendship",
    "Meadow Zone Main Area - Aipom Unlocks": "Meadow Aipom - Chase Power Competition -- Unlocks",
    "Haunted Zone Main Area - Aipom": "Haunted Aipom - Chase Power Competition -- Friendship",
    "Haunted Zone Main Area - Aipom Unlocks": "Haunted Aipom - Chase Power Competition -- Unlocks",

    "Meadow Zone Main Area - Ambipom": "Meadow Ambipom - Battle Power Competition -- Friendship",
    "Haunted Zone Main Area - Ambipom": "Haunted Ambipom - Battle Power Competition -- Friendship",

    "Beach Zone Main Area - Krabby": "Beach Krabby - Chase Power Competition -- Friendship",
    "Ice Zone Main Area - Krabby": "Ice Krabby - Chase Power Competition -- Friendship",

    "Beach Zone Main Area - Mudkip": "Beach Mudkip - Hide and Seek Power Competition -- Friendship",
    "Ice Zone Main Area - Mudkip": "Ice Mudkip - Hide and Seek Power Competition -- Friendship",

    "Beach Zone Main Area - Taillow": "Beach Taillow - Chase Power Competition -- Friendship",
    "Ice Zone Main Area - Taillow": "Ice Taillow - Chase Power Competition -- Friendship",
    "Granite Zone Main Area - Taillow": "Granite Taillow - Chase Power Competition -- Friendship",

    "Beach Zone Main Area - Staravia": "Beach Staravia - Battle Power Competition -- Friendship",
    "Ice Zone Main Area - Staravia": "Ice Staravia - Battle Power Competition -- Friendship",

    "Beach Zone Main Area - Wingull": "Beach Wingull - Chase Power Competition -- Friendship",
    "Ice Zone Lower Lift Area - Wingull": "Ice Wingull - Chase Power Competition -- Friendship",

    "Beach Zone Main Area - Corphish": "Beach Corphish - Battle Power Competition -- Friendship",
    "Ice Zone Lower Lift Area - Corphish": "Ice Corphish - Battle Power Competition -- Friendship",

    "Ice Zone Main Area - Teddiursa": "Ice Teddiursa - Chase Power Competition -- Friendship",
    "Cavern Zone Main Area - Teddiursa": "Cavern Teddiursa - Quiz Power Competition -- Friendship",
    "Flower Zone Main Area - Teddiursa": "Flower Teddiursa - Chase Power Competition -- Friendship",

    "Cavern Zone Main Area - Aron": "Cavern Aron - Errand -- Friendship",
    "Magma Zone Main Area - Aron": "Magma Aron - Errand -- Friendship",

    "Cavern Zone Main Area - Torchic": "Cavern Torchic - Battle Power Competition -- Friendship",
    "Magma Zone Main Area - Torchic": "Magma Torchic - Battle Power Competition -- Friendship",

    "Cavern Zone Main Area - Geodude": "Cavern Geodude - Hide and Seek Power Competition -- Friendship",
    "Magma Zone Main Area - Geodude": "Magma Geodude - Hide and Seek Power Competition -- Friendship",

    "Cavern Zone Main Area - Raichu": "Cavern Raichu - Chase Power Competition -- Friendship",
    "Haunted Zone Main Area - Raichu": "Haunted Raichu - Chase Power Competition -- Friendship",

    "Cavern Zone Main Area - Meowth": "Cavern Meowth - Quiz Power Competition -- Friendship",
    "Haunted Zone Main Area - Meowth": "Haunted Meowth - Quiz Power Competition -- Friendship",

    "Cavern Zone Main Area - Marowak": "Cavern Marowak - Battle Power Competition -- Friendship",
    "Granite Zone Main Area - Marowak": "Granite Marowak - Battle Power Competition -- Friendship",

    "Magma Zone Main Area - Baltoy": "Magma Baltoy - Battle Power Competition -- Friendship",
    "Magma Zone Main Area - Baltoy Unlocks": "Magma Baltoy - Battle Power Competition -- Unlocks",
    "Granite Zone Main Area - Baltoy": "Granite Baltoy - Battle Power Competition -- Friendship",
    "Granite Zone Main Area - Baltoy Unlocks": "Granite Baltoy - Battle Power Competition -- Unlocks",

    "Magma Zone Circle Area - Meditite": "Magma Meditite - Quiz Power Competition -- Friendship",
    "Flower Zone Main Area - Meditite": "Flower Meditite - Quiz Power Competition -- Friendship",

    "Magma Zone Main Area - Claydol": "Magma Claydol - Battle Power Competition -- Friendship",
    "Granite Zone Main Area - Claydol": "Granite Claydol - Battle Power Competition -- Friendship",

    "Granite Zone Main Area - Drifloon": "Granite Drifloon - Friendship",

    "Granite Zone Main Area - Furret": "Granite Furret - Hide and Seek Power Competition -- Friendship",
    "Flower Zone Main Area - Furret": "Flower Furret - Hide and Seek Power Competition -- Friendship",

}

ENTRANCES_BY_NAME = {e.name: e for e in ALL_ENTRANCES}
EXITS_BY_NAME = {e.name: e for e in ALL_EXITS}

class EntranceRandomizer:
    def __init__(self, world: "PokeparkWorld"):
        self.world = world
        self.multiworld = world.multiworld
        self.player = world.player
        self.entrances_rules: dict[str, Callable[[CollectionState], bool]] = {}
        self.entrance_to_exit: dict[Entrance, Exit] = {
        }
        self.final_entrance_to_exit: dict[Entrance, Exit] = {
        }
        for entrance_name, exit_name in VANILLA_ENTRANCE_TO_EXIT.items():
            self.entrance_to_exit[ENTRANCES_BY_NAME[entrance_name]] = EXITS_BY_NAME[exit_name]

    def get_one_entrance_set(self, attractions: bool = False, treehouse_gates: bool = False, fast_travel: bool =
    False, general_entrances: bool = False):
        relevant_entrances: list[Entrance] = []
        relevant_exits: list[Exit] = []
        if attractions:
            relevant_entrances += ATTRACTION_ENTRANCES
            relevant_exits += ATTRACTION_EXITS
        if treehouse_gates:
            relevant_entrances += TREEHOUSE_GATE_ENTRANCES
            relevant_exits += TREEHOUSE_GATE_EXITS
        if fast_travel:
            relevant_entrances += FAST_TRAVEL_ENTRANCES
            relevant_exits += FAST_TRAVEL_EXITS
        if general_entrances:
            relevant_entrances += GENERAL_ENTRANCES
            relevant_exits += GENERAL_EXITS
        return relevant_entrances, relevant_exits

    def get_randomizable_entrance_sets(self):
        options = self.world.options

        attractions = bool(options.randomize_attraction_entrances)
        mixed_pools = bool(options.mix_entrance_pools)
        treehouse_gates = bool(options.randomize_treehouse_gates_entrances)
        fast_travel = bool(options.randomize_fast_travel_entrances)
        general_entrances = bool(options.randomize_general_entrances)

        if attractions:
            yield self.get_one_entrance_set(attractions=attractions)
        if mixed_pools:
            yield self.get_one_entrance_set(
                general_entrances=general_entrances, fast_travel=fast_travel, treehouse_gates=treehouse_gates
            )
        else:
            if treehouse_gates:
                yield self.get_one_entrance_set(treehouse_gates=treehouse_gates)
            if fast_travel:
                yield self.get_one_entrance_set(fast_travel=fast_travel)
            if general_entrances:
                yield self.get_one_entrance_set(general_entrances=general_entrances)

    def randomize_set(self, relevant_entrances: list[Entrance], relevant_exits: list[Exit]):

        self.world.random.shuffle(relevant_exits)

        for entrance in relevant_entrances.copy():  # WIP TODO: real logic
            exit = self.world.random.sample(relevant_exits, 1).pop()
            self.entrance_to_exit[entrance] = exit
            relevant_exits.remove(exit)

    def add_bi_directional_entrance_to_exit(self):
        reverse_entrance_connections: dict[Entrance, Exit] = {}
        for entrance, exit in self.entrance_to_exit.items():
            # skip Pokemon Regions
            if entrance in EACH_ZONE_ENTRANCES:
                continue
            if exit in EACH_ZONE_EXITS:
                continue

            reverse_entrance = Entrance(
                name=exit.name,
                parent_region=exit.region_name
            )
            reverse_exit = Exit(
                name=entrance.name,
                region_name=entrance.parent_region
            )
            if reverse_entrance in self.entrance_to_exit:  # debugging stuff currently
                raise ValueError(f"Ambiguous Entrance/Exit naming: {reverse_entrance.name}")
            if reverse_entrance in reverse_entrance_connections:
                raise ValueError(f"Duplicate reverse entrance: {reverse_entrance.name}")

            reverse_entrance_connections[reverse_entrance] = reverse_exit

        self.final_entrance_to_exit = {
            **self.entrance_to_exit,
            **reverse_entrance_connections,
        }

    def randomize_entrances(self):
        self.entrances_rules = get_entrance_rules_dict(
            self.player,
            self.world.options
        )
        for relevant_entrances, relevant_exits in self.get_randomizable_entrance_sets():
            self.randomize_set(relevant_entrances, relevant_exits)
        self.add_bi_directional_entrance_to_exit()

        for entrance, exit in self.final_entrance_to_exit.items():
            entrance_name = f"{entrance.name} -> {exit.name}"
            self.multiworld.get_region(entrance.parent_region, self.player).connect(
                self.multiworld.get_region(
                    exit.region_name,
                    self.player
                ),
                entrance_name,
                self.entrances_rules[entrance.name]
            )

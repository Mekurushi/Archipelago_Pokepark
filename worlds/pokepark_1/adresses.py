from dataclasses import dataclass, field
from enum import Enum
from typing import List

from worlds.pokepark_1 import FRIENDSHIP_ITEMS, UNLOCK_ITEMS, BERRIES
from worlds.pokepark_1.LocationIds import MinigameLocationIds, OverworldPokemonLocationIds, QuestLocationIds
from worlds.pokepark_1.items import PRISM_ITEM, REGION_UNLOCK

pokemon_id_address = 0x8036dc20
stage_id_address = 0x8036AEF0  # word
is_in_menu_address = 0x80482F04
meadow_zone_stage_id = 0x13002E8
meadow_zone_loadscreen_stage_id = 0x12FFDFC
beach_zone_stage_id = 0x1591C24
beach_zone_loadscreen_stage_id = 0x15916FC
ice_zone_stage_id= 0x129D6A0
treehouse_stage_id = 0x13282F8
main_menu_stage_id = 0x6FC360
main_menu2_stage_id = 0x93BEA0
main_menu3_stage_id = 0x2A080
intro_stage_id = 0x940220
bulbasaur_minigame_stage_id = 0x98F584
venusaur_minigame_stage_id = 0xA81938
pelipper_minigame_stage_id = 0xD92358
gyarados_minigame_stage_id = 0xC61408
empoleon_minigame_stage_id = 0xBE6D00

LOADSCREEN_TO_ZONE = {
meadow_zone_loadscreen_stage_id:meadow_zone_stage_id,
beach_zone_loadscreen_stage_id: beach_zone_stage_id
}

class MemoryRange(Enum):
    BYTE = 1  # 1 Byte
    HALFWORD = 2  # 2 Bytes
    WORD = 4  # 4 Bytes

    @property
    def mask(self):
        if self == MemoryRange.WORD:
            return 0xFFFFFFFF
        elif self == MemoryRange.HALFWORD:
            return 0xFFFF
        else:  # BYTE
            return 0xFF


@dataclass
class MemoryAddress:
    base_address: int
    offset: int = 0
    memory_range: MemoryRange = MemoryRange.WORD
    value: int = 0

    @property
    def final_address(self):
        return self.base_address + self.offset


@dataclass
class UnlockItem:
    item: MemoryAddress  #
    itemId: int | None = None
    location: List[MemoryAddress] | None = None
    locationId: int | None = None
    is_blocked_until_location: bool = False
    blocked_zone:int = None


@dataclass
class PrismaItem:
    item: MemoryAddress
    location: MemoryAddress
    locationId: int
    itemId: int
    stage_id: int

@dataclass
class PokemonLocation:
    location: MemoryAddress
    zone_id: int
    pokemon_ids: List[int]
    locationId: int
    friendship_items_to_block: List[int] | None = None,
    unlock_items_to_block: List[int] | None = None
    is_special_exception: bool = False


@dataclass
class PokemonStateInfo:
    item: MemoryAddress
    locations: List[PokemonLocation] = field(default_factory=list)





@dataclass
class MinigameLocation:
    locationId: int
    location: MemoryAddress
    stage_id: int


@dataclass
class QuestLocation:
    locationId: int
    location: MemoryAddress
    check_mask: int


@dataclass
class ZoneGateUnlocks:
    item_ids: List[int]
    stage_id: int
    gate: MemoryAddress


@dataclass
class ZoneState:
    """Represents a specific zone unlock state"""
    item_id: int
    world_state_value: int
    addresses: List[MemoryAddress]
    fast_travel_flag: int


@dataclass
class ZoneSystem:
    """Complete zone system including world states and gates"""
    world_state_address: int
    fast_travel_address: int
    states: List[ZoneState]
    treehouse_gates: List[ZoneGateUnlocks]
    connected_zone_gates: List[ZoneGateUnlocks]


ZONESYSTEM = ZoneSystem(world_state_address=0x8037500D,
               fast_travel_address=0x8037502F,
               states=[
                   ZoneState(
                       item_id=REGION_UNLOCK["Meadow Zone Unlock"],
                       world_state_value=0x7c0,
                       addresses=[
                           MemoryAddress(  # unlock bidoof in beach zone
                               base_address=0x8037500F,
                               value=0b01100000,
                               memory_range=MemoryRange.BYTE),
                       ],
                       fast_travel_flag=0x80),
                   ZoneState(
                       item_id=REGION_UNLOCK["Beach Zone Unlock"],
                       world_state_value=0x870,
                       addresses=[
                           MemoryAddress( #unlock bidoof in beach zone
                               base_address=0x80376af0,
                               value=0b00001000,
                               memory_range=MemoryRange.BYTE),
                           MemoryAddress( # bidoof quest state on completed
                               base_address=0x80375026,
                               value=0b00000011,
                               memory_range=MemoryRange.BYTE
                           ),
                           MemoryAddress(  #activate all bridges in beach zone
                               base_address=0x80375010,
                               value=0b00111011,
                               memory_range=MemoryRange.BYTE
                           )
                       ],
                       fast_travel_flag=0x40),
                   ZoneState(
                       item_id=REGION_UNLOCK["Ice Zone Unlock"],
                       world_state_value=0xC1E,
                       addresses=[
                           MemoryAddress(
                               base_address=0x80375021, # lift
                               value=0b00001000,
                               memory_range=MemoryRange.BYTE
                           ),
                           MemoryAddress(
                               base_address=0x80375013, #gate and lake
                               value=0b00001100,
                               memory_range=MemoryRange.BYTE
                           ),
                           MemoryAddress(
                               base_address=0x80375031,  # skip first christmas tree quest step
                               value=0b00100000,
                               memory_range=MemoryRange.BYTE
                           ),
                       ],
                       fast_travel_flag=0x20),
               ],
               treehouse_gates=[
                   ZoneGateUnlocks(
                       stage_id=0x13282F8,
                       item_ids=[REGION_UNLOCK["Beach Zone Unlock"]],
                       gate=MemoryAddress(
                           base_address=0x80D53068,
                           memory_range=MemoryRange.WORD,
                           value=0x01
                       )
                   ),
                   ZoneGateUnlocks(
                       stage_id=0x13282F8,
                       item_ids=[REGION_UNLOCK["Meadow Zone Unlock"]],
                       gate=MemoryAddress(
                           base_address=0x80D52128,
                           memory_range=MemoryRange.WORD,
                           value=0x01
                       )
                   )
               ],
               connected_zone_gates=[ZoneGateUnlocks(
                   stage_id=0x13282F8,  # not used here
                   item_ids=[REGION_UNLOCK["Beach Zone Unlock"],REGION_UNLOCK["Ice Zone Unlock"]],
                   gate=MemoryAddress( # removes stone to lapras
                       base_address=0x80375012,
                       memory_range=MemoryRange.BYTE,
                       value=0b00010000)
               )])

QUEST_LOCATIONS = [
    # Meadow Zone
    #
    QuestLocation(
        locationId=QuestLocationIds.MEADOW_BIDOOF_HOUSING1.value,
        location=MemoryAddress(
            base_address=0x8037500F,
            memory_range=MemoryRange.BYTE,
            value=0b00000110),
        check_mask=0b00000110
    ),
    QuestLocation(
        locationId=QuestLocationIds.MEADOW_BIDOOF_HOUSING2.value,
        location=MemoryAddress(
            base_address=0x8037500F,
            memory_range=MemoryRange.BYTE,
            value=0b00001010),
        check_mask=0b00001010
    ),
    QuestLocation(
        locationId=QuestLocationIds.MEADOW_BIDOOF_HOUSING3.value,
        location=MemoryAddress(
            base_address=0x8037500F,
            memory_range=MemoryRange.BYTE,
            value=0b00001110),
        check_mask=0b00001110
    ),
    QuestLocation(
        locationId=QuestLocationIds.MEADOW_BIDOOF_HOUSING4.value,
        location=MemoryAddress(
            base_address=0x8037500F,
            memory_range=MemoryRange.BYTE,
            value=0b00010010),
        check_mask=0b00010010
    ),

    # Beach Zone
    #
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE1.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00010000),
        check_mask=0b00010000
    ),
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE2.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00100000),
        check_mask=0b00100000
    ),
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE3.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00110000),
        check_mask=0b00110000
    ),
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE4.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b01000000),
        check_mask=0b01000000
    ),
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE5.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b01010000),
        check_mask=0b01010000
    ),
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE6.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b01100000),
        check_mask=0b01100000
    ),

    QuestLocation(
        locationId=QuestLocationIds.IGLOO_QUEST1.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00000010),
        check_mask=0b00000010
    ),
    QuestLocation(
        locationId=QuestLocationIds.IGLOO_QUEST2.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00000100),
        check_mask=0b00000100
    ),
    QuestLocation(
        locationId=QuestLocationIds.IGLOO_QUEST3.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00000110),
        check_mask=0b00000110
    ),
    QuestLocation(
        locationId=QuestLocationIds.CHRISTMAS_TREE1.value,
        location=MemoryAddress(
            base_address=0x80375023,
            memory_range=MemoryRange.BYTE,
            value=0b00010110),
        check_mask=0b00010110
    ),
    QuestLocation(
        locationId=QuestLocationIds.CHRISTMAS_TREE2.value,
        location=MemoryAddress(
            base_address=0x80375023,
            memory_range=MemoryRange.BYTE,
            value=0b00100111),
        check_mask=0b00100111
    ),
    QuestLocation(
        locationId=QuestLocationIds.CHRISTMAS_TREE3.value,
        location=MemoryAddress(
            base_address=0x80375023,
            memory_range=MemoryRange.BYTE,
            value=0b00110111),
        check_mask=0b00110111
    ),
    QuestLocation(
        locationId=QuestLocationIds.CHRISTMAS_TREE4.value,
        location=MemoryAddress(
            base_address=0x80375023,
            memory_range=MemoryRange.BYTE,
            value=0b01001111),
        check_mask=0b01001111
    ),

    # Power up Quest Check
    QuestLocation(
        locationId=QuestLocationIds.THUNDERBOLT_POWERUP1.value,
        location=MemoryAddress(
            base_address=0x8037501C,
            memory_range=MemoryRange.BYTE,
            value=0b00000001),
        check_mask=0b00000001
    ),
    QuestLocation(
        locationId=QuestLocationIds.THUNDERBOLT_POWERUP2.value,
        location=MemoryAddress(
            base_address=0x8037501C,
            memory_range=MemoryRange.BYTE,
            value=0b00000010),
        check_mask=0b00000010
    ),
    QuestLocation(
        locationId=QuestLocationIds.THUNDERBOLT_POWERUP3.value,
        location=MemoryAddress(
            base_address=0x8037501C,
            memory_range=MemoryRange.BYTE,
            value=0b00000011),
        check_mask=0b00000011
    ),
    QuestLocation(
        locationId=QuestLocationIds.DASH_POWERUP1.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00010000),
        check_mask=0b00010000
    ),
    QuestLocation(
        locationId=QuestLocationIds.DASH_POWERUP2.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00100000),
        check_mask=0b00100000
    ),
    QuestLocation(
        locationId=QuestLocationIds.DASH_POWERUP3.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00110000),
        check_mask=0b00110000
    ),
    QuestLocation(
        locationId=QuestLocationIds.HEALTH_POWERUP1.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00000001),
        check_mask=0b00000001
    ),
    QuestLocation(
        locationId=QuestLocationIds.HEALTH_POWERUP2.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00000010),
        check_mask=0b00000010
    ),
    QuestLocation(
        locationId=QuestLocationIds.HEALTH_POWERUP3.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00000011),
        check_mask=0b00000011
    ),

    QuestLocation(
        locationId=QuestLocationIds.IRON_TAIL_POWERUP1.value,
        location=MemoryAddress(
            base_address=0x8037501E,
            memory_range=MemoryRange.BYTE,
            value=0b00010000),
        check_mask=0b00010000
    ),
    QuestLocation(
        locationId=QuestLocationIds.IRON_TAIL_POWERUP2.value,
        location=MemoryAddress(
            base_address=0x8037501E,
            memory_range=MemoryRange.BYTE,
            value=0b00100000),
        check_mask=0b00100000
    ),
    QuestLocation(
        locationId=QuestLocationIds.IRON_TAIL_POWERUP3.value,
        location=MemoryAddress(
            base_address=0x8037501E,
            memory_range=MemoryRange.BYTE,
            value=0b00110000),
        check_mask=0b00110000
    ),
]

MINIGAME_LOCATIONS = [
    # Meadow Zone - Bulbasaur's Daring Dash Minigame
    #
    MinigameLocation(
        MinigameLocationIds.PIKACHU_DASH.value,
        MemoryAddress(
            base_address=0x80377E30,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TURTWIG_DASH.value,
        MemoryAddress(
            base_address=0x80377EE4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MUNCHLAX_DASH.value,
        MemoryAddress(
            base_address=0x80377F20,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CHIMCHAR_DASH.value,
        MemoryAddress(
            base_address=0x80377EC0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TREECKO_DASH.value,
        MemoryAddress(
            base_address=0x80377ECC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BIBAREL_DASH.value,
        MemoryAddress(
            base_address=0x80377ED8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BULBASAUR_DASH.value,
        MemoryAddress(
            base_address=0x80377EF0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BIDOOF_DASH.value,
        MemoryAddress(
            base_address=0x80377EFC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.ODDISH_DASH.value,
        MemoryAddress(
            base_address=0x80377F08,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SHROOMISH_DASH.value,
        MemoryAddress(
            base_address=0x80377F14,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BONSLY_DASH.value,
        MemoryAddress(
            base_address=0x80377F2C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.LOTAD_DASH.value,
        MemoryAddress(
            base_address=0x80377F38,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.WEEDLE_DASH.value,
        MemoryAddress(
            base_address=0x80377F44,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CATERPIE_DASH.value,
        MemoryAddress(
            base_address=0x80377F50,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAGIKARP_DASH.value,
        MemoryAddress(
            base_address=0x80377F5C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.JOLTEON_DASH.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=bulbasaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.ARCANINE_DASH.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.LEAFEON_DASH.value,
        MemoryAddress(
            base_address=0x80377E60,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SCYTHER_DASH.value,
        MemoryAddress(
            base_address=0x80377e6c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.PONYTA_DASH.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SHINX_DASH.value,
        MemoryAddress(
            base_address=0x80377E84,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.EEVEE_DASH.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PACHIRISU_DASH.value,
        MemoryAddress(
            base_address=0x80377E9C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BUNEARY_DASH.value,
        MemoryAddress(
            base_address=0x80377EA8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CROAGUNK_DASH.value,
        MemoryAddress(
            base_address=0x80377EB4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),

    # Meadow Zone - Venusaur's Vine Swing Minigame
    #
    MinigameLocation(
        MinigameLocationIds.PIKACHU_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376DBC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MUNCHLAX_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e64,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAGIKARP_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e70,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.BLAZIKEN_VINE_SWING.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=venusaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.INFERNAPE_VINE_SWING.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=venusaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.LUCARIO_VINE_SWING.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
         MinigameLocationIds.PRIMEAPE_VINE_SWING.value,
         MemoryAddress(
             base_address=0x80376E04,
             memory_range=MemoryRange.HALFWORD,
             value=0x0001),
         stage_id=venusaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.TANGROWTH_VINE_SWING.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.AMBIPOM_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e10,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CROAGUNK_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e4c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MANKEY_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e1c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.AIPOM_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e28,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CHIMCHAR_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e34,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TREECKO_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e40,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PACHIRISU_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e58,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),

    # Beach Zone Pelipper's Circle Circuit
    #
    MinigameLocation(
        MinigameLocationIds.PIKACHU_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377380,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.STARAPTOR_CIRCLE.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=pelipper_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.TOGEKISS_CIRCLE.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=pelipper_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.HONCHKROW_CIRCLE.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=pelipper_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.GLISCOR_CIRCLE.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PELIPPER_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377338,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.STARAVIA_CIRCLE.value,
        MemoryAddress(
            base_address=0x803772FC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PIDGEOTTO_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377308,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BUTTERFREE_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377374,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TROPIUS_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377368,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.MURKROW_CIRCLE.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TAILLOW_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377320,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SPEAROW_CIRCLE.value,
        MemoryAddress(
            base_address=0x8037732C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.STARLY_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377344,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.WINGULL_CIRCLE.value,
        MemoryAddress(
            base_address=0x8037735c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),

    # Beach Zone Gyarados' Aqua Dash
    #
    MinigameLocation(
        MinigameLocationIds.PIKACHU_AQUA.value,
        MemoryAddress(
            base_address=0x80377218,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PSYDUCK_AQUA.value,
        MemoryAddress(
            base_address=0x80377224,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.AZURILL_AQUA.value,
        MemoryAddress(
            base_address=0x80377230,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SLOWPOKE_AQUA.value,
        MemoryAddress(
            base_address=0x8037723c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
         MinigameLocationIds.EMPOLEON_AQUA.value,
         MemoryAddress(
             base_address=0x80377194,
             memory_range=MemoryRange.HALFWORD,
             value=0x0001),
         stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.FLOATZEL_AQUA.value,
        MemoryAddress(
            base_address=0x803771a0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.FERALIGATR_AQUA.value,
        MemoryAddress(
            base_address=0x803771ac,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.GOLDUCK_AQUA.value,
        MemoryAddress(
            base_address=0x803771b8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.VAPOREON_AQUA.value,
        MemoryAddress(
            base_address=0x803771c4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.PRINPLUP_AQUA.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BIBAREL_AQUA.value,
        MemoryAddress(
            base_address=0x803771dc,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BUIZEL_AQUA.value,
        MemoryAddress(
            base_address=0x803771f4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CORSOLA_AQUA.value,
        MemoryAddress(
            base_address=0x803771e8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PIPLUP_AQUA.value,
        MemoryAddress(
            base_address=0x80377200,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.LOTAD_AQUA.value,
        MemoryAddress(
            base_address=0x8037720c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),

    # Ice Zone - Empoleon's Snow Slide
    MinigameLocation(
        MinigameLocationIds.PIKACHU_SLIDE.value,
        MemoryAddress(
            base_address=0x803775F0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TEDDIURSA_SLIDE.value,
        MemoryAddress(
            base_address=0x803775FC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PIPLUP_SLIDE.value,
        MemoryAddress(
            base_address=0x803775CC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.LAPRAS_SLIDE.value,
        MemoryAddress(
            base_address=0x80377590,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SPHEAL_SLIDE.value,
        MemoryAddress(
            base_address=0x803775D8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAGIKARP_SLIDE.value,
        MemoryAddress(
            base_address=0x80377608,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.GLACEON_SLIDE.value,
        MemoryAddress(
            base_address=0x8037756C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.GLALIE_SLIDE.value,
        MemoryAddress(
            base_address=0x80377584,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.DELIBIRD_SLIDE.value,
        MemoryAddress(
            base_address=0x803775A8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PILOSWINE_SLIDE.value,
        MemoryAddress(
            base_address=0x803775E4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PRINPLUP_SLIDE.value,
        MemoryAddress(
            base_address=0x8037759C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SQUIRTLE_SLIDE.value,
        MemoryAddress(
            base_address=0x803775C0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.QUAGSIRE_SLIDE.value,
        MemoryAddress(
            base_address=0x803775B4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.EMPOLEON_SLIDE.value,
        MemoryAddress(
            base_address=0x80377560,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),

]

blocked_friendship_itemIds = []
blocked_friendship_unlock_itemIds = []
POKEMON_STATES = {
    # Meadow Zone Pokemon
    #
    FRIENDSHIP_ITEMS["Chikorita"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375C74, memory_range=MemoryRange.BYTE, value=0x80),
    ),

    FRIENDSHIP_ITEMS["Pachirisu"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375210, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375210, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000031, 0x00000004],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Pachirisu"]],
                locationId=FRIENDSHIP_ITEMS["Pachirisu"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Bulbasaur"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375490, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375490, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Bulbasaur"]],
                locationId=FRIENDSHIP_ITEMS["Bulbasaur"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Munchlax"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037529C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037529C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000002f, 0x00000005],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Munchlax"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Tropius Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Munchlax"],
                is_special_exception=True
            )
        ]
),
    FRIENDSHIP_ITEMS["Tropius"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753DC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803753DC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000017],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Tropius"]],
                locationId=FRIENDSHIP_ITEMS["Tropius"],
                is_special_exception=True
            )
        ],
),
    FRIENDSHIP_ITEMS["Turtwig"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803751D4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803751D4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000002d, 0x00000002],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Turtwig"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Bonsly Unlock"], UNLOCK_ITEMS["Pachirisu Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Turtwig"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Bonsly"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803752C4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803752C4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Bonsly"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Sudowoodo Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Bonsly"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Sudowoodo"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803752D8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803752D8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Sudowoodo"]],
                locationId=FRIENDSHIP_ITEMS["Sudowoodo"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Buneary"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037533C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037533C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000003],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Buneary"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Lotad Unlock"], UNLOCK_ITEMS["Shinx Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Buneary"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Shinx"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753F0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803753F0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000010, 0x0000002c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Shinx"]],
                locationId=FRIENDSHIP_ITEMS["Shinx"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Mankey"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375314, memory_range=MemoryRange.BYTE, value=0x80),
    ),
    FRIENDSHIP_ITEMS["Spearow"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753C8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803753C8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000027, 0x00000013],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Spearow"]],
                locationId=FRIENDSHIP_ITEMS["Spearow"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Croagunk"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037547C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037547C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Croagunk"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Scyther Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Croagunk"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Chatot"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80376034, memory_range=MemoryRange.BYTE, value=0x80),
    ),
    FRIENDSHIP_ITEMS["Lotad"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375224, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375224, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000021, 0x00000009, 0x00000028, 0x00000029],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Lotad"]],
                locationId=FRIENDSHIP_ITEMS["Lotad"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Treecko"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803751FC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803751FC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000006],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Treecko"]],
                locationId=FRIENDSHIP_ITEMS["Treecko"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Caterpie"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375274, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375274, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Caterpie"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Butterfree Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Caterpie"]
            )
        ],
),
    FRIENDSHIP_ITEMS["Butterfree"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375288, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375288, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000002e, 0x00000016],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Butterfree"]],
                locationId=FRIENDSHIP_ITEMS["Butterfree"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Chimchar"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375A94, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375A94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000007],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Chimchar"]],
                locationId=FRIENDSHIP_ITEMS["Chimchar"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Aipom"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037542C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037542C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000025, 0x00000012],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Aipom"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Ambipom Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Aipom"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Ambipom"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375440, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375440, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000019],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Ambipom"]],
                locationId=FRIENDSHIP_ITEMS["Ambipom"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Weedle"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375260, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375260, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Weedle"]],
                locationId=FRIENDSHIP_ITEMS["Weedle"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Shroomish"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803752EC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803752EC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Shroomish"]],
                locationId=FRIENDSHIP_ITEMS["Shroomish"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Magikarp"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756D4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803756D4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000008],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Magikarp"]],
                locationId=FRIENDSHIP_ITEMS["Magikarp"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Oddish"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753A0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803753A0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Oddish"]],
                locationId=FRIENDSHIP_ITEMS["Oddish"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Leafeon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803754CC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803754CC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001C],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Leafeon"]],
                locationId=FRIENDSHIP_ITEMS["Leafeon"],
                is_special_exception=True
            )
        ]
),
    FRIENDSHIP_ITEMS["Bidoof"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375238, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375238, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000c],
                unlock_items_to_block=[UNLOCK_ITEMS["Bidoof Unlock"],
                                       UNLOCK_ITEMS["Bidoof Unlock 2"],
                                       UNLOCK_ITEMS["Bidoof Unlock 3"],
                                       UNLOCK_ITEMS["Bidoof Unlock 3"]],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Bidoof"]],
                locationId=FRIENDSHIP_ITEMS["Bidoof"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Starly"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375364, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation( # Meadow Zone
                location=MemoryAddress(base_address=0x80375364, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000023, 0x00000024, 0x0000002a, 0x00000015, 0x00000026],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Starly"]],
                locationId=FRIENDSHIP_ITEMS["Starly"]
            ),
            PokemonLocation( # Beach Zone
                location=MemoryAddress(base_address=0x80375364, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000026, 0x00000008],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Starly"]],
                locationId=OverworldPokemonLocationIds.STARLY_BEACH.value
            ),
            PokemonLocation( # Ice Zone
                location=MemoryAddress(base_address=0x80375364, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000001f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Starly"]],
                locationId=OverworldPokemonLocationIds.STARLY_ICE.value
            )
        ]
),
    FRIENDSHIP_ITEMS["Torterra"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803751E8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803751E8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000014],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Torterra"]],
                locationId=FRIENDSHIP_ITEMS["Torterra"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Bibarel"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037524C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037524C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000018],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Bibarel"]],
                locationId=FRIENDSHIP_ITEMS["Bibarel"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Scyther"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375454, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375454, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Scyther"]],
                locationId=FRIENDSHIP_ITEMS["Scyther"]
            )
        ]
),

    # Beach Zone Pokemon
    #
    #
    FRIENDSHIP_ITEMS["Buizel"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755d0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803755d0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000002],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Buizel"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Floatzel Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Buizel"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Psyduck"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755F8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803755F8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000003],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Psyduck"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Golduck Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Psyduck"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Slowpoke"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755BC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803755BC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000004],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Slowpoke"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Mudkip Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Slowpoke"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Azurill"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375558, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375558, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000005],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Azurill"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Totodile Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Azurill"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Totodile"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375670, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375670, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000000c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Totodile"]],
                locationId=FRIENDSHIP_ITEMS["Totodile"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Mudkip"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037556C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037556C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000000d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Mudkip"]],
                locationId=FRIENDSHIP_ITEMS["Mudkip"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Pidgeotto"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375634, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375634, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000018],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Pidgeotto"]],
                locationId=FRIENDSHIP_ITEMS["Pidgeotto"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Taillow"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375620, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation( # Beach Zone
                location=MemoryAddress(base_address=0x80375620, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000029, 0x00000024],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Taillow"]],
                locationId=FRIENDSHIP_ITEMS["Taillow"]
            ),
            PokemonLocation( # Ice Zone
                location=MemoryAddress(base_address=0x80375620, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000000f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Taillow"]],
                locationId=OverworldPokemonLocationIds.TAILLOW_ICE.value
            )
        ]
),
    FRIENDSHIP_ITEMS["Wingull"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756ac, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803756ac, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000000a, 0x0000002b, 0x00000024],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Wingull"]],
                locationId=FRIENDSHIP_ITEMS["Wingull"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x803756ac, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000002f, 0x0000002e, 0x00000010],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Wingull"]],
                locationId=OverworldPokemonLocationIds.WINGULL_ICE.value
            )
        ]
),

    FRIENDSHIP_ITEMS["Staravia"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375378, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation( # Beach Zone
                location=MemoryAddress(base_address=0x80375378, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000017],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Staravia"]],
                locationId=FRIENDSHIP_ITEMS["Staravia"]
            ),
            PokemonLocation( # Ice Zone
                location=MemoryAddress(base_address=0x80375378, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000000e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Staravia"]],
                locationId=OverworldPokemonLocationIds.STARAVIA_ICE.value
            )
        ]
),
    FRIENDSHIP_ITEMS["Corsola"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755A8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803755A8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000022, 0x00000021, 0x00000006],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Corsola"]],
                locationId=FRIENDSHIP_ITEMS["Corsola"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Floatzel"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755E4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803755E4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000016],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Floatzel"]],
                locationId=FRIENDSHIP_ITEMS["Floatzel"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Vaporeon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803754E0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803754E0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000014],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Vaporeon"]],
                locationId=FRIENDSHIP_ITEMS["Vaporeon"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Golduck"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037560C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037560C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000015],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Golduck"]],
                locationId=FRIENDSHIP_ITEMS["Golduck"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Pelipper"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756C0, memory_range=MemoryRange.BYTE, value=0x80)),
    FRIENDSHIP_ITEMS["Sharpedo"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80376048, memory_range=MemoryRange.BYTE, value=0x80)),
    FRIENDSHIP_ITEMS["Wynaut"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375C88, memory_range=MemoryRange.BYTE, value=0x80)),
    FRIENDSHIP_ITEMS["Carvanha"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375FE4, memory_range=MemoryRange.BYTE, value=0x80)),
    FRIENDSHIP_ITEMS["Krabby"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375580, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation( # Beach Zone
                location=MemoryAddress(base_address=0x80375580, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000002c, 0x0000002d, 0x0000000b, 0x00000020],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Krabby"]],
                locationId=FRIENDSHIP_ITEMS["Krabby"],
            ),
            PokemonLocation( # Ice Zone
                location=MemoryAddress(base_address=0x80375580, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000002d, 0x00000004, 0x0000002c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Krabby"]],
                locationId=OverworldPokemonLocationIds.KRABBY_ICE.value
            )
        ]
),
    FRIENDSHIP_ITEMS["Wailord"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803760ac, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803760ac, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000013],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Wailord"]],
                locationId=FRIENDSHIP_ITEMS["Wailord"],
                is_special_exception=True
            )
        ]
),
    FRIENDSHIP_ITEMS["Corphish"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375594, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375594, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000002f, 0x0000002e, 0x0000000e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Corphish"]],
                locationId=FRIENDSHIP_ITEMS["Corphish"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375594, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000005, 0x00000022, 0x00000023],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Corphish"]],
                locationId=OverworldPokemonLocationIds.CORPHISH_ICE.value
            )
        ]
),
    FRIENDSHIP_ITEMS["Gyarados"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756E8, memory_range=MemoryRange.BYTE, value=0x80)),
    FRIENDSHIP_ITEMS["Feraligatr"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375684, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375684, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000001b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Feraligatr"]],
                locationId=FRIENDSHIP_ITEMS["Feraligatr"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Piplup"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803757EC, memory_range=MemoryRange.BYTE, value=0x80)),

    # Treehouse
    FRIENDSHIP_ITEMS["Burmy"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80376020, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80376020, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=treehouse_stage_id,
                pokemon_ids=[0x00000014],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Burmy"]],
                locationId=FRIENDSHIP_ITEMS["Burmy"]
            )
        ]
),

    # multiple versions since friendship is possible in multiple region, but for now its juts one location
    FRIENDSHIP_ITEMS["Drifblim"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375f94, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation( #Treehouse
                location=MemoryAddress(base_address=0x80375f94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=treehouse_stage_id,
                pokemon_ids=[0x0000001d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifblim"]],
                locationId=FRIENDSHIP_ITEMS["Drifblim"]
            ),
            PokemonLocation( # Meadow Zone
                location=MemoryAddress(base_address=0x80375f94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifblim"]],
                locationId=FRIENDSHIP_ITEMS["Drifblim"]
            ),
            PokemonLocation( # Beach Zone
                location=MemoryAddress(base_address=0x80375f94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000001f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifblim"]],
                locationId=FRIENDSHIP_ITEMS["Drifblim"]
            ),
            PokemonLocation( # Ice Zone
                location=MemoryAddress(base_address=0x80375f94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000001c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifblim"]],
                locationId=FRIENDSHIP_ITEMS["Drifblim"]
            )
        ]
),



    # also multiple version of lapras since it has Beach Zone and Ice Zone locations, for now one location
    FRIENDSHIP_ITEMS["Lapras"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375698, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation( # Beach Zone
                location=MemoryAddress(base_address=0x80375698, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000001c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Lapras"]],
                locationId=FRIENDSHIP_ITEMS["Lapras"]
            ),
            PokemonLocation( # Ice Zone
                location=MemoryAddress(base_address=0x80375698, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000017],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Lapras"]],
                locationId=FRIENDSHIP_ITEMS["Lapras"]
            )
        ]
),

    FRIENDSHIP_ITEMS["Spheal"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375724, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375724, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000001d, 0x00000026, 0x0000001e, 0x00000029, 0x00000028, 0x00000006,0x00000027],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Spheal"]],
                locationId=FRIENDSHIP_ITEMS["Spheal"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Octillery"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375788, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375788, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000024, 0x00000014,0x00000025],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Octillery"]],
                locationId=FRIENDSHIP_ITEMS["Octillery"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Teddiursa"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756FC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803756FC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000021, 0x00000007],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Teddiursa"]],
                locationId=FRIENDSHIP_ITEMS["Teddiursa"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Delibird"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375774, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375774, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000008],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Delibird"]],
                locationId=FRIENDSHIP_ITEMS["Delibird"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Smoochum"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375738, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375738, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000000b,0x00000030,0x00000031],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Smoochum"]],
                locationId=FRIENDSHIP_ITEMS["Smoochum"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Squirtle"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375648, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375648, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000000c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Squirtle"]],
                locationId=FRIENDSHIP_ITEMS["Squirtle"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Glaceon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803754F4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803754F4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000016],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Glaceon"]],
                locationId=FRIENDSHIP_ITEMS["Glaceon"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Prinplup"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375800, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375800, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000001b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Prinplup"]],
                locationId=FRIENDSHIP_ITEMS["Prinplup"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Sneasel"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037574C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037574C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000020,0x00000001],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Sneasel"]],
                locationId=FRIENDSHIP_ITEMS["Sneasel"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Piloswine"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803757C4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803757C4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000000a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Piloswine"]],
                locationId=FRIENDSHIP_ITEMS["Piloswine"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Glalie"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037579C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037579C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000015],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Glalie"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Ursaring Unlock"],UNLOCK_ITEMS["Primeape Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Glalie"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Froslass"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803757B0, memory_range=MemoryRange.BYTE, value=0x80)
),
    FRIENDSHIP_ITEMS["Primeape"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375328, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375328, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000012],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Primeape"]],
                locationId=FRIENDSHIP_ITEMS["Primeape"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Ursaring"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375710, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375710, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000013],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Ursaring"]],
                locationId=FRIENDSHIP_ITEMS["Ursaring"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Mamoswine"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803757D8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803757D8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000019],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Mamoswine"]],
                locationId=FRIENDSHIP_ITEMS["Mamoswine"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Kirlia"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375DC8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375DC8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000009],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Kirlia"]],
                locationId=FRIENDSHIP_ITEMS["Kirlia"]
            )
        ]
),
    FRIENDSHIP_ITEMS["Quagsire"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375760, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375760, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000002a, 0x00000011,0x0000002b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Quagsire"]],
                locationId=FRIENDSHIP_ITEMS["Quagsire"],
                is_special_exception=True
            )
        ]
),
    FRIENDSHIP_ITEMS["Empoleon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375814, memory_range=MemoryRange.BYTE, value=0x80)
),


}

prisma_blocked_itemIds = []

PRISMAS = {
    PRISM_ITEM["Bulbasaur Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80377E1C, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80377e1c, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Bulbasaur Prisma"],
        itemId=PRISM_ITEM["Bulbasaur Prisma"],
        stage_id=bulbasaur_minigame_stage_id
    ),
    PRISM_ITEM["Venusaur Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80376DA8, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80376DA8, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Venusaur Prisma"],
        itemId=PRISM_ITEM["Venusaur Prisma"],
        stage_id=venusaur_minigame_stage_id
    ),
    PRISM_ITEM["Pelipper Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x803772B8, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x803772B8, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Pelipper Prisma"],
        itemId=PRISM_ITEM["Pelipper Prisma"],
        stage_id=pelipper_minigame_stage_id
    ),
    PRISM_ITEM["Gyarados Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80377174, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80377174, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Gyarados Prisma"],
        itemId=PRISM_ITEM["Gyarados Prisma"],
        stage_id=gyarados_minigame_stage_id
    ),
    PRISM_ITEM["Empoleon Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80377540, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80377540, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Empoleon Prisma"],
        itemId=PRISM_ITEM["Empoleon Prisma"],
        stage_id=empoleon_minigame_stage_id
    ),
}

BLOCKED_UNLOCKS = []

UNLOCKS = {
    # Misc
    UNLOCK_ITEMS["Drifblim Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376AD0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x40000000
        )
    ),

    # Meadow Zone Unlocks
    #
    UNLOCK_ITEMS["Tropius Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00400000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x40
        )],
        locationId=UNLOCK_ITEMS["Tropius Unlock"]
    ),

    UNLOCK_ITEMS["Pachirisu Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000008
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0003,
            memory_range=MemoryRange.BYTE,
            value=0x08
        ),
            MemoryAddress(
                base_address=0x80376ad0,
                offset=0x7FFF + 0x0002,
                memory_range=MemoryRange.BYTE,
                value=0x40
            ),
        ],
        locationId=UNLOCK_ITEMS["Pachirisu Unlock"]
    ),
    UNLOCK_ITEMS["Bonsly Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376Ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00004000
        )
    ),
    UNLOCK_ITEMS["Sudowoodo Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00400000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad8,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x40
        )],
        locationId=UNLOCK_ITEMS["Sudowoodo Unlock"]
    ),
    UNLOCK_ITEMS["Lotad Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000100
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0002,
            memory_range=MemoryRange.BYTE,
            value=0x80
        )],
        locationId=UNLOCK_ITEMS["Lotad Unlock"]
    ),
    UNLOCK_ITEMS["Shinx Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376Ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00008000
        ),
    ),
    UNLOCK_ITEMS["Scyther Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x04000000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0000,
            memory_range=MemoryRange.BYTE,
            value=0x04
        )],
        locationId=UNLOCK_ITEMS["Scyther Unlock"]
    ),
    UNLOCK_ITEMS["Caterpie Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000200
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0002,
            memory_range=MemoryRange.BYTE,
            value=0x02
        )],
        locationId=UNLOCK_ITEMS["Caterpie Unlock"],
        is_blocked_until_location=True,
        blocked_zone=meadow_zone_stage_id
    ),
    UNLOCK_ITEMS["Butterfree Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00200000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x20
        )],
        locationId=UNLOCK_ITEMS["Butterfree Unlock"]
    ),
    UNLOCK_ITEMS["Chimchar Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000040
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0003,
            memory_range=MemoryRange.BYTE,
            value=0x40
        )],
        locationId=UNLOCK_ITEMS["Chimchar Unlock"]
    ),
    UNLOCK_ITEMS["Ambipom Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x01000000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0000,
            memory_range=MemoryRange.BYTE,
            value=0x01
        )],
        locationId=UNLOCK_ITEMS["Ambipom Unlock"]
    ),
    UNLOCK_ITEMS["Weedle Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000400
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0002,
            memory_range=MemoryRange.BYTE,
            value=0x04
        )],
        locationId=UNLOCK_ITEMS["Weedle Unlock"],
        is_blocked_until_location=True,
        blocked_zone=meadow_zone_stage_id
    ),
    UNLOCK_ITEMS["Shroomish Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00002000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0002,
            memory_range=MemoryRange.BYTE,
            value=0x20
        )],
        locationId=UNLOCK_ITEMS["Shroomish Unlock"],
        is_blocked_until_location=True,
        blocked_zone=meadow_zone_stage_id
    ),
    UNLOCK_ITEMS["Magikarp Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000080
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0003,
            memory_range=MemoryRange.BYTE,
            value=0x80
        )],
        locationId=UNLOCK_ITEMS["Magikarp Unlock"],
        is_blocked_until_location=True,
        blocked_zone=meadow_zone_stage_id
    ),
    UNLOCK_ITEMS["Bidoof Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x80000000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0000,
            memory_range=MemoryRange.BYTE,
            value=0x80
        )],
        locationId=UNLOCK_ITEMS["Bidoof Unlock"]
    ),
    UNLOCK_ITEMS["Bidoof Unlock 2"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000001
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0003,
            memory_range=MemoryRange.BYTE,
            value=0x01
        )],
        locationId=UNLOCK_ITEMS["Bidoof Unlock 2"]
    ),
    UNLOCK_ITEMS["Bidoof Unlock 3"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000002
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0003,
            memory_range=MemoryRange.BYTE,
            value=0x02
        )],
        locationId=UNLOCK_ITEMS["Bidoof Unlock 3"]
    ),
    UNLOCK_ITEMS["Bibarel Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00800000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x80
        )],
        locationId=UNLOCK_ITEMS["Bibarel Unlock"]
    ),
    UNLOCK_ITEMS["Starly Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00100000
        )
    ),
    UNLOCK_ITEMS["Starly Unlock 2"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000010
        )
    ),
    UNLOCK_ITEMS["Torterra Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00080000
        ),

    ),

    # Beach Zone Unlock
    #
    UNLOCK_ITEMS["Floatzel Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x02000000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0000,
            memory_range=MemoryRange.BYTE,
            value=0x02
        )],
        locationId=UNLOCK_ITEMS["Floatzel Unlock"]
    ),
    UNLOCK_ITEMS["Golduck Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x01000000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0000,
            memory_range=MemoryRange.BYTE,
            value=0x01
        )],
        locationId=UNLOCK_ITEMS["Golduck Unlock"]
    ),
    UNLOCK_ITEMS["Mudkip Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00040000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x04
        )],
        locationId=UNLOCK_ITEMS["Mudkip Unlock"]
    ),
    UNLOCK_ITEMS["Totodile Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00020000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x02
        )],
        locationId=UNLOCK_ITEMS["Totodile Unlock"]
    ),
    UNLOCK_ITEMS["Krabby Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00010000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x01
        )],
        locationId=UNLOCK_ITEMS["Krabby Unlock"],
        is_blocked_until_location=True,
        blocked_zone=beach_zone_stage_id
    ),
    UNLOCK_ITEMS["Corphish Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00080000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x08
        )],
        locationId=UNLOCK_ITEMS["Corphish Unlock"],
        is_blocked_until_location=True,
        blocked_zone=beach_zone_stage_id
    ),

    # Misc
    #
    UNLOCK_ITEMS["Pikachu Balloon"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x8037AEC3,
            memory_range=MemoryRange.BYTE,
            value=0x08
        )
    ),
    UNLOCK_ITEMS["Pikachu Surfboard"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x8037AEC3,
            memory_range=MemoryRange.BYTE,
            value=0x01
        )
    ),
    UNLOCK_ITEMS["Pikachu Snowboard"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x8037AEC3,
            memory_range=MemoryRange.BYTE,
            value=0x04
        )
    ),

    UNLOCK_ITEMS["Delibird Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000200
        )
    ),
    UNLOCK_ITEMS["Squirtle Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000800
        )
    ),
    UNLOCK_ITEMS["Smoochum Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000400
        )
    ),
    UNLOCK_ITEMS["Sneasel Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000080
        )
    ),
    UNLOCK_ITEMS["Mamoswine Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00040000
        )
    ),
    UNLOCK_ITEMS["Glalie Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ae4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00800000
        )
    ),
    UNLOCK_ITEMS["Primeape Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00002000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad8,
            offset=0x7FFF + 0x0002,
            memory_range=MemoryRange.BYTE,
            value=0x20
        )],
        locationId=UNLOCK_ITEMS["Primeape Unlock"]
    ),
    UNLOCK_ITEMS["Ursaring Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00004000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad8,
            offset=0x7FFF + 0x0002,
            memory_range=MemoryRange.BYTE,
            value=0x40
        )],
        locationId=UNLOCK_ITEMS["Ursaring Unlock"]
    ),
}

POWER_INCREMENTS = {
    "thunderbolt": {
        "increments": [0x10, 0x20, 0x40, 0x80],  # +20, +40, +80
    },
    "dash": {
        "increments": [0x01,0x04, 0x08, 0x4000],  # +4, +8, +4000
    },
    "health": {
        "increments": [0x100, 0x200, 0x400]
    },
    "iron_tail": {
        "increments": [0x800,0x1000,0x2000]
    }
}

POWER_SHARED_ADDR = 0x8037AEEE

berry_item_checks = {
    BERRIES["10 Berries"]: [(0x8037AEDE, 0xa)],
    BERRIES["20 Berries"]: [(0x8037AEDE, 0x14)],
    BERRIES["50 Berries"]: [(0x8037AEDE, 0x32)],
    BERRIES["100 Berries"]: [(0x8037AEDE, 0x64)],
}

logic_adresses = [
    # clean up pokemon id
    (0x8004faa0, 0x3d808037),
    (0x8004faa4, 0x38600000),
    (0x8004faa8, 0x906CDC20),
    (0x8004faac, 0x4e800020),

    # Friendship trigger logic
    (0x80126508, 0x98030001),
    # unlock trigger logic
    (0x8018397c, 0x90047fff),
    (0x80183970, 0x38600000),
    # disable berries in friendship
    # (0x80180a3c, 0x60000000),
    # disable check is friend check for locations
    # (0x801812f8,0x60000000)
    # (0x801146f8,0x38600000),
    # (0x801812e0,0x38600000)

    # find out pokemon id
    (0x80026664, 0x3ca08037),
    (0x80026668, 0x9085dc20),
    (0x8002666c, 0x4e800020),

    # prism trigger logic
    (0x801261e0, 0x90037fff),

    # deactivate power level up
    (0x801268f4, 0x60000000)
]

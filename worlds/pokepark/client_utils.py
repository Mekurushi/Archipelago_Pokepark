import re
from dataclasses import dataclass
from enum import Enum

import dolphin_memory_engine


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


class PointerTableOffsets:
    PATCHER_VERSION_OFFSET = 0x0
    PLAYER_NAME_OFFSET = 0x4
    GIVE_ITEM_ARRAY_OFFSET = 0x8
    SHOULD_PRINT_AP_BUFFER_OFFSET = 0xC
    ARCHIPELAGO_TEXT_BUFFER_OFFSET = 0x10
    IS_DEATH_OFFSET = 0x14
    DEATH_TRIGGER_OFFSET = 0x18
    FPS_ENHANCEMENT_OFFSET = 0x1C
    GLOBAL_MANAGER_DATA_OFFSET = 0x20
    IS_IN_TITLE_SCREEN_OFFSET = 0x24
    GAME_BOOTED_UP_OFFSET = 0x28
    ATTRACTION_ID_OFFSET = 0x2C
    POINTER_TABLE_ADDR = {
        b"R8AJ99": 0x80366348,
        b"R8AE99": 0x80366348,
        b"R8AP99": 0x80366348,
    }


class ClientAddresses:
    def __init__(self, dme: dolphin_memory_engine, game_id: bytes):
        base = PointerTableOffsets.POINTER_TABLE_ADDR[game_id]
        self.PATCHER_VERSION_ADDRESS = dme.read_word(base + PointerTableOffsets.PATCHER_VERSION_OFFSET)
        self.PLAYER_NAME_ADDRESS = dme.read_word(base + PointerTableOffsets.PLAYER_NAME_OFFSET)
        self.GIVE_ITEM_ARRAY_ADDRESS = dme.read_word(base + PointerTableOffsets.GIVE_ITEM_ARRAY_OFFSET)
        self.SHOULD_PRINT_AP_BUFFER_ADDRESS = dme.read_word(base + PointerTableOffsets.SHOULD_PRINT_AP_BUFFER_OFFSET)
        self.ARCHIPELAGO_TEXT_BUFFER_ADDRESS = dme.read_word(base + PointerTableOffsets.ARCHIPELAGO_TEXT_BUFFER_OFFSET)
        self.IS_DEATH_ADDRESS = dme.read_word(base + PointerTableOffsets.IS_DEATH_OFFSET)
        self.DEATH_TRIGGER_ADDRESS = dme.read_word(base + PointerTableOffsets.DEATH_TRIGGER_OFFSET)
        self.FPS_ENHANCEMENT = dme.read_word(base + PointerTableOffsets.FPS_ENHANCEMENT_OFFSET)
        self.GLOBAL_MANAGER_DATA_ADDRESS = dme.read_word(base + PointerTableOffsets.GLOBAL_MANAGER_DATA_OFFSET)
        self.IS_IN_TITLE_SCREEN_ADDRESS = dme.read_word(base + PointerTableOffsets.IS_IN_TITLE_SCREEN_OFFSET)
        self.GAME_BOOTED_UP_ADDRESS = dme.read_word(base + PointerTableOffsets.GAME_BOOTED_UP_OFFSET)
        self.ATTRACTION_ID_ADDRESS = dme.read_word(base + PointerTableOffsets.ATTRACTION_ID_OFFSET)


STAGE_NAME_MAP = {
    0x0101.to_bytes(2): "Meadow Zone Main Area",
    0x0102.to_bytes(2): "Meadow Zone Venusaur Area",
    0x0201.to_bytes(2): "Treehouse",
    0x0301.to_bytes(2): "Beach Zone Main Area",
    0x0302.to_bytes(2): "Ice Zone Main Area",
    0x0303.to_bytes(2): "Ice Zone Empoleon Area",
    0x0401.to_bytes(2): "Cavern Zone Main Area",
    0x0402.to_bytes(2): "Magma Zone Main Area",
    0x0403.to_bytes(2): "Magma Zone Blaziken Area",
    0x0501.to_bytes(2): "Haunted Zone Main Area",
    0x0502.to_bytes(2): "Haunted Zone Mansion Area",
    0x0503.to_bytes(2): "Haunted Zone Rotom Area",
    0x0601.to_bytes(2): "Granite Zone Main Area",
    0x0602.to_bytes(2): "Flower Zone Main Area",
    0x0701.to_bytes(2): "Skygarden",
    0x6301.to_bytes(2): "Pokepark Entrance",
}

ATTRACTION_ID_MAP = {
    0x0: "Absol's Hurdle Bounce Attraction",
    0x1: "Rayquaza's Balloon Panic Attraction",
    0x2: "Venusaur's Vine Swing Attraction",
    0x3: "Tangrowth's Swing-Along Attraction",
    0x4: "Dusknoir's Speed Slam Attraction",
    0x5: "Gyarados' Aqua Dash Attraction",
    0x6: "Pelipper's Circle Circuit Attraction",
    0x8: "Empoleon's Snow Slide Attraction",
    0x9: "Bastiodon's Panel Crush Attraction",
    0xa: "Rhyperior's Bumper Burn Attraction",
    0xb: "Blaziken's Boulder Bash Attraction",
    0xc: "Rotom's Spooky Shoot-'em-Up Attraction",
    0xe: "Salamence's Sky Race Attraction",
    0xF: "Bulbasaur's Daring Dash Attraction",
}


CLIENT_TEXT_BUFFER_SIZE = 512

# Time for a client message to disappear in-game (in seconds, not including stagger time for multiple lines in the queue)
CLIENT_TEXT_TIMEOUT = 6

# Max number of characters in a line for in-game client text
INGAME_LINE_LENGTH = 64

COLOR_CONTROL_SEQUENCES = {
    "black": "\x0e\x00\x03\x02\x00",
    "red": "\x0e\x00\x03\x02\x01",
    "orange": "\x0e\x00\x03\x02\x02",
    "blue": "\x0e\x00\x03\x02\x03",
    "green": "\x0e\x00\x03\x02\x04",
    "yellow": "\x0e\x00\x03\x02\x05",
    "plum": "\x0e\x00\x03\x02\x06",
    "cyan": "\x0e\x00\x03\x02\x07",
    "salmon": "\x0e\x00\x03\x02\x08",
    "magenta": "\x0e\x00\x03\x02\x09",
    "slateblue": "\x0e\x00\x03\x02\x0a",
}
CONTROL_SEQ = re.compile(r'\x0e.{4}', re.DOTALL)
COLOR_RESET = "\x0e\x00\x03\x02\uffff"


def visible_len(s: str) -> int:
    return len(CONTROL_SEQ.sub('', s))


def wrap_line(line: str, max_width: int) -> list[str]:
    result = []
    current = ""
    active_color = ""

    for word in line.split(' '):
        # control sequences shouldn't count to the width
        width = visible_len(current) + visible_len(word) + 1
        if current and width > max_width:
            result.append(active_color + current + (COLOR_RESET if active_color else ""))
            # find the current active color for the width forced line break
            for m in CONTROL_SEQ.finditer(current):
                active_color = "" if m.group(0) == COLOR_RESET else m.group(0)
            current = word
        else:
            current = (current + ' ' + word).lstrip(' ')

    if current:
        result.append(active_color + current + (COLOR_RESET if active_color else ""))

    return result

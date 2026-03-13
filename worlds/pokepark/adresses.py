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
    GLOBAL_MANAGER_DATA_OFFSET = 0x1C
    IS_IN_TITLE_SCREEN_OFFSET = 0x20
    GAME_BOOTED_UP_OFFSET = 0x24
    ATTRACTION_ID_OFFSET = 0x28
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
        self.GLOBAL_MANAGER_DATA_ADDRESS = dme.read_word(base + PointerTableOffsets.GLOBAL_MANAGER_DATA_OFFSET)
        self.IS_IN_TITLE_SCREEN_ADDRESS = dme.read_word(base + PointerTableOffsets.IS_IN_TITLE_SCREEN_OFFSET)
        self.GAME_BOOTED_UP_ADDRESS = dme.read_word(base + PointerTableOffsets.GAME_BOOTED_UP_OFFSET)
        self.ATTRACTION_ID_ADDRESS = dme.read_word(base + PointerTableOffsets.ATTRACTION_ID_OFFSET)

CLIENT_TEXT_BUFFER_SIZE = 512

# Time for a client message to disappear in-game (in seconds, not including stagger time for multiple lines in the queue)
CLIENT_TEXT_TIMEOUT = 6

# Max number of characters in a line for in-game client text
INGAME_LINE_LENGTH = 64
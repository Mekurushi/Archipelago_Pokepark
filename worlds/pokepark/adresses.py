from dataclasses import dataclass
from enum import Enum


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


POWER_MAP = {
    "Progressive Dash": [0x01, 0x04, 0x08, 0x4000],
    "Progressive Thunderbolt": [0x10, 0x20, 0x40, 0x80],
    "Progressive Health": [0x100, 0x200, 0x400],
    "Progressive Iron Tail": [0x800, 0x1000, 0x2000],
    "Double Dash": [0x02]
}

SLOT_NAME_ADDR = {
    b"R8AJ99": 0x803663D0,
    b"R8AE99": 0x80368850,
    b"R8AP99": 0x80368D70
}

GLOBAL_MANAGER_OPCODE_ADDR = {
    b"R8AJ99": 0x80366274,
    b"R8AE99": 0x803686F0,
    b"R8AP99": 0x80368C10
}

GLOBAL_MANAGER_PARAMETER1_ADDR = {
    b"R8AJ99": 0x80366278,
    b"R8AE99": 0x803686F4,
    b"R8AP99": 0x80368C14
}

GLOBAL_MANAGER_PARAMETER2_ADDR = {
    b"R8AJ99": 0x8036627c,
    b"R8AE99": 0x803686F8,
    b"R8AP99": 0x80368C18
}

GLOBAL_MANAGER_DATA_STRUC_ADDRESS = {
    b"R8AJ99": 0x80374fe0,
    b"R8AE99": 0x80378460,
    b"R8AP99": 0x803789e8
}

BATTLE_COMP_DEATH_CHECK_ADDRESSES = {
    b"R8AJ99": 0x804A6CDB,
    b"R8AE99": 0x804aa493,
    b"R8AP99": 0x804aaa73
}

HIDE_AND_SEEK_COMP_DEATH_CHECK_ADDRESSES = {
    b"R8AJ99": 0x804AF4B3,
    b"R8AE99": 0x804B2C73,
    b"R8AP99": 0x804b3253

}

CHASE_COMP_DEATH_CHECK_ADDRESSES = {
    b"R8AJ99": 0x8049E4EB,
    b"R8AE99": 0x804a1ca3,
    b"R8AP99": 0x804a2283,

}

ATHLETIC_COMP_DEATH_CHECK_ADDRESSES = {
    b"R8AJ99": 0x804B7B5B,
    b"R8AE99": 0x804bb31b,
    b"R8AP99": 0x804bb8fb,

}

BATTLE_COMP_GIVE_DEATH_ADDRESSES = {
    b"R8AJ99": 0x804af1d2,
    b"R8AE99": 0x804b298a,
    b"R8AP99": 0x804b2f6a,

}

HIDE_AND_SEEK_COMP_GIVE_DEATH_ADDRESSES = {
    b"R8AJ99": 0x804b79a6,
    b"R8AE99": 0x804bb166,
    b"R8AP99": 0x804bb746,

}

CHASE_COMP_GIVE_DEATH_ADDRESSES = {
    b"R8AJ99": 0x804a69e2,
    b"R8AE99": 0x804aa19a,
    b"R8AP99": 0x804aa77a,

}

ATHLETIC_COMP_GIVE_DEATH_ADDRESSES = {
    b"R8AJ99": 0x804b80ea,
    b"R8AE99": 0x804BB8AA,
    b"R8AP99": 0x804bbe8a,

}

ATTRACTION_ID_ADDRESSES = {
    b"R8AJ99": 0x8039CA48,
    b"R8AE99": 0x8039FED8,
    b"R8AP99": 0x803A0460
}

IS_IN_PAUSE_MENU_ADDRESSES = {
    b"R8AJ99": 0x80482F04,
    b"R8AE99": 0x80486380,
    b"R8AP99": 0x80486930
}

IS_INITIALIZED_ADDRESSES = {
    b"R8AJ99": 0x8037afd4,
    b"R8AE99": 0x8037e454,
    b"R8AP99": 0x8037e9dc
}

IS_IN_MAIN_MENU_ADDRESSES = {
    b"R8AJ99": 0x80496E50,
    b"R8AE99": 0x8049A2F0,
    b"R8AP99": 0x8049A8D0
}

IS_IN_GAME_END_STATE_ADDRESSES = {
    b"R8AJ99": 0x8036C997,
    b"R8AE99": 0x8036EE17,
    b"R8AP99": 0x8036F397
}

IS_IN_LOADING_SCREEN_ADDRESSES = {
    b"R8AJ99": 0x80496D2F,
    b"R8AE99": 0x8049A1CF,
    b"R8AP99": 0x8049A7AF
}

CURRENT_STAGE_ADDRESSES = {
    b"R8AJ99": 0x8037AEE0,
    b"R8AE99": 0x0,
    b"R8AP99": 0x0
}
NEXT_STAGE_ADDRESSES = {
    b"R8AJ99": 0x8037AF20,
    b"R8AE99": 0x0,
    b"R8AP99": 0x0
}

SCENE_NAME_ADDR = {
    b"R8AJ99": 0x803663C0,
    b"R8AE99": 0x80368840,
    b"R8AP99": 0x80368D60
}
SCENE_PARAM1_ADDR = {
    b"R8AJ99": 0x8036668C,
    b"R8AE99": 0x80368B0C,
    b"R8AP99": 0x8036902C
}

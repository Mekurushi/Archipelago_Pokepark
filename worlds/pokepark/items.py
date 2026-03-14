from typing import NamedTuple, Optional

from BaseClasses import Item, ItemClassification as IC


class PokeparkItemData(NamedTuple):
    type: str
    classification: IC
    code: Optional[int]
    quantity: int
    item_id: int


class PokeparkItem(Item):
    game: str = "PokePark"
    type: Optional[str]

    def __init__(self, name: str, player: int, data: PokeparkItemData, classification: Optional[IC] = None) -> None:
        super().__init__(
            name,
            data.classification if classification is None else classification,
            None if data.code is None else PokeparkItem.get_apid(data.code),
            player,
        )

        self.type = data.type
        self.item_id = data.item_id

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given item code.

        :param code: The unique code for the item.
        :return: The computed Archipelago ID.
        """
        base_id: int = 10000
        return base_id + code


def generate_flagname(flag: str) -> bytes:
    return flag.encode('ascii') + b'\x00'

ITEM_TABLE: dict[str, PokeparkItemData] = {
    "Chatot Friendship": PokeparkItemData(
        "Item", IC.progression, 0, 1, 0
    ),
    "Chikorita Friendship": PokeparkItemData(
        "Item", IC.progression, 1, 1, 1
    ),
    "Turtwig Friendship": PokeparkItemData(
        "Item", IC.progression, 2, 1, 2
    ),
    "Torterra Friendship": PokeparkItemData(
        "Item", IC.progression, 3, 1, 3
    ),
    "Buneary Friendship": PokeparkItemData(
        "Item", IC.progression, 4, 1, 4
    ),
    "Munchlax Friendship": PokeparkItemData(
        "Item", IC.progression, 5, 1, 5
    ),
    "Treecko Friendship": PokeparkItemData(
        "Item", IC.progression, 6, 1, 6
    ),
    "Mankey Friendship": PokeparkItemData(
        "Item", IC.progression, 7, 1, 7
    ),
    "Bidoof Friendship": PokeparkItemData(
        "Item", IC.progression, 8, 1, 8
    ),
    "Bibarel Friendship": PokeparkItemData(
        "Item", IC.progression, 9, 1, 9
    ),
    "Oddish Friendship": PokeparkItemData(
        "Item", IC.progression, 10, 1, 10
    ),
    "Aipom Friendship": PokeparkItemData(
        "Item", IC.progression, 11, 1, 11
    ),
    "Ambipom Friendship": PokeparkItemData(
        "Item", IC.progression, 12, 1, 12
    ),
    "Leafeon Friendship": PokeparkItemData(
        "Item", IC.progression, 13, 1, 13
    ),
    "Spearow Friendship": PokeparkItemData(
        "Item", IC.progression, 14, 1, 14
    ),
    "Croagunk Friendship": PokeparkItemData(
        "Item", IC.progression, 15, 1, 15
    ),
    "Starly Friendship": PokeparkItemData(
        "Item", IC.progression, 16, 1, 16
    ),
    "Bonsly Friendship": PokeparkItemData(
        "Item", IC.progression, 17, 1, 17
    ),
    "Sudowoodo Friendship": PokeparkItemData(
        "Item", IC.progression, 18, 1, 18
    ),
    "Pachirisu Friendship": PokeparkItemData(
        "Item", IC.progression, 19, 1, 19
    ),
    "Lotad Friendship": PokeparkItemData(
        "Item", IC.progression, 20, 1, 20
    ),
    "Shinx Friendship": PokeparkItemData(
        "Item", IC.progression, 21, 1, 21
    ),
    "Scyther Friendship": PokeparkItemData(
        "Item", IC.progression, 22, 1, 22
    ),
    "Magikarp Friendship": PokeparkItemData(
        "Item", IC.progression, 23, 1, 23
    ),
    "Caterpie Friendship": PokeparkItemData(
        "Item", IC.progression, 24, 1, 24
    ),
    "Butterfree Friendship": PokeparkItemData(
        "Item", IC.progression, 25, 1, 25
    ),
    "Weedle Friendship": PokeparkItemData(
        "Item", IC.progression, 26, 1, 26
    ),
    "Shroomish Friendship": PokeparkItemData(
        "Item", IC.progression, 27, 1, 27
    ),
    "Tropius Friendship": PokeparkItemData(
        "Item", IC.progression, 28, 1, 28
    ),
    "Bulbasaur Friendship": PokeparkItemData(
        "Item", IC.progression, 29, 1, 29
    ),
    "Venusaur Friendship": PokeparkItemData(
        "Item", IC.progression, 30, 1, 30
    ),
    "Piplup Friendship": PokeparkItemData(
        "Item", IC.progression, 31, 1, 31
    ),
    "Slowpoke Friendship": PokeparkItemData(
        "Item", IC.progression, 32, 1, 32
    ),
    "Azurill Friendship": PokeparkItemData(
        "Item", IC.progression, 33, 1, 33
    ),
    "Corsola Friendship": PokeparkItemData(
        "Item", IC.progression, 34, 1, 34
    ),
    "Wynaut Friendship": PokeparkItemData(
        "Item", IC.progression, 35, 1, 35
    ),
    "Carvanha Friendship": PokeparkItemData(
        "Item", IC.progression, 36, 1, 36
    ),
    "Sharpedo Friendship": PokeparkItemData(
        "Item", IC.progression, 37, 1, 37
    ),
    "Wailord Friendship": PokeparkItemData(
        "Item", IC.progression, 38, 1, 38
    ),
    "Totodile Friendship": PokeparkItemData(
        "Item", IC.progression, 39, 1, 39
    ),
    "Feraligatr Friendship": PokeparkItemData(
        "Item", IC.progression, 40, 1, 40
    ),
    "Lapras Friendship": PokeparkItemData(
        "Item", IC.progression, 41, 1, 41
    ),
    "Psyduck Friendship": PokeparkItemData(
        "Item", IC.progression, 42, 1, 42
    ),
    "Golduck Friendship": PokeparkItemData(
        "Item", IC.progression, 43, 1, 43
    ),
    "Buizel Friendship": PokeparkItemData(
        "Item", IC.progression, 44, 1, 44
    ),
    "Floatzel Friendship": PokeparkItemData(
        "Item", IC.progression, 45, 1, 45
    ),
    "Vaporeon Friendship": PokeparkItemData(
        "Item", IC.progression, 46, 1, 46
    ),
    "Mudkip Friendship": PokeparkItemData(
        "Item", IC.progression, 47, 1, 47
    ),
    "Taillow Friendship": PokeparkItemData(
        "Item", IC.progression, 48, 1, 48
    ),
    "Staravia Friendship": PokeparkItemData(
        "Item", IC.progression, 49, 1, 49
    ),
    "Pidgeotto Friendship": PokeparkItemData(
        "Item", IC.progression, 50, 1, 50
    ),
    "Krabby Friendship": PokeparkItemData(
        "Item", IC.progression, 51, 1, 51
    ),
    "Corphish Friendship": PokeparkItemData(
        "Item", IC.progression, 52, 1, 52
    ),
    "Blastoise Friendship": PokeparkItemData(
        "Item", IC.progression, 53, 1, 53
    ),
    "Wingull Friendship": PokeparkItemData(
        "Item", IC.progression, 54, 1, 54
    ),
    "Pelipper Friendship": PokeparkItemData(
        "Item", IC.progression, 55, 1, 55
    ),
    "Gyarados Friendship": PokeparkItemData(
        "Item", IC.progression, 56, 1, 56
    ),
    "Glalie Friendship": PokeparkItemData(
        "Item", IC.progression, 57, 1, 57
    ),
    "Froslass Friendship": PokeparkItemData(
        "Item", IC.progression, 58, 1, 58
    ),
    "Piloswine Friendship": PokeparkItemData(
        "Item", IC.progression, 59, 1, 59
    ),
    "Mamoswine Friendship": PokeparkItemData(
        "Item", IC.progression, 60, 1, 60
    ),
    "Teddiursa Friendship": PokeparkItemData(
        "Item", IC.progression, 61, 1, 61
    ),
    "Ursaring Friendship": PokeparkItemData(
        "Item", IC.progression, 62, 1, 62
    ),
    "Kirlia Friendship": PokeparkItemData(
        "Item", IC.progression, 63, 1, 63
    ),
    "Spheal Friendship": PokeparkItemData(
        "Item", IC.progression, 64, 1, 64
    ),
    "Quagsire Friendship": PokeparkItemData(
        "Item", IC.progression, 65, 1, 65
    ),
    "Glaceon Friendship": PokeparkItemData(
        "Item", IC.progression, 66, 1, 66
    ),
    "Octillery Friendship": PokeparkItemData(
        "Item", IC.progression, 67, 1, 67
    ),
    "Delibird Friendship": PokeparkItemData(
        "Item", IC.progression, 68, 1, 68
    ),
    "Primeape Friendship": PokeparkItemData(
        "Item", IC.progression, 69, 1, 69
    ),
    "Squirtle Friendship": PokeparkItemData(
        "Item", IC.progression, 70, 1, 70
    ),
    "Smoochum Friendship": PokeparkItemData(
        "Item", IC.progression, 71, 1, 71
    ),
    "Sneasel Friendship": PokeparkItemData(
        "Item", IC.progression, 72, 1, 72
    ),
    "Prinplup Friendship": PokeparkItemData(
        "Item", IC.progression, 73, 1, 73
    ),
    "Empoleon Friendship": PokeparkItemData(
        "Item", IC.progression, 74, 1, 74
    ),
    "Mr. Mime Friendship": PokeparkItemData(
        "Item", IC.progression, 75, 1, 75
    ),
    "Mawile Friendship": PokeparkItemData(
        "Item", IC.progression, 76, 1, 76
    ),
    "Aron Friendship": PokeparkItemData(
        "Item", IC.progression, 77, 1, 77
    ),
    "Gible Friendship": PokeparkItemData(
        "Item", IC.progression, 78, 1, 78
    ),
    "Marowak Friendship": PokeparkItemData(
        "Item", IC.progression, 79, 1, 79
    ),
    "Zubat Friendship": PokeparkItemData(
        "Item", IC.progression, 80, 1, 80
    ),
    "Golbat Friendship": PokeparkItemData(
        "Item", IC.progression, 81, 1, 81
    ),
    "Diglett Friendship": PokeparkItemData(
        "Item", IC.progression, 82, 1, 82
    ),
    "Dugtrio Friendship": PokeparkItemData(
        "Item", IC.progression, 83, 1, 83
    ),
    "Snorlax Friendship": PokeparkItemData(
        "Item", IC.progression, 84, 1, 84
    ),
    "Geodude Friendship": PokeparkItemData(
        "Item", IC.progression, 85, 1, 85
    ),
    "Machamp Friendship": PokeparkItemData(
        "Item", IC.progression, 86, 1, 86
    ),
    "Meowth Friendship": PokeparkItemData(
        "Item", IC.progression, 87, 1, 87
    ),
    "Scizor Friendship": PokeparkItemData(
        "Item", IC.progression, 88, 1, 88
    ),
    "Cranidos Friendship": PokeparkItemData(
        "Item", IC.progression, 89, 1, 89
    ),
    "Phanpy Friendship": PokeparkItemData(
        "Item", IC.progression, 90, 1, 90
    ),
    "Raichu Friendship": PokeparkItemData(
        "Item", IC.progression, 91, 1, 91
    ),
    "Magnemite Friendship": PokeparkItemData(
        "Item", IC.progression, 92, 1, 92
    ),
    "Magnezone Friendship": PokeparkItemData(
        "Item", IC.progression, 93, 1, 93
    ),
    "Hitmonlee Friendship": PokeparkItemData(
        "Item", IC.progression, 94, 1, 94
    ),
    "Electivire Friendship": PokeparkItemData(
        "Item", IC.progression, 95, 1, 95
    ),
    "Bastiodon Friendship": PokeparkItemData(
        "Item", IC.progression, 96, 1, 96
    ),
    "Charmander Friendship": PokeparkItemData(
        "Item", IC.progression, 97, 1, 97
    ),
    "Hitmontop Friendship": PokeparkItemData(
        "Item", IC.progression, 98, 1, 98
    ),
    "Hitmonchan Friendship": PokeparkItemData(
        "Item", IC.progression, 99, 1, 99
    ),
    "Camerupt Friendship": PokeparkItemData(
        "Item", IC.progression, 100, 1, 100
    ),
    "Chimchar Friendship": PokeparkItemData(
        "Item", IC.progression, 101, 1, 101
    ),
    "Infernape Friendship": PokeparkItemData(
        "Item", IC.progression, 102, 1, 102
    ),
    "Vulpix Friendship": PokeparkItemData(
        "Item", IC.progression, 103, 1, 103
    ),
    "Ninetales Friendship": PokeparkItemData(
        "Item", IC.progression, 104, 1, 104
    ),
    "Farfetch'd Friendship": PokeparkItemData(
        "Item", IC.progression, 105, 1, 105
    ),
    "Meditite Friendship": PokeparkItemData(
        "Item", IC.progression, 106, 1, 106
    ),
    "Magby Friendship": PokeparkItemData(
        "Item", IC.progression, 107, 1, 107
    ),
    "Magmortar Friendship": PokeparkItemData(
        "Item", IC.progression, 108, 1, 108
    ),
    "Flareon Friendship": PokeparkItemData(
        "Item", IC.progression, 109, 1, 109
    ),
    "Magcargo Friendship": PokeparkItemData(
        "Item", IC.progression, 110, 1, 110
    ),
    "Torkoal Friendship": PokeparkItemData(
        "Item", IC.progression, 111, 1, 111
    ),
    "Golem Friendship": PokeparkItemData(
        "Item", IC.progression, 112, 1, 112
    ),
    "Quilava Friendship": PokeparkItemData(
        "Item", IC.progression, 113, 1, 113
    ),
    "Baltoy Friendship": PokeparkItemData(
        "Item", IC.progression, 114, 1, 114
    ),
    "Claydol Friendship": PokeparkItemData(
        "Item", IC.progression, 115, 1, 115
    ),
    "Ponyta Friendship": PokeparkItemData(
        "Item", IC.progression, 116, 1, 116
    ),
    "Rhyperior Friendship": PokeparkItemData(
        "Item", IC.progression, 117, 1, 117
    ),
    "Torchic Friendship": PokeparkItemData(
        "Item", IC.progression, 118, 1, 118
    ),
    "Blaziken Friendship": PokeparkItemData(
        "Item", IC.progression, 119, 1, 119
    ),
    "Murkrow Friendship": PokeparkItemData(
        "Item", IC.progression, 120, 1, 120
    ),
    "Honchkrow Friendship": PokeparkItemData(
        "Item", IC.progression, 121, 1, 121
    ),
    "Gliscor Friendship": PokeparkItemData(
        "Item", IC.progression, 122, 1, 122
    ),
    "Drifloon Friendship": PokeparkItemData(
        "Item", IC.progression, 123, 1, 123
    ),
    "Kakuna Friendship": PokeparkItemData(
        "Item", IC.progression, 124, 1, 124
    ),
    "Metapod Friendship": PokeparkItemData(
        "Item", IC.progression, 125, 1, 125
    ),
    "Tangrowth Friendship": PokeparkItemData(
        "Item", IC.progression, 126, 1, 126
    ),
    "Riolu Friendship": PokeparkItemData(
        "Item", IC.progression, 127, 1, 127
    ),
    "Sableye Friendship": PokeparkItemData(
        "Item", IC.progression, 128, 1, 128
    ),
    "Spinarak Friendship": PokeparkItemData(
        "Item", IC.progression, 129, 1, 129
    ),
    "Breloom Friendship": PokeparkItemData(
        "Item", IC.progression, 130, 1, 130
    ),
    "Pichu Friendship": PokeparkItemData(
        "Item", IC.progression, 131, 1, 131
    ),
    "Misdreavus Friendship": PokeparkItemData(
        "Item", IC.progression, 132, 1, 132
    ),
    "Mismagius Friendship": PokeparkItemData(
        "Item", IC.progression, 133, 1, 133
    ),
    "Elekid Friendship": PokeparkItemData(
        "Item", IC.progression, 134, 1, 134
    ),
    "Electabuzz Friendship": PokeparkItemData(
        "Item", IC.progression, 135, 1, 135
    ),
    "Luxray Friendship": PokeparkItemData(
        "Item", IC.progression, 136, 1, 136
    ),
    "Stunky Friendship": PokeparkItemData(
        "Item", IC.progression, 137, 1, 137
    ),
    "Skuntank Friendship": PokeparkItemData(
        "Item", IC.progression, 138, 1, 138
    ),
    "Voltorb Friendship": PokeparkItemData(
        "Item", IC.progression, 139, 1, 139
    ),
    "Electrode Friendship": PokeparkItemData(
        "Item", IC.progression, 140, 1, 140
    ),
    "Umbreon Friendship": PokeparkItemData(
        "Item", IC.progression, 141, 1, 141
    ),
    "Espeon Friendship": PokeparkItemData(
        "Item", IC.progression, 142, 1, 142
    ),
    "Gastly Friendship": PokeparkItemData(
        "Item", IC.progression, 143, 1, 143
    ),
    "Haunter Friendship": PokeparkItemData(
        "Item", IC.progression, 144, 1, 144
    ),
    "Gengar Friendship": PokeparkItemData(
        "Item", IC.progression, 145, 1, 145
    ),
    "Duskull Friendship": PokeparkItemData(
        "Item", IC.progression, 146, 1, 146
    ),
    "Dusknoir Friendship": PokeparkItemData(
        "Item", IC.progression, 147, 1, 147
    ),
    "Charizard Friendship": PokeparkItemData(
        "Item", IC.progression, 148, 1, 148
    ),
    "Flygon Friendship": PokeparkItemData(
        "Item", IC.progression, 149, 1, 149
    ),
    "Porygon-Z Friendship": PokeparkItemData(
        "Item", IC.progression, 150, 1, 150
    ),
    "Bronzor Friendship": PokeparkItemData(
        "Item", IC.progression, 151, 1, 151
    ),
    "Togekiss Friendship": PokeparkItemData(
        "Item", IC.progression, 152, 1, 152
    ),
    "Arcanine Friendship": PokeparkItemData(
        "Item", IC.progression, 153, 1, 153
    ),
    "Lopunny Friendship": PokeparkItemData(
        "Item", IC.progression, 154, 1, 154
    ),
    "Furret Friendship": PokeparkItemData(
        "Item", IC.progression, 155, 1, 155
    ),
    "Staraptor Friendship": PokeparkItemData(
        "Item", IC.progression, 156, 1, 156
    ),
    "Skorupi Friendship": PokeparkItemData(
        "Item", IC.progression, 157, 1, 157
    ),
    "Eevee Friendship": PokeparkItemData(
        "Item", IC.progression, 158, 1, 158
    ),
    "Hoppip Friendship": PokeparkItemData(
        "Item", IC.progression, 159, 1, 159
    ),
    "Jumpluff Friendship": PokeparkItemData(
        "Item", IC.progression, 160, 1, 160
    ),
    "Aerodactyl Friendship": PokeparkItemData(
        "Item", IC.progression, 161, 1, 161
    ),
    "Jolteon Friendship": PokeparkItemData(
        "Item", IC.progression, 162, 1, 162
    ),
    "Tyranitar Friendship": PokeparkItemData(
        "Item", IC.progression, 163, 1, 163
    ),
    "Garchomp Friendship": PokeparkItemData(
        "Item", IC.progression, 164, 1, 164
    ),
    "Absol Friendship": PokeparkItemData(
        "Item", IC.progression, 165, 1, 165
    ),
    "Salamence Friendship": PokeparkItemData(
        "Item", IC.progression, 166, 1, 166
    ),
    "Bellossom Friendship": PokeparkItemData(
        "Item", IC.progression, 167, 1, 167
    ),
    "Budew Friendship": PokeparkItemData(
        "Item", IC.progression, 168, 1, 168
    ),
    "Skiploom Friendship": PokeparkItemData(
        "Item", IC.progression, 169, 1, 169
    ),
    "Cyndaquil Friendship": PokeparkItemData(
        "Item", IC.progression, 170, 1, 170
    ),
    "Mareep Friendship": PokeparkItemData(
        "Item", IC.progression, 171, 1, 171
    ),
    "Dragonite Friendship": PokeparkItemData(
        "Item", IC.progression, 172, 1, 172
    ),
    "Lucario Friendship": PokeparkItemData(
        "Item", IC.progression, 173, 1, 173
    ),
    "Rayquaza Friendship": PokeparkItemData(
        "Item", IC.progression, 174, 1, 174
    ),
    "Drifblim Friendship": PokeparkItemData(
        "Item", IC.progression, 175, 1, 175
    ),
    "Burmy Friendship": PokeparkItemData(
        "Item", IC.progression, 176, 1, 176
    ),
    "Mime Jr. Friendship": PokeparkItemData(
        "Item", IC.progression, 177, 1, 177
    ),
    "Abra Friendship": PokeparkItemData(
        "Item", IC.progression, 178, 1, 178
    ),
    "Mew Friendship": PokeparkItemData(
        "Item", IC.progression, 179, 1, 179
    ),
    "Jirachi Friendship": PokeparkItemData(
        "Item", IC.progression, 180, 1, 180
    ),
    "Manaphy Friendship": PokeparkItemData(
        "Item", IC.progression, 181, 1, 181
    ),
    "Latias Friendship": PokeparkItemData(
        "Item", IC.progression, 182, 1, 182
    ),
    "Suicune Friendship": PokeparkItemData(
        "Item", IC.progression, 183, 1, 183
    ),
    "Metagross Friendship": PokeparkItemData(
        "Item", IC.progression, 184, 1, 184
    ),
    "Heatran Friendship": PokeparkItemData(
        "Item", IC.progression, 185, 1, 185
    ),
    "Groudon Friendship": PokeparkItemData(
        "Item", IC.progression, 186, 1, 186
    ),
    "Celebi Friendship": PokeparkItemData(
        "Item", IC.progression, 187, 1, 187
    ),
    "Darkrai Friendship": PokeparkItemData(
        "Item", IC.progression, 188, 1, 188
    ),
    "Rotom Friendship": PokeparkItemData(
        "Item", IC.progression, 189, 1, 189
    ),
    "Shaymin Friendship": PokeparkItemData(
        "Item", IC.progression, 190, 1, 190
    ),
    "Latios Friendship": PokeparkItemData(
        "Item", IC.progression, 191, 1, 191
    ),
    "Deoxys Friendship": PokeparkItemData(
        "Item", IC.progression, 192, 1, 192
    ),

    "Tropius Unlock": PokeparkItemData(
        "Item", IC.progression, 193, 1, 193
    ),
    "Pachirisu Unlock": PokeparkItemData(
        "Item", IC.progression, 194, 1, 194
    ),
    "Bonsly Unlock": PokeparkItemData(
        "Item", IC.progression, 195, 1, 195
    ),
    "Sudowoodo Unlock": PokeparkItemData(
        "Item", IC.progression, 196, 1, 196
    ),
    "Lotad Unlock": PokeparkItemData(
        "Item", IC.progression, 197, 1, 197
    ),
    "Shinx Unlock": PokeparkItemData(
        "Item", IC.progression, 198, 1, 198
    ),
    "Scyther Unlock": PokeparkItemData(
        "Item", IC.progression, 199, 1, 199
    ),
    "Caterpie Unlock": PokeparkItemData(
        "Item", IC.progression, 200, 1, 200
    ),
    "Butterfree Unlock": PokeparkItemData(
        "Item", IC.progression, 201, 1, 201
    ),
    "Chimchar Unlock": PokeparkItemData(
        "Item", IC.progression, 202, 1, 202
    ),
    "Ambipom Unlock": PokeparkItemData(
        "Item", IC.progression, 203, 1, 203
    ),
    "Weedle Unlock": PokeparkItemData(
        "Item", IC.progression, 204, 1, 204
    ),
    "Shroomish Unlock": PokeparkItemData(
        "Item", IC.progression, 205, 1, 205
    ),
    "Magikarp Unlock": PokeparkItemData(
        "Item", IC.progression, 206, 1, 206
    ),
    "Bidoof Unlock": PokeparkItemData(
        "Item", IC.filler, 207, 1, 207
    ),
    "Bidoof 2 Unlock": PokeparkItemData(
        "Item", IC.filler, 208, 1, 208
    ),
    "Bidoof 3 Unlock": PokeparkItemData(
        "Item", IC.filler, 209, 1, 209
    ),
    "Beach Bidoof Unlock": PokeparkItemData(
        "Item", IC.filler, 210, 1, 210
    ),
    "Bibarel Unlock": PokeparkItemData(
        "Item", IC.progression, 211, 1, 211
    ),
    "Starly Unlock": PokeparkItemData(
        "Item", IC.progression, 212, 1, 212
    ),
    "Starly 2 Unlock": PokeparkItemData(
        "Item", IC.progression, 213, 1, 213
    ),
    "Torterra Unlock": PokeparkItemData(
        "Item", IC.progression, 214, 1, 214
    ),
    "Floatzel Unlock": PokeparkItemData(
        "Item", IC.progression, 215, 1, 215
    ),
    "Mudkip Unlock": PokeparkItemData(
        "Item", IC.progression, 216, 1, 216
    ),
    "Totodile Unlock": PokeparkItemData(
        "Item", IC.progression, 217, 1, 217
    ),
    "Golduck Unlock": PokeparkItemData(
        "Item", IC.progression, 218, 1, 218
    ),
    "Krabby Unlock": PokeparkItemData(
        "Item", IC.progression, 219, 1, 219
    ),
    "Corphish Unlock": PokeparkItemData(
        "Item", IC.progression, 220, 1, 220
    ),
    "Delibird Unlock": PokeparkItemData(
        "Item", IC.progression, 221, 1, 221
    ),
    "Squirtle Unlock": PokeparkItemData(
        "Item", IC.progression, 222, 1, 222
    ),
    "Smoochum Unlock": PokeparkItemData(
        "Item", IC.progression, 223, 1, 223
    ),
    "Sneasel Unlock": PokeparkItemData(
        "Item", IC.progression, 224, 1, 224
    ),
    "Mamoswine Unlock": PokeparkItemData(
        "Item", IC.progression, 225, 1, 225
    ),
    "Glalie Unlock": PokeparkItemData(
        "Item", IC.progression, 226, 1, 226
    ),
    "Primeape Unlock": PokeparkItemData(
        "Item", IC.progression, 227, 1, 227
    ),
    "Ursaring Unlock": PokeparkItemData(
        "Item", IC.progression, 228, 1, 228
    ),
    "Magnemite Unlock": PokeparkItemData(
        "Item", IC.progression, 229, 1, 229
    ),
    "Machamp Unlock": PokeparkItemData(
        "Item", IC.filler, 230, 1, 230
    ),
    "Magnemite 2 Unlock": PokeparkItemData(
        "Item", IC.progression, 231, 1, 231
    ),
    "Magnemite 3 Unlock": PokeparkItemData(
        "Item", IC.progression, 232, 1, 232
    ),
    "Diglett Unlock": PokeparkItemData(
        "Item", IC.progression, 233, 1, 233
    ),
    "Magnezone Unlock": PokeparkItemData(
        "Item", IC.progression, 234, 1, 234
    ),
    "Phanpy Unlock": PokeparkItemData(
        "Item", IC.progression, 235, 1, 235
    ),
    "Raichu Unlock": PokeparkItemData(
        "Item", IC.progression, 236, 1, 236
    ),
    "Infernape Unlock": PokeparkItemData(
        "Item", IC.progression, 237, 1, 237
    ),
    "Ninetales Unlock": PokeparkItemData(
        "Item", IC.progression, 238, 1, 238
    ),
    "Ponyta Unlock": PokeparkItemData(
        "Item", IC.progression, 239, 1, 239
    ),
    "Torkoal Unlock": PokeparkItemData(
        "Item", IC.progression, 240, 1, 240
    ),
    "Golem Unlock": PokeparkItemData(
        "Item", IC.progression, 241, 1, 241
    ),
    "Baltoy Unlock": PokeparkItemData(
        "Item", IC.progression, 242, 1, 242
    ),
    "Claydol Unlock": PokeparkItemData(
        "Item", IC.progression, 243, 1, 243
    ),
    "Hitmonchan Unlock": PokeparkItemData(
        "Item", IC.progression, 244, 1, 244
    ),
    "Hitmonlee Unlock": PokeparkItemData(
        "Item", IC.progression, 245, 1, 245
    ),
    "Honchkrow Unlock": PokeparkItemData(
        "Item", IC.progression, 246, 1, 246
    ),
    "Metapod Unlock": PokeparkItemData(
        "Item", IC.progression, 247, 1, 247
    ),
    "Kakuna Unlock": PokeparkItemData(
        "Item", IC.progression, 248, 1, 248
    ),
    "Voltorb Unlock": PokeparkItemData(
        "Item", IC.progression, 249, 1, 249
    ),
    "Elekid Unlock": PokeparkItemData(
        "Item", IC.progression, 250, 1, 250
    ),
    "Electabuzz Unlock": PokeparkItemData(
        "Item", IC.progression, 251, 1, 251
    ),
    "Luxray Unlock": PokeparkItemData(
        "Item", IC.progression, 252, 1, 252
    ),
    "Stunky Unlock": PokeparkItemData(
        "Item", IC.progression, 253, 1, 253
    ),
    "Skuntank Unlock": PokeparkItemData(
        "Item", IC.progression, 254, 1, 254
    ),
    "Breloom Unlock": PokeparkItemData(
        "Item", IC.progression, 255, 1, 255
    ),
    "Mismagius Unlock": PokeparkItemData(
        "Item", IC.progression, 256, 1, 256
    ),
    "Electrode Unlock": PokeparkItemData(
        "Item", IC.progression, 257, 1, 257
    ),
    "Haunter Unlock": PokeparkItemData(
        "Item", IC.progression, 258, 1, 258
    ),
    "Gastly Unlock": PokeparkItemData(
        "Item", IC.progression, 259, 1, 259
    ),
    "Gastly 2 Unlock": PokeparkItemData(
        "Item", IC.progression, 260, 1, 260
    ),
    "Dusknoir Unlock": PokeparkItemData(
        "Item", IC.progression, 261, 1, 261
    ),
    "Espeon Unlock": PokeparkItemData(
        "Item", IC.progression, 262, 1, 262
    ),
    "Gengar Unlock": PokeparkItemData(
        "Item", IC.progression, 263, 1, 263
    ),
    "Blastoise Unlock": PokeparkItemData(
        "Item", IC.progression, 264, 1, 264
    ),
    "Electivire Unlock": PokeparkItemData(
        "Item", IC.progression, 265, 1, 265
    ),
    "Magmortar Unlock": PokeparkItemData(
        "Item", IC.progression, 266, 1, 266
    ),
    "Jolteon Unlock": PokeparkItemData(
        "Item", IC.progression, 267, 1, 267
    ),
    "Aerodactyl Unlock": PokeparkItemData(
        "Item", IC.progression, 268, 1, 268
    ),
    "Tyranitar Unlock": PokeparkItemData(
        "Item", IC.progression, 269, 1, 269
    ),
    "Garchomp Unlock": PokeparkItemData(
        "Item", IC.progression, 270, 1, 270
    ),
    "Rayquaza Unlock": PokeparkItemData(
        "Item", IC.progression, 271, 1, 271
    ),
    "Celebi Unlock": PokeparkItemData(
        "Item", IC.filler, 272, 1, 272
    ),
    "Darkrai Unlock": PokeparkItemData(
        "Item", IC.filler, 273, 1, 273
    ),
    "Groudon Unlock": PokeparkItemData(
        "Item", IC.filler, 274, 1, 274
    ),
    "Jirachi Unlock": PokeparkItemData(
        "Item", IC.filler, 275, 1, 275
    ),
    "Pikachu Balloon": PokeparkItemData(
        "Item", IC.progression, 276, 1, 276
    ),
    "Pikachu Surfboard": PokeparkItemData(
        "Item", IC.progression, 277, 1, 277
    ),
    "Pikachu Snowboard": PokeparkItemData(
        "Item", IC.progression, 278, 1, 278
    ),
    "10 Berries": PokeparkItemData(
        "Item", IC.filler, 279, 1, 279
    ),
    "20 Berries": PokeparkItemData(
        "Item", IC.filler, 280, 1, 280
    ),
    "50 Berries": PokeparkItemData(
        "Item", IC.filler, 281, 1, 281
    ),
    "100 Berries": PokeparkItemData(
        "Item", IC.filler, 282, 1, 282
    ),
    "Bulbasaur Prisma": PokeparkItemData(
        "Item", IC.progression, 283, 1, 283
    ),
    "Venusaur Prisma": PokeparkItemData(
        "Item", IC.progression, 284, 1, 284
    ),
    "Pelipper Prisma": PokeparkItemData(
        "Item", IC.progression, 285, 1, 285
    ),
    "Gyarados Prisma": PokeparkItemData(
        "Item", IC.progression, 286, 1, 286
    ),
    "Empoleon Prisma": PokeparkItemData(
        "Item", IC.progression, 287, 1, 287
    ),
    "Bastiodon Prisma": PokeparkItemData(
        "Item", IC.progression, 288, 1, 288
    ),
    "Rhyperior Prisma": PokeparkItemData(
        "Item", IC.progression, 289, 1, 289
    ),
    "Blaziken Prisma": PokeparkItemData(
        "Item", IC.progression, 290, 1, 290
    ),
    "Tangrowth Prisma": PokeparkItemData(
        "Item", IC.progression, 291, 1, 291
    ),
    "Dusknoir Prisma": PokeparkItemData(
        "Item", IC.progression, 292, 1, 292
    ),
    "Rotom Prisma": PokeparkItemData(
        "Item", IC.progression, 293, 1, 293
    ),
    "Absol Prisma": PokeparkItemData(
        "Item", IC.progression, 294, 1, 294
    ),
    "Salamence Prisma": PokeparkItemData(
        "Item", IC.progression, 295, 1, 295
    ),
    "Rayquaza Prisma": PokeparkItemData(
        "Item", IC.progression, 296, 1, 296
    ),
    "Progressive Dash": PokeparkItemData(
        "Item", IC.progression, 297, 4, 297
    ),
    "Progressive Thunderbolt": PokeparkItemData(
        "Item", IC.progression, 298, 4, 298
    ),
    "Progressive Health": PokeparkItemData(
        "Item", IC.progression, 299, 3, 299
    ),
    "Progressive Iron Tail": PokeparkItemData(
        "Item", IC.progression, 300, 3, 300
    ),
    "Double Dash": PokeparkItemData(
        "Item", IC.useful, 301, 1, 301
    ),
    "Meadow Zone Fast Travel": PokeparkItemData(
        "Item", IC.useful, 302, 1, 302
    ),
    "Beach Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 303, 1, 303
    ),
    "Ice Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 304, 1, 304
    ),
    "Cavern Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 305, 1, 305
    ),
    "Magma Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 306, 1, 306
    ),
    "Haunted Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 307, 1, 307
    ),
    "Granite Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 308, 1, 308
    ),
    "Flower Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 309, 1, 309
    ),

    "Beach Bridge 1 Unlock": PokeparkItemData(
        "Item", IC.progression, 310, 1, 310
    ),
    "Beach Bridge 2 Unlock": PokeparkItemData(
        "Item", IC.progression, 311, 1, 311
    ),
    "Magma Zone Fire Wall Unlock": PokeparkItemData(
        "Item", IC.progression, 312, 1, 312
    ),
    "Haunted Zone Mansion Gem Doors Unlock": PokeparkItemData(
        "Item", IC.progression, 313, 1, 313
    ),
    "Ice Zone Frozen Lake Unlock": PokeparkItemData(
        "Item", IC.progression, 314, 1, 314
    ),
    "Ice Zone Lift Unlock": PokeparkItemData(
        "Item", IC.progression, 315, 1, 315
    ),
    "Victory": PokeparkItemData(
        "Event", IC.progression, None, 1, None
    ),
    "Glitched Item": PokeparkItemData(
        "Event", IC.progression_skip_balancing, None, 1, None
    )
}
LOOKUP_ID_TO_NAME: dict[int, str] = {
    PokeparkItem.get_apid(data.code): item for item, data in ITEM_TABLE.items() if data.code is not None
}

item_name_groups = {

}
_simple_groups = {
    ("Friendship Items", "Friendship"),
    ("Unlock Items", "Unlock"),
    ("Prisma Items", "Prisma"),
    ("Fast Travel Items", "Fast Travel")
}

for basename, substring in _simple_groups:
    if basename not in item_name_groups:
        item_name_groups[basename] = set()
    for itemname in ITEM_TABLE:
        if substring in itemname:
            item_name_groups[basename].add(itemname)

TOTAL_FRIENDSHIP_ITEMS = 193

static_progressive_items = [
    "Bulbasaur Prisma",
    "Venusaur Prisma",
    "Pelipper Prisma",
    "Gyarados Prisma",
    "Empoleon Prisma",
    "Bastiodon Prisma",
    "Rhyperior Prisma",
    "Blaziken Prisma",
    "Tangrowth Prisma",
    "Dusknoir Prisma",
    "Rotom Prisma",
    "Absol Prisma",
    "Salamence Prisma",
    "Rayquaza Prisma",

    "Meadow Zone Fast Travel",
    "Beach Zone Fast Travel",
    "Ice Zone Fast Travel",
    "Cavern Zone Fast Travel",
    "Magma Zone Fast Travel",
    "Haunted Zone Fast Travel",
    "Granite Zone Fast Travel",
    "Flower Zone Fast Travel",

    "Beach Bridge 1 Unlock",
    "Beach Bridge 2 Unlock",
    "Magma Zone Fire Wall Unlock",
    "Haunted Zone Mansion Gem Doors Unlock",
    "Ice Zone Lift Unlock",
    "Ice Zone Frozen Lake Unlock",

]
static_useful_items = {
    "Double Dash",
    "Progressive Dash",
    "Progressive Thunderbolt",
    "Progressive Iron Tail",
    "Progressive Health"
}

fast_travel_items = [
    "Meadow Zone Fast Travel",
    "Beach Zone Fast Travel",
    "Ice Zone Fast Travel",
    "Cavern Zone Fast Travel",
    "Magma Zone Fast Travel",
    "Haunted Zone Fast Travel",
    "Granite Zone Fast Travel",
    "Flower Zone Fast Travel",
]
road_block_items = [
    "Beach Bridge 1 Unlock",
    "Beach Bridge 2 Unlock",
    "Magma Zone Fire Wall Unlock",
    "Haunted Zone Mansion Gem Doors Unlock",
    "Ice Zone Lift Unlock",
    "Ice Zone Frozen Lake Unlock",
]

option_to_progression: dict[tuple[str, int], (int, list[str])] = {
    ("remove_legendary_pokemon_power_comp_locations", 0): (0, [
        "Celebi Unlock",
        "Groudon Unlock",
        "Darkrai Unlock",
        "Jirachi Unlock",

        "Progressive Health",
        "Progressive Iron Tail",
        "Progressive Thunderbolt",
        "Progressive Dash"
    ]),
    ("remove_power_training_locations", 0): (0, [
        "Golem Unlock",
        "Progressive Dash"
    ]),
    ("remove_battle_power_comp_locations", 0): (60, [
        "Lotad Unlock",
        "Weedle Unlock",
        "Bibarel Unlock",
        "Torterra Unlock",
        "Scyther Unlock",
        "Chimchar Unlock",
        "Ambipom Unlock",
        "Totodile Unlock",
        "Golduck Unlock",
        "Blastoise Unlock",
        "Floatzel Unlock",
        "Corphish Unlock",
        "Smoochum Unlock",
        "Squirtle Unlock",
        "Primeape Unlock",
        "Ursaring Unlock",
        "Mamoswine Unlock",
        "Magnezone Unlock",
        "Hitmonlee Unlock",
        "Electivire Unlock",
        "Infernape Unlock",
        "Torkoal Unlock",
        "Hitmonchan Unlock",
        "Magmortar Unlock",
        "Baltoy Unlock",
        "Honchkrow Unlock",
        "Electabuzz Unlock",
        "Voltorb Unlock",
        "Skuntank Unlock",
        "Breloom Unlock",
        "Mismagius Unlock",
        "Gengar Unlock",
        "Aerodactyl Unlock",
        "Tyranitar Unlock",
        "Garchomp Unlock",
        "Claydol Unlock",
        "Glalie Unlock",

        "Progressive Health",
        "Progressive Iron Tail",
        "Progressive Thunderbolt",
        "Progressive Dash"
    ]),
    ("remove_chase_power_comp_locations", 0): (100, [
        "Pachirisu Unlock",
        "Shinx Unlock",
        "Caterpie Unlock",
        "Butterfree Unlock",
        "Magikarp Unlock",
        "Shroomish Unlock",
        "Starly Unlock",
        "Starly 2 Unlock",
        "Krabby Unlock",
        "Sneasel Unlock",
        "Raichu Unlock",
        "Ninetales Unlock",
        "Ponyta Unlock",
        "Espeon Unlock",
        "Luxray Unlock",
        "Stunky Unlock",
        "Haunter Unlock",
        "Gastly Unlock",
        "Gastly 2 Unlock",
        "Jolteon Unlock",
        "Progressive Dash"
    ]),
    ("remove_hide_and_seek_power_comp_locations", 0): (0, [
        "Bonsly Unlock",
        "Sudowoodo Unlock",
        "Mudkip Unlock",
        "Elekid Unlock"
    ]),
    ("remove_errand_power_comp_locations", 0): (0, [
        "Tropius Unlock",
        "Phanpy Unlock",
        "Progressive Thunderbolt",
        "Mankey Friendship",
        "Delibird Unlock",
        "Spheal Friendship",
        "Teddiursa Friendship",
        "Squirtle Unlock",
        "Squirtle Friendship",
        "Smoochum Friendship",
        "Smoochum Unlock",
        "Glalie Unlock",
        "Progressive Thunderbolt",
        "Progressive Dash"
    ]),
    ("remove_misc_power_comp_locations", 0): (80, [
        "Magnemite Unlock",
        "Magnemite 2 Unlock",
        "Magnemite 3 Unlock",
        "Electrode Unlock",
        "Golem Unlock",
        "Metapod Unlock",
        "Kakuna Unlock",
        "Diglett Unlock",
        "Dusknoir Unlock",
        "Rayquaza Unlock",
        "Progressive Dash"

    ]),
    ("goal", 1): (193, []),  # option postgame
    ("goal", 0): (0, [  # option mew
        "Progressive Health",
        "Progressive Iron Tail",
        "Progressive Thunderbolt",
        "Progressive Dash"
    ]),
    ("remove_attraction_locations", 0): (80, [
        "Turtwig Friendship",
        "Munchlax Friendship",
        "Chimchar Friendship",
        "Treecko Friendship",
        "Bibarel Friendship",
        "Bulbasaur Friendship",
        "Bidoof Friendship",
        "Oddish Friendship",
        "Shroomish Friendship",
        "Bonsly Friendship",
        "Lotad Friendship",
        "Weedle Friendship",
        "Caterpie Friendship",
        "Magikarp Friendship",
        "Jolteon Friendship",
        "Arcanine Friendship",
        "Leafeon Friendship",
        "Scyther Friendship",
        "Ponyta Friendship",
        "Shinx Friendship",
        "Eevee Friendship",
        "Pachirisu Friendship",
        "Buneary Friendship",
        "Croagunk Friendship",
        "Mew Friendship",

        "Magikarp Friendship",
        "Munchlax Friendship",
        "Blaziken Friendship",
        "Infernape Friendship",
        "Lucario Friendship",
        "Primeape Friendship",
        "Tangrowth Friendship",
        "Ambipom Friendship",
        "Croagunk Friendship",
        "Mankey Friendship",
        "Aipom Friendship",
        "Chimchar Friendship",
        "Treecko Friendship",
        "Pachirisu Friendship",
        "Jirachi Friendship",

        "Staraptor Friendship",
        "Togekiss Friendship",
        "Honchkrow Friendship",
        "Gliscor Friendship",
        "Pelipper Friendship",
        "Staravia Friendship",
        "Pidgeotto Friendship",
        "Butterfree Friendship",
        "Tropius Friendship",
        "Murkrow Friendship",
        "Taillow Friendship",
        "Spearow Friendship",
        "Starly Friendship",
        "Wingull Friendship",
        "Latias Friendship",

        "Psyduck Friendship",
        "Azurill Friendship",
        "Slowpoke Friendship",
        "Empoleon Friendship",
        "Floatzel Friendship",
        "Feraligatr Friendship",
        "Golduck Friendship",
        "Vaporeon Friendship",
        "Prinplup Friendship",
        "Bibarel Friendship",
        "Buizel Friendship",
        "Corsola Friendship",
        "Piplup Friendship",
        "Lotad Friendship",
        "Manaphy Friendship",

        "Teddiursa Friendship",
        "Magikarp Friendship",
        "Empoleon Friendship",
        "Glaceon Friendship",
        "Blastoise Friendship",
        "Glalie Friendship",
        "Lapras Friendship",
        "Delibird Friendship",
        "Piloswine Friendship",
        "Prinplup Friendship",
        "Squirtle Friendship",
        "Piplup Friendship",
        "Quagsire Friendship",
        "Spheal Friendship",
        "Suicune Friendship",

        "Sableye Friendship",
        "Meowth Friendship",
        "Torchic Friendship",
        "Electivire Friendship",
        "Magmortar Friendship",
        "Hitmonlee Friendship",
        "Ursaring Friendship",
        "Mr. Mime Friendship",
        "Raichu Friendship",
        "Sudowoodo Friendship",
        "Charmander Friendship",
        "Gible Friendship",
        "Chimchar Friendship",
        "Magby Friendship",
        "Metagross Friendship",

        "Magnemite Friendship",
        "Rhyperior Friendship",
        "Tyranitar Friendship",
        "Hitmontop Friendship",
        "Flareon Friendship",
        "Venusaur Friendship",
        "Snorlax Friendship",
        "Torterra Friendship",
        "Magnezone Friendship",
        "Claydol Friendship",
        "Quilava Friendship",
        "Torkoal Friendship",
        "Baltoy Friendship",
        "Bonsly Friendship",
        "Heatran Friendship",

        "Geodude Friendship",
        "Phanpy Friendship",
        "Blaziken Friendship",
        "Garchomp Friendship",
        "Scizor Friendship",
        "Magmortar Friendship",
        "Hitmonchan Friendship",
        "Machamp Friendship",
        "Marowak Friendship",
        "Farfetch'd Friendship",
        "Cranidos Friendship",
        "Camerupt Friendship",
        "Bastiodon Friendship",
        "Mawile Friendship",
        "Groudon Friendship",

        "Meowth Friendship",
        "Pichu Friendship",
        "Lucario Friendship",
        "Infernape Friendship",
        "Blaziken Friendship",
        "Riolu Friendship",
        "Sneasel Friendship",
        "Raichu Friendship",
        "Ambipom Friendship",
        "Primeape Friendship",
        "Aipom Friendship",
        "Electabuzz Friendship",
        "Chimchar Friendship",
        "Croagunk Friendship",
        "Celebi Friendship",

        "Stunky Friendship",
        "Gengar Friendship",
        "Mismagius Friendship",
        "Scizor Friendship",
        "Espeon Friendship",
        "Dusknoir Friendship",
        "Umbreon Friendship",
        "Cranidos Friendship",
        "Skuntank Friendship",
        "Voltorb Friendship",
        "Gastly Friendship",
        "Duskull Friendship",
        "Misdreavus Friendship",
        "Krabby Friendship",
        "Darkrai Friendship",

        "Magnemite Friendship",
        "Porygon-Z Friendship",
        "Magnezone Friendship",
        "Gengar Friendship",
        "Magmortar Friendship",
        "Electivire Friendship",
        "Mismagius Friendship",
        "Claydol Friendship",
        "Electabuzz Friendship",
        "Haunter Friendship",
        "Abra Friendship",
        "Elekid Friendship",
        "Mr. Mime Friendship",
        "Baltoy Friendship",
        "Rotom Friendship",

        "Chikorita Friendship",
        "Absol Friendship",
        "Lucario Friendship",
        "Ponyta Friendship",
        "Ninetales Friendship",
        "Lopunny Friendship",
        "Espeon Friendship",
        "Infernape Friendship",
        "Breloom Friendship",
        "Riolu Friendship",
        "Furret Friendship",
        "Mareep Friendship",
        "Eevee Friendship",
        "Vulpix Friendship",
        "Shaymin Friendship",

        "Salamence Friendship",
        "Charizard Friendship",
        "Dragonite Friendship",
        "Flygon Friendship",
        "Aerodactyl Friendship",
        "Staraptor Friendship",
        "Honchkrow Friendship",
        "Gliscor Friendship",
        "Pidgeotto Friendship",
        "Togekiss Friendship",
        "Golbat Friendship",
        "Taillow Friendship",
        "Murkrow Friendship",
        "Zubat Friendship",
        "Latios Friendship",

        "Lucario Friendship",
        "Glaceon Friendship",
        "Luxray Friendship",
        "Mamoswine Friendship",
        "Infernape Friendship",
        "Floatzel Friendship",
        "Rhyperior Friendship",
        "Absol Friendship",
        "Breloom Friendship",
        "Mareep Friendship",
        "Cyndaquil Friendship",
        "Totodile Friendship",
        "Chikorita Friendship",
        "Mime Jr. Friendship",
        "Deoxys Friendship",

        "Dusknoir Unlock",
        "Rayquaza Unlock",
        "Pikachu Surfboard",
        "Pikachu Snowboard",
        "Pikachu Balloon",
    ]),
    ("remove_attraction_prisma_locations", 0): (80, [
        "Pikachu Surfboard",
        "Pikachu Snowboard",
        "Pikachu Balloon",
        "Dusknoir Unlock",
        "Rayquaza Unlock",

        "Deoxys Friendship",
        "Rotom Friendship",

    ]),
    ("remove_pokemon_unlock_locations", 0): (85, [
        "Progressive Dash",
        "Progressive Thunderbolt"
    ]),
    ("remove_quiz_power_comp_locations", 0): (85, [
        "Delibird Unlock"
    ])
}

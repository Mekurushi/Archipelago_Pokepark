from typing import Any

MAP_INDEX: dict[str, int] = {
    "Treehouse": 1,
    "Meadow Zone Main Area": 2,
    "Pokepark Entrance": 3,
    "Meadow Zone Venusaur Area": 4,
    "Beach Zone Main Area": 5,
    "Ice Zone Main Area": 6,
    "Ice Zone Empoleon Area": 7,
    "Cavern Zone Main Area": 8,
    "Magma Zone Main Area": 9,
    "Magma Zone Blaziken Area": 10,
    "Haunted Zone Main Area": 11,
    "Haunted Zone Mansion Area": 12,
    "Haunted Zone Rotom Area": 13,
    "Granite Zone Main Area": 14,
    "Flower Zone Main Area": 15,
    "Skygarden": 16,

    "Bulbasaur's Daring Dash Attraction": 17,
    "Venusaur's Vine Swing Attraction": 18,
    "Pelipper's Circle Circuit Attraction": 19,
    "Gyarados' Aqua Dash Attraction": 20,
    "Empoleon's Snow Slide Attraction": 21,
    "Bastiodon's Panel Crush Attraction": 22,
    "Rhyperior's Bumper Burn Attraction": 23,
    "Blaziken's Boulder Bash Attraction": 24,
    "Tangrowth's Swing-Along Attraction": 25,
    "Dusknoir's Speed Slam Attraction": 26,
    "Rotom's Spooky Shoot-'em-Up Attraction": 27,
    "Absol's Hurdle Bounce Attraction": 28,
    "Salamence's Sky Race Attraction": 29,
    "Rayquaza's Balloon Panic Attraction": 30,

}


class UTStuff:
    ut_can_gen_without_yaml = True
    glitches_item_name = "Glitched Item"
    found_entrances_datastorage_key = ["pokepark_event_location_{team}_{player}"]
    tracker_world: dict

    def __init__(self, *args, **kwargs):
        super(UTStuff, self).__init__(*args, **kwargs)
        self.tracker_world = {
            "external_pack_key": "ut_poptracker_path",
            "map_page_maps": "maps/maps.jsonc",
            "map_page_locations": ["locations/entrances/treehouse.jsonc",
                                   "locations/entrances/meadow_zone.jsonc",
                                   "locations/entrances/pokepark_entrance.jsonc",
                                   "locations/entrances/beach_zone.jsonc",
                                   "locations/entrances/ice_zone.jsonc",
                                   "locations/entrances/cavern_zone.jsonc",
                                   "locations/entrances/magma_zone.jsonc",
                                   "locations/entrances/haunted_zone.jsonc",
                                   "locations/entrances/granite_zone.jsonc",
                                   "locations/entrances/flower_zone.jsonc",
                                   "locations/entrances/skygarden.jsonc",
                                   "locations/overview.json",
                                   "ut_locations/overworld/treehouse.json",
                                   "ut_locations/overworld/skygarden.json",
                                   "ut_locations/overworld/meadow_zone.json",
                                   "ut_locations/overworld/beach_zone.json",
                                   "ut_locations/overworld/ice_zone.json",
                                   "ut_locations/overworld/cavern_zone.json",
                                   "ut_locations/overworld/magma_zone.json",
                                   "ut_locations/overworld/haunted_zone.json",
                                   "ut_locations/overworld/granite_zone.json",
                                   "ut_locations/overworld/flower_zone.json",
                                   "ut_locations/attractions/bulbasaur_daring_dash.json",
                                   "ut_locations/attractions/absol_hurdle_bounce.json",
                                   "ut_locations/attractions/bastiodon_panel_crush.json",
                                   "ut_locations/attractions/blaziken_boulder_bash.json",
                                   "ut_locations/attractions/dusknoir_speed_slam.json",
                                   "ut_locations/attractions/empoleon_snow_slide.json",
                                   "ut_locations/attractions/gyarados_aqua_dash.json",
                                   "ut_locations/attractions/pelipper_circle_circuit.json",
                                   "ut_locations/attractions/rayquaza_balloon_panic.json",
                                   "ut_locations/attractions/rhyperior_bumper_burn.json",
                                   "ut_locations/attractions/rotom_spooky_shoot.json",
                                   "ut_locations/attractions/salamence_sky_race.json",
                                   "ut_locations/attractions/tangrowth_swing_along.json",
                                   "ut_locations/attractions/venusaur_vine_swing.json"],
            "map_page_setting_key": "pokepark_map_{team}_{player}",
            "map_page_index": self.map_page_index,
            "poptracker_entrance_mapping": {
            }
        }

    def map_page_index(self, data: Any) -> int:
        return MAP_INDEX.get(data, 0)

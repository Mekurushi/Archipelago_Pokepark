import asyncio
import copy
import random
import textwrap
import time
import traceback
from typing import Optional, Any, Type

import dolphin_memory_engine as dme

import ModuleUpdate
import kvui
from worlds.pokepark import PokeparkItem, LOCATION_TABLE, VERSION
from worlds.pokepark.adresses import ATHLETIC_COMP_DEATH_CHECK_ADDRESSES, ATHLETIC_COMP_GIVE_DEATH_ADDRESSES, \
    ATTRACTION_ID_ADDRESSES, BATTLE_COMP_DEATH_CHECK_ADDRESSES, \
    BATTLE_COMP_GIVE_DEATH_ADDRESSES, CHASE_COMP_DEATH_CHECK_ADDRESSES, \
    CHASE_COMP_GIVE_DEATH_ADDRESSES, CLIENT_TEXT_BUFFER_SIZE, CLIENT_TEXT_TIMEOUT, CURRENT_STAGE_ADDRESSES, \
    GLOBAL_MANAGER_DATA_STRUC_ADDRESS, \
    GLOBAL_MANAGER_OPCODE_ADDR, \
    GLOBAL_MANAGER_PARAMETER1_ADDR, \
    GLOBAL_MANAGER_PARAMETER2_ADDR, HIDE_AND_SEEK_COMP_DEATH_CHECK_ADDRESSES, HIDE_AND_SEEK_COMP_GIVE_DEATH_ADDRESSES, \
    INGAME_LINE_LENGTH, IS_INITIALIZED_ADDRESSES, IS_IN_GAME_END_STATE_ADDRESSES, IS_IN_LOADING_SCREEN_ADDRESSES, \
    IS_IN_MAIN_MENU_ADDRESSES, \
    IS_IN_PAUSE_MENU_ADDRESSES, \
    NEXT_STAGE_ADDRESSES, POWER_MAP, \
    MemoryAddress, SCENE_NAME_ADDR, SCENE_PARAM1_ADDR, SLOT_NAME_ADDR, TEXT_BUFFER_ADDR
from worlds.pokepark.dme_helper import read_memory
from worlds.pokepark.items import LOOKUP_ID_TO_NAME, ITEM_TABLE, PokeparkPowerItemClientData
from worlds.pokepark.locations import MEW_GOAL_CODE, POSTGAME_PRISMA_GOAL_CODE
from worlds.pokepark.options import Goal

ModuleUpdate.update()

import Utils

from NetUtils import ClientStatus, NetworkItem
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, server_loop


def _check_universal_tracker_version() -> bool:
    import re
    if tracker_loaded:
        match = re.search(r"v\d+.(\d+).(\d+)", UT_VERSION)
        if len(match.groups()) < 2:
            return False
        if int(match.groups()[0]) < 2:
            return False
        if int(match.groups()[1]) < 12:
            return False
        return True
    return False


tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    from worlds.tracker import UT_VERSION

    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext


CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for Pokepark. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Pokepark is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."
AP_VISITED_STAGE_NAMES_KEY_FORMAT = "pokepark_visited_stages_%i"

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


class PokeparkCommandProcessor(ClientCommandProcessor):

    def __init__(self, ctx: SuperContext):
        """
        Initialize the command processor with the provided context.

        :param ctx: Context for the client.
        """
        super().__init__(ctx)

    def _cmd_dolphin(self) -> None:
        """
        Display the current Dolphin emulator connection status.
        """
        if isinstance(self.ctx, PokeparkContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, PokeparkContext):
            self.ctx.death_link_enabled = not self.ctx.death_link_enabled
            self.ctx.death_link_just_changed = True
            Utils.async_start(
                self.ctx.update_death_link(
                    self.ctx.death_link_enabled
                ), name="Update Deathlink"
            )
            logger.info(f"Deathlink is now {'enabled' if self.ctx.death_link_enabled else 'disabled'}")


class PokeparkContext(SuperContext):
    tags = {"AP"}
    command_processor = PokeparkCommandProcessor
    game = "PokePark"
    items_handling = 0b111  # full remote
    victory = False
    goal_code = None
    slot_data: dict[str, Any] | None = None
    death_link_enabled = False
    death_link_just_changed = False


    def __init__(self, server_address, password):
        super(PokeparkContext, self).__init__(server_address, password)
        self.items_received_2: list[tuple[NetworkItem, int]] = []
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False
        self.last_rcvd_index: int = -1
        self.visited_stage_names: Optional[set[str]] = None
        self.has_send_death: bool = False
        self.game_id: Optional[bytes] = None
        self.ingame_client_messages: list[tuple[float, str]] = []

    async def disconnect(self, allow_autoreconnect: bool = False) -> None:
        """
        Disconnect the client from the server and reset game state variables.

        :param allow_autoreconnect: Allow the client to auto-reconnect to the server. Defaults to `False`.

        """
        self.auth = None
        self.current_stage_name = ""
        self.visited_stage_names = None
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info("Awaiting connection to Dolphin to get player information.")
            return
        await self.send_connect()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.slot_data = args.get("slot_data", None)
            self.items_received_2 = []
            self.last_rcvd_index = -1
            if self.slot_data and self.slot_data.get("options", {}).get("death_link"):
                self.death_link_enabled = bool(self.slot_data["options"]["death_link"])
                Utils.async_start(self.update_death_link(bool(self.slot_data["options"]["death_link"])))
            if self.slot_data and self.slot_data.get("options", {}).get("goal") == Goal.option_mew:
                self.goal_code = MEW_GOAL_CODE
            if self.slot_data and self.slot_data.get("options", {}).get("goal") == Goal.option_postgame:
                self.goal_code = POSTGAME_PRISMA_GOAL_CODE
            # Request the connected slot's dictionary (used as a set) of visited stages.
            visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            Utils.async_start(self.send_msgs([{"cmd": "Get", "keys": [visited_stages_key]}]))
        elif cmd == "ReceivedItems":
            if args["index"] >= self.last_rcvd_index:
                self.last_rcvd_index = args["index"]
                for item in args["items"]:
                    self.items_received_2.append((item, self.last_rcvd_index))
                    self.last_rcvd_index += 1
            self.items_received_2.sort(key=lambda v: v[1])
        elif cmd == "Retrieved":
            requested_keys_dict = args["keys"]
            # Read the connected slot's dictionary (used as a set) of visited stages.
            if self.slot is not None:
                visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
                if visited_stages_key in requested_keys_dict:
                    visited_stages = requested_keys_dict[visited_stages_key]
                    # If it has not been set before, the value in the response will be `None`.
                    visited_stage_names = set() if visited_stages is None else set(visited_stages.keys())
                    # If the current stage name is not in the set, send a message to update the dictionary on the
                    # server.
                    current_stage_name = self.current_stage_name
                    if current_stage_name and current_stage_name not in visited_stage_names:
                        visited_stage_names.add(current_stage_name)
                        Utils.async_start(self.update_visited_stages(current_stage_name))
                    self.visited_stage_names = visited_stage_names

    def make_gui(self) -> Type["kvui.GameManager"]:
        from kvui import GameManager
        class PokeparkManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = f"Archipelago Pokepark Client v{'.'.join(map(str, VERSION))}"

        if not tracker_loaded:
            return PokeparkManager
        if not _check_universal_tracker_version():
            Utils.messagebox(
                "Universal Tracker needs to be updated",
                f"The minimum version of Universal Tracker required for Pokepark is v0.2.11. The version currently "
                f"installed is {UT_VERSION}.",
                error=True
            )
            return PokeparkManager

        class TrackerManager(super().make_gui()):
            logging_pairs = [("Client", "Archipelago")]
            base_title = f"Archipelago Pokepark Client v{'.'.join(map(str, VERSION))} with UT {UT_VERSION}"

        return TrackerManager

    def on_deathlink(self, data: dict[str, Any]) -> None:
        """
        Handle a DeathLink event.

        :param data: The data associated with the DeathLink event.
        """
        super().on_deathlink(data)
        Utils.async_start(_give_death(self))

    async def update_visited_stages(self, newly_visited_stage_name: str) -> None:
        """
        Update the server's data storage of the visited stage names to include the newly visited stage name.

        :param newly_visited_stage_name: The name of the stage recently visited.
        """
        if self.slot is not None:
            visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            await self.send_msgs(
                [
                    {
                        "cmd": "Set",
                        "key": visited_stages_key,
                        "default": {},
                        "want_reply": False,
                        "operations": [{"operation": "update", "value": {newly_visited_stage_name: True}}],
                    }
                ]
            )

    def forward_client_message(self, msg: str):
        lines = []
        for raw_line in msg.split("\n"):
            lines.extend(
                textwrap.wrap(
                    raw_line,
                    INGAME_LINE_LENGTH,
                )
            )

        timestamp = time.time()
        # We want to stagger the messages so large amounts of text can "scroll"
        # if they go over the character limit
        for line in lines:
            self.ingame_client_messages.append(
                (timestamp + len(self.ingame_client_messages) * 0.5, line)
            )

    async def show_messages_ingame(self) -> None:
        # Filter out old messages
        line_list = []
        filtered_msgs = []
        curr_timestamp = time.time()
        for tup in self.ingame_client_messages:
            if curr_timestamp - tup[0] > CLIENT_TEXT_TIMEOUT:
                continue

            filtered_msgs.append(tup)
            line_list.append(tup[1])

        self.ingame_client_messages = filtered_msgs

        if len(line_list) == 0:
            await self.write_string_to_buffer("")
        else:
            # Want to cap it at 16 lines so the text doesn't get too obtrusive
            # (which could happen if each line is quite short)
            await self.write_string_to_buffer("\n".join(line_list[:16]))

    def on_print_json(self, args: dict):
        # Don't show messages in-game for item sends irrelevant to this slot
        if not self.is_uninteresting_item_send(args):
            self.forward_client_message(
                self.rawjsontotextparser(copy.deepcopy(args["data"]))
            )

        super().on_print_json(args)

    async def write_string_to_buffer(self, text: str):
        if TEXT_BUFFER_ADDR[self.game_id] != 0x0:
            # Truncate text to fit in the buffer, then write to buffer
            text_bytes = text.encode("utf-8")[: CLIENT_TEXT_BUFFER_SIZE -
                                                1].ljust(
                CLIENT_TEXT_BUFFER_SIZE, b"\x00"
            )
            dme.write_bytes(TEXT_BUFFER_ADDR[self.game_id], text_bytes)


def _give_item(ctx: PokeparkContext, item_name: str) -> bool:
    """
    Give an item to the player in-game.

    :param ctx: The Pokepark client context.
    :param item_name: Name of the item to give.
    :return: Whether the item was successfully given.
    """
    if not check_ingame(ctx.game_id):
        return False

    item_slot = dme.read_word(GLOBAL_MANAGER_PARAMETER1_ADDR[ctx.game_id])
    opcode_slot = dme.read_word(GLOBAL_MANAGER_OPCODE_ADDR[ctx.game_id])
    item = ITEM_TABLE[item_name].client_data
    if item_slot == 0xFFFFFFFF and opcode_slot == 0xFFFFFFFF:

        if isinstance(item, PokeparkPowerItemClientData):
            index = sum(
                1 for item, idx in ctx.items_received_2
                if item.item == PokeparkItem.get_apid(ITEM_TABLE[item_name].code)
            )

            max_index = len(POWER_MAP[item_name])
            if index > max_index:
                index = max_index
            parameter1 = sum(POWER_MAP[item_name][:index])
            parameter2 = item.parameter2
            opcode = item.opcode

        else:
            parameter1 = item.parameter1
            parameter2 = item.parameter2
            opcode = item.opcode

        dme.write_bytes(item.flag_address, item.flag_name)
        dme.write_word(GLOBAL_MANAGER_PARAMETER2_ADDR[ctx.game_id], parameter2)
        # parameter 1 and opcode are trigger
        dme.write_word(
            GLOBAL_MANAGER_PARAMETER1_ADDR[ctx.game_id], parameter1
        )
        dme.write_word(GLOBAL_MANAGER_OPCODE_ADDR[ctx.game_id], opcode)

        return True

    return False


async def _give_death(ctx: PokeparkContext) -> None:
    """
    Trigger the player's death in-game by failing the current active Power Competition

    :param ctx: The Pokepark client context.
    """

    if (
            ctx.slot is not None
            and dme.is_hooked()
            and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
            and check_ingame(ctx.game_id)
    ):
        DEATH_SIGNAL = 0x0001.to_bytes(2, byteorder='big')
        ACTIVE_STATUS = 0x1

        COMP_MAPPINGS = [
            (BATTLE_COMP_DEATH_CHECK_ADDRESSES, BATTLE_COMP_GIVE_DEATH_ADDRESSES),
            (HIDE_AND_SEEK_COMP_DEATH_CHECK_ADDRESSES, HIDE_AND_SEEK_COMP_GIVE_DEATH_ADDRESSES),
            (CHASE_COMP_DEATH_CHECK_ADDRESSES, CHASE_COMP_GIVE_DEATH_ADDRESSES),
            (ATHLETIC_COMP_DEATH_CHECK_ADDRESSES, ATHLETIC_COMP_GIVE_DEATH_ADDRESSES),
        ]

        for check_addr, give_addr in COMP_MAPPINGS:
            if dme.read_byte(check_addr[ctx.game_id]) == ACTIVE_STATUS:
                dme.write_bytes(give_addr[ctx.game_id], DEATH_SIGNAL)

        await asyncio.sleep(1)

        if dme.read_word(SCENE_PARAM1_ADDR[ctx.game_id]) == 0xFFFFFFFF and check_ingame(ctx.game_id):
            if get_attraction_id(ctx.game_id) != 0xFFFFFFFF:
                dme.write_bytes(SCENE_NAME_ADDR[ctx.game_id], "Challenge".encode('ascii') + b'\x00')
                dme.write_word(SCENE_PARAM1_ADDR[ctx.game_id], 0)
                ctx.has_send_death = True
            else:
                current_stage = dme.read_word(CURRENT_STAGE_ADDRESSES[ctx.game_id])
                dme.write_word(NEXT_STAGE_ADDRESSES[ctx.game_id], current_stage)
                dme.write_bytes(SCENE_NAME_ADDR[ctx.game_id], "ZoneChange".encode('ascii') + b'\x00')
                dme.write_word(SCENE_PARAM1_ADDR[ctx.game_id], 1)
                ctx.has_send_death = True


async def give_items(ctx: PokeparkContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: Pokepark client context.
    """
    global_manager_data_struc_address = GLOBAL_MANAGER_DATA_STRUC_ADDRESS[ctx.game_id]
    chapter_address = global_manager_data_struc_address + 0x2d
    if check_ingame(ctx.game_id):
        # Read the expected index of the player, which is the index of the latest item they've received.
        expected_idx = int.from_bytes(dme.read_bytes(chapter_address, 2), byteorder="big")

        received_items = ctx.items_received
        if len(received_items) <= expected_idx:
            return

        # Loop through items to give.
        for idx, item in enumerate(received_items[expected_idx:], start=expected_idx):
            # If the item's index is greater than the player's expected index, give the player the item.
            if expected_idx <= idx:
                # Attempt to give the item and increment the expected index.
                while not _give_item(ctx, LOOKUP_ID_TO_NAME[item.item]):
                    await asyncio.sleep(0.01)

                # Increment the expected index.
                dme.write_bytes(chapter_address, (idx + 0x1).to_bytes(2, byteorder="big"))


async def check_current_stage_changed(ctx: PokeparkContext) -> None:
    """
    Check if the player has moved to a new stage.
    If so, update all trackers with the new stage name.
    If the stage has never been visited, additionally update the server.

    :param ctx: The Pokepark client context.
    """
    global_manager_data_struc_address = GLOBAL_MANAGER_DATA_STRUC_ADDRESS[ctx.game_id]
    new_stage = dme.read_bytes(global_manager_data_struc_address + 0x5F00, 2)
    new_stage_name = STAGE_NAME_MAP.get(new_stage)
    attraction_id = get_attraction_id(ctx.game_id)
    attraction_name = ATTRACTION_ID_MAP.get(attraction_id)
    if attraction_name:
        new_stage_name = attraction_name

    if new_stage_name:
        current_stage_name = ctx.current_stage_name
        if new_stage_name != current_stage_name:
            ctx.current_stage_name = new_stage_name
            # Send a Bounced message containing the new stage name to all trackers connected to the current slot.
            data_to_send = {"pokepark_stage_name": new_stage_name}
            message = {
                "cmd": "Bounce",
                "slots": [ctx.slot],
                "data": data_to_send,
            }
            await ctx.send_msgs([message])
            # If the stage has never been visited before, update the server's data storage to indicate that it has been
            # visited.
            visited_stage_names = ctx.visited_stage_names
            if visited_stage_names is not None and new_stage_name not in visited_stage_names:
                visited_stage_names.add(new_stage_name)
                await ctx.update_visited_stages(new_stage_name)


async def check_locations(ctx: PokeparkContext) -> None:
    """
    Iterate through all locations and check whether the player has checked each location.

    Update the server with all newly checked locations since the last update. If the player has completed the goal,
    notify the server.

    :param ctx: The Pokepark client context.
    """

    global_manager_data_struc_address = GLOBAL_MANAGER_DATA_STRUC_ADDRESS[ctx.game_id]
    for location, data in LOCATION_TABLE.items():
        client_data = data.client_data
        expected_value = client_data.expected_value
        memory = MemoryAddress(
            global_manager_data_struc_address,
            client_data.final_offset,
            memory_range=client_data.memory_range
        )
        current_value = read_memory(dme, memory)
        if client_data.is_progressive:
            is_checked = (current_value & client_data.bit_mask) >= expected_value
        else:
            is_checked = (current_value & client_data.bit_mask) == expected_value
        if is_checked:
            if data.code == ctx.goal_code:
                if not ctx.victory:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    if check_ingame(ctx.game_id):
                        pass
                        # dme.write_bytes(SCENE_NAME_ADDR[ctx.game_id], "Ending".encode('ascii') + b'\x00')
                        # dme.write_word(SCENE_PARAM1_ADDR[ctx.game_id], 1)
                    ctx.victory = True
            else:
                ctx.locations_checked.add(PokeparkItem.get_apid(data.code))

    # Send the list of newly-checked locations to the server.
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])


def read_string(console_address: int, strlen: int) -> str:
    """
    Read a string from Dolphin memory.

    :param console_address: Address to start reading from.
    :param strlen: Length of the string to read.
    :return: The string.
    """
    return dme.read_bytes(console_address, strlen).split(b"\0", 1)[0].decode()


def check_ingame(game_id: bytes) -> bool:
    """
    Check if the player is currently in-game.

    :return: `True` if the player is in-game, otherwise `False`.
    """
    if dme.read_byte(IS_INITIALIZED_ADDRESSES[game_id]) == 0:
        return False

    is_in_pause_menu = dme.read_byte(IS_IN_PAUSE_MENU_ADDRESSES[game_id]) == 0x1
    is_in_main_menu = dme.read_byte(IS_IN_MAIN_MENU_ADDRESSES[game_id]) == 0x1
    is_in_game_end_state = dme.read_byte(IS_IN_GAME_END_STATE_ADDRESSES[game_id]) == 0x1
    is_in_loading_screen = dme.read_byte(IS_IN_LOADING_SCREEN_ADDRESSES[game_id]) == 0x1

    return not (is_in_pause_menu or is_in_main_menu or
                is_in_game_end_state or is_in_loading_screen)


def get_attraction_id(game_id: bytes):
    attraction_id_address = ATTRACTION_ID_ADDRESSES[game_id]
    attraction_id = dme.read_word(attraction_id_address)
    return attraction_id


async def check_death(ctx: PokeparkContext) -> None:
    """
    Check if the player is currently dead in-game.
    If DeathLink is on, notify the server of the player's death.

    :return: `True` if the player is dead, otherwise `False`.
    """
    if ctx.death_link_just_changed:
        ctx.death_link_just_changed = False
        return
    if ctx.slot is not None and check_ingame(ctx.game_id):
        failed_status = {0x3, 0x4}
        battle_comp = dme.read_byte(BATTLE_COMP_DEATH_CHECK_ADDRESSES[ctx.game_id])
        hide_and_seek_comp = dme.read_byte(HIDE_AND_SEEK_COMP_DEATH_CHECK_ADDRESSES[ctx.game_id])
        chase_comp = dme.read_byte(CHASE_COMP_DEATH_CHECK_ADDRESSES[ctx.game_id])
        athletic_comp = dme.read_byte(ATHLETIC_COMP_DEATH_CHECK_ADDRESSES[ctx.game_id])
        if (battle_comp in failed_status or hide_and_seek_comp in failed_status or
                chase_comp in failed_status or athletic_comp in failed_status):
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 5:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " lost a friend.")
        else:
            ctx.has_send_death = False


async def dolphin_sync_task(ctx: PokeparkContext) -> None:
    """
    The task loop for managing the connection to Dolphin.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: The Pokepark client context.
    """

    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    sleep_time = 0.0
    while not ctx.exit_event.is_set():
        if sleep_time > 0.0:
            try:
                # ctx.watcher_event gets set when receiving ReceivedItems or LocationInfo, or when shutting down.
                await asyncio.wait_for(ctx.watcher_event.wait(), sleep_time)
            except asyncio.TimeoutError:
                pass
            sleep_time = 0.0
        ctx.watcher_event.clear()
        try:
            if dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                await ctx.show_messages_ingame()
                if not check_ingame(ctx.game_id):
                    # Reset the give item array while not in the game.
                    dme.write_bytes(GLOBAL_MANAGER_PARAMETER1_ADDR[ctx.game_id], bytes([0xFF] * 0xC))
                    sleep_time = 0.1
                    continue
                if ctx.slot is not None:
                    if ctx.death_link_enabled:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                    await check_current_stage_changed(ctx)
                else:
                    if not ctx.auth:
                        ctx.auth = read_string(SLOT_NAME_ADDR[ctx.game_id], 0x40)
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                sleep_time = 0.1
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dme.hook()
                if dme.is_hooked():
                    value = dme.read_bytes(0x80000000, 6)
                    if value not in (b"R8AJ99", b"R8AE99", b"R8AP99"):
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dme.un_hook()
                        sleep_time = 5
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.game_id = value
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    sleep_time = 5
                    continue
        except Exception:
            dme.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            sleep_time = 5
            continue


def main(connect=None, password=None):
    Utils.init_logging("PokeparkClient", exception_logger="Client")

    async def _main(connect, password):
        ctx = PokeparkContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        # Wake the sync task, if it is currently sleeping, so it can start shutting down when it sees that the
        # exit_event is set.
        await ctx.exit_event.wait()
        ctx.watcher_event.set()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await ctx.dolphin_sync_task

    import colorama
    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser(description="Pokepark Client, for text interfacing.")
    args, rest = parser.parse_known_args()
    main(args.connect, args.password)

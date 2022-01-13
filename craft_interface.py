import os
from util import get_micro
from data.db import get_itemdb, get_translations
from data.inventory import Inventory
from data.events.parser import parse_events

from ethercraft import Ethercraft

class BotInterface():
    
    def __init__(self):
        self.ec = Ethercraft()
        self.ec.load_contracts()

    def get_inventory(self, id):

        contract = self.ec.get_contract('character')

        inventory_integer = contract.caller.viewInventory(id)
        inventory = Inventory()
        for i in range(3, 78, 5):
            item_id = get_micro(inventory_integer, i, 3)
            item_count = get_micro(inventory_integer, i + 2, 2)
            inventory.add_items(item_id, item_count)
            # if item_id:
            #     desc = f"item id: {item_id}"
            #     if itemdb[item_id]:
            #         item_info = get_translations(itemdb[item_id])
            #         if item_info:
            #             desc = f"{item_info.get('name', 'unknown_name')}, {item_info.get('description', 'unknown_description')}"
            #     retval += f"{desc}\n\t\tcount: {item_count}\n"
        return inventory

    def get_equipment(self, id):
        contract = self.ec.get_contract('character')

        equipment_integer = contract.caller.viewEquipment(id)
        equipment_sets = [
            ('HELMET', 3, 3),
            ('CHEST', 6, 3),
            ('LOWER', 9, 3),
            ('BOOTS', 12, 3),
            ('LHAND', 27, 3),
            ('RHAND', 30, 3),
            ('GLOVES', 63, 3),
            ('LWRIST', 33, 3),
            ('RWRIST', 36, 3),
            ('AMULET', 15, 3),
            ('WAIST', 18, 3),
            ('CLOAK', 21, 3),
            ('BACKPACK', 24, 3),
            ('LRING1', 39, 3),
            ('RRING1', 42, 3),
            ('LRING2', 45, 3),
            ('RRING2', 48, 3),
            ('LRING3', 51, 3),
            ('RRING3', 54, 3),
            ('LRING4', 57, 3),
            ('RRING4', 60, 3)
        ]
        retval = ""
        for equipment in equipment_sets:
            equipment_id = get_micro(equipment_integer, equipment[1], equipment[2])
            if equipment_id:
                retval += f"{equipment_id} equipped on {equipment[0]}\n"
        return retval
    

    def get_run_info(self, run_ids):
        dungeon_contract_instance = self.ec.get_contract('dungeon')
        combat_contract_instance = self.ec.get_contract('combat')

        dungeon_events = [
            dungeon_contract_instance.events.FloorEntered,
            dungeon_contract_instance.events.EnteredRoom,
            dungeon_contract_instance.events.EffectEncountered,
            dungeon_contract_instance.events.EnemyEncountered,
            dungeon_contract_instance.events.TrapEncountered,
            dungeon_contract_instance.events.LootEncountered,
            dungeon_contract_instance.events.CreditsEncountered,
            dungeon_contract_instance.events.ExperienceGained
        ]

        combat_events = [
            combat_contract_instance.events.CombatEvent
        ]

        all_entries = []

        for event in dungeon_events:
            print(f"event: {event.event_name}")
            filter = event.createFilter(
                fromBlock='0x0',
                argument_filters={"_run": run_ids}
            )
            for i in filter.get_all_entries():
                all_entries.append(i)

        for event in combat_events:
            print(f"event: {event.event_name}")
            filter = event.createFilter(
                fromBlock='0x0',
                argument_filters={"_runID": run_ids}
            )
            for i in filter.get_all_entries():
                all_entries.append(i)

        all_entries.sort(key=lambda x: x['logIndex'])

        return all_entries

    async def view_runs(self):
        contract = self.ec.get_contract('character')

        for i in range(20):
            print( f"{i} - {contract.caller.viewRuns(i)}" )

# if __name__ == '__main__':

    # contract.caller.viewRuns(10)
    # # print(contract)
    # import asyncio
    # asyncio.run(view_runs())

    # get_run_info(contract.caller.viewRuns(5))
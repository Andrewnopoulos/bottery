from util import AttrDict

from data.events.types import *

def parse_events(sorted_event_list):
    messageLog = []
    encounters = []
    activeCombatEncounter = None

    for event in sorted_event_list:
        if event.event == 'CombatEvent':
            if not activeCombatEncounter:
                activeCombatEncounter = CombatEncounter(event)
            else:
                activeCombatEncounter.add_event(event)
        else:
            if activeCombatEncounter:
                encounters.append(activeCombatEncounter)
                activeCombatEncounter = None                

        if event.event == 'FloorEntered':
            encounters.append(EnteredFloorEvent(event))
        elif event.event == 'EnteredRoom':
            encounters.append(EnteredRoomEvent(event))
        elif event.event == 'EffectEncountered':
            encounters.append(EffectEvent(event))
        elif event.event == 'EnemyEncountered':
            encounters.append(EnemyEncounterEvent(event))
        elif event.event == 'TrapEncountered':
            encounters.append(TrapEvent(event))
        elif event.event == 'LootEncountered':
            encounters.append(LootEvent(event))
        elif event.event == 'CreditsEncountered':
            encounters.append(CreditsEvent(event))
        elif event.event == 'ExperienceGained':
            encounters.append(ExperienceEvent(event))
    if activeCombatEncounter:
        encounters.append(activeCombatEncounter)
        activeCombatEncounter = None

    for encounter in encounters:
        yield from encounter.get_event_messages()

    return messageLog


if __name__ == '__main__':

    from craft_interface import character_contract, get_run_info
    contract = character_contract()

    # contract.caller.viewRuns(10)
    # # print(contract)
    # import asyncio
    # asyncio.run(view_runs())

    run_data = get_run_info(contract.caller.viewRuns(5))
    for log in parse_events(run_data):
        print(log)
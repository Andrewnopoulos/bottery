from toolz.itertoolz import diff
from util import AttrDict, get_micro
from data.db import get_beastdb, get_itemdb, get_translations

class EventBase():
    def __init__(self, events):
        self.events = events

    def digit_to_emoji(self, number):
        if number < 0:
            return ':heavy_minus_sign:' + self.digit_to_emoji(abs(number))
        if number == 0:
            return ':zero:'
        elif number == 1:
            return ':one:'
        elif number == 2:
            return ':two:'
        elif number == 3:
            return ':three:'
        elif number == 4:
            return ':four:'
        elif number == 5:
            return ':five:'
        elif number == 6:
            return ':six:'
        elif number == 7:
            return ':seven:'
        elif number == 8:
            return ':eight:'
        elif number == 9:
            return ':nine:'
        elif number == 10:
            return ':keycap_ten:'
        elif number > 10:
            retstr = ''
            for digit in str(number):
                retstr += self.digit_to_emoji(int(digit))
            return retstr
        else:
            return ''

    def parse(self, event):
        print(f"missing parse or get_event_messages override for {str(self)}")
        return event

    def emojis(self, event):
        print(f"missing emoji representation or get_event_emojis override for {str(self)}")
        return event

    def get_event_messages(self):
        for event in self.events:
            yield from self.parse(event)

    def get_event_emojis(self):
        for event in self.events:
            yield from self.emojis(event)

class EnteredFloorEvent(EventBase):
    def __init__(self, event):
        super().__init__([event])

    def parse(self, event):
        ## TODO: we can display inventory or equipment here
        yield f"Entered the dungeon"

    def emojis(self, event):
        yield ":arrow_right::homes:"

class EnteredRoomEvent(EventBase):
    def __init__(self, event):
        super().__init__([event])
    
    def parse(self, event):
        roomMessage = ''
        if event.args._room == 1:
            roomMessage = "Entered a small room"
        elif event.args._room == 2:
            roomMessage = "Entered a medium sized room"
        elif event.args._room == 3:
            roomMessage = 'Entered a large room'
        yield roomMessage

    def emojis(self, event):
        roomMessage = ""
        if event.args._room == 1:
            roomMessage = ":arrow_right::house_abandoned:"
        elif event.args._room == 2:
            roomMessage = ":arrow_right::house:"
        elif event.args._room == 3:
            roomMessage = ":arrow_right::classical_building:"
        yield roomMessage

class EffectEvent(EventBase):
    def __init__(self, event):
        super().__init__([event])

    def parse(self, event):
        effect = AttrDict({
            "effectType": event.args._type,
            "type": 'effect',
            "id": event.args._index,
            "amount": event.args._amount,
            "combatant": event.args._combatant,
            "room": event.args._roomIndex
        })
        if effect.effectType == 1:
            yield f"You take {effect.amount} damage"
        elif effect.effectType == 2:
            yield f"A cool breeze replenishes {effect.amount} HP"

    def emojis(self, event):
        
        if event.args._type == 1:
            yield f":wind_blowing_face::heavy_minus_sign:{self.digit_to_emoji(event.args._amount)}"
        elif event.args._type == 2:
            yield f":wind_blowing_face::heavy_plus_sign:{self.digit_to_emoji(event.args._amount)}"

class EnemyEncounterEvent(EventBase):
    def __init__(self, event):
        super().__init__([event])

    def parse(self, event):
        beast_db = get_beastdb()
        creatureID = event.args._creatureID
        if creatureID < len(beast_db) and creatureID >= 0:
            yield f"Encountered {beast_db[creatureID].get('name', 'a nameless monster')}"

    def emojis(self, event):
        beast_db = get_beastdb()
        creatureID = event.args._creatureID
        if creatureID < len(beast_db) and creatureID >= 0:
            yield f"{beast_db[creatureID].get('discord', ':imp:')}"
        
class TrapEvent(EventBase):
    def __init__(self, event):
        super().__init__([event])

    def parse(self, event):
        trapName = ''
        trapDamage = event.args._damage
        if event.args._trap == 0:
            trapName = "spike pit"
        elif event.args._trap == 1:
            trapName = "swinging axe"
        elif event.args._trap == 2:
            trapName = "falling net"
        elif event.args._trap == 3:
            trapName = "flame jet"
        elif event.args._trap == 4:
            trapName = "poison darts"
        if trapName:
            yield f"Encountered a {trapName}"
            if trapDamage:
                yield f"Took {trapDamage} damage"

class LootEvent(EventBase):
    def __init__(self, event):
        super().__init__([event])

    def parse(self, event):
        item_db = get_itemdb()
        if event.args._loot >= 0 and event.args._loot < len(item_db):
            name = get_translations(item_db[event.args._loot]).get('name', 'unidentifiable item')
            if event.args._dropped:
                yield f"Enemy dropped {name}"
            else:
                yield f"Found {name}"

class CreditsEvent(EventBase):
    def __init__(self, event):
        super().__init__([event])

    def parse(self, event):
        yield f"Picked up {event.args._amount} gold"

class ExperienceEvent(EventBase):
    def __init__(self, event):
        super().__init__([event])

    def parse(self, event):
        yield f"Gained {event.args._amount} experience"

class NonCombatEvent(EventBase):
    def __init__(self, event):
        super().__init__([event])
    
    def parse(self, event):
        return f"{event.event} - {event.args}"

class CombatEncounter(EventBase):
    def __init__(self, first_event):
        super().__init__([first_event])
        self.encounterIndex = first_event.args._encounterNumber
        self.totalTurns = 0
        
    def process_combat_info(self, combat_info):

        ### movement indices:
        ### 0 = attack
        ### 1 = dodge
        ### 2 = parry
        ### 3 = escape
        ### 4 = do nothing
        ### 5 = ranged
        ### 6 = ? (combat effect?)
        ### 7 = item used
        ### 8 = death

        debugstr = f'AFirst: {combat_info.AFirst}\nMoveA: {combat_info.moveA}\nMoveB: {combat_info.moveB}\nhealthA: {combat_info.healthA}\nhealthB: {combat_info.healthB}\n'
        message_list = []
        
        if combat_info.AFirst:
            if combat_info.moveA == 3:
                message_list.append("you escaped successfully")
                return message_list
            
            if combat_info.moveB == 3:
                message_list.append('Enemy tried to escape')
            elif combat_info.moveB == 1:
                message_list.append('Enemy tried to dodge')
            elif combat_info.moveB == 2:
                message_list.append('Enemy attacked you (parry)')
            elif combat_info.moveB == 0:
                message_list.append('Enemy attacked you')
            
            if combat_info.damageA:
                message_list.append(f'You took {combat_info.damageA} damage')

            if combat_info.moveA == 0:
                message_list.append(f'You attacked')
            elif combat_info.moveA == 1:
                message_list.append(f'You dodged')
            elif combat_info.moveA == 2:
                message_list.append(f'You parried')
            
            if combat_info.damageB:
                message_list.append(f"You did {combat_info.damageB} damage")

        else:
            if combat_info.moveB == 3:
                message_list.append('Enemy escaped successfully')
                return message_list
            
            if combat_info.moveA == 3:
                message_list.append('You tried to escape')
            elif combat_info.moveA == 1:
                message_list.append('You tried to dodge')
            elif combat_info.moveA == 2:
                message_list.append('You tried to parry')
            elif combat_info.moveA == 0:
                message_list.append('You tried to attack')

            if combat_info.damageB:
                message_list.append(f"You did {combat_info.damageB} damage")

            if combat_info.moveB == 0:
                message_list.append(f'Enemy attacked')
            elif combat_info.moveB == 1:
                message_list.append(f'Enemy dodged')
            elif combat_info.moveB == 2:
                message_list.append(f'Enemy parried')

            if combat_info.damageA:
                message_list.append(f'You took {combat_info.damageA} damage')

        if ((combat_info.moveA == 3 and combat_info.moveB == 3) or
            (combat_info.moveA == 1 and combat_info.moveB == 1) or
            (combat_info.moveA == 3 and combat_info.moveB == 1) or
            (combat_info.moveA == 1 and combat_info.moveB == 3) or
            (combat_info.moveA == 4 and combat_info.moveB == 3) or
            (combat_info.moveA == 4 and combat_info.moveB == 1) or
            (combat_info.moveA == 3 and combat_info.AFirst) or
            (combat_info.moveB == 3 and not combat_info.AFirst)): ## A escapes and B escapes or A dodges and B dodges OR either A or B dodge + escape
            message_list.append('You and the enemy both escape')
            return message_list

        if combat_info.moveB == 8: ## B dies
            message_list.append('You killed the enemy')
        elif combat_info.healthA == 0:
            message_list.append('The enemy killed you')

        return message_list

    def get_event_messages(self):
        for combat_info in self.iterate_combat():
            messages = self.process_combat_info(combat_info)
            yield from messages

    def iterate_combat(self):
        for index in range(self.totalTurns+1):
            yield self.get_combat_info(index)

    def get_combat_info(self, turn):
        if turn > self.totalTurns or turn < 0:
            return False
        
        combat_event = self.events[turn]
        
        combat_info = AttrDict({
            "turn": turn,
            "encounter": combat_event.args._encounterNumber,
            "healthA": combat_event.args._healthA,
            "healthB": combat_event.args._healthB,
            "damageA": 0,
            "damageB": 0,
            "moveA": combat_event.args._moveA,
            "moveB": combat_event.args._moveB,
            "AFirst": combat_event.args._AFirst,
            "combatEffect": False,
            "itemUsage": {
                "item": 0,
                "amount": 0
            },
            "maxHealthB": self.events[0].args._healthB,
        })

        combat_info.combatEffect = combat_info.moveA == "6" or combat_info.moveB == "6"
        if combat_info.moveA == "7":
            combat_info.itemUsage.item = combat_info.healthA
            combat_info.itemUsage.amount = combat_info.healthB
            if turn > 0:
                combat_info.healthA = self.events[turn - 1].args._healthA
                combat_info.healthB = self.events[turn - 1].args._healthB

        if turn < self.totalTurns:
            combat_info.damageA = combat_info.healthA - self.events[turn + 1].args._healthA
            combat_info.damageB = combat_info.healthB - self.events[turn + 1].args._healthB

        return combat_info

    def add_event(self, new_event):
        if new_event.args._encounterNumber != self.encounterIndex:
            print("unable to add event, wrong encounter index")
            return False
        
        self.events.append(new_event)
        self.totalTurns += 1

        return True
    
    def message_list(self):
        return self.events



if __name__ == '__main__':

    from craft_interface import character_contract, get_run_info
    contract = character_contract()

    # contract.caller.viewRuns(10)
    # # print(contract)
    # import asyncio
    # asyncio.run(view_runs())

    run_data = get_run_info(contract.caller.viewRuns(5))

    # for data in run_data:
    #     ev = NonCombatEvent(data)
    #     for i in ev.get_event_messages():
    #         print (i)
    
    # for log in parse_events(run_data):
    #     print(log)
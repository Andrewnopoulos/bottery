abi = [{"constant":True,"inputs":
[],"name":"equipmentCore","outputs":
[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":
[],"name":"RNG","outputs":
[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":
[],"name":"characterCore","outputs":
[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"inputs":
[{"name":"_entropy","type":"address"},{"name":"_characterCore","type":"address"},{"name":"_equipmentCore","type":"address"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":
[{"indexed":True,"name":"_runID","type":"uint256"},{"indexed":False,"name":"_moveA","type":"uint8"},{"indexed":False,"name":"_moveB","type":"uint8"},{"indexed":False,"name":"_healthA","type":"uint256"},{"indexed":False,"name":"_healthB","type":"uint256"},{"indexed":False,"name":"_encounterNumber","type":"uint256"},{"indexed":False,"name":"_AFirst","type":"bool"}],"name":"CombatEvent","type":"event"},{"anonymous":False,"inputs":
[{"indexed":True,"name":"_runID","type":"uint256"},{"indexed":False,"name":"_atHuman","type":"bool"},{"indexed":False,"name":"_encounterNumber","type":"uint256"}],"name":"ProjectileFired","type":"event"},{"anonymous":False,"inputs":
[{"indexed":True,"name":"_runID","type":"uint256"},{"indexed":False,"name":"_encounterNumber","type":"uint256"}],"name":"ProjectileDeflected","type":"event"},{"anonymous":False,"inputs":
[{"indexed":False,"name":"_multiplier","type":"uint256"},{"indexed":False,"name":"_encounterNumber","type":"uint256"}],"name":"CriticalStrike","type":"event"},{"constant":False,"inputs":
[],"name":"addBattle","outputs":
[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":
[{"name":"_encounterInfo","type":"uint256[9]"}],"name":"determineVictor","outputs":
[{"name":"","type":"uint256"},{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"}]
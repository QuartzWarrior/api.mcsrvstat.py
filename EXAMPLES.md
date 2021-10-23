## Usage Examples

- Basic implementation, we're using a `java` server here but it can be `bedrock` depending on what type of server it is.
```python
from mcsrvstat import Stats

stat = Stats(server_platform='java', server_url='bedcraft.minecraftersbd.com', ignore_status_code=False)
# ignore_status_code can be set to True for disabling request status code checks
```

- Checking if the server is online:
```python
if stat.check_if_online():
    print('Yay, the server is online!')
else:
    print('The server is offline.')
```

- Get the server's icon:
```python
icon = stat.get_server_icon()
```

- Get the server's software and version.
```python
server_stuff = stat.get_server_software()

if not server_stuff:
    print('Maybe the server is off, or maybe it\'s just non-existent.')
else:
    print(f'Version: {server_stuff.version}; Software: {server_stuff.software}')
```

- Get one of the server's debug value.
```python
value = server.get_server_debug_value(debug_value='ping')

try:
    if value:
        print('SLP is enabled.')
    else:
        print('SLP is disabled.')
except LookupError:
    print('You\'ve put a wrong debug value type right there!')
```

- Get the server's MOTD:
```python
motd = stat.get_server_motd(motd_type='clean')

if not motd:
    print('Either the server is offline or it simply doesn\'t exist (not applicable).')
else:
    print(motd)
```

- Getting an online player by name:
```python
try:
    player = stat.get_player_by_name('HorizonUwU')
except LookupError:
    print('Player not found online / on Earth!')
else:
    print(f'Name: {player.name}, UUID: {player.uuid}')
```

- Getting the online and the max player count:
```python
player_count = stat.get_player_amount()

if not player_count:
    print('The server is offline / non-existent.')
else:
    print(f'Online: {player_count.online} | Max: {player_count.max}')
```

- Getting a list of players currently playing on the server:
```python
players = stat.get_players()

if players is None:
    print('The server is offline.')
else:
    for player in players:
        print(f'{player.name} > {player.uuid}')
```

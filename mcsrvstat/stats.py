import aiohttp


async def requestGet(endpoint: str, json: bool, ignore_status_code: bool):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as request:

                if not ignore_status_code:
                    if request.status != 200:
                        raise LookupError('The API is down, for now.')
                    else:
                        return request.json() if json else request
                else:
                    return request.json() if json else request

    except aiohttp.ClientConnectionError:
        raise LookupError('You must have a stable internet connection.')


class Player:
    """
    The default class for accessing player metadata.

    Attributes:\n
        `name` - The friendly name of the player.\n
        `uuid` - The UUID of the player.
    """

    def __init__(self, name: str, uuid: str):
        self.name = name
        self.uuid = uuid

    def __str__(self):
        return f'Name: {self.name}; UUID: {self.uuid}'


class ServerSoftware:
    """
    The default class for accessing server software and version information.

    Attributes:\n
        `version` - The version of the backend used by the server.\n
        `software` - The software / vendor name.'
    """

    def __init__(self, version: str, software: str):
        self.version = version
        self.software = software

    def __str__(self):
        return f'Version: {self.version}; Software: {self.software}'


class ServerPlayerCount:
    """
    The default class for accessing server player count.

    Attributes:\n
        `online` - The amount of players currently online.\n
        `max` - The maximum amount of players the server can hold at a time.
    """

    def __init__(self, online: int, max: int):
        self.online = online
        self.max = max

    def __str__(self):
        return f'Online: {self.online}; Max: {self.max}'


class Base:
    """
    The root class of the library for directly interacting with the API.
    """

    def __init__(self, server_platform: str, server_url: str, ignore_status_code: bool):
        self.server_platform = server_platform.lower()
        self.server_url = server_url
        self.available_platforms = ['java', 'bedrock']
        self.default_endpoint = 'https://api.mcsrvstat.us/'
        self.icon_endpoint = 'https://api.mcsrvstat.us/icon/'
        self.ignore_status_code = ignore_status_code

    async def lookup_server(self):
        """
        Returns an application/json value for the given server once invoked.
        """
        
        if self.server_platform not in self.available_platforms:
            raise AttributeError('Server type has to be java or bedrock.')

        if self.server_platform == self.available_platforms[0]:
            self.default_endpoint += f'2/{self.server_url}'
        else:
            self.default_endpoint += f'bedrock/2/{self.server_url}'
            
        return await requestGet(endpoint=self.default_endpoint, json=True, ignore_status_code=self.ignore_status_code)

    async def lookup_server_icon(self):
        """
        Returns an image which refers to the server's icon. A 64x64 PNG image will always be returned.
        """

        self.icon_endpoint += self.server_url
        return await requestGet(endpoint=self.icon_endpoint, json=True, ignore_status_code=self.ignore_status_code)


class Stats:
    """
    The initialization part of the library.

    Parameters:\n
        `server_platform` - The platform in which the Minecraft server is running (has to be `java` or `bedrock`).\n
        `server_url` - The link for joining the server.
        `ignore_status_code` - Choose if request status code checks should be enabled or disabled.
    """

    def __init__(self, server_platform: str, server_url: str, ignore_status_code: bool):
        self.base = Base(server_platform=server_platform, server_url=server_url, ignore_status_code=ignore_status_code)

    def check_if_online(self) -> bool:
        """
        Gives out a boolean value depending on whether the server is online or not.
        """
        
        server = self.base.lookup_server()
        return server['online']

    def get_server_icon(self):
        """
        Gives out the default icon of the server. A 64x64 PNG image will always be returned.
        """
        
        return self.base.lookup_server_icon()

    def get_server_motd(self, motd_type: str) -> str:
        """
        Gives out a list containing the server's MOTD.

        Parameters:\n
            `type` - Specifies the type of the MOTD (has to be `raw`, `clean` or `html`).
        """
        
        server = self.base.lookup_server()
        motd_type = motd_type.lower()

        try:
            return server['motd'][motd_type]
        except KeyError:
            return None

    def get_server_software(self) -> ServerSoftware:
        """
        Gives out a `ServerSoftware` object containing the version and software information of the given server. Returns `None` if not applicable.
        """

        server = self.base.lookup_server()

        try:
            return ServerSoftware(version=server['version'], software=server['software'])
        except KeyError:
            return None

    def get_server_debug_value(self, debug_value: str) -> bool:
        """
        Gives out a specific debug value of the server. Returns `None` if not applicable.
        """

        server = self.base.lookup_server()
        debug_value = debug_value.lower()
        
        try:
            return server['debug'][debug_value]
        except KeyError:
            raise LookupError('Invalid debug value passed.')

    def get_player_by_name(self, player_name: str) -> Player:
        """
        Gives out a `Player` object if a player is found active / online by the given name. Returns `None` if not applicable.
        """

        server = self.base.lookup_server()

        try:
            if player_name in server['players']['uuid']:
                return Player(name=player_name, uuid=server['players']['uuid'][player_name])

        except KeyError:
            raise LookupError('Player offline / non-existent.')

    def get_player_amount(self) -> ServerPlayerCount:
        """
        Gives out a `ServerPlayerCount` object containing both the online and the max player count. Returns `None` if not applicable.
        """

        server = self.base.lookup_server()
        
        try:
            return ServerPlayerCount(online=server['players']['online'], max=server['players']['max'])
        except KeyError:
            return None

    def get_players(self) -> list:
        """
        Gives out a list containing `Player` objects, each indicating an online player. Returns `None` if not applicable.
        """

        server = self.base.lookup_server()
        players = list()

        try:
            for player in server['players']['list']:
                players.append(Player(name=player, uuid=server['players']['uuid'][player])) 

            return players

        except KeyError:
            return None

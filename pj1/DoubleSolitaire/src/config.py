"""
Config manager to handle any persistent information using configparser.
"""
import configparser

class ConfigManager:
    def __init__(self):

        self.filename = 'config.cfg'
        self.config = configparser.ConfigParser()
        self.config.read(self.filename)
        self.reload_config()
        self.gamePlayerType = 2
        self.gameTimeLimit = 12
        self.gameStackMovement = 0
        self.gameStackSize = 0

    def reload_config(self):
        """Reload configuration values from the config file."""
        self.gameResWidth = self.config.getint('info', 'ResWidth')
        self.gameResHeight = self.config.getint('info', 'ResHeight')
        self.gameLoadGame = self.config.getboolean('info', 'LoadGame')
        self.gameAiHelper = self.config.getint('info', 'Ai_Helper')
        self.gameFastMode = self.config.getboolean('info', 'fast mode')
        self.gameNoAnims = self.config.getboolean('info', 'no anims')
        self.gameFullscreen = self.config.getboolean('info', 'Fullscreen')
        self.gameGlints = self.config.getboolean('info', 'Glints')

    def update_config(self, option, value):
        """
        Update a configuration option, write the config file, and reload values.
        """
        self.config.set('info', option, str(value))
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
        self.reload_config()

# Create a singleton instance that can be imported elsewhere.
config_manager = ConfigManager()

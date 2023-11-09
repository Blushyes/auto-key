from interaction.command_line import CommandLineInteractionLayer
from interaction.main import InteractionLayer

if __name__ == '__main__':
    interaction: InteractionLayer = CommandLineInteractionLayer()
    interaction.start()

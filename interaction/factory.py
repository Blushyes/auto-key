from context.config import get_config, Config
from interaction import InteractionLayer
from interaction.command_line import CommandLineInteractionLayer
from interaction.gui import QTGUIInteractionLayer


class InteractionLayerType:
    COMMAND_LINE = 'command_line'
    GUI = 'gui'


def get_interaction_layer(interaction_layer_name: str) -> InteractionLayer:
    match interaction_layer_name:
        case InteractionLayerType.COMMAND_LINE:
            return CommandLineInteractionLayer()
        case InteractionLayerType.GUI:
            return QTGUIInteractionLayer()
        case _:
            raise ValueError(f'Unknown interaction layer: {interaction_layer_name}')


def get_interaction_layer_from_config() -> InteractionLayer:
    config = get_config()
    interaction_name = config[Config.INTERACTION]
    return get_interaction_layer(interaction_name)

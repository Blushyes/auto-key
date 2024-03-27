from context.config import initialize_config
from interaction import InteractionLayer
from interaction.factory import get_interaction_layer_from_config

if __name__ == '__main__':
    initialize_config()
    interaction: InteractionLayer = get_interaction_layer_from_config()
    interaction.start()

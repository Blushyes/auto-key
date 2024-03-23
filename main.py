from context.config import initialize_config
from interaction.factory import get_interaction_layer_from_config
from interaction.main import InteractionLayer

if __name__ == '__main__':
    initialize_config()
    interaction: InteractionLayer = get_interaction_layer_from_config()
    interaction.start()

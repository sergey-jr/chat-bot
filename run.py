from kutana import *
import settings

# Create engine
engine = Kutana()

# Add VKController to engine
engine.add_controller(
    VKController(settings.token)
)

# Load and register plugins
engine.executor.register_plugins(*load_plugins("plugins/"))

# Run engine
engine.run()
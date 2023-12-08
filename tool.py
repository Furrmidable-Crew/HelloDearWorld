import os
import json

from cat.mad_hatter.decorators import tool
from cat.utils import get_plugins_path


@tool
def complete_json(tool_input, cat):
    """Useful to put a dictionary-like text inside a JSON file.
    Input is a python dictionary."""
    json_file = os.path.join(get_plugins_path(), "start_from_here", "plugin.json")
    try:
        json_content = eval(tool_input)
    except Exception as exc:
        return "There might be an error in the dictionary you wrote"

    if "name" not in json_content:
        return "uh-oh I think you forgot to tell me the name of your plugin"

    with open(json_file, "w") as file:
        json.dump(json_content, file)

    return "This has been magical! Go check the plugin in the `cat/plugins/start_from_here` folder"


@tool
def complete_hook(tool_input, cat):
    """Useful to complete the .py file to change the Cat's personality.
    Input is a string describing how the Cat should behave."""
    plugin_file = os.path.join(get_plugins_path(), "start_from_here", "plugin.py")
    hook_start = """from cat.mad_hatter.decorators import hook
    
    @hook
    def agent_prompt_prefix(prefix, cat):
    """

    hook_end = """
        return prefix
    """

    hook = f"""
    {hook_start}
        prefix="{tool_input}"
        {hook_end}
    """

    with open(plugin_file, "w") as file:
        file.write(hook)

    return "Go and take a look at how the file is changed!"

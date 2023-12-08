import os
import json

from cat.log import log
from cat.utils import get_static_path, get_plugins_path
from cat.mad_hatter.decorators import plugin, hook
from cat.looking_glass.cheshire_cat import CheshireCat
from cat.looking_glass.prompts import MAIN_PROMPT_PREFIX


URLS = [
    "https://cheshire-cat-ai.github.io/docs/technical/plugins/plugins/",
    "https://cheshire-cat-ai.github.io/docs/technical/plugins/tools/",
    "https://cheshire-cat-ai.github.io/docs/technical/plugins/hooks/",
    "https://cheshire-cat-ai.github.io/docs/technical/plugins/settings/",
    "https://cheshire-cat-ai.github.io/docs/technical/plugins/dependencies/"
]
TUTORIAL_PATH = os.path.join(get_plugins_path(), "start_from_here")
MAIN_PROMPT_PREFIX = None


ccat = CheshireCat()


@plugin
def activated(plugin):
    declarative_memory = ccat.memory.vectors.declarative
    for url in URLS:
        metadata = {
            "source": url
        }

        points = declarative_memory.client.scroll(
            collection_name="declarative",
            scroll_filter=declarative_memory._qdrant_filter_from_dict(metadata),
        )
        log.debug(points)
        if len(points[0]) != 0:
            continue
        log.error(f"Ingesting {url}")
        ccat.rabbit_hole.ingest_file(stray=ccat, file=url)

    # clonare template?

    if not os.path.isdir(TUTORIAL_PATH):
        os.mkdir(TUTORIAL_PATH)
        with open(os.path.join(TUTORIAL_PATH, "plugin.py"), "w"):
            pass
        # creare json


@hook
def agent_prompt_prefix(prefix, cat):
    global MAIN_PROMPT_PREFIX
    MAIN_PROMPT_PREFIX = prefix


@hook
def before_cat_reads_message(message, cat):
    if not "hdw" in cat.working_memory and os.path.isdir(TUTORIAL_PATH):
        cat.working_memory["hdw"] = True


@hook
def before_cat_recalls_procedural_memories(settings, cat):
    if "hdw" in cat.working_memory and cat.working_memory["hdw"] is False:
        settings["threshold"] = 1.1

        del cat.working_memory["hdw"]

    return settings


@hook
def agent_fast_reply(reply, cat):

    if "hdw" in cat.working_memory and cat.working_memory["hdw"] is True:
        cat.working_memory["hdw"] = False

        content = cat.llm(f"{MAIN_PROMPT_PREFIX}. Tell the user that the 'Hello Dear World' experience has begun.")
        res = cat({
            "text": "Introduce me about the Cheshire Cat's plugin. Explain the following like I'm five:"
                    "- Plugin"
                    "- Hooks"
                    "- Tools"
        })  # funge, cercare risp migliore

        return {"output": f"{content}\n{res['content']}\nAre you ready to begin? Yes/No"}

        # __________________

    if not "hdw" in cat.working_memory or cat.working_memory["hdw"] is False:
        return reply

    if cat.working_memory["plugin_begin"] is None: # TODO: here crasha ricomincia da qua
        if "yes" in cat.working_memory["user_json_message"]["text"].lower():
            # Start

            # def agent_prompt_prefix(prefix, cat):
                # prefix = dimmi la tua personalità
                # return
            #
            message = """Let's try build a plugin together, this is a plugin that changes my personality.
         
            @hook
            def agent_prompt_prefix(prefix, cat):
                prefix = "Choose my personality"
                return prefix
                
            what personality do you want me to have? Write a description
            """
            del cat.working_memory["plugin_begin"]
            return  {
                "output": message
            }

# creare forzatamente cartella plugin nuovo? "ti ho creato un plugin, vai a controllare al path...i file servono a..."
# plugin.json con chiavi vuote --> riempibile con tools
# hook esempio con --> completa tu --> il completamento viene scritto dentro al .py
# requirements?

# info preliminari plugin hook tool (cerca a mano nella memoria e fai un prompt con dentro il contesto pescato?)
# sei pronto per una piccola sfida? si/no
# si -> un piccolo plugin da fare (sfida con few-shots? llm sbizzarrisce)
# no -> vai avanti con altre info preliminari
import click
from logger import logger




def initial_input(prompt: str = ""):
    try:
        logger.debug("Asking user via keyboard...")
        return click.prompt(text=prompt, prompt_suffix=" ", default="", show_default=False)
    except KeyboardInterrupt:
        logger.info("User interrupted the program.")
        logger.info("Exiting the program...")
        exit(0)

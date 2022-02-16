from utn_tools import bot
from utn_tools.tgm import text


COMPLETE_SURVEYS_COMMAND_NAME = "completar encuestas"


def help(update, context) -> None:
    context.bot.sendMessage(
        chat_id=update.effective_user["id"],
        parse_mode="MarkdownV2",
        disable_web_page_preview=True,
        text=text.get_help_message(COMPLETE_SURVEYS_COMMAND_NAME),
    )


def _complete_surveys(update, context, dni: int, password: str, legajo: int) -> int:
    survey_bot = bot.SurveyBot(dni, password, legajo, headless=True)
    try:
        surveys_completed = survey_bot.complete_surveys()
        context.bot.sendMessage(
            chat_id=update.effective_user["id"],
            parse_mode="MarkdownV2",
            disable_web_page_preview=True,
            text=text.get_surveys_completed_message(
                update.effective_user["username"], surveys_completed
            ),
        )
    except Exception:
        context.bot.sendMessage(
            chat_id=update.effective_user["id"],
            parse_mode="MarkdownV2",
            disable_web_page_preview=True,
            text=text.get_login_error_message(dni, legajo, password),
        )

    return survey_bot.surveys_completed


def parser(update, context) -> None:
    command = str(update.message.text).strip()
    if command.startswith(COMPLETE_SURVEYS_COMMAND_NAME + " "):
        _complete_surveys(update, context, *command.split(" ")[2:])
    else:
        context.bot.sendMessage(
            chat_id=update.effective_user["id"],
            parse_mode="MarkdownV2",
            disable_web_page_preview=True,
            text=text.COMMAND_NOT_FOUND_MESSAGE,
        )

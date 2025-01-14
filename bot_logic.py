from call_apis import post_to_flowdock, post_to_slack
import logging
import datetime as dt
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s %(name)s:%(lineno)d - %(message)s")
logger = logging.getLogger(__name__)


W_GENDER = "Women"
M_GENDER = "Men"

ping_message = "<!channel> It's sauna day! Remember to turn on the sauna!"
nonping_message = "Today's sauna shifts are following:"


def __get_nice_adjective() -> str:
    adjective = random.choice(["great", "fantastic", "fabulous", "wonderful", "exceptional", "positive", "rad",
                               "excellent", "amazing", "incredible", "superb", "awe-inspiring", "dynamite", "super",
                               "swell", "divine", "remarkable", "enjoyable", "cool", "brilliant"])
    return f"{'a' if adjective[0] not in ['a', 'e', 'i', 'u', 'o'] else 'an'} {adjective}"


def _get_inspirational_message() -> str:
    return f"\n\n" \
           f"There are towels, soap and a hairdryer in the sauna for your convenience.\n" \
           f"Have {__get_nice_adjective()} Friday and weekend!"


def _get_message(weeknumber: int, ping_channel: bool):
    first_shift = W_GENDER if weeknumber % 2 == 0 else M_GENDER
    secondshift = M_GENDER if first_shift == W_GENDER else W_GENDER

    message = f"{ping_message if ping_channel else nonping_message}\n\n" \
              f"{first_shift} first (week {weeknumber}):\n\n" \
              f"{first_shift}'s sauna: 17-18:30\n" \
              f"{secondshift}'s sauna: 18:30-20:00\n" \
              f"Mixed: 20:00 -> (and all other times)" \
              f"{'' if ping_channel else _get_inspirational_message()}"
    return message


def send_message_to_slack(token: str, channel_name: str, ping_channel: bool):
    weeknumber = dt.datetime.today().isocalendar()[1]
    logger.info(f'This is week {weeknumber}')
    try:
        message = _get_message(weeknumber, ping_channel)

        post_to_slack(token,
                      channel_name,
                      message)
    except BaseException as e:
        logger.info(e)

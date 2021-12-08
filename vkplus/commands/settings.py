from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from json import loads, dumps
from utils.emojis import enabled, disabled, error
from os import getcwd


bp = Blueprint("Settings command")
config_path = getcwd().replace("\\", "/") + "/config.json"


# Настройки
@bp.on.message(text="<prefix>для всех")
async def for_everyone(message: Message):
    with open(config_path, "r") as f:
        content = loads(f.read())
    if content["work_for_everyone"] is False:
        with open(config_path, "w") as f:
            content["work_for_everyone"] = True
            f.write(dumps(content, indent=4))
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            "Команды для всех включены " + enabled,
        )

    else:
        with open(config_path, "w") as f:
            content["work_for_everyone"] = False
            f.write(dumps(content, indent=4))
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            "Команды для всех выключены " + disabled,
        )


@bp.on.message(text="<prefix>время бомбы <time>")
async def set_bomb_time(message: Message, time):
    try:
        time = int(time)
        if time < 1:
            await edit_msg(
                bp.api,
                message.id,
                message.peer_id,
                text="Время бомбы не может быть меньше 1! " + error,
            )
        else:
            with open(config_path, "r") as f:
                content = loads(f.read())
            with open(config_path, "w") as f:
                content["bomb_time"] = int(message.text.split()[2])
                f.write(dumps(content, indent=4))

            await edit_msg(
                bp.api,
                message.id,
                message.peer_id,
                text=f"Время бомбы изменено на {content['bomb_time']} секунд "
                + enabled,
            )

    except ValueError:
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Время бомбы - не число! " + error,
        )


@bp.on.message(text="<prefix>время удаления <time>")
async def set_delete_time(message: Message, time):
    try:
        time = int(time)
        if time < 0:
            await edit_msg(
                bp.api,
                message.id,
                message.peer_id,
                text="Время удаления не может быть меньше 0! " + error,
            )
        else:
            with open(config_path, "r") as f:
                content = loads(f.read())
            with open(config_path, "w") as f:
                content["delete_after"] = int(message.text.split()[2])
                f.write(dumps(content, indent=4))

            await edit_msg(
                bp.api,
                message.id,
                message.peer_id,
                text=(
                    "Время удаления изменено на "
                    f"{content['delete_after']} секунд "
                )
                + enabled
            )

    except ValueError:
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Время удаления - не число! " + error
        )


@bp.on.message(text="<prefix>префикс <prefix_new>")
async def set_prefix(message: Message, prefix_new):
    with open(config_path, "r") as f:
        content = loads(f.read())
    with open(config_path, "w") as f:
        content["prefix"] = prefix_new
        f.write(dumps(content, indent=4))
    await edit_msg(
        bp.api,
        message.id,
        message.peer_id,
        text=f'Ваш префикс изменился на "{content["prefix"]}"! ' + enabled
    )


@bp.on.message(text="<prefix>инфо лс")
async def info_in_dm(message: Message):
    with open(config_path, "r") as f:
        content = loads(f.read())

    f = open(config_path, "w")
    if content["send_info_in_dm"] is True:
        content["send_info_in_dm"] = False
        f.write(dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Теперь информация будет присылаться в чат &#128101;",
        )

    else:
        content["send_info_in_dm"] = True
        f.write(dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Теперь информация будет присылаться в лс &#128100;",
        )


@bp.on.message(text="<prefix>ред")
async def edit_or_del(message: Message):
    with open(config_path, "r") as f:
        content = loads(f.read())

    f = open(config_path, "w")
    if content["edit_or_send"] == "edit":
        content["edit_or_send"] = "send"
        f.write(dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Теперь сообщения будут отправляться, а не редактироваться "
            + disabled,
        )

    else:
        content["edit_or_send"] = "edit"
        f.write(dumps(content, indent=4))
        f.close()
        await edit_msg(
            bp.api,
            message.id,
            message.peer_id,
            text="Теперь сообщения будут редактироваться, а не отправляться "
            + enabled,
        )

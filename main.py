import vk
from telethon import TelegramClient

vk_app_id = 1234567
vk_login = 'login'
vk_password = 'password'
scope = 'messages'

vk_conversation_id = 55

tg_api_id = 123456
tg_api_hash = 'hash'
two_step_verification_code = '282'
target_chat_name = 'TargetConf'
phone_num = '+79111234567'


def getLinkOfMaxPictureByPicData(photo_data):
    xxxbig = 'src_xxxbig'
    xxbig = 'src_xxbig'
    xbig = 'src_xbig'
    big = 'src_big'

    if xxxbig in photo_data:
        return photo_data[xxxbig]

    if xxbig in photo_data:
        return photo_data[xxbig]

    if xbig in photo_data:
        return photo_data[xbig]

    if big in photo_data:
        return photo_data[big]


def getListOfPicLinks():
    links = []

    session = vk.AuthSession(vk_app_id, vk_login, vk_password, scope=scope)
    vk_api = vk.API(session)

    start_from = ''
    while (1):
        photos = vk_api.messages.getHistoryAttachments(peer_id=2000000000 + vk_conversation_id,
                                                       count=200,
                                                       media_type='photo',
                                                       start_from=start_from)

        if 'next_from' in photos:
            start_from = photos['next_from']
            del photos['next_from']
        else:
            break

        del photos['0']

        for photo_data in photos.values():
            links.append(getLinkOfMaxPictureByPicData(photo_data['photo']))

    return links


def putPicsToTelegramConference(listOfPics):
    client = TelegramClient('session_name', tg_api_id, tg_api_hash)
    client.start(password=two_step_verification_code, phone=phone_num)

    dialogs = client.get_dialogs(limit=200)

    for dialog in dialogs:
        if dialog.name == target_chat_name:
            confEntity = dialog.entity
            for pic in listOfPics:
                client.send_message(confEntity, pic)
            break


links = getListOfPicLinks()
putPicsToTelegramConference(links)

START = 'start'
CREATE_GROUP = 'createGroup'
DELETE_GROUP = 'delGroup'
GET_GROUP = 'getGroup'
GET_ALL_GROUPS = 'getAllGroups'
HELP = 'help'
CALLBACK_INLINE_SPIN = 'spin'
CALLBACK_INLINE_GROUP_SHUFFLE = 'gShuffle'
CALLBACK_INLINE_GROUP_NORMAL = 'gUnshuffle'
CALLBACK_INLINE_QUEUE_SHUFFLE = 'qShuffle'
CALLBACK_INLINE_QUEUE_NORMAL = 'qUnshuffle'
CALLBACK_INLINE_QUEUE_PREVIOUS = 'qPrev'
CALLBACK_INLINE_QUEUE_NEXT = 'qNext'
CALLBACK_INLINE_QUEUE_SKIP = 'qSkip'
CALLBACK_INLINE_QUEUE_DELETE = 'qDele'
CALLBACK_INLINE_QUEUE_CREATE = 'qCrea'
CALLBACK_INLINE_QUEUE_ADD = 'qAdd'
CALLBACK_INLINE_QUEUE_PRIORITY_SETTINGS = 'qPri'
CALLBACK_INLINE_QUEUE_PRIORITY_START = 'qStart'

COMMANDS_DESCRIPTION = {
    START: 'Инлайн-бот, существует для создания рандомной очереди из людей. Узнайте возможности бота в /help',
    CREATE_GROUP: 'Для создания группы отправьте список людей в чат где есть бот' \
                  'и ответьте на сообщение со списком командой /creategroup и названием группы через пробел.\n' \
                  'Внимание каждая позиция группы должна начинаться с новой строки 1 строка = 1 позиция.\n' \
                  'Для того чтобы запустить очередь напишите: "@тег_бота(Пробел)Название_вашей_группы" в любой чат и нажмите на Shuffle',
    DELETE_GROUP: 'Удаление группы: через пробел укажите название группы',
    GET_GROUP: 'Узнать содержимое группы: через пробел укажите название группы',
    GET_ALL_GROUPS: 'Узнать все доступные вам группы',
    '/inline - queue': 'Создать очередь из указанной группы',
    '/inline - spin': 'Бот предложит запустить бегущую строку из указанного текста после инлайн-вызова бота',
}

HELP_DESCRIPTION = '\n\n'.join('/' + key + " \n" + val for key, val in COMMANDS_DESCRIPTION.items())

from loader import dp

from .admins import AdminFilter, IsSuperUser
from .group_filter import IsGroup
from .private_chat import IsPrivate
from .callback_catcher import CallbackActionStartswith

if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsSuperUser)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(CallbackActionStartswith)    

user_navigation  ={}

def push_page(user_id: int, page: str):
    """Stackga yangi sahofa qo'shish"""
    user_navigation.setdefault(user_id, []).append(page)
    
def pop_page(user_id: int) -> str | None:
    """Stackdan oxirgi sahifani olib tashlash va qaytarish"""
    if user_id in user_navigation and user_navigation[user_id]:
        return user_navigation[user_id].pop()
    return None


def current_page(user_id: int) -> str | None:
    """Hozirgi sahifa nomini olish"""
    if user_id in user_navigation and user_navigation[user_id]:
        return user_navigation[user_id][-1]
    return None
from aiogram import types

routes = [
    {
        "id":"001",
        "title":"#01 Kerakli dasturlar",
        "url":"https://python.sariq.dev/ilk-qadamlar/01-software",
        "description":"Ushbu bo'limda python dasturlash tilini organish uchun kerak bo'lgan dasturlarni ko'rib chiqamiz"
    },
    {
        "id":"002",
        "title":"#02 Hello World!",
        "url":"https://python.sariq.dev/ilk-qadamlar/hello-world",
        "description":"Pythonda birinchi dasturimizni yozamiz."
    },
    {
        "id":"003",
        "title":"#03 PRINT(), SINTEKS VA ARIFMETIK AMALLAR",
        "url":"https://python.sariq.dev/ilk-qadamlar/03-print",
        "description":"print() funksiyasi, Python sintaksi va arifmetik amallar"
    }
]

inline_results_python = []
for route in routes:
    inline_results_python.append(
        types.InlineQueryResultArticle(
            id=route["id"],
            title=route["title"],
            input_message_content=types.InputTextMessageContent(
                message_text=f"{route['title']} darisga link: {route['url']}",
                parse_mode='HTML'
            ),
            url=route['url'],
            description=route['description']
        )
    )
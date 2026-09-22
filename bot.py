import os
import re
import requests

from datetime import datetime
from difflib import get_close_matches

from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)


# =========================================================
# SOZLAMALAR
# =========================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


# =========================================================
# OY NOMLARI
# =========================================================

OYLIK = {
    "yanvar": 1,
    "fevral": 2,
    "mart": 3,
    "aprel": 4,
    "may": 5,
    "iyun": 6,
    "iyul": 7,
    "avgust": 8,
    "sentyabr": 9,
    "sentabr": 9,
    "oktyabr": 10,
    "oktabr": 10,
    "noyabr": 11,
    "dekabr": 12,
}


# =========================================================
# BAYROQLAR
# =========================================================

BAYROQLAR = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "RUB": "🇷🇺",
    "CNY": "🇨🇳",
    "GBP": "🇬🇧",
    "JPY": "🇯🇵",
    "KZT": "🇰🇿",
    "KGS": "🇰🇬",
    "TRY": "🇹🇷",
    "AED": "🇦🇪",
    "SAR": "🇸🇦",
    "KRW": "🇰🇷",
    "CHF": "🇨🇭",
    "CAD": "🇨🇦",
    "AUD": "🇦🇺",
    "PLN": "🇵🇱",
    "CZK": "🇨🇿",
    "SEK": "🇸🇪",
    "NOK": "🇳🇴",
    "DKK": "🇩🇰",

    "AZN": "🇦🇿",
    "BDT": "🇧🇩",
    "BHD": "🇧🇭",
    "BND": "🇧🇳",
    "BRL": "🇧🇷",
    "BYN": "🇧🇾",
    "CUP": "🇨🇺",
    "DZD": "🇩🇿",
    "EGP": "🇪🇬",
    "AFN": "🇦🇫",
    "ARS": "🇦🇷",
    "GEL": "🇬🇪",
    "HKD": "🇭🇰",
    "HUF": "🇭🇺",
    "IDR": "🇮🇩",
    "ILS": "🇮🇱",
    "INR": "🇮🇳",
    "IQD": "🇮🇶",
    "IRR": "🇮🇷",
    "ISK": "🇮🇸",
    "JOD": "🇯🇴",
    "KHR": "🇰🇭",
    "KWD": "🇰🇼",
    "LAK": "🇱🇦",
    "LBP": "🇱🇧",
    "LYD": "🇱🇾",
    "MAD": "🇲🇦",
    "MDL": "🇲🇩",
    "MMK": "🇲🇲",
    "MNT": "🇲🇳",
    "MXN": "🇲🇽",
    "MYR": "🇲🇾",
    "NZD": "🇳🇿",
    "OMR": "🇴🇲",
    "PHP": "🇵🇭",
    "PKR": "🇵🇰",
    "QAR": "🇶🇦",
    "RON": "🇷🇴",
    "RSD": "🇷🇸",
    "AMD": "🇦🇲",
    "SDG": "🇸🇩",
    "SGD": "🇸🇬",
    "SYP": "🇸🇾",
    "THB": "🇹🇭",
    "TJS": "🇹🇯",
    "TMT": "🇹🇲",
    "TND": "🇹🇳",
    "UAH": "🇺🇦",
    "UYU": "🇺🇾",
    "VES": "🇻🇪",
    "VND": "🇻🇳",
    "YER": "🇾🇪",
    "ZAR": "🇿🇦",

    # SDR — davlat valyutasi emas
    "XDR": "🌐",
}


# =========================================================
# QISQA NOMLAR
# =========================================================

QISQA_NOMLAR = {
    "USD": "AQSH",
    "EUR": "Yevro",
    "RUB": "Rossiya",
    "GBP": "Angliya",
    "JPY": "Yaponiya",
    "AZN": "Ozarbayjon",
    "BDT": "Bangladesh",
    "BHD": "Bahrayn",
    "BND": "Bruney",
    "BRL": "Braziliya",
    "BYN": "Belarus",
    "CAD": "Kanada",
    "CHF": "Shveytsariya",
    "CNY": "Xitoy",
    "CUP": "Kuba",
    "CZK": "Chexiya",
    "DKK": "Daniya",
    "DZD": "Jazoir",
    "EGP": "Misr",
    "AFN": "Afg‘oniston",
    "ARS": "Argentina",
    "GEL": "Gruziya",
    "HKD": "Gonkong",
    "HUF": "Vengriya",
    "IDR": "Indoneziya",
    "ILS": "Isroil",
    "INR": "Hindiston",
    "IQD": "Iroq",
    "IRR": "Eron",
    "ISK": "Islandiya",
    "JOD": "Iordaniya",
    "AUD": "Avstraliya",
    "KGS": "Qirg‘iziston",
    "KHR": "Kambodja",
    "KRW": "Janubiy Koreya",
    "KWD": "Quvayt",
    "KZT": "Qozog‘iston",
    "LAK": "Laos",
    "LBP": "Livan",
    "LYD": "Liviya",
    "MAD": "Marokash",
    "MDL": "Moldova",
    "MMK": "Myanma",
    "MNT": "Mongoliya",
    "MXN": "Meksika",
    "MYR": "Malayziya",
    "NOK": "Norvegiya",
    "NZD": "Yangi Zelandiya",
    "OMR": "Ummon",
    "PHP": "Filippin",
    "PKR": "Pokiston",
    "PLN": "Polsha",
    "QAR": "Qatar",
    "RON": "Ruminiya",
    "RSD": "Serbiya",
    "AMD": "Armaniston",
    "SAR": "Saudiya Arabistoni",
    "SDG": "Sudan",
    "SEK": "Shvetsiya",
    "SGD": "Singapur",
    "SYP": "Suriya",
    "THB": "Tailand",
    "TJS": "Tojikiston",
    "TMT": "Turkmaniston",
    "TND": "Tunis",
    "TRY": "Turkiya",
    "UAH": "Ukraina",
    "AED": "BAA",
    "UYU": "Urugvay",
    "VES": "Venesuela",
    "VND": "Vyetnam",
    "XDR": "SDR",
    "YER": "Yaman",
    "ZAR": "Janubiy Afrika",
}


# =========================================================
# ASOSIY MENYU
# =========================================================

def asosiy_menyu():

    keyboard = [
        ["💱 Bugungi kurs"],
        ["🌍 Davlatlar / Valyutalar"],
        ["📅 Sana bo‘yicha kurs"],
        ["ℹ️ Yordam"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# =========================================================
# SANANI ANIQLASH
# =========================================================

def sanani_topish(matn):

    original = matn.strip().lower()

    # Apostroflarni soddalashtirish
    text = original.replace("’", "'")
    text = text.replace("‘", "'")
    text = text.replace("`", "'")

    # Belgilarni soddalashtirish
    text = text.replace(",", " ")
    text = text.replace(".", " ")
    text = text.replace("/", " ")
    text = text.replace("-", " ")

    # "yil" so'zini olib tashlash
    text = re.sub(r"\byil\b", " ", text)
    text = re.sub(r"\bйил\b", " ", text)

    # Ortiqcha bo'shliqlar
    text = re.sub(r"\s+", " ", text).strip()

    # -----------------------------------------------------
    # 1. Raqamli sanalar
    # -----------------------------------------------------

    raqamlar = re.findall(r"\d+", text)

    if len(raqamlar) == 3:

        a, b, c = map(int, raqamlar)

        # 2026 09 01
        if 1900 <= a <= 2100 and 1 <= b <= 12 and 1 <= c <= 31:

            try:
                return datetime(
                    a,
                    b,
                    c
                ).strftime("%Y-%m-%d")

            except ValueError:
                return None

        # 01 09 2026
        if 1 <= a <= 31 and 1 <= b <= 12 and 1900 <= c <= 2100:

            try:
                return datetime(
                    c,
                    b,
                    a
                ).strftime("%Y-%m-%d")

            except ValueError:
                return None

    # -----------------------------------------------------
    # 2. Matnli sana
    # -----------------------------------------------------

    words = text.split()

    kun = None
    oy = None
    yil = None

    for word in words:

        # Masalan: 1-kuni, 1-kun
        word = re.sub(
            r"[^a-zа-яё0-9]",
            "",
            word
        )

        # 1-kuni -> 1kuni
        kun_match = re.match(
            r"^(\d{1,2})(?:kuni|kun)?$",
            word
        )

        if kun_match:

            son = int(
                kun_match.group(1)
            )

            if 1 <= son <= 31:
                kun = son
                continue

        if word.isdigit():

            son = int(word)

            if 1900 <= son <= 2100:

                yil = son

            elif 1 <= son <= 31 and kun is None:

                kun = son

        else:

            oy_sozi = word

            # Oy qo'shimchalarini olib tashlash
            for suffix in [
                "ning",
                "dan",
                "da",
                "kuni",
                "kun"
            ]:

                if (
                    oy_sozi.endswith(suffix)
                    and len(oy_sozi) > len(suffix) + 2
                ):

                    oy_sozi = oy_sozi[:-len(suffix)]
                    break

            # Aniq oy
            if oy_sozi in OYLIK:

                oy = OYLIK[oy_sozi]

            else:

                # Kichik imlo xatolarini tuzatish
                yaqin = get_close_matches(
                    oy_sozi,
                    OYLIK.keys(),
                    n=1,
                    cutoff=0.60
                )

                if yaqin:
                    oy = OYLIK[yaqin[0]]

    # Sana to'liq bo'lsa
    if kun and oy and yil:

        try:

            return datetime(
                yil,
                oy,
                kun
            ).strftime("%Y-%m-%d")

        except ValueError:

            return None

    return None


# =========================================================
# /START
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "💱 Valyuta kurslari botiga xush kelibsiz!\n\n"
        "O‘zbekiston Respublikasi Markaziy bankining "
        "rasmiy valyuta kurslarini ko‘rishingiz mumkin.\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=asosiy_menyu()
    )


# =========================================================
# KURS MA'LUMOTLARINI OLISH
# =========================================================

def cbu_malumotlarini_olish(sana=None):

    if sana:

        url = (
            "https://cbu.uz/uz/"
            "arkhiv-kursov-valyut/json/all/"
            f"{sana}/"
        )

    else:

        url = (
            "https://cbu.uz/uz/"
            "arkhiv-kursov-valyut/json/"
        )

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data


# =========================================================
# BARCHA KURSLARNI KO'RSATISH
# =========================================================

async def kurs(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if context.args:

        sana = context.args[0]

    else:

        sana = None

    try:

        data = cbu_malumotlarini_olish(sana)

        if not data:

            await update.message.reply_text(
                "❌ Bu sana uchun kurs ma'lumotlari topilmadi."
            )

            return

        haqiqiy_sana = data[0]["Date"]

        xabar = (
            "💱 O‘ZBEKISTON MARKAZIY BANKI\n"
            "   RASMIY VALYUTA KURSLARI\n\n"
            f"📅 Kurs sanasi: {haqiqiy_sana}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
        )

        for item in data:

            kod = item["Ccy"]
            nom = item["CcyNm_UZ"]
            rate = item["Rate"]
            nominal = item["Nominal"]

            bayroq = BAYROQLAR.get(
                kod,
                "🌐"
            )

            xabar += (
                f"{bayroq} {nom}\n"
                f"   💰 {nominal} {kod} = {rate} so‘m\n\n"
            )

        # Telegram 4096 belgilik limit
        if len(xabar) <= 4096:

            await update.message.reply_text(
                xabar
            )

        else:

            qismlar = []
            joriy = ""

            for qator in xabar.split("\n\n"):

                if len(joriy) + len(qator) + 2 > 4000:

                    qismlar.append(joriy)

                    joriy = qator + "\n\n"

                else:

                    joriy += qator + "\n\n"

            if joriy:
                qismlar.append(joriy)

            for qism in qismlar:

                await update.message.reply_text(
                    qism
                )

    except Exception as xato:

        print("XATO:", xato)

        await update.message.reply_text(
            "❌ Kurslarni olishda xatolik yuz berdi.\n\n"
            "Iltimos, qaytadan urinib ko‘ring."
        )


# =========================================================
# DAVLATLAR / VALYUTALAR MENYUSI
# =========================================================

async def davlatlar_menyusi(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        data = cbu_malumotlarini_olish()

        if not data:

            await update.message.reply_text(
                "❌ Valyutalar ro‘yxatini olishda xatolik."
            )

            return

        keyboard = []
        mapping = {}

        qator = []

        for item in data:

            kod = item["Ccy"]

            bayroq = BAYROQLAR.get(
                kod,
                "🌐"
            )

            nom = QISQA_NOMLAR.get(
                kod,
                item["CcyNm_UZ"]
            )

            tugma = f"{bayroq} {nom} ({kod})"

            mapping[tugma] = kod

            qator.append(tugma)

            # Har qatorda 2 ta tugma
            if len(qator) == 2:

                keyboard.append(qator)
                qator = []

        # Oxirgi tugma
        if qator:

            keyboard.append(qator)

        # Ortga qaytish
        keyboard.append(
            ["🔙 Asosiy menyu"]
        )

        # Keyingi bosishda foydalanish uchun saqlaymiz
        context.user_data["valyuta_mapping"] = mapping

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            "🌍 DAVLATLAR / VALYUTALAR\n\n"
            "Kerakli davlat yoki valyutani tanlang:\n\n"
            "👇 Kursini ko‘rmoqchi bo‘lgan "
            "valyutani bosing.",
            reply_markup=reply_markup
        )

    except Exception as xato:

        print("DAVLATLAR XATOSI:", xato)

        await update.message.reply_text(
            "❌ Valyutalar ro‘yxatini olishda xatolik yuz berdi."
        )


# =========================================================
# BIRTA VALYUTA KURSINI KO'RSATISH
# =========================================================

async def bitta_valyuta(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    kod: str
):

    try:

        data = cbu_malumotlarini_olish()

        topilgan = None

        for item in data:

            if item["Ccy"] == kod:

                topilgan = item
                break

        if not topilgan:

            await update.message.reply_text(
                "❌ Bu valyuta bo‘yicha ma'lumot topilmadi."
            )

            return

        bayroq = BAYROQLAR.get(
            kod,
            "🌐"
        )

        nom = topilgan["CcyNm_UZ"]
        rate = topilgan["Rate"]
        nominal = topilgan["Nominal"]
        sana = topilgan["Date"]

        xabar = (
            f"{bayroq} {nom}\n\n"
            "💱 O‘ZBEKISTON MARKAZIY BANKI\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📅 Kurs sanasi: {sana}\n\n"
            f"💰 {nominal} {kod} = {rate} so‘m\n\n"
            "ℹ️ Rasmiy Markaziy bank kursi."
        )

        keyboard = [
            ["🌍 Boshqa valyuta"],
            ["🔙 Asosiy menyu"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            xabar,
            reply_markup=reply_markup
        )

    except Exception as xato:

        print("VALYUTA XATOSI:", xato)

        await update.message.reply_text(
            "❌ Valyuta kursini olishda xatolik yuz berdi."
        )


# =========================================================
# YORDAM
# =========================================================

async def yordam(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "ℹ️ BOTDAN FOYDALANISH\n\n"

        "💱 Bugungi kurs\n"
        "— barcha rasmiy valyuta kurslarini ko‘rsatadi.\n\n"

        "🌍 Davlatlar / Valyutalar\n"
        "— kerakli davlat yoki valyutani tanlab, "
        "faqat uning kursini ko‘rishingiz mumkin.\n\n"

        "📅 Sana bo‘yicha kurs\n"
        "— istalgan sana uchun rasmiy kurslarni topadi.\n\n"

        "📅 Sana yozish misollari:\n"
        "• 1 sentyabr 2026\n"
        "• 1 sentabr 2026\n"
        "• 01.09.2026\n"
        "• 01/09/2026\n"
        "• 2026-09-01\n"
        "• 2026 yil 1 sentyabr\n\n"

        "⌨️ Buyruq orqali:\n"
        "/kurs 2026-09-01"
    )


# =========================================================
# TELEGRAM TUGMALARI VA SANA
# =========================================================

async def tugma(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text.strip()

    # -----------------------------------------------------
    # BUGUNGI KURS
    # -----------------------------------------------------

    if text == "💱 Bugungi kurs":

        await kurs(
            update,
            context
        )

        return

    # -----------------------------------------------------
    # DAVLATLAR / VALYUTALAR
    # -----------------------------------------------------

    if text == "🌍 Davlatlar / Valyutalar":

        await davlatlar_menyusi(
            update,
            context
        )

        return

    # -----------------------------------------------------
    # BOSHQA VALYUTA
    # -----------------------------------------------------

    if text == "🌍 Boshqa valyuta":

        await davlatlar_menyusi(
            update,
            context
        )

        return

    # -----------------------------------------------------
    # ASOSIY MENYU
    # -----------------------------------------------------

    if text == "🔙 Asosiy menyu":

        await update.message.reply_text(
            "🏠 Asosiy menyu:",
            reply_markup=asosiy_menyu()
        )

        return

    # -----------------------------------------------------
    # SANA BO'YICHA KURS
    # -----------------------------------------------------

    if text == "📅 Sana bo‘yicha kurs":

        await update.message.reply_text(
            "📅 Kerakli sanani yuboring.\n\n"

            "Masalan:\n\n"

            "1 sentyabr 2026\n"
            "1 sentabr 2026\n"
            "01.09.2026\n"
            "01/09/2026\n"
            "2026-09-01\n"
            "2026 yil 1 sentyabr\n\n"

            "✍️ Kichik imlo xatosi bilan yozsangiz ham "
            "tushunishga harakat qilaman."
        )

        return

    # -----------------------------------------------------
    # YORDAM
    # -----------------------------------------------------

    if text == "ℹ️ Yordam":

        await yordam(
            update,
            context
        )

        return

    # -----------------------------------------------------
    # VALYUTA TUGMASI BOSILDI
    # -----------------------------------------------------

    mapping = context.user_data.get(
        "valyuta_mapping",
        {}
    )

    if text in mapping:

        kod = mapping[text]

        await bitta_valyuta(
            update,
            context,
            kod
        )

        return

    # -----------------------------------------------------
    # FOYDALANUVCHI SANA YOZDI
    # -----------------------------------------------------

    sana = sanani_topish(text)

    if sana:

        context.args = [sana]

        await kurs(
            update,
            context
        )

        return

    # -----------------------------------------------------
    # TUSHUNILMAGAN MATN
    # -----------------------------------------------------

    await update.message.reply_text(
        "❓ So‘rovni tushuna olmadim.\n\n"

        "🌍 Kerakli valyutani tanlash uchun "
        "«Davlatlar / Valyutalar» tugmasini bosing.\n\n"

        "📅 Sana bo‘yicha kurs uchun sanani yozing.\n\n"

        "Masalan:\n"
        "1 sentyabr 2026"
    )


# =========================================================
# ASOSIY FUNKSIYA
# =========================================================

def main():

    if not BOT_TOKEN:

        print(
            "❌ XATO: BOT_TOKEN topilmadi!"
        )

        return

    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    # /start
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # /kurs
    app.add_handler(
        CommandHandler(
            "kurs",
            kurs
        )
    )

    # Oddiy matn va tugmalar
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            tugma
        )
    )

    print("🤖 Bot ishga tushdi...")
    print(
        "Telegram'da /start yoki /kurs "
        "yuborishingiz mumkin."
    )

    app.run_polling()


# =========================================================
# DASTURNI ISHGA TUSHIRISH
# =========================================================

if __name__ == "__main__":

    main()
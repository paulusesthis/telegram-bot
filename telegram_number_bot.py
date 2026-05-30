import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram import LinkPreviewOptions
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN  = os.getenv("BOT_TOKEN")  
CHANNEL_ID = os.getenv("CHANNEL_ID")          

ROWS_PER_PAGE = 5

MENU_HEADER = (
    "🌍 *All Available Countries & Prices*\n\n"
    "📋 Browse the list below to see all countries, prices, and stock availability\."
)

COUNTRIES = [
    # ( "FLAG NAME",            "CODE",   PRICE,  STOCK )
    ("🇦🇫 Afghanistan",         "AF",      1.00,   383),
    ("🇦🇱 Albania",             "AL",      2.10,    38),
    ("🇦🇴 Angola",              "AO",      0.81,   368),
    ("🇦🇷 Argentina",           "AR",      1.20,   933),
    ("🇦🇲 Armenia",             "AM",      2.00,    33),
    ("🇦🇺 Australia",           "AU",      2.15,     2),
    ("🇦🇹 Austria",             "AT",      1.50,   169),
    ("🇦🇿 Azerbaijan",          "AZ",      2.00,    71),
    ("🇵🇬 Babo",                "BABO",    1.50,   259),
    ("🇧🇸 Bahamas",             "BS",      1.80,    20),
    ("🇧🇭 Bahrain",             "BH",      5.00,    27),
    ("🇧🇩 Bangladesh",          "BD",      0.65,  1873),
    ("🇧🇪 Belgium",             "BE",      2.40,    18),
    ("🇧🇿 Belize",              "BZ",      1.88,    66),
    ("🇧🇼 Botswana",            "BW",      1.00,    49),
    ("🇧🇷 Brazil",              "BR",      1.30,   351),
    ("🇨🇦 Canada",              "CA",      1.00,    83),
    ("🇨🇻 Cape Verde",          "CV",      1.80,    20),
    ("🇨🇫 Central Africa",      "CF",      1.00,    63),
    ("🇹🇩 Chad",                "TD",      1.55,   129),
    ("🇨🇱 Chile",               "CL",      0.90,   262),
    ("🇨🇳 China",               "CN",      1.70,   276),
    ("🇰🇲 Comoros",             "KM",      1.56,    47),
    ("🇨🇬 Congo",               "CG",      1.40,    50),
    ("🇨🇷 Costa Rica",          "CR",      1.52,   949),
    ("🇨🇺 Cuba",                "CU",      1.10,   266),
    ("🇨🇿 Czech Republic",      "CZ",      1.30,    71),
    ("🇩🇰 Denmark",             "DK",      3.90,   122),
    ("🇩🇯 Djibouti",            "DJ",      1.50,     2),
    ("🇩🇲 Dominica",            "DM",      1.60,    39),
    ("🇩🇴 Dominican",           "DO",      1.10,   822),
    ("🇪🇨 Ecuador",             "EC",      1.55,  2973),
    ("🇪🇬 Egypt",               "EG",      1.00,  1498),
    ("🇸🇻 El Salvador",         "SV",      1.80,  1776),
    ("🇪🇪 Estonia",             "EE",      1.55,    75),
    ("🇸🇿 Eswatini",            "SZ",      1.30,   302),
    ("🇫🇯 Fiji",                "FJ",      1.70,   351),
    ("🇫🇮 Finland",             "FI",      1.50,    22),
    ("🇫🇷 France",              "FR",      2.00,   613),
    ("🇬🇦 Gabon",               "GA",      1.70,    36),
    ("🇬🇪 Georgia",             "GE",      2.00,    26),
    ("🇩🇪 Germany",             "DE",      2.50,   379),
    ("🇬🇭 Ghana",               "GH",      1.20,   698),
    ("🇬🇷 Greece",              "GR",      2.00,     2),
    ("🇻🇨 Grenadines",          "VC",      1.40,    27),
    ("🇬🇵 Guadeloupe",          "GP",      1.33,     6),
    ("🇬🇺 Guam",                "GU",      1.35,    65),
    ("🇬🇹 Guatemala",           "GT",      1.90,   485),
    ("🇭🇹 Haiti",               "HT",      1.90,   964),
    ("🇭🇳 Honduras",            "HN",      1.90,   289),
    ("🇭🇰 Hong Kong",           "HK",      2.09,    41),
    ("🇭🇺 Hungary",             "HU",      1.70,   106),
    ("🇮🇸 Iceland",             "IS",      2.50,    50),
    ("🇮🇳 India",               "IN",      1.00,   258),
    ("🇮🇩 Indonesia",           "ID",      1.10,   261),
    ("🇮🇷 Iran",                "IR",      1.21,   289),
    ("🇮🇶 Iraq",                "IQ",      4.00,   167),
    ("🇮🇪 Ireland",             "IE",      1.25,    17),
    ("🇮🇱 Israel",              "IL",      1.20,    76),
    ("🇮🇹 Italy",               "IT",      2.00,   245),
    ("🇨🇮 Ivory Coast",          "CI",      1.54,    11),
    ("🇯🇲 Jamaica",             "JM",      1.43,   175),
    ("🇯🇵 Japan",               "JP",      2.00,    45),
    ("🇯🇴 Jordan",              "JO",      2.50,   194),
    ("🇰🇿 Kazakhstan",          "KZ",      1.70,   107),
    ("🇰🇪 Kenya",               "KE",      1.00,  6834),
    ("🇰🇮 Kiribati",            "KI",      2.00,     2),
    ("🇰🇼 Kuwait",              "KW",      2.70,   192),
    ("🇱🇦 Laos",                "LA",      1.70,    50),
    ("🇱🇻 Latvia",              "LV",      2.50,    41),
    ("🇱🇧 Lebanon",              "LB",      2.30,   222),
    ("🇱🇸 Lesotho",              "LS",      1.50,    79),
    ("🇱🇾 Libya",                "LY",      2.50,    90),
    ("🇱🇹 Lithuania",            "LT",      3.00,    12),
    ("🇱🇨 Lucia",                "LC",      1.60,     9),
    ("🇱🇺 Luxembourg",           "LU",      2.50,     6),
    ("🇲🇴 Macau",                "MO",      2.20,    51),
    ("🇲🇬 Madagascar",           "MG",      1.10,   788),
    ("🇲🇼 Malawi",               "MW",      1.70,   163),
    ("🇲🇾 Malaysia",             "MY",      2.00,   262),
    ("🇲🇻 Maldives",             "MV",      2.00,    21),
    ("🇲🇷 Mauritania",           "MR",      1.60,   332),
    ("🇲🇺 Mauritius",            "MU",      1.50,    34),
    ("🇲🇽 Mexico",               "MX",      1.45,   136),
    ("🇲🇿 Mozambique",           "MZ",      1.10,   318),
    ("🇲🇲 Myanmar",              "MM",      0.75,   123),
    ("🇳🇵 Nepal",                "NP",      0.65,  3028),
    ("🇳🇱 Netherlands",          "NL",      2.00,   128),
    ("🇳🇿 New Zealand",          "NZ",      2.30,    28),
    ("🇳🇮 Nicaragua",            "NI",      2.00,   611),
    ("🇳🇴 Norway",               "NO",      4.20,   339),
    ("🇴🇲 Oman",                 "OM",      2.75,   167),
    ("🇵🇰 Pakistan",             "PK",      1.20,    22),
    ("🇵🇸 Palestine",            "PS",      2.40,    62),
    ("🇵🇦 Panama",               "PA",      1.82,    36),
    ("🇵🇾 Paraguay",             "PY",      1.60,    60),
    ("🇵🇪 Peru",                 "PE",      1.65,   255),
    ("🇵🇭 Philippines",          "PH",      1.20,   159),
    ("🇵🇱 Poland",               "PL",      1.10,    90),
    ("🇵🇹 Portugal",             "PT",      2.60,   534),
    ("🇸🇹 Príncipe",             "ST",      2.00,    19),
    ("🇵🇷 Puerto Rico",          "PR",      1.00,    36),
    ("🇶🇦 Qatar",                "QA",      4.00,    49),
    ("🇷🇴 Romania",              "RO",      2.25,  1394),
    ("🇷🇺 Russia",               "RU",      2.50,     5),
    ("🇼🇸 Samoa",                "WS",      2.00,    88),
    ("🇸🇦 Saudi Arabia",         "SA",      2.30,   700),
    ("🇸🇳 Senegal",              "SN",      1.35,   100),
    ("🇸🇨 Seychelles",           "SC",      2.00,    96),
    ("🇸🇱 Sierra Leone",         "SL",      1.50,   291),
    ("🇸🇬 Singapore",            "SG",      4.00,    14),
    ("🇸🇮 Slovenia",             "SI",      2.50,    40),
    ("🇸🇧 Solomon Islands",      "SB",      2.00,    18),
    ("🇸🇴 Somalia",              "SO",      1.80,   310),
    ("🇸🇸 South Sudan",          "SS",      1.50,    46),
    ("🇪🇸 Spain",                "ES",      2.50,   236),
    ("🇱🇰 Sri Lanka",            "LK",      1.50,   204),
    ("🇸🇩 Sudan",                "SD",      1.60,  1524),
    ("🇸🇷 Suriname",             "SR",      1.90,    33),
    ("🇸🇪 Sweden",               "SE",      1.95,    53),
    ("🇨🇭 Switzerland",          "CH",      3.00,    48),
    ("🇸🇾 Syria",                "SY",      1.88,    20),
    ("🇹🇼 Taiwan",               "TW",      2.00,    40),
    ("🇹🇯 Tajikistan",           "TJ",      1.80,   190),
    ("🇹🇭 Thailand",             "TH",      1.00,   574),
    ("🇹🇱 Timor",                "TL",      1.50,    20),
    ("🇹🇬 Togo",                 "TG",      1.10,    16),
    ("🇹🇴 Tonga",                "TO",      1.80,    29),
    ("🇹🇹 Trinidad",             "TT",      1.30,    30),
    ("🇹🇳 Tunisia",              "TN",      1.65,   398),
    ("🇹🇷 Turkey",               "TR",      1.80,   431),
    ("🇹🇲 Turkmenistan",         "TM",      1.66,   279),
    ("🇺🇬 Uganda",               "UG",      1.00,     9),
    ("🇦🇪 United Arab Emirates",      "UAE",      3.00,   154), 
    ("🇬🇧 United Kingdom",       "GB",      1.30,    15),
    ("🇺🇸 United States",        "US",      1.20,  2954),
    ("🇺🇾 Uruguay",              "UY",      1.55,     7),
    ("🇺🇿 Uzbekistan",           "UZ",      1.50,  1249),
    ("🇻🇳 Vietnam",              "VN",      1.50,  1158),
    ("🇾🇪 Yemen",                "YE",      1.50,   167),
    ("🇿🇲 Zambia",               "ZM",      1.25,   132),
]

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

ITEMS_PER_PAGE = ROWS_PER_PAGE * 2  


def sorted_countries(sort_by: str) -> list:
    if sort_by == "price":
        return sorted(COUNTRIES, key=lambda c: c[2])
    if sort_by == "stock":
        return sorted(COUNTRIES, key=lambda c: -c[3])
    return sorted(COUNTRIES, key=lambda c: c[0])   # A-Z


def build_message(sort_by: str, page: int) -> str:
    """
    Build the text message as a neat table using monospace formatting.
    Each page shows ROWS_PER_PAGE × 2 countries laid out as:

    🌍 All Available Countries & Prices
    ...header...

    ┌─────────────────────────────────────┐
    │ 🇦🇫 Afghanistan   $0.65   [383]     │
    │ 🇦🇱 Albania       $1.56   [38]      │
    ...
    └─────────────────────────────────────┘
    Page 1 of 5  •  Sorted by A-Z
    """
    data    = sorted_countries(sort_by)
    total   = len(data)
    pages   = (total + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    page    = max(0, min(page, pages - 1))   # clamp

    start   = page * ITEMS_PER_PAGE
    chunk   = data[start : start + ITEMS_PER_PAGE]

    sort_label = {"az": "A\-Z", "price": "Price ↑", "stock": "Stock ↓"}.get(sort_by, "A\-Z")

    lines = []
    for name, code, price, stock in chunk:
        # pad name to fixed width for alignment
        padded = f"{name:<20}"[:20]
        lines.append(f"  {padded}  ${price:.2f}   \[{stock}\]")

    table = "\n".join(lines)

    text = (
        f"{MENU_HEADER}\n\n"
        f"```\n"
        f"{'COUNTRY':<20}  PRICE   STOCK\n"
        f"{'─' * 38}\n"
        f"{chr(10).join(lines)}\n"
        f"{'─' * 38}```\n\n"
        f"📄 Page *{page + 1}* of *{pages}*  •  Sorted by *{sort_label}*"
    )
    return text


def build_keyboard(sort_by: str, page: int) -> InlineKeyboardMarkup:
    """
    Row 1 → Sort tabs   (A-Z | Price | Stock)
    Row 2 → Navigation  (⬅️ Prev | page indicator | Next ➡️)
    """
    data  = sorted_countries(sort_by)
    total = len(data)
    pages = (total + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    page  = max(0, min(page, pages - 1))

    # sort tabs
    def tab(label, key):
        prefix = "✅ " if sort_by == key else ""
        return InlineKeyboardButton(f"{prefix}{label}", callback_data=f"sort_{key}_0")

    sort_row = [tab("🔡 A-Z", "az"), tab("💲 Price", "price"), tab("📦 Stock", "stock")]

    # navigation
    prev_btn = (
        InlineKeyboardButton("⬅️ Prev", callback_data=f"page_{sort_by}_{page - 1}")
        if page > 0
        else InlineKeyboardButton("⬅️", callback_data="noop")   # disabled
    )
    next_btn = (
        InlineKeyboardButton("Next ➡️", callback_data=f"page_{sort_by}_{page + 1}")
        if page < pages - 1
        else InlineKeyboardButton("➡️", callback_data="noop")   # disabled
    )
    page_indicator = InlineKeyboardButton(
        f"· {page + 1} / {pages} ·", callback_data="noop"
    )
    nav_row = [prev_btn, page_indicator, next_btn]

    return InlineKeyboardMarkup([sort_row, nav_row])


# command ha1ndlers

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start — show the price list in the bot chat."""
    await update.message.reply_text(
        text=build_message("az", 0),
        parse_mode="MarkdownV2",
        reply_markup=build_keyboard("az", 0),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


async def cmd_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/post — send the first page of the price list to your channel."""
    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=build_message("az", 0),
            parse_mode="MarkdownV2",
            reply_markup=build_keyboard("az", 0),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
        await update.message.reply_text("✅ Price list posted to channel!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to post: {e}")


async def cmd_preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/preview — check how the post looks before sending to the channel."""
    await update.message.reply_text(
        text=build_message("az", 0),
        parse_mode="MarkdownV2",
        reply_markup=build_keyboard("az", 0),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


# callback handlers

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "noop":
        return   # disabled button, do nothing

    # sort tab pressed:  sort_az_0 / sort_price_0 / sort_stock_0
    if data.startswith("sort_"):
        _, sort_by, page = data.split("_", 2)
        page = int(page)

    # page arrow pressed:  page_az_2 / page_price_1 etc.
    elif data.startswith("page_"):
        _, sort_by, page = data.split("_", 2)
        page = int(page)

    else:
        return

    await query.edit_message_text(
        text=build_message(sort_by, page),
        parse_mode="MarkdownV2",
        reply_markup=build_keyboard(sort_by, page),
    )


# main

def main():
    print("🤖 Bot starting…")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",   cmd_start))
    app.add_handler(CommandHandler("post",    cmd_post))
    app.add_handler(CommandHandler("preview", cmd_preview))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("✅ Running!  /start  /preview  /post")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ParseMode

from loader import dp, languages_worker, users_worker, subscribes_worker
from keyboards.inline import get_main_keyboard, get_subscribes_keyboard, get_move_keyboard, get_balance_keyboard, \
    get_cancel_keyboard, get_search_keyboard, get_fundraising_keyboard
from keyboards.inline.callbacks import navigation_callback
from states.make_question import QuestionInput


@dp.callback_query_handler(navigation_callback.filter(to="main"))
async def send_main_menu(call: CallbackQuery):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "mainMenu")

    await call.message.edit_text(text["mainMenu"], reply_markup=await get_main_keyboard(call.from_user.id))


@dp.callback_query_handler(navigation_callback.filter(to="subscribes"))
async def send_subscribes_menu(call: CallbackQuery):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "subscribesMenu, subscribeFormat")
    is_sub = subscribes_worker.is_user_have_active_subscribe(call.from_user.id)

    print(is_sub)
    if is_sub:
        subscribe_status = text["subscribeFormat"].format(end_date=is_sub)
    else:
        subscribe_status = ""
    print(subscribe_status)

    await call.message.edit_text(text["subscribesMenu"].format(subscribe=subscribe_status),
                                 reply_markup=await get_subscribes_keyboard(call.from_user.id))


@dp.callback_query_handler(navigation_callback.filter(to="info"))
async def send_info(call: CallbackQuery):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "info")

    await call.message.edit_text(text["info"], reply_markup=await get_move_keyboard(call.from_user.id))


@dp.callback_query_handler(navigation_callback.filter(to="balance"))
async def send_balance(call: CallbackQuery):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "balanceMenu")

    await call.message.edit_text(text["balanceMenu"].format(balance=users_worker.get_balance(call.from_user.id)),
                                 reply_markup=await get_balance_keyboard(call.from_user.id))


@dp.callback_query_handler(navigation_callback.filter(to="question"))
async def send_question_input(call: CallbackQuery, state: FSMContext):
    await state.update_data(main_msg=call.message)
    await QuestionInput.input.set()

    text = languages_worker.get_text_on_user_language(call.from_user.id, "questionInput")

    await call.message.edit_text(text["questionInput"], reply_markup=await get_cancel_keyboard(call.from_user.id))


@dp.callback_query_handler(navigation_callback.filter(to="archive"))
async def send_archive_search(call: CallbackQuery):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "booksArchiveMenu")

    await call.message.edit_text(text["booksArchiveMenu"], reply_markup=await get_search_keyboard(call.from_user.id))


@dp.callback_query_handler(navigation_callback.filter(to="fundraising"))
async def send_fundraising_menu(call: CallbackQuery):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "fundraisingMenu")

    await call.message.edit_text(text["fundraisingMenu"], reply_markup=await get_fundraising_keyboard(call.from_user.id))

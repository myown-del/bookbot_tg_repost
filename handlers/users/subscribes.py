from aiogram.types import CallbackQuery

from loader import dp, users_worker, languages_worker
from keyboards.inline import get_subscribes_keyboard, get_payment_keyboard
from keyboards.inline.callbacks import buy_subscribe_callback


@dp.callback_query_handler(buy_subscribe_callback.filter())
async def send_sub_payment(call: CallbackQuery, callback_data: dict):
    text = languages_worker.get_text_on_user_language(call.from_user.id, "paymentMenu")

    await call.message.edit_text(text["paymentMenu"],
                                 reply_markup=await get_payment_keyboard(call.from_user.id, for_subs=True, value=callback_data["id"], back="subscribes"))
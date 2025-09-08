from aiogram.dispatcher import FSMContext


async def safe_state_finish(state: FSMContext):
    """Safely finish state without causing KeyError"""
    try:
        current_state = await state.get_state()
        if current_state:
            await state.finish()
    except KeyError:
        print("State was already cleaned up")
    except Exception as e:
        print(f"Error finishing state: {e}")
        try:
            await state.reset_state()
        except:
            pass

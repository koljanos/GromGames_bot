import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, SceneRegistry, ScenesManager, on
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.types import KeyboardButton, Message, ReplyKeyboardRemove
from aiogram.utils.formatting import (
    Bold,
    as_key_value,
    as_list,
    as_numbered_list,
    as_section,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import yaml
with open('config.yaml') as f:
    config = yaml.safe_load(f)
TOKEN = config['token']

@dataclass
class Answer:
    """
    Represents an answer to a question.
    """

    text: str
    """The answer text"""
    next_state: str
    """Indicates if the answer is correct"""


@dataclass
class Question:
    """
    Class representing a onboarding with a question and a list of answers.
    """

    text: str
    """The question text"""

    previous: str
    """Previous state"""

    answers: list[Answer]
    """List of answers"""


scenes = config['states']
print(TOKEN)
QUESTIONS = {}
for k,v in scenes.items():
    QUESTIONS[k]=(Question(text=v['text'], previous =v['previous'],
                              answers=[Answer(text=elem['text'], next_state=elem['next_state']) for elem in v['buttons']]))


class OnboardingScene(Scene, state="onboarding"):
    """
    This class represents a scene for a onboarding game.

    It inherits from Scene class and is associated with the state "onboarding".
    It handles the logic and flow of the onboarding.
    """

    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext, status: str = 'welcome') -> Any:
        """
        Method triggered when the user enters the onboarding scene.

        It displays the current question and answer options to the user.

        :param message:
        :param state:
        :param step: Scene argument, can be passed to the scene using the wizard
        :return:
        """
        if status == 'welcome':
            # This is the first step, so we should greet the user
            await state.update_data(status=status, previous = 'welcome')
            await message.answer("Welcome to the onboarding!")
        
            

        try:
            onboarding = QUESTIONS[status]
        except IndexError:
            # This error means that the question's list is over
            return await self.wizard.exit()

        markup = ReplyKeyboardBuilder()
        markup.add(*[KeyboardButton(text=answer.text) for answer in onboarding.answers])

        # markup.button(text="🔙 Back")
        # markup.button(text="🚫 Exit")
        data = await state.get_data()
        await state.update_data(status=status, previous = data['status'])
        return await message.answer(
            text=QUESTIONS[status].text,
            reply_markup=markup.adjust(2).as_markup(resize_keyboard=True),
            parse_mode = ParseMode.HTML,
            disable_web_page_preview= True,
        )

    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext) -> None:
        """
        Method triggered when the user exits the onboarding scene.

        It displays the user's answers and clears the stored answers.

        :param message:
        :param state:
        :return:
        """
        data = await state.get_data()
        answers = data.get("answers", {})

        user_answers = []
        for step, answer in answers.items():
            user_answers.append(f"Question {step + 1}: {answer}")

        content = as_list(
            as_section(
                Bold("Your answers:"),
                as_numbered_list(*user_answers),
            ),
        )

        await message.answer(**content.as_kwargs(), reply_markup=ReplyKeyboardRemove())
        await state.set_data({})

    # @on.message(F.text == "🔙 Back")
    # async def back(self, message: Message, state: FSMContext) -> None:
    #     """
    #     Method triggered when the user selects the "Back" button.

    #     It allows the user to go back to the previous question.

    #     :param message:
    #     :param state:
    #     :return:
    #     """
    #     data = await state.get_data()
    #     status = data["status"]
    #     previous_status = QUESTIONS[status].previous
    #     await state.update_data(status=previous_status, previous = previous_status)

    #     return await self.wizard.retake(status=previous_status)

    # @on.message(F.text == "🚫 Exit")
    # async def exit(self, message: Message) -> None:
    #     """
    #     Method triggered when the user selects the "Exit" button.

    #     It exits the onboarding.

    #     :param message:
    #     :return:
    #     """
    #     await self.wizard.exit()

    @on.message(F.text)
    async def answer(self, message: Message, state: FSMContext) -> None:
        """
        Method triggered when the user selects an answer.

        It stores the answer and proceeds to the next question.

        :param message:
        :param state:
        :return:
        """
        data = await state.get_data()
        previous_status = data["status"]
        inbound_status = message.text
        for elem in QUESTIONS[previous_status].answers:
            if inbound_status == elem.text:
                status = elem.next_state
        await state.update_data(status=status, previous=previous_status)

        await self.wizard.retake(status=status)

    @on.message()
    async def unknown_message(self, message: Message) -> None:
        """
        Method triggered when the user sends a message that is not a command or an answer.

        It asks the user to select an answer.

        :param message: The message received from the user.
        :return: None
        """
        await message.answer("Please select an answer.")


onboarding_router = Router(name=__name__)
# Add handler that initializes the scene
onboarding_router.message.register(OnboardingScene.as_handler(), Command("onboarding"))


@onboarding_router.message(Command("start"))
async def command_start(message: Message, scenes: ScenesManager):
    await scenes.close()
    await message.answer(
        config['welcome'],
        reply_markup=ReplyKeyboardRemove(),
    )


def create_dispatcher():
    # Event isolation is needed to correctly handle fast user responses
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation(),
    )
    dispatcher.include_router(onboarding_router)

    # To use scenes, you should create a SceneRegistry and register your scenes there
    scene_registry = SceneRegistry(dispatcher)
    # ... and then register a scene in the registry
    # by default, Scene will be mounted to the router that passed to the SceneRegistry,
    # but you can specify the router explicitly using the `router` argument
    scene_registry.add(OnboardingScene)

    return dispatcher


async def main():
    dispatcher = create_dispatcher()
    bot = Bot(TOKEN)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    # Alternatively, you can use aiogram-cli:
    # `aiogram run polling onboarding_scene:create_dispatcher --log-level info --token BOT_TOKEN`
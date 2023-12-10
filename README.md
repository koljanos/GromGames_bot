# GromGames_bot
 A telegram chatbot for gromgames

This is a Python project that uses a virtual environment and requires certain dependencies to run. Follow the instructions below to set up the project.
## Setting Up the Virtual Environment

To create a virtual environment, navigate to the project directory and run the following command:
```bash
python3 -m venv venv
```


This will create a new virtual environment in a folder named venv.

To activate the virtual environment, use the following command:

- On Windows:
```bash
.\venv\Scripts\activate
```


- On Unix or MacOS:
```bash
source venv/bin/activate
```
activate

## Installing Dependencies

This project has a list of dependencies specified in a requirements.txt file. After activating the virtual environment, install these dependencies using the following command:
txt
```bash
pip install -r requirements.txt
```

## Configuring the Project

The project's configuration is stored in a `config.yaml` file. You can edit this file to change the configuration of the project. Be sure to follow the correct YAML syntax when editing this file.

The config.yaml file is used to configure the behavior of the bot. Here's a brief explanation of each section:
```yaml
token: "Your Bot Token" # Replace with your bot token
welcome: "Welcome Message" # The welcome message when a user starts the bot

states: # The states represent the different stages or screens of your bot
  welcome: # The name of the state
    text: "Welcome message" # The message to display in this state
    previous: "previous state" # The name of the previous state
    buttons: # The buttons to display in this state
      - text: "Button Text" # The text on the button
        next_state: "next state" # The state to go to when this button is clicked
```

You can add as many states as you want, and each state can have as many buttons as you want. The previous field is optional and is used to specify a state to go back to.

Here's an example of how to edit the `config.yaml` file:
```yaml
token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11" # Replace with your bot token
welcome: "Hello, start with /onboarding"

states:
  welcome:
    text: "Welcome <b>{'name'}</b>"
    previous: "welcome"
    buttons:
      - text: "Who are you?"
        next_state: "whoareu"
  whoareu:
    text: "Choose your role"
    previous: "welcome"
    buttons:
      - text: "Game Studio"
        next_state: "gamemaker"
      - text: "Content Maker"
        next_state: "contentmaker"
      - text: "Back"
        next_state: "welcome"
```

Remember to replace the token with your actual bot token. The welcome field should be the command that users use to start the bot. The states field defines the different stages of your bot. Each state has a text field which is the message that will be displayed in that state, and a buttons field which is a list of buttons that will be displayed in that state. Each button has a text field which is the text that will be displayed on the button, and a next_state field which is the state that the bot will go to when the button is clicked.

## Running the Project
```
python bot.py
```
After setting up the virtual environment, installing dependencies, and configuring the project, you can now run the project. The command to run the project will depend on the specific project. Typically, it might be something like:

```
python bot.py
```


Remember to always activate the virtual environment before running the project.
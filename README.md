# GAFT(gpt assistant for telegram)


## Описание
Проект GAFT на базе проекта <a href="https://github.com/xtekky/gpt4free">GPT4FREE</a> 
позволяет перенаправлять сообщения к телеграмм-боту провайдерам gpt-ассистентов,
отправлять от имени телеграмм-бота полученные ответы в исходный чат, поддерживая
контекст беседы

## Как запустить проект:

* Выполнить последовательно в командной строке:
  - Клонировать репозиторий:
    ```
    git clone https://github.com/acunathink/gaft_bot.git && cd gaft_bot
    ```

  - Cоздать виртуальное окружение:
    * <sub>linux/macos:</sub>
    ```
    python3 -m venv .venv
    ```
    * <sub>windows:</sub>
    ```
    python -m venv .venv
    ```

  - Aктивировать виртуальное окружение:
    * <sub>linux/macos:</sub>
    ```
    source .venv/bin/activate
    ```
    * <sub>windows:</sub>
    ```
    source .venv/scripts/activate
    ```

  - Установить зависимости из файла requirements.txt:
    ```
    pip install -r requirements.txt
    ```

    - Cоздать файл .env c вашим токеном для телеграам бота:
    ```
    echo "TELEGRAM_TOKEN = '001000100:OOO0oOooo0oOOo-OOOOo00oO-o0OOOooOO'" > .env
    ```

    Запустить модуль get_gpt.py:
    ```
    python get_gpt.py
    ```

## Логгирование осуществляется в файл log_gpt.txt
* Просмотреть логи можно через cat, например:
    ```
    cat log_gpt.txt
    ```



> **Note**
> By using this repository or any code related to it, you agree to the [legal notice](./LEGAL_NOTICE.md). The author is not responsible for any copies, forks, re-uploads made by other users, or anything else related to GPT4Free. This is the author's only account and repository. To prevent impersonation or irresponsible actions, please comply with the GNU GPL license this Repository uses.

## New features
* Telegram Channel: [t.me/g4f_channel](https://telegram.me/g4f_channel)
* g4f documentation (unfinished): [g4f.mintlify.app](https://g4f.mintlify.app) | Contribute to the docs via: [github.com/xtekky/gpt4free-docs](https://github.com/xtekky/gpt4free-docs)

## Usage

### The `g4f` Package
##### Proxy and Timeout Support:

All providers support specifying a proxy and increasing timeout in the create functions.

```py
import g4f

response = g4f.ChatCompletion.create(
    model=g4f.models.default,
    messages=[{"role": "user", "content": "Hello"}],
    proxy="http://host:port",
    # or socks5://user:pass@host:port
    timeout=120, # in secs
)

print(f"Result:", response)
```

### interference openai-proxy API (use with openai python package)

#### run interference API from PyPi package:
```py
from g4f.api import run_api

run_api()
```

#### run interference API from repo:
If you want to use the embedding function, you need to get a Hugging Face token. You can get one at https://huggingface.co/settings/tokens make sure your role is set to write. If you have your token, just use it instead of the OpenAI api-key.

run server:

```sh
g4f api
```

or

```sh
python -m g4f.api
```

```py
import openai

# Set your Hugging Face token as the API key if you use embeddings
# If you don't use embeddings, leave it empty
openai.api_key = "YOUR_HUGGING_FACE_TOKEN"  # Replace with your actual token

# Set the API base URL if needed, e.g., for a local development environment
openai.api_base = "http://localhost:1337/v1"

def main():
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "write a poem about a tree"}],
        stream=True,
    )

    if isinstance(chat_completion, dict):
        # Not streaming
        print(chat_completion.choices[0].message.content)
    else:
        # Streaming
        for token in chat_completion:
            content = token["choices"][0]["delta"].get("content")
            if content is not None:
                print(content, end="", flush=True)

if __name__ == "__main":
    main()

```

This project is currently using reverse engineered bing from
<a href="https://github.com/xtekky/gpt4free">GPT4FREE</a>

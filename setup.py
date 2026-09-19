from setuptools import setup, find_packages

setup(
    name="json-telegram-bot",
    version="0.1.2",
    packages=find_packages(),
    author="https://t.me/jackson_rodger",
    description=(
        "Build Telegram bots from JSON configuration with JsonTelegramBot"
    ),
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sinofarmonov323/jsonbot",
    project_urls={
        "Source": "https://github.com/sinofarmonov323/JsonTelegramBot",
        "Issues": "https://github.com/sinofarmonov323/JsonTelegramBot/issues",
        "Documentation": "https://github.com/sinofarmonov323/JsonTelegramBot#readme",
    },
    license="MIT",
    license_files=("LICENSE",),
    keywords=[
        "telegram",
        "telegram-bot",
        "telegram-bot-api",
        "json",
        "json-config",
        "python",
        "osonbot",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "osonbot"
    ]
)

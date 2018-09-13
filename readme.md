# Forensic Framework

## About

This framework provides utilities for quick development of functions for forensic analysis of databases.

Currently the following databases are supported:
- MySQL / MariaDB
- PostgreSQL
- SQLite
- Oracle

The following classes can be used to generate visually appealing results:
- Chat (Conversation, Participant, Message)
- Purchases (ShoppingCard, Article)
- Timeline (TimelineElement)

Each of these classes support exporting as HTML or Excel.

## Installation

Make sure you have `python 3.7`, `pip` and `pipenv` installed. Clone this repository and do:
- `pipenv install`
- `pipenv shell`
- `python main.py --help` 

## Examples

Take a look at the `plugins` directory. Example databases can be downloaded here: [databases.zip](https://files.fm/u/44s6dceq)

## Available Commands

### connection:list

Each time the framework boots, it loads the `Connectionfile` file. This command prints out each section to the console. Mainly used for debugging purposes.

### connection:show \<connection\>

Prints out info about a given connection. Mainly used for debugging purposes.

### connection:hash \<connection\>

Generates a similarity hash over a given connection name by serializing all of the column names. The resulting hash can be used in the metadata file of a plugin. The framework can then guess which plugins are likely to be used for this connection. Mainly used for creating the metadata in a `Pluginfile`.

### connection:guess \<connection\>

Tries to find a matching plugin by calculating the similarity hash for the given connection. The framework then compares the value against each `Pluginfile`. If a plugin has a similarity over 75% it will be printed.

### plugin:list

This command lists all detected plugins in the `plugin` directory. Mainly used for debugging purposes.

### plugin:show \<plugin\>

Prints out info about a given plugin. Mainly used for debugging purposes.

### plugin:run:\<plugin\>

Executes the given plugin. If no further commands are given, it will print a help page.

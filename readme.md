# Forensic Framework

## Commands

### connection:list

Each time the framework boots, it loads the `connections.ini` file. This command prints out each section to the console. Mainly used for debugging purposes.

### connection:hash

Generates a similarity hash over a given connection name by serializing all of the tables and column names. The resulting hash can be used in the metadata file of a plugin. The framework can then guess which plugins are likely to be used for this connection.
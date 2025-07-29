# Graph visualiser

The Graph Visualizer is a program that loads and displays graphs. 
Data source plugins convert files into graph data, while visualizers render them for viewing.

## Getting started

Make sure you have Python 3.10 installed on your system before running this project. 

You can check your Python version by running the following command:

```bash
python --version
```

### Installation

*Optional*: Install virtual environment with following command:
```bash
chmod +x venv.sh && ./venv.sh  # for linux / macos
call venv.bat                  # for windows (run in cmd, not integrated terminal)
```

Install project dependencies:
```bash
chmod +x install.sh && ./install.sh # for linux / macOS
call install.bat                    # for windows (run in cmd, not integrated terminal)
```

Run server:
```bash
chmod +x run.sh && ./run.sh # for linux
call run.bat                # for windows (run in cmd, not integrated terminal)
```
## Plugins
There are two types of plugins - *visualizer* and *data sources*.
#### Data source plugins:
- JSON
- todo...
#### Visualizer plugins:
- Block visualizer
- Simple visualizer

### JSON Data Source
This plugin parses a JSON file and creates a graph. The JSON syntax is extended to support cyclic graphs.
- By default, each node has an `"@id"` key representing its unique identifier.
- To create an edge between two nodes, use the format `"&<id>"` in the value of the key to reference the target node.

Here’s an example:
```json
[
  {
    "@id": "YWtvX292b19jaXRhc19jYXJfc2k=",
    "name": "Joe",
    "friends": ["&amFfc2FtX3N2ZXRza2lfbWVnYV9jYXI="] 
  },
  {
    "@id": "amFfc2FtX3N2ZXRza2lfbWVnYV9jYXI=",
    "name": "Jane",
    "friends": ["&YWtvX292b19jaXRhc19jYXJfc2k=", "&bmFjZXNfbmlzdGFfemFuaW1saml2b19uYWNpX292ZGU="]
  },
  {
    "@id": "bmFjZXNfbmlzdGFfemFuaW1saml2b19uYWNpX292ZGU=",
    "name": "Bob",
    "friends": ["&YWtvX292b19jaXRhc19jYXJfc2k="]
  }
]
```
You can change the name of unique key and reference prefix with CLI:
```bash
json_loader init                    # Initializes the JSON config file
json_loader --id <id>               # Sets a new ID for the config (replace <id> with your desired value)
json_loader --ref-prefix <prefix>   # Sets a new reference for the config (replace <prefix> with your desired value)
json_loader --help | -h             # Shows this help page
```
or directly in `config.json` file:
```json
{
    "id-field": "@id",
    "ref-prefix": "&"
}
```
>  ⚠️ A node cannot reference the same node more than once. The following is not valid:
> ```json
> [
>   {
>     "@id": "123"
>   },
>   {
>     "ref": "&123",
>     "second_ref": "&123"
>   }
> ]
> ```

> ⚠️ All references must be defined!



## Authors:
- [Lazar Nagulov](https://github.com/lazarnagulov)
- [Filip Tot](https://github.com/FilipT03)
- [Stefan Lekić](https://github.com/SirBoi)
- [Leon Jurić](https://github.com/ConfusingBox)
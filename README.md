<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url] 
[![Unlicense License][license-shield]][license-url]
[![Last Commit][last-commit-shield]][last-commit-url]


<div align="center"> 
    <h1 align="center">GRAPH VISUALIZER</h1> 
    <p align="center"> <br /> 
        <a href="https://github.com/lazarnagulov/graph-visualizer/issues/new?labels=bug">Report Bug</a> 
    </p> 
</div> 

<details> 
    <summary>Table of Contents</summary> 
    <ol> 
        <li> <a href="#-about-the-project">About The Project</a> 
            <ul> 
                <li><a href="#-built-with">Built With</a></li> 
            </ul> 
        </li> 
        <li> <a href="#-getting-started">Getting Started</a> 
            <ul> 
                <li><a href="#-installation-steps">Installation Steps</a></li> 
            </ul> 
        </li> 
        <li><a href="#-plugins">Plugins</a>
            <ul>
                <li><a href="#-json-data-source">JSON Data Source</a></li> 
                <li><a href="#-python-data-source">Python Data Source</a></li> 
            </ul>
        </li> 
        <li><a href="#-running-the-server">Running the Server</a></li> 
        <li><a href="#-authors">Authors</a></li> 
    </ol> 
</details>

## 📋 About The Project
Graph Visualizer is a modular and extensible web platform designed to load and render graphs.
It allows you to visualize complex data structures using plugin-based data sources and visual renderers. 
The backend is powered by Django, while the core logic is implemented in Python.
<br/>
### 🔧 Built With
This project uses the following core technologies:

[![Python][Python-img]][Python-url]  

[![Django][Django-img]][Django-url]

[![D3.js][D3-img]][D3-url]  

[![HTMX][HTMX-img]][HTMX-url]

<br/>

## 🚀 Getting Started
Before running the project, ensure you have Python 3.10+ installed.

Check your version:
```bash
python --version
```

### 🛠️ Installation Steps
1. Clone the repository:
```bash
git clone https://github.com/lazarnagulov/graph-visualizer.git
cd graph-visualizer
```
2. Create and activate virtual environment (optional but recommended):
```bash
chmod +x venv.sh && ./venv.sh   # Linux / macOS
call venv.bat                   # Windows (use CMD, not integrated terminal) 
```
3.  Install dependencies:
```bash
chmod +x install.sh && ./install.sh   # Linux / macOS
call install.bat                      # Windows (use CMD) 
```
<br/>

## 🧩 Plugins
Graph Visualizer uses a plugin-based architecture. There are two plugin types:

#### 🔌 Data Source Plugins
These convert raw files into graph data.
- JSON
- Python

#### 🖼️ Visualizer Plugins
These render the graph in different ways.
- Block Visualizer
- Simple Visualizer
<br/>

### 🧾 JSON Data Source
The JSON plugin supports cyclic graph definitions using a custom referencing system.
#### 🔗 Syntax Overview
Each node can include a unique ID field (default: "@id").
To create edges, use references with the prefix "&" followed by the target node's ID.
Example:
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

> [!IMPORTANT]
> References must be defined!

#### ⚙️ Custom Configuration
Customize ID field and reference prefix:
```
json_loader init
json_loader --id <your_id_field>
json_loader --ref-prefix <your_prefix>
```
Or modify directly in config.json:
```json
{
  "id-field": "@id",
  "ref-prefix": "&"
}
```

### 🐍 Python Data Source
The Python plugin generates graphs by analyzing the AST, representing functions and classes as nodes 
and calls as edges.</br>

## ▶️ Running the Server
Run the Django server:
```
chmod +x run.sh && ./run.sh     # Linux / macOS
call run.bat                    # Windows (use CMD)
```
Default server URL:
📍 http://localhost:8000
<br/>

## 👤 Authors:
- [Lazar Nagulov](https://github.com/lazarnagulov)
- [Filip Tot](https://github.com/FilipT03)
- [Stefan Lekić](https://github.com/SirBoi)
- [Leon Jurić](https://github.com/ConfusingBox)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Python-img]: https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white
[Python-url]: https://www.python.org/

[Django-img]: https://img.shields.io/badge/Django-5.1+-success?logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/

[D3-img]: https://img.shields.io/badge/D3.js-F9A03C?logo=d3.js&logoColor=white
[D3-url]: https://d3js.org/

[HTMX-img]: https://img.shields.io/badge/HTMX-FF6F61?logo=htmx&logoColor=white
[HTMX-url]: https://htmx.org/

[contributors-shield]: https://img.shields.io/github/contributors/lazarnagulov/graph-visualizer.svg?style=for-the-badge
[contributors-url]: https://github/contributors/lazarnagulov/graph-visualizer/graphs/contributors
[license-shield]: https://img.shields.io/github/license/lazarnagulov/graph-visualizer.svg?style=for-the-badge
[license-url]: https://github.com/lazarnagulov/graph-visualizer/blob/master/LICENSE.txt
[last-commit-shield]: https://img.shields.io/github/last-commit/lazarnagulov/graph-visualizer?branch=main&style=for-the-badge
[last-commit-url]: https://github.com/lazarnagulov/graph-visualizer/commits/main
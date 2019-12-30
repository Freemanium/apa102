# stripctl

## Installation

```bash
git clone https://github.com/Freemanium/stripctl
cd stripctl
pip install -U .
```

## Usage

```python
from stripctl import APA102
from stripctl.colors import *

strip = APA102(60)
strip.reset()
strip.flush()
```

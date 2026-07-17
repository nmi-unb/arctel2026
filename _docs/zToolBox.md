<link rel="stylesheet" type="text/css" href=".css/style.css">

# ToolBox Manual

## ⚠️ Atualizar a instalação global

Se você alterar ou adicionar módulos na `toolbox`, reinstale a ferramenta:

```pwsh
    :: Caminho Relativo
$TOOLBOX_DIR = "..\toolbox"
uv tool install --reinstall $TOOLBOX_DIR
```

## Caminhos úteis

- Direitório atual
```pwsh
    :: Caminho Relativo
    $REPO_ALVO = "..\arctel2026"
```
- Direitório da ToolBox
```pwsh
    :: Caminho Relativo
    $TOOLBOX_DIR = "..\toolbox"
```
- Path filtro:
```pwsh
    $CONFIG_FILE = "..\arctel2026\_docs\zFilter.py"
```


## Tree

- Fluxo mínimo recomendado:

```pwsh
    $TOOLBOX_DIR = "C:\Users\Cadu\Documents\GitHub\toolbox"   # substitua pelo seu caminho
    cd $TOOLBOX_DIR
    uv sync
    uv run toolbox list
    uv tool install $TOOLBOX_DIR
    cd $REPO_ALVO
```

- Exemplo de Uso
```pwsh
$REPO_ALVO="..\arctel2026"

$TOOLBOX_DIR="..\toolbox"

$CONFIG_FILE="..\arctel2026\_docs\zFilter.py"

toolbox run file_tree -- $REPO_ALVO --config $CONFIG_FILE
```

- Exemplo de Uso [UBUNTU]
```BASH
REPO_ALVO="../arctel2026"

TOOLBOX_DIR="../toolbox"

CONFIG_FILE="_docs/zFilter.py"

toolbox run file_tree -- "$REPO_ALVO" --config "$CONFIG_FILE"
```


### init_gen

```pwsh
    toolbox run init_generator "[TAGET_DIR]"
```

### deploy

```pwsh
    toolbox run deploy_filter -- ../arctel2026 --config .\_docs\dFilter.py
```
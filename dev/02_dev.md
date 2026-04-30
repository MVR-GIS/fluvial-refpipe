# Chat Instructions

## Specify Chat Instructions
```{r}
reproducibleai::use_instructions(c("chat-manual", "goals", "r-package"))
```

## Start new chat prompt text:
Target repo: `MVR-GIS/fluvial-refpipe`  
Read `dev/instructions/CHAT_INSTRUCTIONS.md` and follow the specified instruction modules in order. 
Task: Next unchecked item in `dev/05_plan.md`.

## Update AI Chat Artifacts
```{r}
reproducibleai::extract_copilot_chat(file.path(
  Sys.getenv("USERPROFILE"), "Downloads", "copilot_export.zip")
)
```



# Conda Environment

## Initialize conda to work inside PowerShell (do once per computer)
```{powershell}
conda init powershell
```

## Create the conda environment (do once percomputer)
```{powershell}
mamba env create -f environment.yml
```

## Daily update routine
```{powershell}
conda activate analysis
mamba env update -f environment.yml --prune
python -m pip install -e .
pytest -q
```


## Run tests
```{powershell}
conda activate analysis
python -m pip install -e .
pytest -q
```
# Chat Instructions

## Specify Chat Instructions
```{r}
reproducibleai::use_instructions(c("chat-manual", "goals", "r-package"))
```

## Start new chat prompt text:
# This session will be based on the `MVR-GIS/fluvial-refpipe`
# repo `main` branch. Read `dev/instructions/CHAT_INSTRUCTIONS.md` 
# and follow the instruction modules listed under "Selected 
# instruction modules (read in order)".

## Update AI Chat Artifacts
```{r}
reproducibleai::extract_copilot_chat(file.path(
  Sys.getenv("USERPROFILE"), "Downloads", "copilot_export.zip")
)
```



# Conda Environment

## Initialize conda to work inside PowerShell (do once per computer)
```{bash}
conda init powershell
```

## Create the conda environment (do once percomputer)
```{bash}
mamba env create -f environment.yml
```

## Daily update routine
```{bash}
conda activate analysis
mamba env update -f environment.yml --prune
python -m pip install -e .
refpipe --help
pytest -q
```

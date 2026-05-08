# DoD / USACE Windows + InstallRoot + Miniforge: Conda environment setup (reliable)

This repo uses conda-forge packages. On USACE/DoD networks, TLS inspection + InstallRoot can cause **mamba/libmamba** to fail with errors like:

- `schannel: ... untrusted root`
- `self-signed certificate in certificate chain`
- `CA file exceeds max size of 1048576 bytes`

This guidance avoids those issues with a reliable baseline that works on locked-down networks.

---

## 0) Prerequisites (one time)

### InstallRoot
1. Install **InstallRoot** via the USACE App Portal.
2. Open InstallRoot and click **Install Certificates**.

### Miniforge
Install Miniforge (conda-forge). Confirm:

- `conda --version`
- `conda info`

---

## 1) Recommended configuration (one time per user)

### Use the classic solver (reliable on DoD networks)

`libmamba` is fast, but on inspected networks it commonly fails due to Windows SChannel / certificate-chain behavior.

Set conda to use the classic solver:

- `conda config --set solver classic`
- `conda config --set channel_priority strict`
- `conda config --set ssl_verify True`

Verify:

- `conda config --show solver`
- `conda config --show ssl_verify`

Expected:

- `solver: classic`
- `ssl_verify: True`

**Important notes**
- Do **not** set `ssl_verify: False` (insecure).
- Avoid custom CA bundle files unless IT provides an official bundle; ad-hoc CA files can break validation of public CAs (for example, Let’s Encrypt sites like `prefix.dev`).

---

## 2) Create/update the environment (normal workflow)

From the repo root:

- `conda env update -f environment.yml --prune`

Activate and run tests:

- `conda activate <ENV_NAME_FROM_environment.yml>`
- `pytest -q`

Replace `<ENV_NAME_FROM_environment.yml>` with the actual env name (commonly `analysis`).

---

## 3) Make installs fast (avoid solving for every user)

Conda solving can be slow, especially on Windows. The best team workflow is:

- One person (or CI) solves once
- Everyone else installs from an **explicit spec** (no solving)

### 3.1 Create an explicit spec (maintainers)

After you’ve created a working environment:

- `conda activate <ENV_NAME>`
- `conda list --explicit > conda-win-64-explicit.txt`

Commit `conda-win-64-explicit.txt` to the repo.

### 3.2 Install from the explicit spec (users)

This avoids dependency solving and is much faster and more deterministic:

- `conda create -n <ENV_NAME> --file conda-win-64-explicit.txt`
- `conda activate <ENV_NAME>`
- `pytest -q`

### When to regenerate the explicit spec

Regenerate `conda-win-64-explicit.txt` when:

- `environment.yml` changes, or
- you intentionally upgrade core dependencies (Python, GDAL, geopandas stack, etc.).

---

## 4) Troubleshooting

### A) If `mamba env update` fails with SSL errors

Use conda classic instead:

- `conda config --set solver classic`
- `conda config --set ssl_verify True`
- `conda env update -f environment.yml --prune`

### B) If conda fails with `self-signed certificate in certificate chain`

This usually means you are on a network segment doing TLS inspection and Python/conda isn’t seeing the right enterprise trust.

First steps that fix most cases:
1. Run InstallRoot again: **Install Certificates**
2. Close all shells, open a new PowerShell, retry:
   - `conda env update -f environment.yml --prune`

If it still fails:
- Capture the first ~20 lines of error output and the URL it fails on.
- Send to the project maintainer (or attach to an internal ticket).

### C) Git TLS settings

Changing Git’s TLS backend (e.g., `git config --global http.sslBackend schannel`) is unrelated to conda, but it can confuse debugging. Prefer leaving it at default unless required by policy.

## 5) Why we do it this way (rationale)

- InstallRoot primarily configures **Windows trust stores**.
- `mamba/libmamba` on Windows often hits edge cases with SChannel trust and CA bundle handling on inspected networks.
- conda classic is slower at solving, but it’s more reliable in this environment.
- The explicit-spec workflow eliminates most solving cost for end users.

## 6) Common scenario: you re-ran InstallRoot “Install Certificates” (updates)

It’s normal on USACE/DoD machines to re-run InstallRoot periodically to refresh/update certificates. Doing so can change which certificates are present/active in Windows trust stores and can coincide with network/VPN/proxy changes.

### What to do after re-running InstallRoot

1) **Close and reopen PowerShell** (recommended).  
   If things are still weird, rebooting once is the next step.

2) **Re-assert the known-good conda settings** (these are safe to re-run any time):

- `conda config --set solver classic`
- `conda config --set channel_priority strict`
- `conda config --set ssl_verify True`

3) **Clean caches if you were previously failing** (optional but often helpful):

- `conda clean -a`

4) **Update the environment as usual**:

- `conda env update -f environment.yml --prune`

5) **Quick verification**:

- `conda activate <ENV_NAME>`
- `pytest -q`

### If it still fails (after InstallRoot refresh)

- If you see `self-signed certificate in certificate chain` or other SSL errors:
  - Confirm `ssl_verify` is still `True` (not a path to a `.pem` and not `False`):
    - `conda config --show ssl_verify`
  - Retry from a fresh PowerShell session.
  - Capture the first ~20 lines of the error output including the URL it failed on and send it to the maintainer.

### Why this helps

- InstallRoot updates Windows certificate stores and sometimes triggers changes in how network inspection/proxies present certificates.
- Reopening PowerShell (and occasionally rebooting) ensures new processes pick up the updated trust/proxy environment.
- Keeping conda on the classic solver avoids libmamba/SChannel edge cases that commonly appear after cert/proxy changes on DoD networks.

---

## Suggested “Quick start” for README

### Windows (USACE/DoD / InstallRoot) quick start

1. `conda config --set solver classic`
2. `conda config --set channel_priority strict`
3. `conda config --set ssl_verify True`
4. `conda env update -f environment.yml --prune`
5. `conda activate analysis`
6. `pytest -q`

For faster installs, use `conda-win-64-explicit.txt` if provided.

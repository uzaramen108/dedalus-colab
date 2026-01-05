# dedalus on Google Colab

This repository provides a **reproducible Google Colab setup** for running
**dedalus** with MPI support using `micromamba`.

No local installation is required.

---

## 🚀 Colab Quick Start (1 Cell)

Open a new Google Colab notebook and run **this single cell**:

```python
# --------------------------------------------------
# 1️⃣ Mount Google Drive (optional, for cache)
# --------------------------------------------------
from google.colab import drive
import os

if not os.path.ismount("/content/drive"):
    drive.mount("/content/drive")
else:
    print("📦 Google Drive already mounted")

# --------------------------------------------------
# 2️⃣ Clone dedalus-colab repository (idempotent)
# --------------------------------------------------
from pathlib import Path
import subprocess

REPO_URL = "https://github.com/uzaramen108/dedalus-colab.git"
ROOT = Path("/content")
REPO_DIR = ROOT / "dedalus-colab"

def run(cmd):
    #print("$", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)

if not REPO_DIR.exists():
    print("📥 Cloning dedalus-colab...")
    run(["git", "clone", REPO_URL, str(REPO_DIR)])
elif not (REPO_DIR / ".git").exists():
    raise RuntimeError("Directory exists but is not a git repository")
else:
    print("📦 Repository already exists — skipping clone")

# --------------------------------------------------
# 3️⃣ Run setup_dedalus.py IN THIS KERNEL (CRITICAL)
# --------------------------------------------------
print("🚀 Running setup_dedalus.py in current kernel")

USE_CLEAN = False  # <--- Set True to remove existing environment
opts = "--clean" if USE_CLEAN else ""

get_ipython().run_line_magic(
    "run", f"{REPO_DIR / 'setup_dedalus.py'} {opts}"
)

# ==================================================
# 4️⃣ Sanity check
# ==================================================
try:
    get_ipython().run_cell_magic('dedalus', '--info -np 4', '')
except Exception as e:
    print("⚠️ %%dedalus magic not found:", e)
```

After this finishes, the Jupyter cell magic `%%dedalus` becomes available.

---

▶ Example

```python
%%dedalus -np 4 --time

from mpi4py import MPI
import dedalus

comm = MPI.COMM_WORLD

print(f"Hello from rank {comm.rank}", flush=True)
if comm.rank == 0:
    print(f"  dedalus : {dedalus.__version__}")
    print(f"  MPI size: {comm.size}")
```

This will measure elapsed time on rank `0`.

---

### 📦 What This Setup Does

- Installs dedalus using `micromamba`
- Enables MPI execution inside Colab
- Registers a custom Jupyter cell magic `%%dedalus`
- Keeps everything reproducible via GitHub

---

### 🔁 Re-running

- Restarting the Colab runtime removes the environment
- Simply re-run the Quick Start cell to restore everything

---

### 🧹 Clean Reinstall (Optional)

To force a clean reinstall of the environment:

```python
%run {REPO_DIR / 'setup_dedalus.py'} --clean
```

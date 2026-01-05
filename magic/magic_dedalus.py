from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
import subprocess
import sys
from pathlib import Path

@magics_class
class DedalusMagics(Magics):
    @magic_arguments()
    @argument("-np", "--nproc", type=int, default=1, help="Number of MPI processes")
    @cell_magic
    def dedalus(self, line, cell):
        """
        Run the cell content using mpiexec in the 'dedalus' micromamba environment.
        Usage: %%dedalus -np 4
        """
        args = parse_argstring(self.dedalus, line)
        
        # 1. Save cell content to a temporary file
        script_name = "dedalus_script.py"
        Path(script_name).write_text(cell)
        
        # 2. Build the command
        # micromamba run -n dedalus mpiexec -n <N> python <script>
        cmd = [
            "/content/micromamba/bin/micromamba", "run", "-n", "dedalus",
            "mpiexec", "-n", str(args.nproc),
            "python", script_name
        ]
        
        # 3. Run the command and stream output
        # Using Popen to stream stdout/stderr in real-time to Colab notebook
        print(f"🚀 Running with MPI (np={args.nproc})...")
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            for line in process.stdout:
                print(line, end="")
            
            process.wait()
            
            if process.returncode != 0:
                print(f"\n⚠️ Process failed with exit code {process.returncode}")
                
        except Exception as e:
            print(f"❌ Error execution failed: {e}")

# Register the magic
def load_ipython_extension(ipython):
    ipython.register_magics(DedalusMagics)
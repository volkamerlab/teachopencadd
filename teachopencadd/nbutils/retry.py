"""
Utilities to run our notebooks.
"""

import ast
import time

from IPython.core.magic import (
    Magics,
    magics_class,
    cell_magic,
    needs_local_scope,
    no_var_expand,
)


def retry_function(fn, attempts=5, delay_factor=2):
    """
    Attempt function, fn, `attempts` times, with increasing delays.

    Taken from https://github.com/Swarm-DISC/Swarm_quicklooks
    """
    for attempt in range(attempts):
        try:
            outputs = fn()
        except Exception as e:
            if attempt < attempts - 1:
                delay = (attempt + 1) * delay_factor
                print(f"Failed ({type(e).__name__}: {e}). Trying again in {delay}s...")
                time.sleep(delay)
                continue
            else:
                raise
        return outputs


@magics_class
class RetryMagics(Magics):
    @no_var_expand
    @cell_magic
    @needs_local_scope
    def retry(self, line, cell, local_ns=None):
        """"""
        opts, stmt = self.parse_options(line, "n:d:", posix=False, strict=False)
        if stmt == "" and cell is None:
            return

        attempts = int(getattr(opts, "n", 5))
        delay_factor = int(getattr(opts, "d", 2))

        transform = self.shell.transform_cell

        if cell is None:
            # called as line magic
            ast_setup = self.shell.compile.ast_parse("pass")
            ast_stmt = self.shell.compile.ast_parse(transform(stmt))
        else:
            ast_setup = self.shell.compile.ast_parse(transform(stmt))
            ast_stmt = self.shell.compile.ast_parse(transform(cell))

        ast_setup = self.shell.transform_ast(ast_setup)
        ast_stmt = self.shell.transform_ast(ast_stmt)

        retry_ast_template = ast.parse(
            "def inner():\n" "    setup\n" "    stmt\n" "    return locals()\n"
        )

        retry_ast = _RetryTemplateFiller(ast_setup, ast_stmt).visit(retry_ast_template)
        retry_ast = ast.fix_missing_locations(retry_ast)

        code = self.shell.compile(retry_ast, "<magic-retry>", "exec")

        ns = {}
        glob = self.shell.user_ns
        # handles global vars with same name as local vars. We store them in conflict_globs.
        conflict_globs = {}
        if local_ns:
            for var_name, var_val in glob.items():
                if var_name in local_ns:
                    conflict_globs[var_name] = var_val
            glob.update(local_ns)

        exec(code, glob, ns)

        runner = _Runner(attempts, delay_factor)
        runner.inner = ns["inner"]
        output = runner.run()

        # Restore global vars from conflict_globs
        if conflict_globs:
            glob.update(conflict_globs)

        glob.update(output)


class _Runner:
    def __init__(self, attempts=5, delay_factor=2):
        self.attempts = attempts
        self.delay_factor = delay_factor

    def run(self):
        for attempt in range(self.attempts):
            try:
                outputs = self.inner()
            except Exception as e:
                if attempt < self.attempts - 1:
                    delay = (attempt + 1) * self.delay_factor
                    print(f"Failed ({type(e).__name__}: {e}). Trying again in {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    raise
            return outputs


class _RetryTemplateFiller(ast.NodeTransformer):
    """Fill in the AST template for retried execution.

    This is quite closely tied to the template definition, which is in
    :meth:`RetryMagics.retry`.
    """

    def __init__(self, ast_setup, ast_stmt):
        self.ast_setup = ast_setup
        self.ast_stmt = ast_stmt

    def visit_FunctionDef(self, node):
        "Fill in the setup statement"
        self.generic_visit(node)
        if node.name == "inner":
            node.body[:-1] = self.ast_setup.body + self.ast_stmt.body

        return node


def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    ipython.register_magics(RetryMagics)

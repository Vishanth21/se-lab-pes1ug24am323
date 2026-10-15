# Static Analysis Issues - `scholarship_disbursement.py`

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection via string-built query | Security (Bandit B608, CWE-89, Medium) | 10 | `INSERT` is built with `%` interpolation of `student`, `scheme`, `amount`. A student name like `x', 'y', 0); DROP TABLE awards;--` destroys the ledger. | Parameterized query: `conn.execute("INSERT INTO awards (student, scheme, amount, disbursed) VALUES (?, ?, ?, 0)", (student, scheme, amount))`. |
| Mutable default argument `audit=[]` | Bug (Pylint W0102) | 9 | The default list is created once and shared across every call that omits `audit`, so entries accumulate globally. | Default to `audit=None` and create a fresh list inside the function, or drop the parameter. |
| Shell command with swallowed exception | Security (Bandit B605/B607/B110, Pylint W0718) | 24-28 | `os.system("echo archiving awards")` spawns a shell with a partial executable path. `except Exception: pass` hides every failure. | Use `subprocess.run(["echo", "archiving awards"], check=True)` and catch `subprocess.CalledProcessError` instead of `pass`. |
| Inconsistent return in `disburse` | Bug (Pylint R1710) | 15-21 | Returns `row[0]` when the award exists, returns `None` when it does not, so callers cannot distinguish not found from a real amount. | Return an explicit value on every path, e.g. `return 0` in the missing branch. |
| `global` mutation of module state | Design (Pylint W0603, C0103) | 6, 16 | `disbursed_total` is a module-level counter changed via `global`, and its name violates UPPER_CASE style. | Return the sum from `disburse`, or rename to `DISBURSED_TOTAL` and mutate it in one function. |
| Non-snake_case function name | Style (Pylint C0103) | 31 | `bySchemeCount` is camelCase, inconsistent with PEP 8. | Rename to `by_scheme_count` and update the call on line 41. |
| `== None` comparison | Style (Pylint C0121, Flake8 E711) | 32 | Identity comparison written as equality, and `__eq__` can override it. | Use `if scheme is None:`. |
| Missing docstrings | Documentation (Pylint C0114/C0116) | 1, 9, 15, 24, 31, 37 | No module docstring and no function docstrings. | Add a module docstring and one-line docstring per function. |
| Over-long lines | Style (Pylint C0301, Flake8 E501) | 5, 10, 17, 19, 34 | Lines exceed the 79/100-character limits. | Wrap the SQL statements, `SELECT`/`UPDATE` calls and the final `print` across multiple lines. |
| `%` formatting instead of f-string | Style (Pylint C0209) | 10 | printf-style formatting is harder to read. | Use an f-string for any remaining message formatting. |
| `main()` runs at import | Convention | 37-45 | `main()` is called at import time, so the module cannot be imported without side effects. | Guard with `if __name__ == "__main__":`. |

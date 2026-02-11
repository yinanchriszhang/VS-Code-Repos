# Calculator App

A simple desktop calculator implemented with Python's Tkinter.

Usage:

Run the app with:

```powershell
python calculator.py
```

The calculator supports basic arithmetic, parentheses, and exponentiation (`**`).

For a quick self-check (non-GUI), run:

```powershell
python -c "import calculator; print(calculator.self_test())"
```

This should print `True` if the evaluator works correctly.

Logging:

- The app appends each evaluated expression and its result to `calculator_log.csv` in the app folder.
- Columns: `timestamp` (UTC ISO), `expression`, `result`.

If you prefer a different dataset format (JSON, SQLite) or a different filename/location, tell me and I will add it.

import time

def log_step(step_name, start, end, extra=None):
    return {
        "step": step_name,
        "duration_sec": round(end - start, 3),
        "extra": extra
    }
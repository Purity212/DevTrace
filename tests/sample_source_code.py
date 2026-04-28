MIN_CONTROL_VALUE = 0
MAX_CONTROL_VALUE = 100


def run_memory_self_test(memory_status: str) -> bool:
    return memory_status == "ok"


def update_error_flag(memory_status: str) -> bool:
    self_test_passed = run_memory_self_test(memory_status)
    return not self_test_passed


def can_accept_control_command(error_flag: bool) -> bool:
    if error_flag:
        return False
    return True


def select_startup_mode(memory_status: str) -> str:
    if run_memory_self_test(memory_status):
        return "normal"
    return "error"


def clamp_control_command(command_value: int) -> int:
    if command_value < MIN_CONTROL_VALUE:
        return MIN_CONTROL_VALUE
    if command_value > MAX_CONTROL_VALUE:
        return MAX_CONTROL_VALUE
    return command_value


def store_last_control_command(state: dict, command_value: int) -> dict:
    state["last_control_command"] = command_value
    return state


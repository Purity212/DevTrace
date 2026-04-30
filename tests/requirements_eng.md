# Sample Requirements

REQ-CTRL-001: At startup, the system shall perform a memory self-test.
REQ-CTRL-002: If the memory self-test fails, the system shall set error_flag.
REQ-CTRL-003: When error_flag is active, the system shall ignore control commands.
REQ-CTRL-004: If the self-test completes successfully, the system shall switch to normal mode.
REQ-CTRL-005: The system shall clamp the control command to the allowed value range.
REQ-CTRL-006: The system shall store the last accepted control command.

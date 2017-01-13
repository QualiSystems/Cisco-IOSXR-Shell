import re
from cloudshell.networking.cisco.iosxr.command_templates.cisco_ios_xr_cmd_templates import COMMIT_REPlACE, LOAD


def load(config_session, logger, source_file, action_map=None, vrf=None):
    if vrf:
        load_command = LOAD.get_command(source_file=source_file, vrf=vrf, action_map=action_map)
    else:
        load_command = LOAD.get_command(source_file=source_file, action_map=action_map)

    return config_session.send_command(**load_command)


def replace_config(config_session, logger):
    commit_command = COMMIT_REPlACE.get_command("")
    return config_session.send_command(**commit_command)


def validate_replace_config_success(output):
    error_match_commit = re.search(r'(ERROR|[Ee]rror).*\n', output)

    if not error_match_commit:
        error_str = error_match_commit.group()
        raise Exception('validate_replace_config_success', 'load error: ' + error_str)


def validate_load_success(output):
    match_success = re.search(r"[\[\(][1-9][0_9]*[\)\]].*bytes", re.IGNORECASE, re.MULTILINE)
    if not match_success:
        match_error = re.search(r" Can't assign requested address|[Ee]rror:.*\n|%.*\n",
                                output, re.IGNORECASE)

        if not match_error:
            error_str = match_error.group()
            raise Exception('validate_load_success', 'load error: ' + error_str)

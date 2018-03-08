import json
import os


SETTINGS_PRIORITY = (
    'organization_settings',
    'project_settings'
    'spider_settings',
    'job_settings',
)
ENV_PREFIX = 'ENV_' 


def is_shub():
    """
    Whether we're running on scrapinghub
    """
    return 'SHUB_SETTINGS' in os.environ


_env_loaded = False
def load_env():
    """
    Since we can't specify environment variables in scrapinghub directly,
    we're loading them from provided settings by:
    - finding all ENV_ prefixed ones
    - removing the prefix
    - adding to os.environ
    """

    # Make sure we only load once
    global _env_loaded

    if _env_loaded:
        return
    _env_loaded = True

    shub_settings = json.loads(os.environ.get('SHUB_SETTINGS', '{}'))

    for settings_key in SETTINGS_PRIORITY:
        settings = shub_settings.get(settings_key, {})

        for key, value in settings.items():
            if key.startswith(ENV_PREFIX):
                env_key = key[len(ENV_PREFIX):]
                os.environ[env_key] = str(value)

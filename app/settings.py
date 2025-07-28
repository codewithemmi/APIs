def __init__(
    self,
    settings_cls: type[BaseSettings],
    env_file: DotenvType | None = ENV_FILE_SENTINEL,
    env_file_encoding: str | None = None,
    case_sensitive: bool | None = None,
    env_prefix: str | None = None,
    env_nested_delimiter: str | None = None,
    env_ignore_empty: bool | None = None,
    env_parse_none_str: str | None = None,
    env_parse_enums: bool | None = None,
) -> None:
    self.env_file = env_file if env_file != ENV_FILE_SENTINEL else settings_cls.model_config.get('env_file')
    self.env_file_encoding = (
        env_file_encoding if env_file_encoding is not None else settings_cls.model_config.get('env_file_encoding')
    )
    super().__init__(
        settings_cls,
        case_sensitive,
        env_prefix,
        env_nested_delimiter,
        env_ignore_empty,
        env_parse_none_str,
        env_parse_enums,
    )
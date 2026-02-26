"""Jinja2 template compiler for prompt rendering."""

from jinja2 import BaseLoader, Environment, sandbox

from prompt_engine.jinja_extensions.filters import register_filters


class TemplateCompiler:
    """Compiles and renders Jinja2 prompt templates."""

    def __init__(self) -> None:
        self._env = sandbox.SandboxedEnvironment(
            loader=BaseLoader(),
            autoescape=False,
            keep_trailing_newline=True,
            undefined=sandbox.ImmutableSandboxedEnvironment.undefined,
        )
        register_filters(self._env)

    def render(self, template_string: str, variables: dict) -> str:
        template = self._env.from_string(template_string)
        return template.render(**variables)

    def validate(self, template_string: str) -> list[str]:
        errors: list[str] = []
        try:
            self._env.parse(template_string)
        except Exception as e:
            errors.append(str(e))
        return errors

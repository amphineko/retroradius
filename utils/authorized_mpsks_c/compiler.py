#!/usr/bin/env python3

import json

import click
from jinja2 import Template


@click.command()
@click.option('--template', '-t', default='/template.j2')
def main(template):
    stdin = click.get_text_stream('stdin')
    user_input = json.loads(stdin.read())

    template = Template(click.open_file(template).read())

    rendered = template.render({
        "entries": [{
            "addr": entry["addr"].upper(),
            "mpsk": entry["mpsk"],
            "vlan": entry["vlan"],
        } for entry in user_input]
    })

    stdout = click.get_text_stream('stdout')
    stdout.write(rendered)


if __name__ == '__main__':
    main()

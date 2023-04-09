#!/usr/bin/env python3

import hashlib
import json
import secrets

import click
from Crypto.Hash import MD4
from jinja2 import Template


@click.command("authorized_mpsks")
@click.option('--template', '-t', default='/authorized_mpsks.j2')
def authorized_mpsks(template):
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


@click.command("authorized_users")
@click.option('--template', '-t', default='/authorized_users.j2')
def authorized_users(template):
    stdin = click.get_text_stream('stdin')
    user_input = json.loads(stdin.read())

    template = Template(click.open_file(template).read())

    rendered = template.render({
        "entries": [{
            "username": entry["username"],
            "nthash": entry["nthash"],
            "vlan": entry["vlan"],
        } for entry in user_input]
    })

    stdout = click.get_text_stream('stdout')
    stdout.write(rendered)


@click.command("update_user_hash")
@click.option('--json-path', '-j', default='/authorized_users.json')
def update_user_hash(json_path):
    user = click.prompt('Username')
    new_password = click.prompt('New password', hide_input=True)
    confirm_password = click.prompt('Confirm password', hide_input=True)

    if new_password != confirm_password:
        click.echo('Passwords do not match', err=True)
        exit(1)

    # generate random salt
    salt = secrets.token_hex(16)
    sha1 = hashlib.sha1((new_password + salt).encode('utf-8')).digest().hex()

    md4 = MD4.new()
    md4.update(new_password.encode('utf-16le'))
    md4 = md4.digest().hex()

    with open(json_path, 'r') as f:
        user_input = json.load(f)

    updated = 0
    for entry in user_input:
        if entry['username'] == user:
            entry['nthash'] = md4
            entry['ssha'] = sha1 + salt
            updated += 1

    if updated == 0:
        click.echo(f'User {user} not found', err=True)
        exit(1)

    with open(json_path, 'w') as f:
        json.dump(user_input, f, indent=4)


@click.group()
def main():
    pass


if __name__ == '__main__':
    main.add_command(authorized_mpsks)
    main.add_command(authorized_users)
    main.add_command(update_user_hash)
    main()

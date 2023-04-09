## Features

- Aruba MPSK (Multi Pre-Shared Key) authentication
- Username/Password-based authentication
- Automation tools to update `raddb` (FreeRADIUS configuration files) and password hashes

## Getting Started

### Configure Aruba MPSK

Modify `authorized_mpsks.json` to include the MAC address of the device you want to connect.

```json
...
    {
        "_description": "your-device",
        "addr": "11-22-33-44-55-66",
        "vlan": 100,
        "mpsk": "uwuwuwuw"
    }
...
```

Then, compile the `authorized_mpsks.json` file into `raddb/authorized_mpsks`, so FreeRADIUS can read it.

```bash
$ make authorized_mpsks
...
```

You should see the compiler `authorized_c` generated the `raddb/authorized_mpsks` file.

```bash
$ cat raddb/authorized_mpsks | grep -A5 11-22-33-44-55-66
11-22-33-44-55-66
        Tunnel-Type = VLAN,
        Tunnel-Medium-Type = IEEE-802,
        Tunnel-Private-Group-ID = "100",
        Aruba-MPSK-Passphrase = "uwuwuwuw"
```

### Configure Username/Password-based Authentication

Modify `authorized_users.json` to add the username.

```json
[
    {
        "username": "amphideno",
        "vlan": 100
    }
]
```

Then, update password hashes with `authorized_c`.

```bash
$ make update_user_hash
Username: amphideno
New password: 
Confirm password:
```

Finally, compile the `authorized_users.json` file into `raddb/authorized_users`, so FreeRADIUS can read it.

```bash
$ make authorized_users
...
```

You should see the compiler `authorized_c` generated the `raddb/authorized_users` file.

```bash
$ cat raddb/authorized_users | grep -A4 amphideno
"amphideno" NT-Password := "c1ee7833e9a698acf3d5eb962f2c5d18"
        Tunnel-Type = VLAN,
        Tunnel-Medium-Type = IEEE-802,
        Tunnel-Private-Group-ID = "100"
```

### Certificate-based Authentication

TODO: Write this section
import paramiko

def ssh_run(host, port, username, password, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname=host,
        port=port,
        username=username,
        password=password,
        look_for_keys=False,
        allow_agent=False
    )

    stdin, stdout, stderr = client.exec_command(cmd)

    out = stdout.read().decode(errors="ignore")
    err = stderr.read().decode(errors="ignore")

    client.close()

    return out + ("\nERR:\n" + err if err else "")

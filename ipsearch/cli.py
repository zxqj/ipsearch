import click
import socket
import psutil
import re

def matching_ips(pattern):
    """
    Return all IP addresses assigned to local interfaces
    whose reverse-DNS (PTR) record matches the given regex pattern.
    """
    regex = re.compile(pattern)
    results = []

    # Iterate all network interfaces and their addresses
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip = addr.address

                try:
                    # Reverse DNS lookup
                    host, aliases, _ = socket.gethostbyaddr(ip)
                    names = {host, *aliases}
                except socket.herror:
                    # No PTR record
                    continue

                # Match any returned PTR hostname
                if any(regex.search(name) for name in names):
                    results.append(ip)

    return results

@click.argument(
    "pattern"
)
def main(pattern):
    "Command description goes here"
    click.echo(matching_ips(pattern))

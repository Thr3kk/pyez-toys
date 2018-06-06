#!/usr/bin/env python3

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
import yaml

user = 'autobot'
password = 'juniper123'
template = 'ntp.j2'
vars = 'hosts.yml'

config = yaml.load(open(vars).read())


def main():
    hosts = config.get('hosts')

    for host in hosts:
        dev = Device(host=host, user=user, password=password)

        # Open Connection
        try:
            dev.open()
        except Exception as err:
            print("Cannot connect to device: {}".format(err))
            return

        dev.bind(cu=Config)

        # Lock the configuration, load changes, commit
        print("Locking the configuration on: {}".format(host))
        try:
            dev.cu.lock()
        except LockError:
            print("Error: Unable to lock configuration on: {}".format(host))
            dev.close()
            return

        print("Loading configuration changes on: {}".format(host))
        try:
            # If your devices don't already have NTP configured, comment out
            # the next 4 lines
            set_commands = """
            delete system ntp
            """
            dev.cu.load(set_commands, format='set')
            dev.cu.load(template_path=template,
                        template_vars=config, format='text')
        except ValueError as err:
            print(err.message)

        except Exception as err:
            if err.rsp.find('.//ok') is None:
                rpc_msg = err.rsp.findtext('.//error-message')
                print("Unable to load config changes: {}".format(rpc_msg))

            print("Unlocking the configuration")
            try:
                dev.cu.unlock()
            except UnlockError:
                print("Error: Unable to unlock configuration")
            dev.close()
            return

        print("Committing the configuration on: {}".format(host))
        try:
            dev.cu.commit()
            # print dev.cu.diff()
        except CommitError:
            print("Error: Unable to commit configuration")
            print("Unlocking the configuration")
            try:
                dev.cu.unlock()
            except UnlockError:
                print("Error: Unable to unlock configuration")
            dev.close()
            return

        print("Unlocking the configuration")
        try:
            dev.cu.unlock()
        except UnlockError:
            print("Error: Unable to unlock configuration")

        dev.close()


if __name__ == "__main__":
    main()

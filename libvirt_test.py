# coding=utf-8
import sys
import libvirt


def main():
    conn = libvirt.openReadOnly(
        'xen://darius@xen.local.geekspace.us')
    if conn is None:
        print('Failed to open connection to the hypervisor')
        sys.exit(1)

    try:
        domains = conn.listAllDomains()
        dom = domains[0]
        print(dom.state)
    except:
        print('Failed to find the main domain')
        sys.exit(1)


if __name__ == '__main__':
    main()
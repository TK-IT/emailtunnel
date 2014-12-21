import sys
import argparse
import email
import email.mime.multipart
import email.charset
from email.charset import QP

import smtplib

def validate_address(v):
    host, port = v.split(':')
    port = int(port)
    return host, port


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--relay',
        type=validate_address,
        default=('127.0.0.1', 9000),
        help='hostname and port to relay to (default 127.0.0.1:9000)',
    )
    parser.add_argument(
        '--sender', '-F',
        required=True,
        help='envelope sender (recipient of errors)',
    )
    parser.add_argument(
        '--recipient', '-T',
        required=True,
        action='append',
        help='envelope recipient (can be specified multiple times)',
    )
    parser.add_argument(
        '--from', '-f',
        dest='from_',
        help='From-header in message',
    )
    parser.add_argument(
        '--to', '-t',
        action='append',
        help='To-header in message',
    )
    parser.add_argument(
        '--cc', '-c',
        action='append',
        help='Cc-header in message',
    )
    parser.add_argument(
        '--subject', '-s',
        help='Subject-header in message',
    )
    parser.add_argument(
        '--header', '-I',
        nargs=2,
        help='Arbitrary header in message',
    )
    parser.add_argument(
        '--encoding',
        help='Encode the message and set Content-type header',
    )

    return parser


def main(*args, **kwargs):
    input_arguments = list(args)
    for key, value in kwargs.items():
        input_arguments += ['--%s' % key, value]

    parser = get_parser()

    args = parser.parse_args(input_arguments)

    relay_host = smtplib.SMTP(args.relay[0], args.relay[1])
    relay_host.set_debuglevel(0)

    body = sys.stdin.read()
    # print(repr(body))
    message = email.mime.multipart.MIMEMultipart()
    for to in args.to or []:
        message.add_header('To', to)
    for cc in args.cc or []:
        message.add_header('Cc', cc)
    if args.from_:
        message.add_header('From', args.from_)

    message.add_header('Subject', args.subject)

    for key, value in args.header or []:
        message.add_header(key, value)

    body_part = email.message.MIMEPart()
    if args.encoding:
        encoded = body.encode(args.encoding)
        body_part.set_payload(encoded)
        body_part.add_header(
            'Content-Type', 'text/plain')
        email.charset.add_charset(args.encoding, QP, QP)
        body_part.set_charset(args.encoding)
    else:
        body_part.set_payload(body)
        body_part.add_header('Content-Type', 'text/plain')
    message.attach(body_part)

    from email.generator import Generator
    policy = email.message.compat32
    g = Generator(sys.stdout, maxheaderlen=80, policy=policy, mangle_from_=False)
    try:
        g.flatten(message, unixfrom=False)
    except:
        sys.stdout.flush()
        print('')
        raise

    try:
        relay_host.sendmail(
            args.sender, args.recipient, str(message))
    except smtplib.SMTPDataError as e:
        print('Relay returned error on DATA:')
        print(str(e))
    finally:
        try:
            relay_host.quit()
        except smtplib.SMTPServerDisconnected:
            pass


if __name__ == "__main__":
    main(*sys.argv[1:])

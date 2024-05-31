import asyncio
from aiosmtpd.controller import Controller
import hashlib
import json
import logging


logging.basicConfig(level=logging.DEBUG)

class DebuggingHandler:
    async def handle_DATA(self, server, session, envelope):
        logging.info('Message From: %s', envelope.mail_from)
        logging.info('Message To: %s', envelope.rcpt_tos)
        logging.info('Message Data:')
        logging.info(envelope.content.decode('utf8', errors='replace'))

        # MAP RECIPIENT ADDR TO INTERNAL ADDR
        for rec in envelope.rcpt_tos:
            # USE RESOLVER CLASS HERE
            #internalAddr = addrMap.get(rec)
            if internalAddr:
                logging.info(f"Mapping {rec} to internal address {internalAddr}")
            else:
                logging.info(f"No Mapping found for {rec}")

        logging.info('End of Message')
        return '250 Message accepted'

if __name__ == '__main__':
    controller = Controller(DebuggingHandler(), hostname='localhost', port=1025)
    controller.start()
    print('SMTP server running on localhost 1025')
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()

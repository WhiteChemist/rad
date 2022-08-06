from __future__ import print_function
from pyrad import dictionary, packet, server
import database
import logging

logging.basicConfig(filename="pyrad.log", level="DEBUG",
                    format="%(asctime)s [%(levelname)-8s] %(message)s")


class RadiusServer(server.Server):

    def HandleAuthPacket(self, pkt):
        pwd=pkt.PwDecrypt(pkt['User-Password'][0])
        uname=pkt['User-Name'][0]
        print(uname)
        print('Plaintext PW: {}'.format(pwd))
        print("Received an authentication request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        print(database.validateNas(pkt["NAS-Identifier"],pkt["NAS-IP-Address"],pkt["Secret"]))

        reply = self.CreateReplyPacket(pkt, **{
            "Service-Type": "Framed-User",
            "Framed-IP-Address": '192.168.0.1'
        })

        reply.code = packet.AccessAccept
        self.SendReplyPacket(pkt.fd, reply)

    def HandleAcctPacket(self, pkt):

        print("Received an accounting request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleCoaPacket(self, pkt):

        print("Received an coa request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleDisconnectPacket(self, pkt):

        print("Received an disconnect request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        # COA NAK
        reply.code = 45
        self.SendReplyPacket(pkt.fd, reply)


if __name__ == '__main__':

    # create server and read dictionary
    srv = RadiusServer(dict=dictionary.Dictionary("dictionary"), coa_enabled=True)
    hosts=database.getHosts()
    for item in hosts:
        srv.hosts[item[0]] = server.RemoteHost(item[0], str(item[1]).encode('utf-8'), item[2])
    srv.BindToAddress("0.0.0.0")

    # start server
    srv.Run()
import paramiko
import ftplib
from paramiko.auth_handler import AuthenticationException, SSHException
import logging
import re
import datetime
class RemoteClient:



    def __init__(self, ipaddr, username, password):

        self.ipaddr = ipaddr

        self.username = username

        self.password = password

        self.client = None

        self.conn = None



    def connection(self):

        if self.conn is None:

            try:

                self.client = paramiko.SSHClient()

                self.client.load_system_host_keys()

                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())



                self.client.connect(

                    self.ipaddr,

                    username=self.username,

                    password=self.password,

                    look_for_keys=False

                )

            except AuthenticationException as error:

                logging.error("autenticacion fallida, vuelva a intentar \n error es {}".format(error))

                raise error

        return self.client



    def disconnect(self):

        if self.client:

            self.client.close()



    def execute_unix_commands(self, command):

        self.conn = self.connection()

        response = []



        stdin, stdout, stderr = self.conn.exec_command(command)

        stdout.channel.recv_exit_status()

        stdout_lits = stdout.readlines()

        stderr_list = stderr.readlines()

        if len(stdout_lits) == 1:

            return stdout_lits

        if len(stderr_list) == 1:

            return stderr_list




    def eval_dismisspd(self, output_list):
        print(output_list)
        aux = output_list[0].split(' ')

        if output_list[0].find("referenced"):
            aux1 = aux[9].replace('\n','')
            return aux1

        if output_list[0].find("normal"):
            return True

        if output_list[0].find("ldpattern_not_obeyed"):
            return True

        else:
            return False





# Press the green button in the gutter to run the script.

if __name__ == '__main__':

    disk = 187
    eval = True
    remote = RemoteClient('XXX.XXX.XXX.XXX', 'USER', 'PASSWD')
    remote.connection()
    
    while eval:
        output_list = remote.execute_unix_commands("dismisspd {}".format(disk))
        auxiliar = remote.eval_dismisspd(output_list)
        print("dismisspd {}".format(disk))
        if auxiliar:
            print("movech -perm -ovrd -f  {}".format(auxiliar))
            output_list = remote.execute_unix_commands("movech -perm -ovrd -f  {}".format(auxiliar))
            eval = True
        else:
            eval = False

    remote.disconnect()
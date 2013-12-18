import socket, select
import logging

logging.basicConfig()

class tcpClient:
    def __init__(self,ip, port,
                 terminator="\n",
                 timeout=5,
                 recv_max_retries=4,
                 strip_term=False):
        self.ip = ip
        self.port = port
        self.terminator = terminator
        self.len_term = len(terminator)
        self.strip_term = strip_term
        self.timeout = timeout
        self.recv_max_retries = recv_max_retries

        self.logger = logging.getLogger('tcpClient')
        self.logger.setLevel(logging.DEBUG)

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip,port))
        #self.conn.setblocking(0)

        self.conn.settimeout(self.timeout)

        self.data_message = ""
        self.in_buffer = ""
        self.recv_retries = 0

    def send(self,msg):
        self.conn.sendall(msg + self.terminator)

    def recv_nbytes(self,nbytes):
        temp_message = self.in_buffer #Any left over
        while(len(temp_message) < nbytes):
            try:
                temp_message += self.conn.recv(1024)
            except:
                self.logger.warn('RECV HAS TIMED OUT!')
                self.recv_retries = self.recv_retries + 1
                return False
        #We should have the whole message
        self.data_message = temp_message[0:nbytes]
        self.in_buffer = temp_message[nbytes:]

    def recv_term(self):
        self.data_message = ""
        try:
            temp_message = self.conn.recv(128)
        except:
            self.logger.warn('RECV HAS TIMED OUT!')
            self.recv_retries = self.recv_retries + 1
            return False
        
        done = False
        while done is False:
            lf_pos = temp_message.find(self.terminator)
            if lf_pos != -self.len_term:
            #We have a line feed - is it the end of the string?
                if lf_pos == len(temp_message)-1:
                    self.logger.debug('Complete message')
                    self.data_message = self.in_buffer + temp_message
                    self.in_buffer = ""
                    done = True
                else:
                #We have the case where we need to keep rest of buffer
                    self.logger.debug('More than a message')
                    self.data_message = self.in_buffer + temp_message[:lf_pos+self.len_term]
                    self.in_buffer = temp_message[lf_pos+self.len_term:]
                    done = True
            else:
            #We don't have a complete record - just append
                self.logger.debug('Part of a message')
                self.in_buffer = self.in_buffer + temp_message
                try:
                    temp_message = self.conn.recv(128)
                except:
                    self.logger.warn("FAILED TO RECEIVE REPLY")
                    return False
        #And remove the terminator
        self.data_message = self.data_message[:-self.len_term]
        return True 

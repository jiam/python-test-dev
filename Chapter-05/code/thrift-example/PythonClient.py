from tutorial import Calculator


from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def main():
    # 创建socket，连接localhost的9090端口
    transport = TSocket.TSocket('localhost', 9090)

    # 使用带buffer 传输层协议
    transport = TTransport.TBufferedTransport(transport)

    # 使用TBinaryProtocol protocal
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # 创建client
    client = Calculator.Client(protocol)

    # 连接服务端
    transport.open()
    # 调用服务ping方法
    client.ping()
    print('ping()')
    # 调用服务端add方法
    sum_ = client.add(1, 1)
    print('1+1=%d' % sum_)
        # 关闭连接
    transport.close()


if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)
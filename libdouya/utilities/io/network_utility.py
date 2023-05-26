# -*- coding:utf-8 -*-
#!/usr/bin/env python

'''
    network_utility.py - 网络相关的通用方法集
'''

class NetworkUtil(object):
    # 子网掩码地址转长度
    @staticmethod
    def conv_netmask_to_bit_length(mask_net_str:str):
        """
        >>> netmask_to_bit_length('255.255.255.0')
        24
        >>>
        """
        # 分割字符串格式的子网掩码为四段列表
        # 计算二进制字符串中 '1' 的个数
        # 转换各段子网掩码为二进制, 计算十进制
        return sum([bin(int(i)).count('1') for i in mask_net_str.split('.')])

    # 子网掩码长度转地址
    @staticmethod
    def conv_bit_length_to_netmask(mask_int:int):
        """
        >>> bit_length_to_netmask(24)
        '255.255.255.0'
        >>>
        """
        bin_array = ["1"] * mask_int + ["0"] * (32 - mask_int)
        tmpmask = [''.join(bin_array[i * 8:i * 8 + 8]) for i in range(4)]
        tmpmask = [str(int(netmask, 2)) for netmask in tmpmask]
        return '.'.join(tmpmask)

    @staticmethod
    def conv_ip_address_to_binary_address(ip_address_str: str) -> str:
        return ''.join(['{0:08b}'.format(int(part)) for part in ip_address_str.split('.')])

    @staticmethod
    def conv_binary_address_to_ip_address(binary_address_str:str) -> str:
        binary_address_length = len(binary_address_str)
        if 32 > binary_address_length: 
            binary_address_str = '0'* (32 - binary_address_length) + binary_address_str
        return '.'.join('{0}'.format(int(binary_address_str[pos:pos + 8], 2)) for pos in range(0, 32, 8))

    @staticmethod
    def list_sub_net(routing_prefix:str):
        '''
        routing_prefix: CIDR标识符（CIDR Notation），形如: 192.168.0.0/16
        '''
        # numbers 
        ip_address_str, netmask_bit_length_str = routing_prefix.split('/', 1)
        ip_address_binary_number_str = ''.join("{0:08b}".format(int(ip_address_segment_str)) for ip_address_segment_str in ip_address_str.split('.'))

        netmask_bit_length = int(netmask_bit_length_str)  #掩码BIT位长度
        subnet_bit_length = 32 - netmask_bit_length #子网BIT位长度
        subnet_address_count = 1 << subnet_bit_length #子网地址个数

        subnet_first_address_binary_number_str = ip_address_binary_number_str[:netmask_bit_length] + ('0' * subnet_bit_length) #子网网关地址
        
        for i in range(subnet_address_count):
            subnet_address_binary_number_str = '{0:032b}'.format(int(subnet_first_address_binary_number_str, 2) + i)
            yield NetworkUtil.conv_binary_address_to_ip_address(subnet_address_binary_number_str)

    @staticmethod
    def compare_ip_address(lv:str, rv:str) -> int:
        lbv = NetworkUtil.conv_ip_address_to_binary_address(lv)
        rbv = NetworkUtil.conv_ip_address_to_binary_address(rv)
        if lbv > rbv: return 1
        elif lbv < rbv: return -1
        else: return 0
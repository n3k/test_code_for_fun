'''
Created on 18/08/2013

@author: n3k
'''
import math
import sys


class Subnet:
    
    def __init__(self):
        self.subnet_addr = ""
        self.broadcast_addr = ""
        self.subnet_mask = 0
        self.addresses = 0
    

class SubnetSolver:
    
    def __init__(self, prefix, mask, hosts_list):
        self.subnets = []
        self.prefix = prefix
        self.mask = mask
        self.hosts_list = hosts_list
        self.total_addreses = math.pow(2,32-self.mask)
        
    def get_mask_string(self, mask):
        mask_vector = "1" * self.mask + "0" * (32 - self.mask)           
        return mask_vector
    
    def decimal_mask_number(self, mask):
        number = 0
        mask_string = self.get_mask_string(mask)
        for i in range(0, len(mask_string)):
            if mask_string[i] == '1':
                number += math.pow(2, i)
        return int(number)
    
    def check_possible(self):
        addr_sum = 0
        for i in range(0,len(self.hosts_list)):
            addr_sum += self.hosts_list[i] + 2
            print "Subnet %d needs %d addresses" % (i, self.hosts_list[i] + 2)
        print "Total addresses needed: " + str(addr_sum)        
        print "Mask given: " + str(self.mask) + " = " + str(int(self.total_addreses)) + " addresses"
        if self.total_addreses < addr_sum:
            return False
        return True
    
    def minor_mask_subnet(self, hosts):
        for i in range(0, 32 - self.mask + 1):
            if math.pow(2, i) >= hosts:            
                return 32 - i     

 
    def get_subnet_addr(self, prefix, mask):
        hosts =  pow(2, 32 - mask) 
        octets = str.split(prefix, '.')
        new_prefix = ''

        if hosts > 65536:
            aux = hosts / 65536
            new_prefix = octets[0] + '.' + str(int(octets[1]) + aux) + '.0.0'
                        
        elif hosts > 256:
             aux = hosts / 256
             new_prefix = octets[0] + '.' + octets[1]+ '.' + str(int(octets[2]) + aux) + '.0'
             
        else:
            if int(octets[3]) + hosts <= 256:          
                new_prefix = octets[0] + '.' + octets[1]+ '.' + octets[2] + '.' +  str(int(octets[3]) + hosts)         
            else:
                new_prefix = octets[0] + '.' + octets[1]+ '.' +  str(int(octets[2]) + 1) + '.' +  str(hosts)
                
        return new_prefix             
    
    def get_broadcast_addr(self, prefix, mask):
        hosts =  pow(2, 32 - mask)
        octets = str.split(prefix, '.')
        broadcast_addr = ''  
              
        if hosts > 65536:           
            broadcast_addr = octets[0] + '.' + str(int(octets[1]) - 1) + '.255.255'  
        elif hosts > 256:          
             broadcast_addr = octets[0] + '.' + octets[1]+ '.' + str(int(octets[2]) - 1) + '.255'        
        else:       
            broadcast_addr = octets[0] + '.' + octets[1]+ '.' + octets[2] + '.' +  str(int(octets[3]) - 1)
            
        return broadcast_addr  
        
    
    def calculate(self):
        next_subnet = self.prefix
        if not self.check_possible():
            print "Assignment cannot be done, lack of addresses!"
            sys.exit(1)
        else:
            print "Assignment possible"            
            for hosts in sorted(self.hosts_list, reverse=True):  
                prefix_temp = next_subnet             
                subnet = Subnet()
                subnet.subnet_mask = self.minor_mask_subnet(hosts + 2)
                subnet.addresses = pow(2, 32 - subnet.subnet_mask)             
                subnet.subnet_addr = prefix_temp 
                next_subnet = self.get_subnet_addr(prefix_temp,  subnet.subnet_mask)
                subnet.broadcast_addr = self.get_broadcast_addr(next_subnet, subnet.subnet_mask)
                self.subnets.append(subnet)
            
            self.show_results()
        
    
    def show_results(self):
        for sub in self.subnets:
            print "Subnet Address: " + sub.subnet_addr + "   Mask: " + str(sub.subnet_mask) + "   Addresses: " + str(sub.addresses) + "   Broadcast: " + sub.broadcast_addr
        


solver = SubnetSolver("200.87.49.0", 24, [17,5,50,3,60,30])
solver.calculate()
        
    
    
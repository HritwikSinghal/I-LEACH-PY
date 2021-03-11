import pprint

from src.LEACH_configure_sensors import *
from src.LEACH_set_parameters import *


def start(Sensors: list[Sensor], myModel: Model, senders: list, PacketType: str, receivers: list, srp, rrp, sdp, rdp):
    sap = 0  # Send a packet or Number of sent packets
    rap = 0  # Receive a packet or Number of received packets
    if PacketType == 'Hello':
        PacketSize = myModel.HpacketLen
    else:
        PacketSize = myModel.DpacketLen

    # Energy dissipated from Sensors for Sending a packet
    # Each sender will send to each receiver
    for sender in senders:
        for receiver in receivers:
            # calculate euclidean distance between sender and receiver
            distance = sqrt(
                pow(Sensors[sender].xd - Sensors[receiver].xd, 2) + pow(Sensors[sender].yd - Sensors[receiver].yd, 2)
            )
            print(f"dist b/w sender: {sender} and receiver: {receiver} is: {distance}")

            if distance > myModel.do:
                Sensors[sender].E -= myModel.ETX * PacketSize + myModel.Emp * PacketSize * pow(distance, 4)
                print(f'{sender} sent packet to {receiver}. New energy of {sender} = {Sensors[sender].E}')
            else:
                Sensors[sender].E -= myModel.ETX * PacketSize + myModel.Efs * PacketSize * pow(distance, 4)
                print(f'{sender} sent packet to {receiver}. New energy of {sender} = {Sensors[sender].E}')

            # Send a packet and increment counter by 1
            if Sensors[sender].E > 0:
                sap += 1

    for sender in senders:
        for receiver in receivers:
            # Energy dissipated from receivers for Receiving a packet
            Sensors[receiver].E -= (myModel.ERX + myModel.EDA) * PacketSize
            print(f'new energy of {receiver} = {Sensors[receiver].E}')

            # Received a Packet
            if Sensors[sender].E > 0 and Sensors[receiver].E > 0:
                print(f'{receiver} recieved a packet from {sender}')
                rap += 1

    if PacketType == 'Hello':
        srp += sap
        rrp += rap
        print("incremented srp and rrp by 1")
    else:
        sdp += sap
        rdp += rap
        print("incremented sdp and rdp by 1")

    print()
    return srp, rrp, sdp, rdp


# todo: implement this or see if this is implemented in joinToNearestCH
'''

%     else %To Cluster Head
%         
%         for i=1:length( Sender)
%        
%            distance=sqrt((Sensors(Sender(i)).xd-Sensors(Sender(i).MCH).xd)^2 + ...
%                (Sensors(Sender(i)).yd-Sensors(Sender(i).MCH).yd)^2 );   
%        
%            send a packet
%            sap=sap+1;
%            
%            Energy dissipated from Normal sensor
%            if (distance>Model.do)
%            
%                 Sensors(Sender(i)).E=Sensors(Sender(i)).E- ...
%                     (Model.ETX*PacketSize + Model.Emp*PacketSize*(distance^4));
% 
%                 if(Sensors(Sender(i)).E>0)
%                     rap=rap+1;                 
%                 end
%             
%            else
%                 Sensors(Sender(i)).E=Sensors(Sender(i)).E- ...
%                     (Model.ETX*PacketSize + Model.Emp*PacketSize*(distance^2));
% 
%                 if(Sensors(Sender(i)).E>0)
%                     rap=rap+1;                 
%                 end
%             
%            end 
%        end
  


'''

import argparse
import base64
from dns import message

def get_dns_packet_id(base64_data):
    decoded_data = base64.b64decode(base64_data)
    dns_packet = message.from_wire(decoded_data)
    return dns_packet.id

def get_dns_packet_questions(base64_data):
    decoded_data = base64.b64decode(base64_data)
    dns_packet = message.from_wire(decoded_data)
    return dns_packet.question

def get_dns_packet_answers(base64_data):
    decoded_data = base64.b64decode(base64_data)
    dns_packet = message.from_wire(decoded_data)
    return dns_packet.answer

def get_dns_packet_raw(base64_data):
    decoded_data = base64.b64decode(base64_data)
    dns_packet = message.from_wire(decoded_data)
    return dns_packet

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='Extract DNS packet fields')
parser.add_argument('-a', '--answer', required=True, help='Base64 encoded DNS answer')
args = parser.parse_args()

# 提取 DNS 数据包的字段值
dns_packet_id = get_dns_packet_id(args.answer)
dns_packet_questions = get_dns_packet_questions(args.answer)
dns_packet_answers = get_dns_packet_answers(args.answer)
dns_packet_raw = get_dns_packet_raw(args.answer)

# 打印提取的字段值
print("DNS Packet ID:", dns_packet_id)
print("Questions:", dns_packet_questions)
print("Answers:", dns_packet_answers)
print("Raw:", dns_packet_raw)

import base64
from dns import message

def decode_and_parse_dns_packet(base64_data):
    decoded_data = base64.b64decode(base64_data)
    dns_packet = message.from_wire(decoded_data)
    return dns_packet

# 示例经过 Base64 转换的 Answer 字段值
base64_answer = "mZaBgAABAAEAAAAAAmNuBGJpbmcDY29tAAABAAHADAABAAEAAAAKAATKWelk"

# 解码并解析 DNS 数据包
dns_packet = decode_and_parse_dns_packet(base64_answer)

# 访问 DNS 数据包字段示例
print("DNS Packet ID:", dns_packet.id)
print("Questions:", dns_packet.question)
print("Answers:", dns_packet.answer)
# 进一步访问和解析其他字段以获取更多信息


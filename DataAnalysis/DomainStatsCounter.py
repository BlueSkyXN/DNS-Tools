import pandas as pd
import argparse
from collections import Counter

def main(input_file, output_file, chunksize):
    total_counts = Counter()

    # 使用Pandas直接读取CSV文件的块
    for chunk in pd.read_csv(input_file, chunksize=chunksize):
        # 统计"QH"列中域名的出现次数
        total_counts.update(Counter(chunk['QH']))

    # 将结果转换为DataFrame
    result_df = pd.DataFrame.from_dict(total_counts, orient='index').reset_index()
    result_df.columns = ['Domain', 'Count']
    
    # 按计数降序排列
    result_df = result_df.sort_values(by='Count', ascending=False)

    # 保存结果到新的CSV文件
    result_df.to_csv(output_file, index=False)

    print(f"域名统计已保存到 {output_file}")

# 命令行参数解析
parser = argparse.ArgumentParser(description='统计域名出现次数')
parser.add_argument('-i', '--input', type=str, required=True, help='Path to input CSV file')
parser.add_argument('-o', '--output', type=str, required=True, help='Path to output CSV file')
parser.add_argument('-s', '--chunksize', type=int, default=10000, help='Number of lines to process at a time')
args = parser.parse_args()

main(args.input, args.output, args.chunksize)

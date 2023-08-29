import pandas as pd
import argparse
from collections import Counter

def main(input_file, output_file, chunksize, ip_address):
    total_counts = Counter()

    # Using pandas to read chunks directly from the CSV file
    for chunk in pd.read_csv(input_file, chunksize=chunksize):
        # Filter rows based on the specified IP address
        filtered_chunk = chunk[chunk['IP'] == ip_address]
        
        # Count occurrences of domains in the "QH" column
        total_counts.update(Counter(filtered_chunk['QH']))

    # Convert the result to a DataFrame
    result_df = pd.DataFrame.from_dict(total_counts, orient='index').reset_index()
    result_df.columns = ['Domain', 'Count']
    
    # Sort by count in descending order
    result_df = result_df.sort_values(by='Count', ascending=False)

    # Save the result to a new CSV file
    result_df.to_csv(output_file, index=False)

    print(f"域名统计已保存到 {output_file}")

# Entry point
if __name__ == "__main__":

    # 命令行参数解析
    parser = argparse.ArgumentParser(description='统计域名出现次数')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to input CSV file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to output CSV file')
    parser.add_argument('-s', '--chunksize', type=int, default=10000, help='Number of lines to process at a time')
    parser.add_argument("-c", "--ip", required=True, help="Specify the IP to filter.")

    args = parser.parse_args()

    main(args.input, args.output, args.chunksize)
    parser.add_argument("-c", "--ip", required=True, help="Specify the IP to filter.")
    main(args.input, args.output, args.chunksize, args.ip)

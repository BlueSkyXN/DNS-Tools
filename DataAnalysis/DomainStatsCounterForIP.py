import pandas as pd
import argparse
from collections import Counter



def main(input_file, output_file, chunksize, ip_address):
    total_counts = Counter()
    first_time_dict = {}
    last_time_dict = {}

    # Using pandas to read chunks directly from the CSV file
    for chunk in pd.read_csv(input_file, chunksize=chunksize, dtype={11: str}):
        # Filter rows based on the specified IP address
        filtered_chunk = chunk[chunk['IP'] == ip_address]
        
        # Count occurrences of domains in the "QH" column
        total_counts.update(Counter(filtered_chunk['QH']))
        
        # Update FirstTime and LastTime for each domain
        for domain, time in zip(filtered_chunk['QH'], pd.to_datetime(filtered_chunk['T'], format='%Y-%m-%dT%H:%M:%S.%f%z')):
            if domain not in first_time_dict or time < first_time_dict[domain]:
                first_time_dict[domain] = time
            if domain not in last_time_dict or time > last_time_dict[domain]:
                last_time_dict[domain] = time

    # Convert the result to a DataFrame
    result_df = pd.DataFrame.from_dict(total_counts, orient='index').reset_index()
    result_df.columns = ['Domain', 'Count']
    
    # Add FirstTime and LastTime columns
    result_df['FirstTime'] = result_df['Domain'].map(first_time_dict).dt.strftime('%Y-%m-%d %H:%M:%S')
    result_df['LastTime'] = result_df['Domain'].map(last_time_dict).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Sort by count in descending order
    result_df = result_df.sort_values(by='Count', ascending=False)

    # Save the result to a new CSV file
    result_df.to_csv(output_file, index=False)

    print(f"域名统计已保存到 {output_file}")

# Entry point
if __name__ == "__main__":

    # 命令行参数解析
    parser = argparse.ArgumentParser(description='针对目标IP的统计域名出现次数')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to input CSV file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to output CSV file')
    parser.add_argument('-s', '--chunksize', type=int, default=10000, help='Number of lines to process at a time')
    parser.add_argument("-c", "--ip", required=True, help="Specify the IP to filter.")
    args = parser.parse_args()
    main(args.input, args.output, args.chunksize, args.ip)
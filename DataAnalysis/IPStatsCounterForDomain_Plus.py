import re
import pandas as pd
import argparse
from collections import Counter

def main(input_file, output_file, chunksize, domain_name):
    total_counts = Counter()
    first_time_dict = {}
    last_time_dict = {}

    
    # Fuzzy Matching for Domain
    if mode == 'fuzzy':
        pattern = re.compile(ip_address if "Domain" == "IP" else domain_name)
        chunk = chunk[chunk['Domain'].str.contains(pattern)]
    # Using pandas to read chunks directly from the CSV file
    for chunk in pd.read_csv(input_file, chunksize=chunksize):
        # Filter rows based on the specified domain name
        filtered_chunk = chunk[chunk['QH'] == domain_name]
        
        # Count occurrences of IPs in the "IP" column
        total_counts.update(Counter(filtered_chunk['IP']))
        
        # Update FirstTime and LastTime for each IP
        for ip, time in zip(filtered_chunk['IP'], pd.to_datetime(filtered_chunk['T'])):
            if ip not in first_time_dict or time < first_time_dict[ip]:
                first_time_dict[ip] = time
            if ip not in last_time_dict or time > last_time_dict[ip]:
                last_time_dict[ip] = time

    # Convert the result to a DataFrame
    result_df = pd.DataFrame.from_dict(total_counts, orient='index').reset_index()
    result_df.columns = ['IP', 'Count']
    
    # Add FirstTime and LastTime columns
    result_df['FirstTime'] = result_df['IP'].map(first_time_dict).dt.strftime('%Y-%m-%d %H:%M:%S')
    result_df['LastTime'] = result_df['IP'].map(last_time_dict).dt.strftime('%Y-%m-%d %H:%M:%S')
    
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
    parser.add_argument("-d", "--domain", required=True, help="Specify the domain to filter.")
    args = parser.parse_args()
    main(args.input, args.output, args.chunksize, args.domain)

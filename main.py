import os
import pandas as pd
import speedtest

# https://github.com/sivel/speedtest-cli/wiki
def parse_result(r):
  dfs = []
  for k, v in r.items():
    if isinstance(r[k], dict):
      dfs.append(pd.DataFrame(r[k], index=[0]))
    else:
      dfs.append(pd.DataFrame({k: r[k]}, index=[0]))
  df = pd.concat(dfs, axis=1)
  df['timestamp'] = pd.Timestamp(df['timestamp'][0])
  df.set_index('timestamp', inplace=True)
  return df

if __name__ == '__main__':
  print('Running speed test...')
  s = speedtest.Speedtest()
  s.get_best_server()
  s.download()
  s.upload()
  s.results.share()
  r = s.results.dict()
  print('Speed test complete. Writing results')
  result = parse_result(r)
  
  # append to a .csv
  if os.path.isfile('results.csv'):
  	result.to_csv('results.csv', mode='a', header=False, index=True)
  else:
  	result.to_csv('results.csv', index=True)
  print('Done!')

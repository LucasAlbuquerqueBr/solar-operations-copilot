"""Verify original downloads and profile data without cleaning or solving the challenge."""
from pathlib import Path
import csv, hashlib, json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest=json.loads((ROOT/'data/download_manifest.json').read_text())
    for item in manifest:
        path=ROOT/item['file']
        with path.open('rb') as f:
            if hashlib.file_digest(f,'sha256').hexdigest() != item['sha256']:
                raise ValueError(f'Checksum mismatch: {path}')
        if path.stat().st_size != item['bytes']:
            raise ValueError(f'Size mismatch: {path}')
    metadata=json.loads((ROOT/'data/metadata/2107_system_metadata.json').read_text())
    metrics=metadata['Metrics']
    profiles=[]
    dictionary=[]
    for path in sorted((ROOT/'data/raw').glob('*.csv')):
        print('Profiling',path.name,flush=True)
        df=pd.read_csv(path)
        times=pd.to_datetime(df['measured_on'],errors='coerce')
        steps=times.sort_values().drop_duplicates().diff().dt.total_seconds().dropna()
        profiles.append({'file':path.name,'rows':len(df),'columns':len(df.columns),'start':str(times.min()),'end':str(times.max()),'invalid_timestamps':int(times.isna().sum()),'duplicate_local_timestamps':int(times.duplicated().sum()),'median_unique_timestamp_step_seconds':float(steps.median()),'missing_numeric_cells':int(df.drop(columns='measured_on').isna().sum().sum()),'rows_per_year':times.dt.year.value_counts().sort_index().to_dict()})
        for col in df:
            metric=metrics.get(col,{})
            numeric=pd.to_numeric(df[col],errors='coerce') if col!='measured_on' else None
            dictionary.append({'file':path.name,'column':col,'description':metric.get('common_name','Local instrument timestamp' if col=='measured_on' else 'Unmatched: inspect metadata'),'units':metric.get('units','local time' if col=='measured_on' else ''),'aggregation':metric.get('aggregation_type',''),'missing_rows':int(df[col].isna().sum()),'min':numeric.min() if numeric is not None else '', 'max':numeric.max() if numeric is not None else ''})
    report=ROOT/'data/quality'
    report.mkdir(exist_ok=True)
    (report/'raw_profile.json').write_text(json.dumps(profiles,indent=2),encoding='utf-8')
    pd.DataFrame(dictionary).to_csv(ROOT/'data/metadata/channel_dictionary.csv',index=False)
    print(json.dumps(profiles,indent=2))
    print('All original source-file hashes verified. No cleaning performed.')

if __name__=='__main__': main()


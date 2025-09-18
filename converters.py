# converters.py
# This file contains the core data transformation logic for each JSON type.

import pandas as pd

# ===================================================================
#  1. Converter for Globosat (Composite Environment)
# ===================================================================
def convert_globosat_composite(data):
    """Converts a Globosat Composite JSON based on a fixed template."""
    print("Running Globosat Composite converter...")
    
    template_columns = [
        'scheduledDate', 'program|startTime', 'firstExhibition', 'duration',
        'title|duration', 'program|duration', 'showName', 'name', 'title|showName',
        'program|synopsis', 'title|synopsis', 'title|aka', 'title|name',
        'title|season|number', 'title|episodeNumber', 'title|versionCertification',
        'title|versionCertificationConfirmed', 'title|versionSubCertification',
        'title|countries', 'title|yearOfProduction', 'contentType',
        'title|genre|name', 'title|subgenre|name', 'category', 'live',
        'title|resolution', 'title|audios|language', 'title|audios|type',
        'title|directors|name', 'title|cast|name', 'title|mainActors|name',
        'program|name', 'composite', 'title|nationalContent',
        'title|qualifiedContent', 'title|independentProduction', 'id', 'txId',
        'title|id', 'title|registrationNumber', 'title|purchaseId',
        'title|versionId', 'title|season|id', 'title|season|name',
        'title|genre|id', 'title|subgenre|id', 'program|id',
        'program|weekDays|sunday', 'program|weekDays|monday',
        'program|weekDays|tuesday', 'program|weekDays|wednesday',
        'program|weekDays|thursday', 'program|weekDays|friday',
        'program|weekDays|saturday', 'clauses1|id', 'clauses1|name',
        'clauses1|startDate', 'clauses1|endDate', 'clauses2|id',
        'clauses2|name', 'clauses2|startDate', 'clauses2|endDate',
        'clauses3|id', 'clauses3|name', 'clauses3|startDate', 'clauses3|endDate'
    ]
    
    df_normalized = pd.json_normalize(data, sep='|')
    df_final = df_normalized.reindex(columns=template_columns)
    return df_final

# ===================================================================
#  2. Converter for Globosat (Planning Environment)
# ===================================================================
def convert_globosat_planning(data):
    """Converts a Globosat Planning JSON which has a nested 'slots' structure."""
    print("Running Globosat Planning converter...")
    
    template_columns = [ # This template appears identical to Composite, but is kept separate for future flexibility
        'scheduledDate', 'program|startTime', 'firstExhibition', 'duration',
        'title|duration', 'program|duration', 'showName', 'name', 'title|showName',
        'program|synopsis', 'title|synopsis', 'title|aka', 'title|name',
        'title|season|number', 'title|episodeNumber', 'title|versionCertification',
        'title|versionCertificationConfirmed', 'title|versionSubCertification',
        'title|countries', 'title|yearOfProduction', 'contentType',
        'title|genre|name', 'title|subgenre|name', 'category', 'live',
        'title|resolution', 'title|audios|language', 'title|audios|type',
        'title|directors|name', 'title|cast|name', 'title|mainActors|name',
        'program|name', 'composite', 'title|nationalContent',
        'title|qualifiedContent', 'title|independentProduction', 'id', 'txId',
        'title|id', 'title|registrationNumber', 'title|purchaseId',
        'title|versionId', 'title|season|id', 'title|season|name',
        'title|genre|id', 'title|subgenre|id', 'program|id',
        'program|weekDays|sunday', 'program|weekDays|monday',
        'program|weekDays|tuesday', 'program|weekDays|wednesday',
        'program|weekDays|thursday', 'program|weekDays|friday',
        'program|weekDays|saturday', 'clauses1|id', 'clauses1|name',
        'clauses1|startDate', 'clauses1|endDate', 'clauses2|id',
        'clauses2|name', 'clauses2|startDate', 'clauses2|endDate',
        'clauses3|id', 'clauses3|name', 'clauses3|startDate', 'clauses3|endDate'
    ]
    
    all_slots = []
    for day_schedule in data:
        if 'slots' in day_schedule and isinstance(day_schedule['slots'], list):
            all_slots.extend(day_schedule['slots'])
            
    df_normalized = pd.json_normalize(all_slots, sep='|')
    df_final = df_normalized.reindex(columns=template_columns)
    return df_final

# ===================================================================
#  3. Converter for FUBOLN
# ===================================================================
def convert_fuboln(data):
    """Converts a FUBOLN JSON by manually building rows from schedule and airing data."""
    print("Running FUBOLN converter...")
    
    if 'station' not in data or 'schedule' not in data:
        raise ValueError("Required keys 'station' or 'schedule' not found in FUBOLN JSON.")
        
    station_info = data['station']
    last_updated_global = data.get('lastUpdated', '')
    schedule_data = []

    for program in data['schedule']:
        base_info = {
            'Station Name': station_info.get('stationName', ''),
            'Station ID': station_info.get('stationId', ''),
            'Call Sign': station_info.get('callSign', ''),
            'Last Updated': last_updated_global,
            'Program ID': program.get('programId', ''),
            'Title': program.get('title', ''),
            'Episode Title': program.get('episodeTitle', ''),
            'Short Description': program.get('shortDescription', ''),
            'Long Description': program.get('longDescription', ''),
            'Season': program.get('seasonNum', ''),
            'Episode': program.get('episodeNum', ''),
            'Release Year': program.get('releaseYear', ''),
            'Original Air Date': program.get('originalAirDate', ''),
            'Genre': ', '.join(program.get('genres', [])),
            'Sub Genre': ', '.join(program.get('subGenres', [])),
            'Content Rating': program.get('contentRating', ''),
            'Cast': ', '.join(program.get('cast', [])),
        }
        
        if 'airings' in program and 'repeats' in program['airings'] and program['airings']['repeats']:
            for airing in program['airings']['repeats']:
                airing_info = base_info.copy()
                airing_info['Start Date'] = airing.get('startDate', '')
                airing_info['End Date'] = airing.get('endDate', '')
                airing_info['Duration'] = airing.get('duration', '')
                schedule_data.append(airing_info)
        else:
            base_info['Start Date'], base_info['End Date'], base_info['Duration'] = '', '', ''
            schedule_data.append(base_info)

    df_final = pd.DataFrame(schedule_data)
    return df_final

# ===================================================================
#  4. Converter for Generic JSON
# ===================================================================
def convert_generic(data):
    """Converts any JSON by iteratively flattening all nested structures."""
    print("Running Generic JSON converter...")
    
    if not isinstance(data, (dict, list)):
        df = pd.DataFrame([data])
    else:
        df = pd.json_normalize(data, sep='.') # Use dot separator for generic

    # Iteratively flatten the DataFrame
    while any(df.applymap(lambda x: isinstance(x, dict)).any()):
        dict_cols = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, dict)).any()]
        for col in dict_cols:
            flattened_col = pd.json_normalize(df[col])
            flattened_col.columns = [f"{col}.{sub_col}" for sub_col in flattened_col.columns]
            df = df.drop(col, axis=1).join(flattened_col)
            
    return df